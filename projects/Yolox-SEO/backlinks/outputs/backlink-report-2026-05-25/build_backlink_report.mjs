import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const dataPath = path.join(__dirname, "backlink_report_data.json");
const outputPath = path.join(__dirname, "yolox-backlink-progress-2026-05-25.xlsx");

const raw = await fs.readFile(dataPath, "utf8");
const data = JSON.parse(raw);

const workbook = Workbook.create();

function colName(index) {
  let n = index + 1;
  let s = "";
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - m) / 26);
  }
  return s;
}

function rangeAddress(rowCount, colCount) {
  return `A1:${colName(colCount - 1)}${rowCount}`;
}

function value(v) {
  if (v === null || v === undefined) return "";
  if (typeof v === "object") return JSON.stringify(v);
  return v;
}

function writeTable(sheet, headers, rows, options = {}) {
  const matrix = [headers, ...rows.map((row) => headers.map((h) => value(row[h])))];
  const range = sheet.getRange(rangeAddress(matrix.length, headers.length));
  range.values = matrix;
  sheet.getRange(`A1:${colName(headers.length - 1)}1`).format = {
    fill: options.headerFill || "#1F4E79",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
  };
  range.format.wrapText = true;
  sheet.freezePanes.freezeRows(1);
  sheet.showGridLines = false;
  headers.forEach((header, i) => {
    const width = options.widths?.[header] ?? defaultWidth(header);
    sheet.getRange(`${colName(i)}:${colName(i)}`).format.columnWidthPx = width;
  });
}

function defaultWidth(header) {
  const wide = new Set(["notes", "error_log", "live_url", "submit_url", "target_yolox_url"]);
  if (wide.has(header)) return 360;
  if (header.includes("status") || header.includes("method")) return 150;
  if (header.includes("password")) return 220;
  if (header.includes("email")) return 220;
  if (header.includes("domain")) return 180;
  return 120;
}

function addSheet(name) {
  return workbook.worksheets.add(name);
}

const overview = addSheet("Overview");
writeTable(
  overview,
  ["metric", "value"],
  data.summary,
  { widths: { metric: 260, value: 620 }, headerFill: "#17324D" },
);

const statusStart = data.summary.length + 4;
overview.getRange(`A${statusStart}:B${statusStart}`).values = [["status", "count"]];
overview.getRange(`A${statusStart}:B${statusStart}`).format = {
  fill: "#556B2F",
  font: { bold: true, color: "#FFFFFF" },
};
overview.getRange(`A${statusStart + 1}:B${statusStart + data.status_counts.length}`).values =
  data.status_counts.map((r) => [r.status, r.count]);

const relStart = statusStart + data.status_counts.length + 3;
overview.getRange(`A${relStart}:B${relStart}`).values = [["rel_actual", "count"]];
overview.getRange(`A${relStart}:B${relStart}`).format = {
  fill: "#6A3D2A",
  font: { bold: true, color: "#FFFFFF" },
};
overview.getRange(`A${relStart + 1}:B${relStart + data.rel_counts.length}`).values =
  data.rel_counts.map((r) => [r.rel_actual, r.count]);
overview.getRange("A:B").format.columnWidthPx = 260;
overview.getRange("B:B").format.columnWidthPx = 560;

writeTable(
  addSheet("Accounts"),
  [
    "platform_domain",
    "account_email",
    "username",
    "password",
    "auth_method",
    "credential_status",
    "source_submission_id",
    "submission_status",
    "rel_actual",
    "live_url",
    "notes",
    "updated_at",
  ],
  data.accounts,
  {
    headerFill: "#7A3E00",
    widths: {
      platform_domain: 180,
      account_email: 230,
      username: 150,
      password: 260,
      auth_method: 150,
      credential_status: 190,
      source_submission_id: 120,
      submission_status: 190,
      rel_actual: 130,
      live_url: 380,
      notes: 520,
      updated_at: 170,
    },
  },
);

writeTable(
  addSheet("Live Links"),
  ["id", "platform_domain", "status", "rel_actual", "live_url", "notes"],
  data.live_links,
  { headerFill: "#285C3A" },
);

writeTable(
  addSheet("Pending Review"),
  ["id", "platform_domain", "status", "rel_actual", "live_url", "notes"],
  data.pending_next,
  { headerFill: "#806000" },
);

writeTable(
  addSheet("Submissions"),
  [
    "id",
    "source_table",
    "source_id",
    "platform_domain",
    "dr",
    "category",
    "submit_url",
    "target_yolox_url",
    "anchor_text",
    "submit_method",
    "submit_time",
    "status",
    "rel_actual",
    "live_url",
    "error_log",
    "notes",
  ],
  data.submissions,
  {
    headerFill: "#1F4E79",
    widths: {
      id: 70,
      source_table: 120,
      source_id: 90,
      platform_domain: 190,
      dr: 70,
      category: 130,
      submit_url: 360,
      target_yolox_url: 220,
      anchor_text: 220,
      submit_method: 160,
      submit_time: 170,
      status: 190,
      rel_actual: 150,
      live_url: 380,
      error_log: 300,
      notes: 520,
    },
  },
);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

for (const sheetName of ["Overview", "Accounts", "Live Links", "Pending Review", "Submissions"]) {
  await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(outputPath);
