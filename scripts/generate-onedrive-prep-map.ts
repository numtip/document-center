#!/usr/bin/env tsx
/**
 * generate-onedrive-prep-map.ts
 * Phase 5A.6 — Creates onedrive-migration-prep.csv checklist
 *
 * Columns: documentId, title, category, proposedFolder, proposedFilename,
 *          owner, migrationAction, currentStatus, storageUrlStatus,
 *          humanActionRequired, notes
 */

import * as fs from "fs";
import * as pathMod from "path";

// ─── Types ────────────────────────────────────────────────────────────
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

interface Registry {
  version: string;
  updated: string;
  source: string;
  documents: RegistryDocument[];
}

interface TaxonomyCategory {
  id: string;
  name_th: string;
  name_en: string;
  folder: string;
}

// ─── CSV Helpers ──────────────────────────────────────────────────────
function escapeCSV(value: string): string {
  if (value.includes(",") || value.includes('"') || value.includes("\n")) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

// ─── Main ─────────────────────────────────────────────────────────────
function main() {
  const registryPath = process.argv[2];
  const taxonomyPath = process.argv[3];
  const outputPath = process.argv[4];

  if (!registryPath || !outputPath) {
    console.error(
      "Usage: tsx generate-onedrive-prep-map.ts <registry-json> [taxonomy-json] <output-csv>"
    );
    process.exit(1);
  }

  // Load registry
  const registry: Registry = JSON.parse(
    fs.readFileSync(pathMod.resolve(registryPath), "utf-8")
  );

  // Load taxonomy
  let categories: TaxonomyCategory[] = [];
  if (taxonomyPath && fs.existsSync(pathMod.resolve(taxonomyPath))) {
    const taxData = JSON.parse(
      fs.readFileSync(pathMod.resolve(taxonomyPath), "utf-8")
    );
    categories = taxData.categories || [];
  }
  const catMap = new Map(categories.map((c) => [c.id, c]));

  // Build CSV
  const headers = [
    "documentId",
    "title",
    "category",
    "proposedFolder",
    "proposedFilename",
    "owner",
    "migrationAction",
    "currentStatus",
    "storageUrlStatus",
    "humanActionRequired",
    "notes",
  ];

  const rows: string[] = [headers.join(",")];

  for (const doc of registry.documents) {
    const cat = catMap.get(doc.category);
    const proposedFolder = cat ? cat.folder : doc.category;
    const titleSlug = doc.title.replace(/\s+/g, "_").substring(0, 50);
    const proposedFilename = `${doc.id}_${titleSlug}_v1.0.${doc.fileType}`;

    // Determine human action required
    let humanAction: string[] = [];
    if (doc.owner === "TBD") humanAction.push("Assign owner");
    if (doc.storageUrl === "PENDING_ONEDRIVE") humanAction.push("Upload to OneDrive");
    if (doc.storageUrl === "PENDING_ONEDRIVE" && doc.status === "current") {
      humanAction.push("Create share link");
    }
    if (doc.migrationAction === "review") humanAction.push("Human review needed");
    if (doc.migrationAction === "rewrite") humanAction.push("Content rewrite needed");
    if (doc.migrationAction === "merge") humanAction.push("Merge with other docs");

    const row = [
      doc.id,
      doc.title,
      doc.category,
      proposedFolder,
      proposedFilename,
      doc.owner,
      doc.migrationAction,
      doc.status,
      doc.storageUrl === "PENDING_ONEDRIVE" ? "pending" : "needs-link",
      humanAction.join("; ") || "None",
      doc.notes,
    ];

    rows.push(row.map(escapeCSV).join(","));
  }

  const outDir = pathMod.dirname(pathMod.resolve(outputPath));
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  fs.writeFileSync(pathMod.resolve(outputPath), rows.join("\n"), "utf-8");

  console.log(`\n✅ OneDrive migration prep map created: ${outputPath}`);
  console.log(`   Total rows: ${registry.documents.length}`);
}

main();
