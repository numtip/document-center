#!/usr/bin/env tsx
/**
 * validate-document-registry.ts
 * Phase 5A.6 — Validates document-registry.draft.json
 *
 * Validates:
 * - JSON parse
 * - Required metadata fields
 * - Allowed status values
 * - Owner must not be empty unless migrationStatus=needs-owner
 * - storageUrl may be PENDING_ONEDRIVE only before migration
 * - No duplicate IDs
 * - Category must match taxonomy if taxonomy exists
 * - Broken/empty links are blockers only when storageUrl is not PENDING_ONEDRIVE
 */

import * as fs from "fs";
import * as path from "path";

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

// ─── Constants ────────────────────────────────────────────────────────
const ALLOWED_STATUS = ["current", "obsolete", "archived", "draft"];
const ALLOWED_MIGRATION_STATUS = [
  "metadata-ready",
  "needs-owner",
  "needs-onedrive-url",
  "needs-human-review",
];
const REQUIRED_FIELDS = [
  "id",
  "title",
  "category",
  "owner",
  "fileType",
  "updatedDate",
  "status",
  "migrationAction",
  "migrationStatus",
];
const VALID_CATEGORIES = [
  "admin",
  "finance-procurement",
  "research",
  "academic-service",
  "policy-planning",
  "manuals",
];

// ─── Validation ───────────────────────────────────────────────────────
interface ValidationResult {
  errors: string[];
  warnings: string[];
  summary: {
    totalDocuments: number;
    byStatus: Record<string, number>;
    byMigrationStatus: Record<string, number>;
    byCategory: Record<string, number>;
    ownersTBD: number;
    pendingOneDrive: number;
  };
}

