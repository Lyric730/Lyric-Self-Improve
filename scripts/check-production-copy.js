const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const APP_JSON_PATH = path.join(ROOT, "miniprogram", "app.json");

const BANNED_PATTERNS = [
  "内部校验",
  "PM 说明",
  "PM说明",
  "演示状态",
  "演示",
  "模拟",
  "mock",
  "Mock",
  "MVP",
  "调试",
  "临时",
  "占位",
  "本页",
  "本页只做",
  "当前 mock",
  "后续接入",
  "后续切换",
  "服务器记录",
  "后台模板",
  "开发说明",
  "测试随机奖励",
  "演示进入结算",
  "FLOW",
  "已完成"
];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function collectFiles() {
  const appJson = readJson(APP_JSON_PATH);
  const files = [APP_JSON_PATH];

  appJson.pages.forEach((pagePath) => {
    files.push(path.join(ROOT, "miniprogram", `${pagePath}.wxml`));
  });

  const screenDir = path.join(ROOT, "screen");

  if (fs.existsSync(screenDir)) {
    fs.readdirSync(screenDir)
      .filter((fileName) => fileName.endsWith(".html"))
      .forEach((fileName) => files.push(path.join(screenDir, fileName)));
  }

  return files.filter((filePath) => fs.existsSync(filePath));
}

function findViolations(files) {
  const violations = [];

  files.forEach((filePath) => {
    const content = fs.readFileSync(filePath, "utf8");
    const lines = content.split(/\r?\n/);

    lines.forEach((line, index) => {
      BANNED_PATTERNS.forEach((pattern) => {
        if (line.includes(pattern)) {
          violations.push({
            filePath: path.relative(ROOT, filePath),
            line: index + 1,
            pattern,
            text: line.trim()
          });
        }
      });
    });
  });

  return violations;
}

const files = collectFiles();
const violations = findViolations(files);

if (violations.length > 0) {
  console.error("Production copy check failed:");
  violations.forEach((violation) => {
    console.error(`${violation.filePath}:${violation.line} [${violation.pattern}] ${violation.text}`);
  });
  process.exit(1);
}

console.log(`Production copy check OK (${files.length} files checked)`);
