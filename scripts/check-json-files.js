const fs = require("fs");
const path = require("path");

const root = process.cwd();
const rootsToCheck = ["miniprogram", "."];
const ignoredDirs = new Set([".git", "node_modules", ".worktrees"]);
const files = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (ignoredDirs.has(entry.name)) {
        continue;
      }
      walk(path.join(dir, entry.name));
      continue;
    }

    if (entry.isFile() && entry.name.endsWith(".json")) {
      files.push(path.join(dir, entry.name));
    }
  }
}

for (const item of rootsToCheck) {
  const absolutePath = path.join(root, item);
  if (!fs.existsSync(absolutePath)) {
    continue;
  }

  if (fs.statSync(absolutePath).isDirectory()) {
    walk(absolutePath);
  } else if (absolutePath.endsWith(".json")) {
    files.push(absolutePath);
  }
}

const uniqueFiles = [...new Set(files)].sort();
const failures = [];

for (const file of uniqueFiles) {
  try {
    JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    failures.push(`${path.relative(root, file)}: ${error.message}`);
  }
}

if (failures.length > 0) {
  console.error("JSON check failed");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log(`JSON check OK (${uniqueFiles.length} files checked)`);
