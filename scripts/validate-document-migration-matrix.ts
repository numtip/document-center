#!/usr/bin/env tsx
/**
 * validate-document-migration-matrix.ts
 * Phase 5A.6 — Validates migration-matrix.v2.csv for registry hardening
 */

import * as fs from "fs";
import * as path from "path";

// ─── Types ────────────────────────────────────────────────────────────
interface MigrationRow {
  id: string;
  title: string;
  category: string;
  owner: string;
  fileType: string;
  action: string;
  confidence: string;
  registryCandidate: string;
  legacySource: string;
  notes: string;
}

// ─── Constants ────────────────────────────────────────────────────────
const VALID_ACTIONS = ["keep", "rewrite", "merge", "archive", "drop", "review"];
const VALID_CATEGORIES = [
  "admin",
  "finance-procurement",
  "research",
  "academic-service",
  "policy-planning",
  "manuals",
];

const REQUIRED_COLUMNS = [
  "id",
  "title",
  "category",
  "owner",
  "fileType",
  "action",
  "confidence",
  "registryCandidate",
  "legacySource",
];

// ─── CSV Parser (simple, handles quoted fields) ──────────────────────
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') {
        current += '"';
        i++;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        current += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ",") {
        result.push(current.trim());
        current = "";
      } else {
        current += ch;
      }
    }
  }
  result.push(current.trim());
  return result;
}

function parseCSV(content: string): MigrationRow[] {
  const lines = content
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.length > 0);
  if (lines.length === 0) return [];

  const headers = parseCSVLine(lines[0]);
  const rows: MigrationRow[] = [];

  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    const row: Record<string, string> = {};
    headers.forEach((h, idx) => {
      row[h] = values[idx] || "";
    });
    rows.push(row as unknown as MigrationRow);
  }
  return rows;
}

// ─── Validation ───────────────────────────────────────────────────────
interface ValidationResult {
  errors: string[];
  warnings: string[];
  summary: {
    totalRows: number;
    byAction: Record<string, number>;
    byCategory: Record<string, number>;
    registryCandidates: number;
    dropped: number;
  };
}

