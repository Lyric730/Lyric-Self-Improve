"""
Wait for Google CAPTCHA cooldown, then re-run capture_quora_ih.py.

Strategy:
  · Initial wait: 12 min (typical Google soft-block window)
  · Probe with 1 cheap search; if still blocked, wait +5 min, retry up to 3x
  · On success, exec full capture_quora_ih.py
  · Total max wait: 12 + 5*3 = 27 min
"""

import subprocess
import sys
import time
from pathlib import Path

INITIAL_WAIT = 720   # 12 min
RETRY_BACKOFF = 300  # 5 min between probe retries
MAX_PROBES = 3

OPENCLI_PREFIX = "source ~/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && opencli"
PROBE_CMD = f"bash -c '{OPENCLI_PREFIX} google search \"hello world\" --limit 1 -f json'"
CAPTURE_SCRIPT = Path(__file__).parent / "capture_quora_ih.py"


def probe_google():
    """Return True if google search responds with valid data; False if CAPTCHA/empty."""
    try:
        r = subprocess.run(PROBE_CMD, shell=True, capture_output=True, text=True, timeout=60)
        out = r.stdout.strip()
        if r.returncode == 0 and out.startswith("["):
            return True, out[:120]
        return False, (out + r.stderr)[:200]
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)


def main():
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Initial wait {INITIAL_WAIT}s for Google CAPTCHA cooldown...", flush=True)
    time.sleep(INITIAL_WAIT)

    for attempt in range(1, MAX_PROBES + 1):
        elapsed = time.time() - t0
        print(f"\n[{time.strftime('%H:%M:%S')}] +{elapsed:.0f}s · Probe {attempt}/{MAX_PROBES}: testing google search", flush=True)
        ok, sample = probe_google()
        if ok:
            print(f"  ✓ Google reachable. Sample: {sample}", flush=True)
            print(f"\n[{time.strftime('%H:%M:%S')}] Running full capture_quora_ih.py", flush=True)
            r = subprocess.run(
                f"bash -c 'source ~/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && python3 -u {CAPTURE_SCRIPT}'",
                shell=True,
            )
            return r.returncode
        print(f"  ✗ Still blocked: {sample}", flush=True)
        if attempt < MAX_PROBES:
            print(f"  → Wait {RETRY_BACKOFF}s before next probe", flush=True)
            time.sleep(RETRY_BACKOFF)

    elapsed = time.time() - t0
    print(f"\n[{time.strftime('%H:%M:%S')}] Gave up after {elapsed:.0f}s ({MAX_PROBES} probes). CAPTCHA persists.", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
