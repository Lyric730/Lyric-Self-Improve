const fs = require("fs");
const path = require("path");

const ROOT = process.cwd();
const MINIPROGRAM_ROOT = path.join(ROOT, "miniprogram");
const APP_JSON_PATH = path.join(MINIPROGRAM_ROOT, "app.json");

const REQUIRED_PLAYER_FLOW = [
  "pages/challenge-home/challenge-home",
  "pages/waiting-room/waiting-room",
  "pages/accept-challenge/accept-challenge",
  "pages/mode-select/mode-select",
  "pages/points-select/points-select",
  "pages/match-confirm/match-confirm",
  "pages/match-scoring/match-scoring",
  "pages/time-insufficient/time-insufficient",
  "pages/settlement/settlement",
  "pages/refusal/refusal",
  "pages/match-result/match-result"
];

const TAB_PAGES = [
  "pages/challenge-home/challenge-home",
  "pages/my-data/my-data",
  "pages/rankings/rankings",
  "pages/points-perks/points-perks",
  "pages/my-hub/my-hub"
];

const IN_MATCH_PAGES = [
  "pages/waiting-room/waiting-room",
  "pages/accept-challenge/accept-challenge",
  "pages/mode-select/mode-select",
  "pages/points-select/points-select",
  "pages/match-confirm/match-confirm",
  "pages/match-scoring/match-scoring",
  "pages/time-insufficient/time-insufficient",
  "pages/settlement/settlement",
  "pages/refusal/refusal",
  "pages/match-result/match-result"
];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function pageFile(pagePath, extension) {
  return path.join(MINIPROGRAM_ROOT, `${pagePath}.${extension}`);
}

function pageWxml(pagePath) {
  return fs.readFileSync(pageFile(pagePath, "wxml"), "utf8");
}

function assertCondition(condition, message, failures) {
  if (!condition) {
    failures.push(message);
  }
}

const appJson = readJson(APP_JSON_PATH);
const pages = appJson.pages || [];
const failures = [];

assertCondition(
  pages[0] === "pages/challenge-home/challenge-home",
  "The first formal page must be pages/challenge-home/challenge-home.",
  failures
);

assertCondition(
  !pages.includes("pages/ui-kit/ui-kit"),
  "pages/ui-kit/ui-kit must not be listed in miniprogram/app.json formal pages.",
  failures
);

pages.forEach((pagePath) => {
  ["js", "json", "wxml", "wxss"].forEach((extension) => {
    assertCondition(
      fs.existsSync(pageFile(pagePath, extension)),
      `${pagePath}.${extension} is missing.`,
      failures
    );
  });
});

let lastIndex = -1;
REQUIRED_PLAYER_FLOW.forEach((pagePath) => {
  const currentIndex = pages.indexOf(pagePath);

  assertCondition(currentIndex !== -1, `${pagePath} is missing from app.json.`, failures);

  if (currentIndex !== -1) {
    assertCondition(
      currentIndex > lastIndex,
      `${pagePath} must appear after the previous player-flow page in app.json.`,
      failures
    );
    lastIndex = currentIndex;
  }
});

TAB_PAGES.forEach((pagePath) => {
  if (!pages.includes(pagePath)) {
    return;
  }

  assertCondition(
    pageWxml(pagePath).includes("<bottom-nav"),
    `${pagePath} should include <bottom-nav for formal tab navigation.`,
    failures
  );
});

IN_MATCH_PAGES.forEach((pagePath) => {
  if (!pages.includes(pagePath)) {
    return;
  }

  assertCondition(
    !pageWxml(pagePath).includes("<bottom-nav"),
    `${pagePath} is an in-match flow page and must not include <bottom-nav.`,
    failures
  );
});

if (failures.length > 0) {
  console.error("Player flow route check failed:");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("Player flow route check OK");