function validate(filePath: string): ValidationResult {
  const result: ValidationResult = {
    errors: [],
    warnings: [],
    summary: {
      totalRows: 0,
      byAction: {},
      byCategory: {},
      registryCandidates: 0,
      dropped: 0,
    },
  };

  // 1. File exists
  if (!fs.existsSync(filePath)) {
    result.errors.push(`File not found: ${filePath}`);
    return result;
  }

  const content = fs.readFileSync(filePath, "utf-8");
  const rows = parseCSV(content);

  if (rows.length === 0) {
    result.errors.push("CSV file is empty or has no data rows");
    return result;
  }

  result.summary.totalRows = rows.length;

  // 2. Check required columns exist
  const headerLine = content.split("\n")[0];
  const headers = parseCSVLine(headerLine);
  const headerSet = new Set(headers);

  for (const col of REQUIRED_COLUMNS) {
    if (!headerSet.has(col)) {
      result.errors.push(`Missing required column: ${col}`);
    }
  }

  if (result.errors.length > 0) {
    return result;
  }

  // 3. Validate each row
  const seenIds = new Set<string>();
  const seenLegacySources = new Set<string>();

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const rowNum = i + 2; // 1-indexed + header row
    const rowId = row.id || `ROW-${rowNum}`;

    // a. ID must exist (stable id or legacy source)
    if (!row.id && !row.legacySource) {
      result.errors.push(
        `[Row ${rowNum}] Neither 'id' nor 'legacySource' is provided`
      );
    }

    // b. No duplicate IDs
    if (row.id) {
      if (seenIds.has(row.id)) {
        result.errors.push(`[Row ${rowNum}] Duplicate document id: ${row.id}`);
      }
      seenIds.add(row.id);
    }

    // c. No duplicate legacy sources
    if (row.legacySource) {
      if (seenLegacySources.has(row.legacySource)) {
        result.warnings.push(
          `[Row ${rowNum}] Duplicate legacySource: ${row.legacySource}`
        );
      }
      seenLegacySources.add(row.legacySource);
    }

    // d. Valid action
    if (!VALID_ACTIONS.includes(row.action)) {
      result.errors.push(
        `[Row ${rowNum}] Invalid action '${row.action}' — must be one of: ${VALID_ACTIONS.join(", ")}`
      );
    }

    // e. Category not empty for keep/rewrite/merge/archive
    if (
      ["keep", "rewrite", "merge", "archive"].includes(row.action) &&
      (!row.category || row.category.trim() === "")
    ) {
      result.errors.push(
        `[Row ${rowNum}] Category is required for action '${row.action}'`
      );
    }

    // f. Valid category if non-empty
    if (
      row.category &&
      row.category.trim() !== "" &&
      !VALID_CATEGORIES.includes(row.category)
    ) {
      result.warnings.push(
        `[Row ${rowNum}] Category '${row.category}' is not in taxonomy`
      );
    }

    // g. Owner present or marked TBD
    if (!row.owner || row.owner.trim() === "") {
      result.errors.push(`[Row ${rowNum}] Owner is required (or mark TBD)`);
    }

    // h. Confidence preserved for review rows
    if (row.action === "review" && row.confidence === "high") {
      result.warnings.push(
        `[Row ${rowNum}] Review action with high confidence — consider resolving`
      );
    }

    // i. Title not empty
    if (!row.title || row.title.trim() === "") {
      result.errors.push(`[Row ${rowNum}] Title is required`);
    }

    // j. Registry candidate consistency
    if (row.action === "drop" && row.registryCandidate !== "false") {
      result.warnings.push(
        `[Row ${rowNum}] Dropped row should have registryCandidate=false`
      );
    }

    // Aggregate stats
    result.summary.byAction[row.action] =
      (result.summary.byAction[row.action] || 0) + 1;
    result.summary.byCategory[row.category] =
      (result.summary.byCategory[row.category] || 0) + 1;
    if (row.registryCandidate === "true") {
      result.summary.registryCandidates++;
    }
    if (row.action === "drop") {
      result.summary.dropped++;
    }
  }

  return result;
}

// ─── Main ─────────────────────────────────────────────────────────────
function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error("Usage: tsx validate-document-migration-matrix.ts <csv-path>");
    process.exit(1);
  }

  const resolvedPath = path.resolve(filePath);
  console.log(`\n🔍 Validating migration matrix: ${resolvedPath}\n`);

  const result = validate(resolvedPath);

  // Print errors
  if (result.errors.length > 0) {
    console.log("❌ ERRORS:");
    result.errors.forEach((e) => console.log(`   • ${e}`));
    console.log();
  }

  // Print warnings
  if (result.warnings.length > 0) {
    console.log("⚠️  WARNINGS:");
    result.warnings.forEach((w) => console.log(`   • ${w}`));
    console.log();
  }

  // Print summary
  console.log("📊 SUMMARY:");
  console.log(`   Total rows:    ${result.summary.totalRows}`);
  console.log(`   Registry candidates: ${result.summary.registryCandidates}`);
  console.log(`   Dropped:       ${result.summary.dropped}`);
  console.log();
  console.log("   By action:");
  for (const [action, count] of Object.entries(result.summary.byAction)) {
    console.log(`     ${action}: ${count}`);
  }
  console.log();
  console.log("   By category:");
  for (const [cat, count] of Object.entries(result.summary.byCategory)) {
    console.log(`     ${cat}: ${count}`);
  }

  console.log();
  if (result.errors.length === 0) {
    console.log("✅ Validation PASSED — no errors found");
  } else {
    console.log(
      `❌ Validation FAILED — ${result.errors.length} error(s), ${result.warnings.length} warning(s)`
    );
  }

  process.exit(result.errors.length > 0 ? 1 : 0);
}

main();
