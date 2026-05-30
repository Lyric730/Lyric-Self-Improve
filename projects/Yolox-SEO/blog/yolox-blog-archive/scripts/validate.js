const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const POSTS_DIR = path.join(ROOT, "posts");
const MANIFEST_PATH = path.join(ROOT, "manifest.json");

const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const TAG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const REQUIRED_MANIFEST_FIELDS = ["slug", "title", "description", "date", "author", "author_linkedin", "tags"];
const REQUIRED_FRONTMATTER_FIELDS = ["title", "description", "date", "author", "author_linkedin", "tags"];
const SYNC_FIELDS = ["title", "description", "date", "author", "author_linkedin", "tags"];

const errors = [];

function fail(msg) {
  errors.push(msg);
  console.error(`ERROR: ${msg}`);
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;

  const fields = {};
  let currentKey = null;
  let inArray = false;
  let arrayItems = [];

  for (const line of match[1].split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (inArray) {
      if (trimmed.startsWith("- ")) {
        arrayItems.push(trimmed.slice(2).replace(/^["']|["']$/g, ""));
        continue;
      }
      fields[currentKey] = arrayItems;
      inArray = false;
      arrayItems = [];
    }

    const kvMatch = trimmed.match(/^(\w+):\s*(.*)/);
    if (!kvMatch) continue;

    const [, key, rawValue] = kvMatch;
    currentKey = key;

    if (rawValue === "" || rawValue === undefined) {
      inArray = true;
      arrayItems = [];
      continue;
    }

    const inlineArray = rawValue.match(/^\[(.*)?\]$/);
    if (inlineArray) {
      fields[key] = inlineArray[1]
        ? inlineArray[1].split(",").map((s) => s.trim().replace(/^["']|["']$/g, ""))
        : [];
      continue;
    }

    fields[key] = rawValue.replace(/^["']|["']$/g, "");
  }

  if (inArray) {
    fields[currentKey] = arrayItems;
  }

  if (fields.draft !== undefined) {
    fields.draft = fields.draft === "true" || fields.draft === true;
  }

  return fields;
}

// --- Validate manifest.json ---

let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf-8"));
} catch (e) {
  fail(`manifest.json is not valid JSON: ${e.message}`);
  process.exit(1);
}

if (typeof manifest.version !== "number") {
  fail('manifest.json missing numeric "version" field');
}

if (!Array.isArray(manifest.posts)) {
  fail('manifest.json missing "posts" array');
  process.exit(1);
}

const manifestSlugs = new Set();

for (const entry of manifest.posts) {
  const label = entry.slug || "(missing slug)";

  for (const field of REQUIRED_MANIFEST_FIELDS) {
    if (entry[field] === undefined || entry[field] === null || entry[field] === "") {
      fail(`[${label}] manifest entry missing required field "${field}"`);
    }
  }

  if (entry.slug) {
    if (!SLUG_RE.test(entry.slug)) {
      fail(`[${label}] slug must be lowercase kebab-case`);
    }
    if (manifestSlugs.has(entry.slug)) {
      fail(`[${label}] duplicate slug in manifest`);
    }
    manifestSlugs.add(entry.slug);
  }

  if (entry.date && !ISO_DATE_RE.test(entry.date)) {
    fail(`[${label}] date must be ISO 8601 (YYYY-MM-DD), got "${entry.date}"`);
  }

  if (Array.isArray(entry.tags)) {
    for (const tag of entry.tags) {
      if (!TAG_RE.test(tag)) {
        fail(`[${label}] tag "${tag}" must be lowercase kebab-case`);
      }
    }
  }

  if (entry.order !== undefined) {
    if (typeof entry.order !== "number" || !Number.isInteger(entry.order)) {
      fail(`[${label}] order must be an integer`);
    }
  }

  if (entry.coverImage) {
    const coverPath = path.join(ROOT, entry.coverImage);
    if (!fs.existsSync(coverPath)) {
      fail(`[${label}] coverImage file not found: ${entry.coverImage}`);
    }
  }
}

// --- Check sort order: order asc (first), then date desc ---

function sortKey(entry) {
  const hasOrder = entry.order !== undefined && entry.order !== null;
  return {
    group: hasOrder ? 0 : 1,
    order: hasOrder ? entry.order : 0,
    date: entry.date || "",
  };
}

for (let i = 1; i < manifest.posts.length; i++) {
  const a = sortKey(manifest.posts[i - 1]);
  const b = sortKey(manifest.posts[i]);

  let outOfOrder = false;
  if (a.group !== b.group) {
    outOfOrder = a.group > b.group;
  } else if (a.group === 0) {
    outOfOrder = a.order > b.order;
  } else {
    outOfOrder = a.date < b.date;
  }

  if (outOfOrder) {
    const prev = manifest.posts[i - 1].slug;
    const curr = manifest.posts[i].slug;
    fail(`manifest.posts not sorted correctly: "${prev}" should come after "${curr}" (order asc > date desc)`);
  }
}

// --- Validate each post directory ---

const postDirs = fs.existsSync(POSTS_DIR)
  ? fs.readdirSync(POSTS_DIR).filter((d) => fs.statSync(path.join(POSTS_DIR, d)).isDirectory())
  : [];

for (const dir of postDirs) {
  const indexPath = path.join(POSTS_DIR, dir, "index.md");

  if (!SLUG_RE.test(dir)) {
    fail(`[${dir}] directory name must be lowercase kebab-case`);
  }

  if (!fs.existsSync(indexPath)) {
    fail(`[${dir}] missing index.md`);
    continue;
  }

  const content = fs.readFileSync(indexPath, "utf-8");
  const fm = parseFrontmatter(content);

  if (!fm) {
    fail(`[${dir}] index.md missing frontmatter`);
    continue;
  }

  for (const field of REQUIRED_FRONTMATTER_FIELDS) {
    if (fm[field] === undefined || fm[field] === null || fm[field] === "") {
      fail(`[${dir}] frontmatter missing required field "${field}"`);
    }
  }

  if (fm.date && !ISO_DATE_RE.test(fm.date)) {
    fail(`[${dir}] frontmatter date must be ISO 8601 (YYYY-MM-DD), got "${fm.date}"`);
  }

  if (Array.isArray(fm.tags)) {
    for (const tag of fm.tags) {
      if (!TAG_RE.test(tag)) {
        fail(`[${dir}] frontmatter tag "${tag}" must be lowercase kebab-case`);
      }
    }
  }

  // --- Check frontmatter <-> manifest consistency ---

  const manifestEntry = manifest.posts.find((p) => p.slug === dir);

  if (!manifestEntry) {
    fail(`[${dir}] post directory exists but no matching entry in manifest.json`);
    continue;
  }

  for (const field of SYNC_FIELDS) {
    const mVal = JSON.stringify(manifestEntry[field]);
    const fVal = JSON.stringify(fm[field]);
    if (mVal !== fVal) {
      fail(`[${dir}] "${field}" mismatch — manifest: ${mVal}, frontmatter: ${fVal}`);
    }
  }
}

// --- Check manifest entries without post directories ---

for (const entry of manifest.posts) {
  if (!entry.slug) continue;
  const dirPath = path.join(POSTS_DIR, entry.slug);
  if (!fs.existsSync(dirPath)) {
    fail(`[${entry.slug}] manifest entry has no matching post directory`);
  }
}

// --- Check for broken image references in markdown ---

for (const dir of postDirs) {
  const indexPath = path.join(POSTS_DIR, dir, "index.md");
  if (!fs.existsSync(indexPath)) continue;

  const content = fs.readFileSync(indexPath, "utf-8");
  const imageRefs = [...content.matchAll(/!\[.*?\]\(\.\/(.+?)\)/g)];

  for (const [, filename] of imageRefs) {
    const imgPath = path.join(POSTS_DIR, dir, filename);
    if (!fs.existsSync(imgPath)) {
      fail(`[${dir}] broken image reference: ./${filename}`);
    }
  }
}

// --- Summary ---

if (errors.length > 0) {
  console.error(`\nValidation failed with ${errors.length} error(s).`);
  process.exit(1);
} else {
  console.log("Validation passed.");
}
