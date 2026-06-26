#!/usr/bin/env tsx
/**
 * generate-audit-registry.ts
 * Phase 5A.7 — Creates document-registry.audit.json from draft + audit findings
 * Adds: auditStatus, auditFindings, readinessLevel per document
 */

import * as fs from "fs";
import * as pathMod from "path";

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
  [key: string]: any;
}

interface Registry {
  version: string;
  updated: string;
  source: string;
  documents: RegistryDocument[];
}

function determineAuditStatus(doc: RegistryDocument): string {
  if (doc.owner === "TBD") return "blocked";
  if (doc.migrationAction === "review") return "needs-review";
  if (doc.storageUrl === "PENDING_ONEDRIVE") return "needs-review";
  return "ready-for-migration";
}

function determineReadinessLevel(doc: RegistryDocument): string {
  const issues: string[] = [];
  if (doc.owner === "TBD") issues.push("no-owner");
  if (doc.storageUrl === "PENDING_ONEDRIVE") issues.push("no-onedrive-url");
  if (doc.migrationAction === "review") issues.push("needs-human-review");
  if (doc.migrationAction === "rewrite") issues.push("content-rewrite-needed");
  if (doc.migrationAction === "merge") issues.push("merge-candidate");
  if (issues.length === 0) return "ready-for-migration";
  if (issues.includes("no-owner")) return "blocked";
  return "needs-review";
}

function getAuditFindings(doc: RegistryDocument): string[] {
  const findings: string[] = [];
  if (doc.owner === "TBD") findings.push("owner-unassigned");
  if (doc.storageUrl === "PENDING_ONEDRIVE") findings.push("no-onedrive-url");
  if (doc.migrationAction === "review") findings.push("requires-human-review");
  if (doc.migrationAction === "rewrite") findings.push("content-rewrite-required");
  if (doc.migrationAction === "merge") findings.push("merge-with-related-docs");
  if (doc.id.endsWith("A")) findings.push("non-standard-id-suffix");
  if (doc.notes && doc.notes.includes("external URL")) findings.push("external-link-risk");
  return findings;
}

function main() {
  const draftPath = process.argv[2];
  const outputPath = process.argv[3];

  if (!draftPath || !outputPath) {
    console.error("Usage: tsx generate-audit-registry.ts <draft.json> <audit.json>");
    process.exit(1);
  }

  const registry: Registry = JSON.parse(
    fs.readFileSync(pathMod.resolve(draftPath), "utf-8")
  );

  // Add audit fields to each document
  const auditDocuments = registry.documents.map((doc) => {
    const auditStatus = determineAuditStatus(doc);
    const auditFindings = getAuditFindings(doc);
    const readinessLevel = determineReadinessLevel(doc);

    return {
      ...doc,
      auditStatus,
      auditFindings,
      readinessLevel,
    };
  });

  // Count audit stats
  const auditStats = {
    blocked: auditDocuments.filter((d) => d.auditStatus === "blocked").length,
    "needs-review": auditDocuments.filter((d) => d.auditStatus === "needs-review").length,
    "ready-for-migration": auditDocuments.filter((d) => d.auditStatus === "ready-for-migration").length,
  };

  const auditRegistry = {
    version: "1.0.0",
    updated: "2026-06-18",
    source: "Phase 5A.7 audit — generated from document-registry.draft.json + audit findings",
    migrationPhase: "5A.7",
    auditPhase: true,
    totalDocuments: auditDocuments.length,
    auditStats,
    documents: auditDocuments,
  };

  fs.writeFileSync(
    pathMod.resolve(outputPath),
    JSON.stringify(auditRegistry, null, 2),
    "utf-8"
  );

  console.log(`✅ Audit registry created: ${outputPath}`);
  console.log(`   Total documents: ${auditDocuments.length}`);
  console.log(`   Audit status breakdown:`);
  console.log(`     blocked: ${auditStats.blocked}`);
  console.log(`     needs-review: ${auditStats["needs-review"]}`);
  console.log(`     ready-for-migration: ${auditStats["ready-for-migration"]}`);
}

main();
