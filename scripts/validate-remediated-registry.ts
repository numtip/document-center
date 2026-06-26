#!/usr/bin/env tsx
/**
 * validate-remediated-registry.ts
 * Phase 5A.8 — Validates document-registry.remediated.json
 *
 * Validates:
 * - JSON parse
 * - Required fields
 * - remediationStatus allowed values
 * - ownerProposal exists
 * - review docs have reviewResolution
 * - merge docs have mergeRecommendation
 * - no storageUrl other than PENDING_ONEDRIVE or empty
 * - no final owner invented from low-confidence proposal
 * - no duplicate IDs
 */

import * as fs from "fs";
import * as pathMod from "path";

// ─── Constants ────────────────────────────────────────────────────────
const ALLOWED_REMEDIATION_STATUS = [
  "unresolved",
  "owner-proposed",
  "needs-human-decision",
  "ready-for-onedrive-prep",
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
  "remediationStatus",
];

// ─── Validation ───────────────────────────────────────────────────────
interface ValidationResult {
  errors: string[];
  warnings: string[];
  summary: {
    totalDocuments: number;
    byRemediationStatus: Record<string, number>;
    ownerProposals: number;
    reviewResolutions: number;
    mergeRecommendations: number;
    storageUrlViolations: number;
    lowConfidenceOwnerFabricated: number;
  };
}

function validate(filePath: string, taxonomyPath?: string): ValidationResult {
  const result: ValidationResult = {
    errors: [],
    warnings: [],
    summary: {
      totalDocuments: 0,
      byRemediationStatus: {},
      ownerProposals: 0,
      reviewResolutions: 0,
      mergeRecommendations: 0,
      storageUrlViolations: 0,
      lowConfidenceOwnerFabricated: 0,
    },
  };

  // 1. File exists
  if (!fs.existsSync(filePath)) {
    result.errors.push(`File not found: ${filePath}`);
    return result;
  }

  // 2. JSON parse
  let registry: any;
  try {
    registry = JSON.parse(fs.readFileSync(filePath, "utf-8"));
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

  // 4. Load taxonomy
  let validCategories: Set<string> | null = null;
  if (taxonomyPath && fs.existsSync(pathMod.resolve(taxonomyPath))) {
    try {
      const taxData = JSON.parse(fs.readFileSync(pathMod.resolve(taxonomyPath), "utf-8"));
      validCategories = new Set((taxData.categories || []).map((c: any) => c.id));
    } catch {
      result.warnings.push("Could not load taxonomy");
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
      if (!doc[field] || String(doc[field]).trim() === "") {
        result.errors.push(
          `[Doc ${docNum} (${doc.id || "NO-ID"})] Missing required field: ${field}`
        );
      }
    }

    // b. remediationStatus allowed values
    if (
      doc.remediationStatus &&
      !ALLOWED_REMEDIATION_STATUS.includes(doc.remediationStatus)
    ) {
      result.errors.push(
        `[Doc ${doc.id}] Invalid remediationStatus: '${doc.remediationStatus}'`
      );
    }

    // c. ownerProposal exists
    if (!doc.ownerProposal) {
      result.errors.push(`[Doc ${doc.id}] Missing ownerProposal object`);
    } else {
      result.summary.ownerProposals++;
      // Check no low-confidence owner fabricated into final owner field
      if (
        doc.ownerProposal.confidence === "low" &&
        doc.owner &&
        doc.owner !== "TBD" &&
        doc.owner.trim() !== ""
      ) {
        result.errors.push(
          `[Doc ${doc.id}] Final owner '${doc.owner}' set from low-confidence proposal — fabrication not allowed`
        );
        result.summary.lowConfidenceOwnerFabricated++;
      }
    }

    // d. review docs have reviewResolution
    if (doc.migrationAction === "review" && !doc.reviewResolution) {
      result.errors.push(
        `[Doc ${doc.id}] Review document missing reviewResolution object`
      );
    }
    if (doc.reviewResolution) {
      result.summary.reviewResolutions++;
    }

    // e. merge docs have mergeRecommendation
    if (doc.migrationAction === "merge" && !doc.mergeRecommendation) {
      result.errors.push(
        `[Doc ${doc.id}] Merge document missing mergeRecommendation object`
      );
    }
    if (doc.mergeRecommendation) {
      result.summary.mergeRecommendations++;
    }

    // f. no storageUrl other than PENDING_ONEDRIVE or empty
    if (
      doc.storageUrl &&
      doc.storageUrl !== "PENDING_ONEDRIVE" &&
      doc.storageUrl.trim() !== ""
    ) {
      result.errors.push(
        `[Doc ${doc.id}] storageUrl must be PENDING_ONEDRIVE or empty, got: '${doc.storageUrl}'`
      );
      result.summary.storageUrlViolations++;
    }

    // g. no duplicate IDs
    if (doc.id) {
      if (seenIds.has(doc.id)) {
        result.errors.push(`[Doc ${doc.id}] Duplicate ID found`);
      }
      seenIds.add(doc.id);
    }

    // h. category validation
    if (validCategories && doc.category && !validCategories.has(doc.category)) {
      result.errors.push(
        `[Doc ${doc.id}] Category '${doc.category}' not found in taxonomy`
      );
    }

    // Aggregate stats
    result.summary.byRemediationStatus[doc.remediationStatus] =
      (result.summary.byRemediationStatus[doc.remediationStatus] || 0) + 1;
  }

  return result;
}

// ─── Main ─────────────────────────────────────────────────────────────
function main() {
  const filePath = process.argv[2];
  const taxonomyPath = process.argv[3];

  if (!filePath) {
    console.error(
      "Usage: tsx validate-remediated-registry.ts <registry-json> [taxonomy-json]"
    );
    process.exit(1);
  }

  const resolvedPath = pathMod.resolve(filePath);
  const resolvedTaxonomy = taxonomyPath ? pathMod.resolve(taxonomyPath) : undefined;

  console.log(`\n🔍 Validating remediated registry: ${resolvedPath}`);
  if (resolvedTaxonomy) {
    console.log(`   Taxonomy: ${resolvedTaxonomy}`);
  }
  console.log();

  const result = validate(resolvedPath, resolvedTaxonomy);

  if (result.errors.length > 0) {
    console.log("❌ ERRORS:");
    result.errors.forEach((e) => console.log(`   • ${e}`));
    console.log();
  }

  if (result.warnings.length > 0) {
    console.log("⚠️  WARNINGS:");
    result.warnings.forEach((w) => console.log(`   • ${w}`));
    console.log();
  }

  console.log("📊 SUMMARY:");
  console.log(`   Total documents: ${result.summary.totalDocuments}`);
  console.log(`   Owner proposals: ${result.summary.ownerProposals}`);
  console.log(`   Review resolutions: ${result.summary.reviewResolutions}`);
  console.log(`   Merge recommendations: ${result.summary.mergeRecommendations}`);
  console.log(`   storageUrl violations: ${result.summary.storageUrlViolations}`);
  console.log(`   Low-confidence owners fabricated: ${result.summary.lowConfidenceOwnerFabricated}`);
  console.log();
  console.log("   By remediationStatus:");
  for (const [s, c] of Object.entries(result.summary.byRemediationStatus)) {
    console.log(`     ${s}: ${c}`);
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
