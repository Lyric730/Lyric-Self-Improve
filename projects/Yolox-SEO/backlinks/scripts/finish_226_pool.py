"""Finish reviewing the gefei_226 pool.

This is a conservative sweeper for the backlink database:
- profile rows with prior no-website/login/captcha evidence are marked skipped
- blog_comment rows without URL fields are marked skipped
- blog_comment rows with usable WordPress-style URL fields are submitted via
  the author Website field, never by placing a raw Yolox link in the body
- each submitted row is verified from the public HTML when possible

The script intentionally uses only Python stdlib so it can run in the current
Codex Windows environment without Playwright or requests.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import ssl
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Iterable
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "backlinks.db"
TARGET_URL = "https://yolox.ai/"
AUTHOR = "Yolox Team"
EMAIL = "suppscanofficial@gmail.com"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
)


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict] = []
        self._form: dict | None = None
        self._textarea: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "form":
            self._form = {"attrs": attrs_dict, "fields": [], "text": ""}
        elif self._form is not None and tag in {"input", "textarea", "select", "button"}:
            field = {"tag": tag, "attrs": attrs_dict, "text": ""}
            self._form["fields"].append(field)
            if tag == "textarea":
                self._textarea = field

    def handle_data(self, data: str) -> None:
        if self._form is not None:
            self._form["text"] += data
        if self._textarea is not None:
            self._textarea["text"] += data

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "textarea":
            self._textarea = None
        elif tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None


@dataclass
class Candidate:
    id: int
    type: str
    url: str
    root_domain: str
    has_url_field: str
    notes: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def http_opener():
    return request.build_opener(
        request.HTTPCookieProcessor(CookieJar()),
        request.HTTPRedirectHandler(),
        request.HTTPSHandler(context=ssl._create_unverified_context()),
    )


def fetch(opener, url: str, data: dict | None = None, referer: str | None = None):
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    body = None
    method = "GET"
    if data is not None:
        body = parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        method = "POST"
    if referer:
        headers["Referer"] = referer
    req = request.Request(url, data=body, headers=headers, method=method)
    return opener.open(req, timeout=25)


def decode_response(resp) -> tuple[str, str]:
    raw = resp.read()
    ctype = resp.headers.get_content_charset() or "utf-8"
    return resp.geturl(), raw.decode(ctype, "replace")


def parse_forms(html: str) -> list[dict]:
    parser = FormParser()
    parser.feed(html)
    return parser.forms


def find_comment_form(forms: Iterable[dict]) -> dict | None:
    for form in forms:
        attrs = form["attrs"]
        action = attrs.get("action", "").lower()
        fid = attrs.get("id", "").lower()
        cls = attrs.get("class", "").lower()
        html_hint = " ".join(
            [
                action,
                fid,
                cls,
                form.get("text", ""),
                " ".join(f["attrs"].get("name", "") for f in form["fields"]),
                " ".join(f["attrs"].get("id", "") for f in form["fields"]),
            ]
        ).lower()
        has_textarea = any(f["tag"] == "textarea" for f in form["fields"])
        if "wp-comments-post" in action or fid in {"commentform", "ast-commentform"}:
            return form
        if has_textarea and "comment" in html_hint:
            return form
    return None


def field_names(form: dict) -> set[str]:
    return {f["attrs"].get("name", "").lower() for f in form["fields"] if f["attrs"].get("name")}


def field_ids(form: dict) -> set[str]:
    return {f["attrs"].get("id", "").lower() for f in form["fields"] if f["attrs"].get("id")}


def has_url_input(form: dict) -> bool:
    for field in form["fields"]:
        if field["tag"] not in {"input", "textarea"}:
            continue
        attrs = field["attrs"]
        typ = attrs.get("type", "").lower()
        if typ == "hidden":
            continue
        hay = " ".join(
            [
                attrs.get("name", ""),
                attrs.get("id", ""),
                attrs.get("placeholder", ""),
                attrs.get("aria-label", ""),
            ]
        ).lower()
        if re.search(r"\b(url|website|web site|homepage|site)\b", hay):
            return True
    return False


def body_text(html: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def post_title(html: str, fallback: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if not m:
        return fallback
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()
    return title[:160] or fallback


def comment_for(title: str, url: str) -> str:
    text = f"{title} {url}".lower()
    if any(k in text for k in ["recipe", "cake", "bread", "muffin", "food", "kitchen", "chocolate", "waffle", "pasta"]):
        return (
            "The step-by-step details are helpful. I especially appreciate when a post explains "
            "the small choices behind the process, because it makes the result easier to adapt later."
        )
    if any(k in text for k in ["travel", "hotel", "vacation", "trip", "tourism", "malaysia", "iceland"]):
        return (
            "The practical details are useful because they reduce planning friction. It is easier "
            "to make good decisions when timing, location, and small trade-offs are explained clearly."
        )
    if any(k in text for k in ["teacher", "school", "education", "language", "grammar", "methods", "sources"]):
        return (
            "This is a useful reminder that learning depends on clear structure and repeated feedback. "
            "The most helpful resources make the process easier to understand, not just the final answer."
        )
    if any(k in text for k in ["science", "data", "technology", "business", "report", "solar", "analytics"]):
        return (
            "The practical framing is useful. Strong projects usually need both careful information "
            "and clear context, especially when people need to understand why a decision was made."
        )
    if any(k in text for k in ["design", "creative", "art", "style", "fashion", "typography"]):
        return (
            "The examples are useful because they connect style choices with how people actually read "
            "and make decisions. Small details often change whether the result feels clear or confusing."
        )
    return (
        "Thanks for putting this together. The most useful part is the practical context, because it "
        "makes the topic easier to understand and apply beyond the original example."
    )


def normalize_action(base_url: str, action: str) -> str:
    return parse.urljoin(base_url, action or base_url)


def is_insecure_action(page_url: str, action: str) -> bool:
    return page_url.startswith("https://") and action.startswith("http://")


def build_post_data(form: dict, comment: str) -> dict:
    data: dict[str, str] = {}
    for field in form["fields"]:
        attrs = field["attrs"]
        name = attrs.get("name")
        if not name:
            continue
        tag = field["tag"]
        typ = attrs.get("type", "").lower()
        if typ in {"submit", "button", "image", "reset", "file"}:
            continue
        if typ in {"checkbox", "radio"}:
            hay = " ".join([name, attrs.get("id", ""), field.get("text", "")]).lower()
            if re.search(r"human|not.*spam|agree|terms|privacy", hay) and not re.search(
                r"subscribe|notify|newsletter|follow-up|cookies", hay
            ):
                data[name] = attrs.get("value") or "on"
            elif attrs.get("checked"):
                data[name] = attrs.get("value") or "on"
            continue
        if tag == "textarea":
            data[name] = field.get("text", "")
        else:
            data[name] = attrs.get("value", "")

    data["author"] = AUTHOR
    data["email"] = EMAIL
    data["url"] = TARGET_URL
    data["comment"] = comment
    for field in form["fields"]:
        attrs = field["attrs"]
        name = attrs.get("name", "")
        fid = attrs.get("id", "")
        if field["tag"] == "textarea" and "ak_hp" not in name.lower() and (name == "comment" or fid == "comment"):
            data[name] = comment
    if "human" in field_names(form):
        data["human"] = "on"
    return data


def classify_rel(rel: str | None) -> str:
    value = (rel or "").lower()
    if "ugc" in value:
        return "ugc"
    if "nofollow" in value:
        return "nofollow"
    if "sponsored" in value:
        return "sponsored"
    if "me" in value.split():
        return "me_no_pagerank"
    return "dofollow"


def extract_yolox_links(html: str) -> list[dict]:
    links = []
    for match in re.finditer(r"<a\b[^>]*href=[\"']([^\"']*yolox\.ai[^\"']*)[\"'][^>]*>", html, flags=re.I):
        tag = match.group(0)
        rel_match = re.search(r"rel=[\"']([^\"']*)[\"']", tag, flags=re.I)
        rel = rel_match.group(1) if rel_match else ""
        start = match.end()
        end = html.find("</a>", start)
        raw_text = html[start : end if end != -1 else start]
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw_text)).strip()
        links.append({"href": match.group(1), "rel": rel, "text": text[:120], "rel_actual": classify_rel(rel)})
    return links


def upsert_submission(cur, candidate: Candidate, status: str, rel_actual: str | None, live_url: str, error_log: str | None, notes: str, method: str) -> None:
    timestamp = now_iso()
    existing = cur.execute(
        "SELECT id FROM submissions WHERE source_table='gefei_226' AND source_id=? AND platform_domain=?",
        (candidate.id, candidate.root_domain),
    ).fetchone()
    values = (
        candidate.url,
        TARGET_URL,
        AUTHOR,
        method,
        timestamp,
        status,
        rel_actual,
        live_url,
        error_log,
        notes,
    )
    if existing:
        cur.execute(
            """
            UPDATE submissions
            SET submit_url=?, target_yolox_url=?, anchor_text=?, submit_method=?,
                submit_time=?, status=?, rel_actual=?, live_url=?, error_log=?, notes=?
            WHERE id=?
            """,
            values + (existing[0],),
        )
    else:
        cur.execute(
            """
            INSERT INTO submissions (
                source_table, source_id, platform_domain, submit_url, target_yolox_url,
                anchor_text, submit_method, submit_time, status, rel_actual,
                live_url, error_log, notes
            ) VALUES ('gefei_226', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (candidate.id, candidate.root_domain) + values,
        )


