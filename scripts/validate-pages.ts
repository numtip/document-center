/**
 * Validate built GitHub Pages output
 * Run: rtk npm run validate:pages
 */
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const DIST = resolve(process.cwd(), "dist");
const VERSION = readFileSync(resolve(process.cwd(), "VERSION"), "utf8").trim();

const routes = [
  "index.html",
  "404.html",
  "architecture/index.html",
  "standards/index.html",
  "adr/index.html",
  "roadmap/index.html",
  "release/index.html",
  "operations/index.html",
  "preview/index.html",
];

let errors = 0;

for (const r of routes) {
  const p = resolve(DIST, r);
  if (!existsSync(p)) {
    console.error(`FAIL: missing ${r}`);
    errors++;
  }
}

if (!existsSync(DIST)) {
  console.error("FAIL: dist/ not found — run npm run build first");
  process.exit(1);
}

const root = readFileSync(resolve(DIST, "index.html"), "utf8");
if (!root.includes("RAE Enterprise Canonical Repository")) {
  console.error("FAIL: root is not canonical landing");
  errors++;
}
if (!root.includes(VERSION)) {
  console.error(`FAIL: root missing version ${VERSION}`);
  errors++;
}
if (root.includes("document-grid")) {
  console.error("FAIL: root still contains demo grid");
  errors++;
}

const preview = JSON.parse(
  readFileSync(resolve(DIST, "preview/data/public-registry.sample.json"), "utf8"),
);
if (!preview.preview_mode || preview.documents.length !== 3) {
  console.error("FAIL: preview data invalid");
  errors++;
}

const previewHtml = readFileSync(resolve(DIST, "preview/index.html"), "utf8");
if (!previewHtml.includes("PREVIEW") && !previewHtml.includes("Preview")) {
  console.error("FAIL: preview missing banner");
  errors++;
}

if (errors) {
  console.error(`VALIDATE_PAGES: ${errors} error(s)`);
  process.exit(1);
}
console.log(`VALIDATE_PAGES: OK — v${VERSION} · ${routes.length} routes`);