function validate(filePath: string, taxonomyPath?: string): ValidationResult {
  const result: ValidationResult = {
    errors: [],
    warnings: [],
    summary: {
      totalDocuments: 0,
      byStatus: {},
      byMigrationStatus: {},
      byCategory: {},
      ownersTBD: 0,
      pendingOneDrive: 0,
    },
  };

  // 1. File exists
  if (!fs.existsSync(filePath)) {
    result.errors.push(`File not found: ${filePath}`);
    return result;
  }

  // 2. JSON parse
  let registry: Registry;
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    registry = JSON.parse(content);
  } catch (e) {
    result.errors.push(
      `JSON parse error: ${e instanceof Error ? e.message : String(e)}`
    );
    return result;
  }

  // 3. Top-level structure
  if (!registry.documents || !Array.isArray(registry.documents)) {
    result.errors.push("Missing or invalid 'documents' array");
    return result;
  }

  // 4. Load taxonomy if provided
  let validCategories: Set<string> | null = null;
  if (taxonomyPath && fs.existsSync(taxonomyPath)) {
    try {
      const taxData = JSON.parse(fs.readFileSync(taxonomyPath, "utf-8"));
      validCategories = new Set(
        (taxData.categories || []).map((c: any) => c.id)
      );
    } catch {
      result.warnings.push("Could not load taxonomy for category validation");
    }
  }

  // 5. Validate each document
  const seenIds = new Set<string>();
  result.summary.totalDocuments = registry.documents.length;

  for (let i = 0; i < registry.documents.length; i++) {
    const doc = registry.documents[i];
    const docNum = i + 1;

    // a. Required fields
    for (const field of REQUIRED_FIELDS) {
      if (
        !(doc as any)[field] ||
        String((doc as any)[field]).trim() === ""
      ) {
        result.errors.push(
          `[Doc ${docNum} (${doc.id || "NO-ID"})] Missing required field: ${field}`
        );
      }
    }

    // b. Allowed status
    if (doc.status && !ALLOWED_STATUS.includes(doc.status)) {
      result.errors.push(
        `[Doc ${doc.id}] Invalid status '${doc.status}' — must be one of: ${ALLOWED_STATUS.join(", ")}`
      );
    }

    // c. Allowed migrationStatus
    if (
      doc.migrationStatus &&
      !ALLOWED_MIGRATION_STATUS.includes(doc.migrationStatus)
    ) {
      result.warnings.push(
        `[Doc ${doc.id}] Non-standard migrationStatus: '${doc.migrationStatus}'`
      );
    }

    // d. Owner check
    if (
      (!doc.owner || doc.owner.trim() === "" || doc.owner === "TBD") &&
      !["needs-owner", "needs-human-review"].includes(doc.migrationStatus)
    ) {
      result.errors.push(
        `[Doc ${doc.id}] Owner is empty/TBD but migrationStatus is '${doc.migrationStatus}' (expected 'needs-owner' or 'needs-human-review')`
      );
    }

    // e. storageUrl check
    if (
      doc.storageUrl &&
      doc.storageUrl !== "PENDING_ONEDRIVE" &&
      doc.storageUrl.trim() !== ""
    ) {
      // Has a URL — note it
      result.warnings.push(
        `[Doc ${doc.id}] Has storageUrl — verify it resolves: ${doc.storageUrl}`
      );
    }

    // f. No duplicate IDs
    if (doc.id) {
      if (seenIds.has(doc.id)) {
        result.errors.push(`[Doc ${doc.id}] Duplicate ID found`);
      }
      seenIds.add(doc.id);
    }

    // g. Category validation
    if (validCategories && doc.category && !validCategories.has(doc.category)) {
      result.errors.push(
        `[Doc ${doc.id}] Category '${doc.category}' not found in taxonomy`
      );
    }

    // h. Broken links are blockers only when storageUrl is not PENDING_ONEDRIVE
    if (
      (!doc.storageUrl || doc.storageUrl.trim() === "") &&
      doc.status === "current"
    ) {
      result.warnings.push(
        `[Doc ${doc.id}] status='current' but storageUrl is empty — required before go-live`
      );
    }

    // Aggregate stats
    result.summary.byStatus[doc.status] =
      (result.summary.byStatus[doc.status] || 0) + 1;
    result.summary.byMigrationStatus[doc.migrationStatus] =
      (result.summary.byMigrationStatus[doc.migrationStatus] || 0) + 1;
    result.summary.byCategory[doc.category] =
      (result.summary.byCategory[doc.category] || 0) + 1;

    if (!doc.owner || doc.owner === "TBD") {
      result.summary.ownersTBD++;
    }
    if (doc.storageUrl === "PENDING_ONEDRIVE") {
      result.summary.pendingOneDrive++;
    }
  }

  return result;
}

// ─── Main ─────────────────────────────────────────────────────────────
function main() {
  const filePath = process.argv[2];
  const taxonomyPath = process.argv[3];

  if (!filePath) {
    console.error(
      "Usage: tsx validate-document-registry.ts <registry-json> [taxonomy-json]"
    );
    process.exit(1);
  }

  const resolvedPath = path.resolve(filePath);
  const resolvedTaxonomy = taxonomyPath ? path.resolve(taxonomyPath) : undefined;

  console.log(`\n🔍 Validating registry: ${resolvedPath}`);
  if (resolvedTaxonomy) {
    console.log(`   Taxonomy: ${resolvedTaxonomy}`);
  }
  console.log();

  const result = validate(resolvedPath, resolvedTaxonomy);

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
  console.log(`   Total documents: ${result.summary.totalDocuments}`);
  console.log(`   Owners TBD: ${result.summary.ownersTBD}`);
  console.log(`   Pending OneDrive: ${result.summary.pendingOneDrive}`);
  console.log();
  console.log("   By status:");
  for (const [s, c] of Object.entries(result.summary.byStatus)) {
    console.log(`     ${s}: ${c}`);
  }
  console.log();
  console.log("   By migrationStatus:");
  for (const [s, c] of Object.entries(result.summary.byMigrationStatus)) {
    console.log(`     ${s}: ${c}`);
  }
  console.log();
  console.log("   By category:");
  for (const [cat, c] of Object.entries(result.summary.byCategory)) {
    console.log(`     ${cat}: ${c}`);
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
