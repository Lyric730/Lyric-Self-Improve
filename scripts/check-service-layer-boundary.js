const fs = require("fs");
const path = require("path");

const root = process.cwd();
const pagesRoot = path.join(root, "miniprogram", "pages");
const forbiddenPatterns = [
  {
    pattern: /require\([^)]*ladder-data[^)]*\)/,
    reason: "pages must read local data through miniprogram/services"
  },
  {
    pattern: /require\([^)]*operation-log[^)]*\)/,
    reason: "pages must not write operation logs directly"
  },
  {
    pattern: /require\([^)]*settlement-engine[^)]*\)/,
    reason: "pages must settle through match-service"
  }
];

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      walk(fullPath, files);
      continue;
    }

    if (entry.isFile() && entry.name.endsWith(".js")) {
      files.push(fullPath);
    }
  }

  return files;
}

const failures = [];

for (const file of walk(pagesRoot)) {
  const content = fs.readFileSync(file, "utf8");
  const relativePath = path.relative(root, file);

  for (const item of forbiddenPatterns) {
    if (item.pattern.test(content)) {
      failures.push(`${relativePath}: ${item.reason}`);
    }
  }
}

if (failures.length > 0) {
  console.error("Service layer boundary check failed");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("Service layer boundary check OK");
