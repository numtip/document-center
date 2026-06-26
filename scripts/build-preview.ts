/**
 * Build static GitHub Pages preview into dist/
 * Run: rtk npm run build
 */
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const ROOT = process.cwd();
const PREVIEW = resolve(ROOT, "preview");
const DIST = resolve(ROOT, "dist");
const REGISTRY = resolve(PREVIEW, "data/public-registry.sample.json");

function assertPublicSampleOnly(): void {
  const data = JSON.parse(readFileSync(REGISTRY, "utf8")) as {
    preview_mode?: boolean;
    documents: Array<{
      visibility?: string;
      status?: string;
      storage_url?: string;
    }>;
  };

  if (!data.preview_mode) {
    throw new Error("public-registry.sample.json must set preview_mode=true");
  }

  for (const doc of data.documents) {
    if (doc.visibility !== "public") {
      throw new Error(`Blocked non-public record in preview: ${doc.visibility}`);
    }
    if (doc.status !== "current") {
      throw new Error(`Blocked non-current record in preview: ${doc.status}`);
    }
    if (
      doc.storage_url &&
      !doc.storage_url.includes("example.sharepoint.com") &&
      !doc.storage_url.startsWith("#")
    ) {
      throw new Error(`Blocked non-demo storage_url in preview build`);
    }
  }

  console.log(`PREVIEW_VALIDATE: OK — ${data.documents.length} public sample records`);
}

function main(): void {
  assertPublicSampleOnly();

  rmSync(DIST, { recursive: true, force: true });
  mkdirSync(DIST, { recursive: true });

  cpSync(PREVIEW, DIST, { recursive: true });
  writeFileSync(resolve(DIST, ".nojekyll"), "\n", "utf8");

  console.log("PREVIEW_BUILD: OK — output in dist/");
}

main();
