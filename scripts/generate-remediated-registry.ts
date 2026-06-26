#!/usr/bin/env tsx
/**
 * generate-remediated-registry.ts
 * Phase 5A.8 — Creates document-registry.remediated.json from draft + remediation data
 *
 * Adds:
 * - remediationStatus: unresolved | owner-proposed | needs-human-decision | ready-for-onedrive-prep
 * - ownerProposal: { proposedOwner, confidence, reason }
 * - reviewResolution: { recommendedAction, confidence, reason } (for review docs)
 * - mergeRecommendation: { mergeGroupId, canonicalId, isCanonical } (for merge docs)
 *
 * Readiness logic:
 * - ready-for-onedrive-prep only if:
 *   - owner proposal high confidence
 *   - not review unresolved
 *   - not merge unresolved
 *   - category valid
 *   - storageUrl is PENDING_ONEDRIVE
 */

import * as fs from "fs";
import * as pathMod from "path";

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

function parseCSV(content: string): Record<string, string>[] {
  const lines = content.split("\n").map((l) => l.trim()).filter((l) => l.length > 0);
  if (lines.length < 2) return [];
  const headers = parseCSVLine(lines[0]);
  const rows: Record<string, string>[] = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    const row: Record<string, string> = {};
    headers.forEach((h, idx) => { row[h] = values[idx] || ""; });
    rows.push(row);
  }
  return rows;
}