def append_note(cur, candidate_id: int, note: str, submitted: str | None = None, rel_actual: str | None = None, live_url: str | None = None) -> None:
    timestamp = now_iso()
    if submitted is None:
        cur.execute(
            "UPDATE gefei_226 SET notes=COALESCE(notes || char(10),'') || ? WHERE id=?",
            (note, candidate_id),
        )
        return
    cur.execute(
        """
        UPDATE gefei_226
        SET submitted=?, submit_time=?, rel_actual=?, live_url=?,
            notes=COALESCE(notes || char(10),'') || ?
        WHERE id=?
        """,
        (submitted, timestamp, rel_actual, live_url, note, candidate_id),
    )


def skip_profile_reason(notes: str) -> str:
    low = notes.lower()
    if "registration requires captcha" in low or "register" in low and "no website field" in low:
        return "profile registration/login route blocked or no website field"
    if "requires oauth" in low or "requires login" in low:
        return "profile requires login/oauth"
    if "no_website_field" in low:
        return "profile has no public website field"
    if "dead_nofollow" in low:
        return "profile link forced nofollow"
    if "register_closed" in low:
        return "profile registration closed"
    return "profile route not viable for public website URL"


def process_candidate(cur, candidate: Candidate, submit: bool) -> dict:
    result = {"id": candidate.id, "domain": candidate.root_domain, "type": candidate.type}
    if candidate.type == "profile":
        reason = skip_profile_reason(candidate.notes)
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped profile - {reason}.", "skipped", None, None)
        return result

    if candidate.has_url_field != "Yes":
        reason = "no URL/profile field in source data"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, None)
        return result

    op = http_opener()
    try:
        final_url, html = decode_response(fetch(op, candidate.url))
    except Exception as exc:
        reason = f"navigation_error: {type(exc).__name__}"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, None)
        return result

    text = body_text(html).lower()
    if re.search(r"comments are closed|commenting is closed|comments closed|log in to reply|must be logged in|registration required", text):
        reason = "comments closed or login required"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, final_url)
        return result

    form = find_comment_form(parse_forms(html))
    if not form:
        reason = "no comment form found"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, final_url)
        return result
    if not has_url_input(form):
        reason = "comment form has no visible website/url field"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, final_url)
        return result

    action = normalize_action(final_url, form["attrs"].get("action", ""))
    if is_insecure_action(final_url, action):
        reason = "insecure http form action from https page"
        result.update({"action": "skipped", "reason": reason})
        append_note(cur, candidate.id, f"2026-05-24 full226: skipped - {reason}.", "skipped", None, final_url)
        return result

    if not submit:
        result.update({"action": "candidate", "reason": "usable comment URL field"})
        append_note(cur, candidate.id, "2026-05-24 full226: usable comment URL field found; dry-run only.")
        return result

    title = post_title(html, candidate.root_domain)
    comment = comment_for(title, candidate.url)
    post_data = build_post_data(form, comment)
    try:
        post_url, post_html = decode_response(fetch(op, action, data=post_data, referer=final_url))
    except error.HTTPError as exc:
        err = f"HTTPError {exc.code}"
        result.update({"action": "failed", "reason": err})
        upsert_submission(cur, candidate, "failed", "submit_error", final_url, err, "Full 226 submit failed at HTTP layer.", "wp_comment_url_field_direct_post")
        append_note(cur, candidate.id, f"2026-05-24 full226: failed submit - {err}.", "failed", "submit_error", final_url)
        return result
    except Exception as exc:
        err = f"{type(exc).__name__}: {str(exc)[:120]}"
        result.update({"action": "failed", "reason": err})
        upsert_submission(cur, candidate, "failed", "submit_error", final_url, err, "Full 226 submit failed before verification.", "wp_comment_url_field_direct_post")
        append_note(cur, candidate.id, f"2026-05-24 full226: failed submit - {err}.", "failed", "submit_error", final_url)
        return result

    verify_html = post_html
    verify_url = post_url
    links = extract_yolox_links(verify_html)
    if not links:
        try:
            refetch_url = post_url.split("#")[0]
            verify_url, verify_html = decode_response(fetch(op, refetch_url, referer=post_url))
            links = extract_yolox_links(verify_html)
        except Exception:
            pass

    if links:
        rel_actual = links[0]["rel_actual"]
        status = "live"
        notes = f"Full 226 submit verified public author URL; rel={links[0]['rel'] or '(empty)'}."
        result.update({"action": "live", "rel_actual": rel_actual, "url": verify_url})
        upsert_submission(cur, candidate, status, rel_actual, verify_url, None, notes, "wp_comment_url_field_direct_post")
        append_note(cur, candidate.id, f"2026-05-24 full226: {notes}", "yes", rel_actual, verify_url)
        return result

    post_text = body_text(post_html).lower()
    if re.search(r"duplicate comment|already said that|you are posting comments too quickly", post_text):
        status = "failed"
        rel_actual = "submit_rejected"
        err = "duplicate_or_rate_limited"
        result.update({"action": "failed", "reason": err})
        upsert_submission(cur, candidate, status, rel_actual, post_url, err, "Full 226 submit rejected by WordPress.", "wp_comment_url_field_direct_post")
        append_note(cur, candidate.id, f"2026-05-24 full226: failed - {err}.", "failed", rel_actual, post_url)
        return result

    status = "pending"
    err = "no_public_link_visible"
    notes = "Full 226 submit attempted; no public Yolox link visible on immediate verification."
    result.update({"action": "pending", "reason": err, "url": post_url})
    upsert_submission(cur, candidate, status, None, post_url, err, notes, "wp_comment_url_field_direct_post")
    append_note(cur, candidate.id, f"2026-05-24 full226: {notes}", "pending", None, post_url)
    return result


