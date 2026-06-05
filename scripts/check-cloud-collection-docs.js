const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const CLOUD_FUNCTION_PATH = path.join(ROOT, "cloudfunctions", "yunhanApi", "index.js");
const SCHEMA_PATH = path.join(ROOT, "docs", "cloud-database-schema.md");
const RUNBOOK_PATH = path.join(ROOT, "docs", "cloud-init-runbook.md");

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function extractCodeCollections(source) {
  const collections = new Set();
  const pattern = /db\.collection\(["']([^"']+)["']\)/g;
  let match = pattern.exec(source);

  while (match) {
    collections.add(match[1]);
    match = pattern.exec(source);
  }

  return [...collections].sort();
}

function assertMentioned(collections, documentText, documentName) {
  const missing = collections.filter((collectionName) => !documentText.includes(`\`${collectionName}\``));

  if (missing.length > 0) {
    throw new Error(`${documentName} missing collections: ${missing.join(", ")}`);
  }
}

const codeCollections = extractCodeCollections(readText(CLOUD_FUNCTION_PATH));

if (codeCollections.length === 0) {
  throw new Error("No cloud database collections found in yunhanApi");
}

assertMentioned(codeCollections, readText(SCHEMA_PATH), "docs/cloud-database-schema.md");
assertMentioned(codeCollections, readText(RUNBOOK_PATH), "docs/cloud-init-runbook.md");

console.log(`Cloud collection docs check OK (${codeCollections.length} collections checked)`);
