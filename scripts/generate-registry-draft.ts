#!/usr/bin/env tsx
/**
 * generate-registry-draft.ts
 * Phase 5A.6 — Generates document-registry.draft.json from migration-matrix.v2.csv
 *
 * Rules:
 * - Include only keep/rewrite/merge/archive candidates
 * - Exclude drop
 * - Keep review rows only if registryCandidate=true
 * - Placeholder storageUrl: "PENDING_ONEDRIVE"
 * - migrationStatus field added
 * - No invented URLs or fabricated owners
 * - Preserve legacy URL/source metadata
 */

import * as fs from "fs";
import * as path from "path";

// ─── CSV Parser ───────────────────────────────────────────────────────
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') { current += '"'; i++; }
      else if (ch === '"') { inQuotes = false; }
      else { current += ch; }
    } else {
      if (ch === '"') { inQuotes = true; }
      else if (ch === ",") { result.push(current.trim()); current = ""; }
      else { current += ch; }
    }
  }
  result.push(current.trim());
  return result;
}

// ─── Load taxonomy ────────────────────────────────────────────────────
interface TaxonomyCategory {
  id: string;
  name_th: string;
  name_en: string;
  folder: string;
}

function loadTaxonomy(taxonomyPath: string): TaxonomyCategory[] {
  if (!fs.existsSync(taxonomyPath)) return [];
  const data = JSON.parse(fs.readFileSync(taxonomyPath, "utf-8"));
  return data.categories || [];
}

// ─── Build registry ───────────────────────────────────────────────────
interface RegistryDocument {
  id: string;
  title: string;
  category: string;
  owner: string;
  fileType: string;
  updatedDate: string;
  status: string;
  storageUrl: string;
  tags: string[];
  legacySource: string;
  migrationAction: string;
  migrationStatus: string;
  notes: string;
}

function determineMigrationStatus(
  action: string,
  owner: string,
  confidence: string
): string {
  // Owner TBD takes priority — can't proceed without an owner
  if (!owner || owner === "TBD") return "needs-owner";
  if (action === "review") return "needs-human-review";
  return "needs-onedrive-url";
}

function generateTags(title: string, category: string): string[] {
  const tags: string[] = [];
  tags.push(category);
  // Extract meaningful keywords from title (basic heuristic)
  const words = title.split(/[\s,()]+/).filter((w) => w.length > 3);
  for (const w of words.slice(0, 3)) {
    const lower = w.toLowerCase();
    if (!tags.includes(lower)) tags.push(lower);
  }
  return tags;
}

function main() {
  const matrixPath = process.argv[2];
  const taxonomyPath = process.argv[3];
  const outputPath = process.argv[4];

  if (!matrixPath || !outputPath) {
    console.error(
      "Usage: tsx generate-registry-draft.ts <matrix-csv> [taxonomy-json] <output-json>"
    );
    process.exit(1);
  }

  const resolvedMatrix = path.resolve(matrixPath);
  const resolvedTaxonomy = taxonomyPath ? path.resolve(taxonomyPath) : "";
  const resolvedOutput = path.resolve(outputPath);

  // Load taxonomy
  const categories = resolvedTaxonomy ? loadTaxonomy(resolvedTaxonomy) : [];
  const taxonomyIds = new Set(categories.map((c) => c.id));

  // Load and parse matrix
  const content = fs.readFileSync(resolvedMatrix, "utf-8");
  const lines = content.split("\n").map((l) => l.trim()).filter((l) => l.length > 0);
  if (lines.length < 2) {
    console.error("Migration matrix has no data rows");
    process.exit(1);
  }

  const headers = parseCSVLine(lines[0]);
  const rows: Record<string, string>[] = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    const row: Record<string, string> = {};
    headers.forEach((h, idx) => { row[h] = values[idx] || ""; });
    rows.push(row);
  }

  // Filter and transform
  const documents: RegistryDocument[] = [];

  for (const row of rows) {
    const action = row.action || "";
    const registryCandidate = row.registryCandidate || "false";

    // Include: keep, rewrite, merge, archive
    if (["keep", "rewrite", "merge", "archive"].includes(action)) {
      // Include
    } else if (action === "review" && registryCandidate === "true") {
      // Include review rows with registryCandidate=true
    } else {
      // Skip: drop, review with registryCandidate=false
      continue;
    }

    const owner = row.owner || "TBD";
    const migrationStatus = determineMigrationStatus(action, owner, row.confidence || "");

    documents.push({
      id: row.id || "",
      title: row.title || "",
      category: row.category || "",
      owner: owner,
      fileType: row.fileType || "",
      updatedDate: "2026-06-18",
      status: action === "archive" ? "archived" : "current",
      storageUrl: "PENDING_ONEDRIVE",
      tags: generateTags(row.title || "", row.category || ""),
      legacySource: row.legacySource || "",
      migrationAction: action,
      migrationStatus: migrationStatus,
      notes: row.notes || "",
    });
  }

  // Build output
  const registry = {
    version: "1.0.0",
    updated: "2026-06-18",
    source: "Phase 5A.6 draft — generated from migration-matrix.v2.csv",
    migrationPhase: "5A.6",
    totalDocuments: documents.length,
    documents,
  };

  // Write output
  const outDir = path.dirname(resolvedOutput);
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  fs.writeFileSync(resolvedOutput, JSON.stringify(registry, null, 2), "utf-8");

  console.log(`\n✅ Registry draft created: ${resolvedOutput}`);
  console.log(`   Total documents: ${documents.length}`);

  // Stats
  const byStatus: Record<string, number> = {};
  for (const doc of documents) {
    byStatus[doc.migrationStatus] = (byStatus[doc.migrationStatus] || 0) + 1;
  }
  console.log("   Migration status breakdown:");
  for (const [status, count] of Object.entries(byStatus)) {
    console.log(`     ${status}: ${count}`);
  }
}

main();