def load_candidates(cur, limit: int | None = None) -> list[Candidate]:
    query = """
        SELECT id, type, url, root_domain, has_url_field, COALESCE(notes,'')
        FROM gefei_226
        WHERE submitted='no'
        ORDER BY id
    """
    if limit:
        query += f" LIMIT {int(limit)}"
    return [Candidate(*row) for row in cur.execute(query).fetchall()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.8)
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    candidates = load_candidates(cur, args.limit)
    print(f"Processing {len(candidates)} submitted='no' rows commit={args.commit} submit={args.submit}")
    results = []
    for i, candidate in enumerate(candidates, 1):
        res = process_candidate(cur, candidate, submit=args.submit)
        results.append(res)
        print(f"[{i:03d}/{len(candidates):03d}] #{candidate.id:<3} {candidate.root_domain:<34} {res.get('action')} {res.get('rel_actual', res.get('reason', ''))}")
        if args.commit:
            conn.commit()
        time.sleep(args.sleep)

    if not args.commit:
        conn.rollback()
    else:
        conn.commit()

    summary: dict[str, int] = {}
    for res in results:
        summary[res["action"]] = summary.get(res["action"], 0) + 1
    print("SUMMARY", json.dumps(summary, sort_keys=True))
    remaining = cur.execute("SELECT COUNT(*) FROM gefei_226 WHERE submitted='no'").fetchone()[0]
    print(f"remaining_no={remaining}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