// ─── Main ─────────────────────────────────────────────────────────────
function main() {
  const draftPath = process.argv[2];
  const ownerProposalPath = process.argv[3];
  const reviewResolutionPath = process.argv[4];
  const mergeDecisionPath = process.argv[5];
  const taxonomyPath = process.argv[6];
  const outputPath = process.argv[7];

  if (!draftPath || !outputPath) {
    console.error(
      "Usage: tsx generate-remediated-registry.ts <draft.json> <owner-proposal.csv> <review-resolution.csv> <merge-decision.csv> <taxonomy.json> <output.json>"
    );
    process.exit(1);
  }

  // Load draft registry
  const registry = JSON.parse(fs.readFileSync(pathMod.resolve(draftPath), "utf-8"));

  // Load remediation data
  const ownerProposals = parseCSV(
    fs.readFileSync(pathMod.resolve(ownerProposalPath), "utf-8")
  );
  const reviewResolutions = reviewResolutionPath && fs.existsSync(pathMod.resolve(reviewResolutionPath))
    ? parseCSV(fs.readFileSync(pathMod.resolve(reviewResolutionPath), "utf-8"))
    : [];
  const mergeDecisions = mergeDecisionPath && fs.existsSync(pathMod.resolve(mergeDecisionPath))
    ? parseCSV(fs.readFileSync(pathMod.resolve(mergeDecisionPath), "utf-8"))
    : [];

  // Load taxonomy
  const taxonomy = taxonomyPath && fs.existsSync(pathMod.resolve(taxonomyPath))
    ? JSON.parse(fs.readFileSync(pathMod.resolve(taxonomyPath), "utf-8"))
    : { categories: [] };
  const validCategories = new Set((taxonomy.categories || []).map((c: any) => c.id));

  // Build lookup maps
  const ownerMap = new Map<string, Record<string, string>>();
  for (const row of ownerProposals) {
    ownerMap.set(row.documentId, row);
  }

  const reviewMap = new Map<string, Record<string, string>>();
  for (const row of reviewResolutions) {
    reviewMap.set(row.documentId, row);
  }

  const mergeMap = new Map<string, Record<string, string>>();
  for (const row of mergeDecisions) {
    mergeMap.set(row.sourceDocumentId, row);
  }

  // Process each document
  const remediatedDocs = registry.documents.map((doc: any) => {
    const ownerProposal = ownerMap.get(doc.id);
    const reviewResolution = reviewMap.get(doc.id);
    const mergeRec = mergeMap.get(doc.id);

    // Determine remediation status
    let remediationStatus: string;
    const isReview = doc.migrationAction === "review";
    const isMerge = doc.migrationAction === "merge";
    const isRewrite = doc.migrationAction === "rewrite";
    const hasHighConfidenceOwner = ownerProposal && ownerProposal.confidence === "high";
    const categoryValid = validCategories.has(doc.category);
    const storagePending = doc.storageUrl === "PENDING_ONEDRIVE";

    if (isReview || isMerge || isRewrite) {
      // Review/merge/rewrite docs need human decision
      remediationStatus = "needs-human-decision";
    } else if (hasHighConfidenceOwner && categoryValid && storagePending) {
      // High-confidence owner + valid category + pending storage = ready for OneDrive prep
      remediationStatus = "ready-for-onedrive-prep";
    } else if (ownerProposal && ownerProposal.confidence !== "low") {
      // Medium confidence owner proposed
      remediationStatus = "owner-proposed";
    } else {
      // Low confidence or no proposal
      remediationStatus = "unresolved";
    }

    // Build remediated document
    const remediated: any = { ...doc };

    // Add remediationStatus
    remediated.remediationStatus = remediationStatus;

    // Add ownerProposal
    if (ownerProposal) {
      remediated.ownerProposal = {
        proposedOwner: ownerProposal.proposedOwner,
        confidence: ownerProposal.confidence,
        reason: ownerProposal.reason,
      };
    }

    // Add reviewResolution for review docs
    if (reviewResolution) {
      remediated.reviewResolution = {
        recommendedAction: reviewResolution.recommendedAction,
        confidence: reviewResolution.confidence,
        reason: reviewResolution.reason,
        humanDecisionRequired: reviewResolution.humanDecisionRequired === "true",
      };
    }

    // Add mergeRecommendation for merge docs
    if (mergeRec) {
      remediated.mergeRecommendation = {
        mergeGroupId: mergeRec.mergeGroupId,
        canonicalId: mergeRec.recommendedCanonicalId,
        isCanonical: mergeRec.sourceDocumentId === mergeRec.recommendedCanonicalId,
        canonicalTitle: mergeRec.canonicalTitle,
        mergeReason: mergeRec.mergeReason,
        humanDecisionRequired: mergeRec.humanDecisionRequired === "true",
      };
    }

    return remediated;
  });

  // Count remediation stats
  const remediationStats = {
    unresolved: remediatedDocs.filter((d: any) => d.remediationStatus === "unresolved").length,
    "owner-proposed": remediatedDocs.filter((d: any) => d.remediationStatus === "owner-proposed").length,
    "needs-human-decision": remediatedDocs.filter((d: any) => d.remediationStatus === "needs-human-decision").length,
    "ready-for-onedrive-prep": remediatedDocs.filter((d: any) => d.remediationStatus === "ready-for-onedrive-prep").length,
  };

  const remediatedRegistry = {
    version: "1.0.0",
    updated: "2026-06-18",
    source: "Phase 5A.8 remediated — generated from draft + owner proposals + review resolutions + merge decisions",
    migrationPhase: "5A.8",
    remediationPhase: true,
    totalDocuments: remediatedDocs.length,
    remediationStats,
    documents: remediatedDocs,
  };

  fs.writeFileSync(
    pathMod.resolve(outputPath),
    JSON.stringify(remediatedRegistry, null, 2),
    "utf-8"
  );

  console.log(`✅ Remediated registry created: ${outputPath}`);
  console.log(`   Total documents: ${remediatedDocs.length}`);
  console.log(`   Remediation status breakdown:`);
  console.log(`     unresolved: ${remediationStats.unresolved}`);
  console.log(`     owner-proposed: ${remediationStats["owner-proposed"]}`);
  console.log(`     needs-human-decision: ${remediationStats["needs-human-decision"]}`);
  console.log(`     ready-for-onedrive-prep: ${remediationStats["ready-for-onedrive-prep"]}`);
}

main();
