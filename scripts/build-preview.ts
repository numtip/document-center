/**
 * Build GitHub Pages: canonical portal + preview demo
 * Run: rtk npm run build
 */
import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, relative, resolve } from "node:path";

const ROOT = process.cwd();
const SITE = resolve(ROOT, "site");
const PREVIEW = resolve(ROOT, "preview");
const DIST = resolve(ROOT, "dist");
const VERSION = readFileSync(resolve(ROOT, "VERSION"), "utf8").trim();
const GITHUB = "https://github.com/numtip/document-center/blob/main";
const LOGO = resolve(ROOT, "docs/logorae.png");
const PRODUCTION_URL =
  "https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx";

function assertPublicSampleOnly(): void {
  const registry = resolve(PREVIEW, "data/public-registry.sample.json");
  const data = JSON.parse(readFileSync(registry, "utf8")) as {
    preview_mode?: boolean;
    documents: Array<{ visibility?: string; status?: string; storage_url?: string }>;
  };
  if (!data.preview_mode) throw new Error("preview_mode must be true");
  for (const doc of data.documents) {
    if (doc.visibility !== "public") throw new Error(`Blocked non-public: ${doc.visibility}`);
    if (doc.status !== "current") throw new Error(`Blocked non-current: ${doc.status}`);
    if (
      doc.storage_url &&
      !doc.storage_url.includes("example.sharepoint.com") &&
      !doc.storage_url.startsWith("#")
    ) {
      throw new Error("Blocked non-demo storage_url");
    }
  }
  console.log(`PREVIEW_VALIDATE: OK — ${data.documents.length} sample records`);
}

function shell(prefix: string, active: string, body: string, title: string): string {
  const p = prefix;
  return `<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="RAE Enterprise Canonical Repository — Maejo University" />
  <title>${title}</title>
  <link rel="icon" href="${p}assets/logorae.png" type="image/png" />
  <link rel="stylesheet" href="${p}assets/canonical.css" />
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="${p}">
        <img class="brand-logo" src="${p}assets/logorae.png" width="48" height="48" alt="ตราสำนักวิจัยและส่งเสริมวิชาการการเกษตร มหาวิทยาลัยแม่โจ้" />
        <span class="brand-text"><strong>RAE Canonical Repository</strong><span>Maejo University · v${VERSION}</span></span>
      </a>
      <button class="nav-toggle" type="button" aria-label="เปิดเมนู">☰</button>
      <nav class="main-nav" aria-label="Main">
        <ul>
          <li><a href="${p}" data-nav="home">หน้าแรก</a></li>
          <li><a href="${p}architecture/" data-nav="architecture">สถาปัตยกรรม</a></li>
          <li><a href="${p}standards/" data-nav="standards">มาตรฐาน</a></li>
          <li><a href="${p}adr/" data-nav="adr">ADR</a></li>
          <li><a href="${p}roadmap/" data-nav="roadmap">Roadmap</a></li>
          <li><a href="${p}release/" data-nav="release">Release</a></li>
          <li><a href="${p}operations/" data-nav="operations">Operations</a></li>
          <li><a href="${p}preview/" data-nav="preview">UI Preview</a></li>
        </ul>
      </nav>
    </div>
  </header>
  ${body}
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <h4>RAE Enterprise Canonical Repository</h4>
        <p>คลังสถาปัยกรรมมาตรฐานองค์กร · v${VERSION} · READ-MOSTLY</p>
      </div>
      <div>
        <h4>ลิงก์</h4>
        <ul>
          <li><a href="${PRODUCTION_URL}">Production Document Center</a></li>
          <li><a href="${p}preview/">UI Preview (Demo)</a></li>
          <li><a href="https://github.com/numtip/document-center">GitHub Repository</a></li>
        </ul>
      </div>
      <div>
        <h4>หมายเหตุ</h4>
        <p>GitHub Pages เป็น canonical reference portal — ไม่ใช่ production document portal</p>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>© Maejo University · Office of Agricultural Research and Extension · Canonical release v${VERSION}</p>
    </div>
  </footer>
  <script src="${p}assets/canonical.js"></script>
</body>
</html>`;
}

function gh(path: string): string {
  return `${GITHUB}/${path}`;
}

function writePage(relPath: string, html: string): void {
  const out = resolve(DIST, relPath);
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, html, "utf8");
}

function buildPages(): void {
  const home = shell(
    "./",
    "home",
    `
  <section class="hero">
    <div class="container reveal">
      <img class="hero-logo" src="./assets/logorae.png" width="88" height="88" alt="" aria-hidden="true" />
      <p class="hero-eyebrow">มหาวิทยาลัยแม่โจ้ · สำนักวิจัยและส่งเสริมวิชาการการเกษตร</p>
      <h1>RAE Enterprise Canonical Repository</h1>
      <p class="hero-sub">คลังสถาปัตยกรรมมาตรฐานองค์กร สำนักวิจัยและส่งเสริมวิชาการการเกษตร</p>
      <p class="hero-en">Mandatory architectural reference for all RAE digital platforms · Canonical v${VERSION}</p>
      <div class="hero-badges">
        <span class="badge badge-gold">PRODUCTION BASELINE FROZEN</span>
        <span class="badge badge-outline">CANONICAL REPOSITORY</span>
        <span class="badge badge-outline">READ-MOSTLY</span>
        <span class="badge badge-outline">ENTERPRISE-READY</span>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="${PRODUCTION_URL}" target="_blank" rel="noopener noreferrer">เปิด Production Document Center</a>
        <a class="btn btn-secondary" href="./architecture/">สำรวจสถาปัตยกรรม</a>
        <a class="btn btn-secondary" href="./standards/">มาตรฐาน Canonical</a>
        <a class="btn btn-secondary" href="./adr/">Browse ADRs</a>
        <a class="btn btn-secondary" href="./preview/">UI Preview</a>
        <a class="btn btn-secondary" href="https://github.com/numtip/document-center" target="_blank" rel="noopener noreferrer">GitHub Repository</a>
      </div>
      <p class="note-inline">⚠️ การเข้า Production Document Center อาจต้องใช้ Microsoft 365 organizational sign-in · GitHub Pages ไม่ใช่ production document portal</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="stats-grid">
        <div class="stat-card"><strong>627</strong><span>Production files</span></div>
        <div class="stat-card"><strong>627</strong><span>Registry records</span></div>
        <div class="stat-card"><strong>0</strong><span>Duplicate DocumentIDs</span></div>
        <div class="stat-card"><strong>0</strong><span>Broken Storage URLs</span></div>
        <div class="stat-card"><strong>9</strong><span>Accepted ADRs</span></div>
        <div class="stat-card"><strong>${VERSION}</strong><span>Canonical release</span></div>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="container">
      <h2>บทบาทของระบบ</h2>
      <p class="section-lead">แยกบทบาท Production, Canonical Reference และ UI Demonstration อย่างชัดเจน</p>
      <div class="role-grid">
        <article class="role-card">
          <h3>🏛️ Production System</h3>
          <p>SharePoint Document Center — 627 เอกสารจริง ต้อง authenticate ผ่าน Maejo365</p>
        </article>
        <article class="role-card">
          <h3>📚 Canonical Reference</h3>
          <p>GitHub repository + GitHub Pages — สถาปัตยกรรม มาตรฐาน ADR และ governance</p>
        </article>
        <article class="role-card">
          <h3>🎨 UI Demonstration</h3>
          <p><a href="./preview/">/preview/</a> — 3 mock records · preview_mode: true · ไม่ใช่ข้อมูล production</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>สถาปัตยกรรม</h2>
      <p class="section-lead">Architecture flow — เอกสารจริงอยู่ใน SharePoint · Registry เป็น discovery layer</p>
      <div class="flow-diagram">
        <div class="flow-row">
          <span class="flow-node">Legacy WTMS</span><span class="flow-arrow">→</span>
          <span class="flow-node">Migration</span><span class="flow-arrow">→</span>
          <span class="flow-node highlight">Microsoft 365</span><span class="flow-arrow">→</span>
          <span class="flow-node highlight">SharePoint Libraries</span>
        </div>
        <div class="flow-row">
          <span class="flow-node highlight">RAE Document Registry</span><span class="flow-arrow">→</span>
          <span class="flow-node">Experience Layers</span><span class="flow-arrow">→</span>
          <span class="flow-node">Future AI Services</span>
        </div>
        <div class="sor-grid">
          <div class="sor-item"><strong>Documents</strong> → SharePoint</div>
          <div class="sor-item"><strong>Metadata</strong> → RAE Document Registry</div>
          <div class="sor-item"><strong>Governance</strong> → Microsoft 365</div>
          <div class="sor-item"><strong>Source code</strong> → GitHub</div>
          <div class="sor-item"><strong>Public experience</strong> → Next.js (future)</div>
          <div class="sor-item"><strong>AI services</strong> → Governed sources only</div>
        </div>
      </div>
      <p style="margin-top:1rem"><a href="./architecture/">ดูรายละเอียดสถาปัตยกรรม →</a></p>
    </div>
  </section>

  <section class="section section-alt">
    <div class="container">
      <h2>หลักการสถาปัตยกรรม</h2>
      <p class="section-lead">Architecture Principles — จากเอกสาร governance ที่ได้รับการยอมรับ</p>
      <div class="principles-grid">
        <div class="principle"><strong>Build Less. Govern More.</strong><span>ใช้ foundation ที่มี governance แทนการสร้างระบบซ้ำ</span></div>
        <div class="principle"><strong>Metadata First</strong><span>Metadata ที่ upload time + Registry sync</span></div>
        <div class="principle"><strong>M365 is Source of Truth</strong><span>SharePoint เก็บไฟล์ · Git เก็บมาตรฐาน</span></div>
        <div class="principle"><strong>Website is Presentation Layer</strong><span>Portal แสดง metadata · ไม่เก็บ master files</span></div>
        <div class="principle"><strong>Static-first Public Experience</strong><span>Export JSON สำหรับ public portal</span></div>
        <div class="principle"><strong>AI consumes governed data only</strong><span>DocumentID เป็น join key</span></div>
        <div class="principle"><strong>Architecture before implementation</strong><span>Bootstrap template ก่อนเริ่มโปรเจกต์</span></div>
        <div class="principle"><strong>No duplicate sources of truth</strong><span>System of Records ชัดเจน</span></div>
      </div>
      <p style="margin-top:1rem"><a href="./standards/">ดูมาตรฐานทั้งหมด →</a></p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>เอกสารอ้างอิง</h2>
      <p class="section-lead">Documentation index — ลิงก์ไปยัง source บน GitHub</p>
      <div class="doc-grid">
        <div class="doc-group">
          <h3>Canonical</h3>
          <ul>
            <li><a href="${gh("docs/canonical/CANONICAL_REPOSITORY_CHARTER.md")}">Canonical Repository Charter</a></li>
            <li><a href="${gh("docs/canonical/REFERENCE_STANDARDS.md")}">Reference Standards</a></li>
            <li><a href="${gh("docs/canonical/REPOSITORY_GOVERNANCE.md")}">Repository Governance</a></li>
            <li><a href="${gh("docs/canonical/CHANGE_CONTROL_POLICY.md")}">Change Control Policy</a></li>
            <li><a href="${gh("docs/canonical/PROJECT_MEMORY_FREEZE_v1.md")}">Project Memory Freeze</a></li>
          </ul>
        </div>
        <div class="doc-group">
          <h3>Governance</h3>
          <ul>
            <li><a href="${gh("docs/governance/RAE_ENTERPRISE_PLATFORM_ROADMAP.md")}">Enterprise Platform Roadmap</a></li>
            <li><a href="${gh("docs/governance/CONSUMER_IMPLEMENTATION_GUIDE.md")}">Consumer Implementation Guide</a></li>
            <li><a href="${gh("docs/governance/ARCHITECTURE_PRINCIPLES.md")}">Architecture Principles</a></li>
            <li><a href="${gh("docs/governance/SYSTEM_OF_RECORDS.md")}">System of Records</a></li>
            <li><a href="${gh("docs/governance/CANONICAL_REPOSITORY_CERTIFICATE.md")}">Canonical Certificate</a></li>
          </ul>
        </div>
        <div class="doc-group">
          <h3>Release v1.0</h3>
          <ul>
            <li><a href="${gh("docs/release/DOCUMENT_CENTER_v1.0_PRODUCTION_FREEZE.md")}">Production Freeze</a></li>
            <li><a href="${gh("docs/release/ARCHITECTURE_BASELINE_v1.0.md")}">Architecture Baseline</a></li>
            <li><a href="${gh("docs/release/PRODUCTION_ACCEPTANCE_CERTIFICATE.md")}">Acceptance Certificate</a></li>
            <li><a href="${gh("docs/release/OPERATION_RUNBOOK_v1.0.md")}">Operation Runbook</a></li>
          </ul>
        </div>
      </div>
      <p style="margin-top:1rem"><a href="./roadmap/">Enterprise Roadmap →</a> · <a href="./release/">Release baseline →</a></p>
    </div>
  </section>`,
    "RAE Enterprise Canonical Repository",
  );

  const sub = "../";
  writePage("index.html", home);

  writePage(
    "architecture/index.html",
    shell(
      sub,
      "architecture",
      `
  <section class="page-hero"><div class="container"><h1>สถาปัตยกรรม</h1><p>Architecture Overview · Frozen baseline v1.0</p></div></section>
  <section class="section"><div class="container">
    <div class="content-card">
      <h2>Architecture Flow</h2>
      <div class="flow-diagram">
        <div class="flow-row">
          <span class="flow-node">WTMS (archived)</span><span class="flow-arrow">→</span>
          <span class="flow-node">SharePoint Libraries (627)</span><span class="flow-arrow">→</span>
          <span class="flow-node highlight">RAE Document Registry (627)</span>
        </div>
        <div class="flow-row">
          <span class="flow-node">SharePoint DC Page</span><span class="flow-arrow">→</span>
          <span class="flow-node">Export Layer (planned)</span><span class="flow-arrow">→</span>
          <span class="flow-node">Next.js / Future Portals</span>
        </div>
      </div>
    </div>
    <div class="content-card">
      <h2>Six SharePoint Libraries</h2>
      <ul>
        <li>Administration · FinanceProcurement · PlanningPolicy</li>
        <li>AcademicServices · Research · SOPManuals</li>
      </ul>
    </div>
    <div class="content-card">
      <h2>Key ADRs</h2>
      <ul>
        <li><a href="${gh("docs/adr/ADR-001-m365-source-of-truth.md")}">ADR-001 M365 Source of Truth</a></li>
        <li><a href="${gh("docs/adr/ADR-002-website-presentation-layer.md")}">ADR-002 Presentation Layer</a></li>
        <li><a href="${gh("docs/adr/ADR-003-registry-pattern.md")}">ADR-003 Registry Pattern</a></li>
        <li><a href="${gh("docs/adr/ADR-004-sharepoint-library-strategy.md")}">ADR-004 Library Strategy</a></li>
      </ul>
      <p><a href="../adr/">ดู ADR ทั้งหมด →</a></p>
    </div>
    <div class="content-card">
      <h2>Baseline Document</h2>
      <p><a href="${gh("docs/release/ARCHITECTURE_BASELINE_v1.0.md")}">ARCHITECTURE_BASELINE_v1.0.md</a> — FROZEN</p>
    </div>
  </div></section>`,
      "Architecture — RAE Canonical Repository",
    ),
  );

  writePage(
    "standards/index.html",
    shell(
      sub,
      "standards",
      `
  <section class="page-hero"><div class="container"><h1>มาตรฐาน Canonical</h1><p>Reference Standards & Architecture Principles</p></div></section>
  <section class="section"><div class="container">
    <div class="principles-grid">
      <div class="principle"><strong>Build Less. Govern More.</strong><span>Consume governed foundation</span></div>
      <div class="principle"><strong>Metadata First</strong><span>DocumentID RAE-NNNNN immutable</span></div>
      <div class="principle"><strong>M365 Source of Truth</strong><span>No document binaries in Git</span></div>
      <div class="principle"><strong>Presentation Layer</strong><span>Portals link to SharePoint</span></div>
      <div class="principle"><strong>Static-first Public</strong><span>Export JSON for public portal</span></div>
      <div class="principle"><strong>AI Governed Data</strong><span>Visibility model enforced</span></div>
      <div class="principle"><strong>Architecture First</strong><span>Bootstrap template required</span></div>
      <div class="principle"><strong>No Duplicate SoR</strong><span>Single authority per domain</span></div>
    </div>
    <div class="content-card" style="margin-top:1.5rem">
      <h2>Normative Documents</h2>
      <ul>
        <li><a href="${gh("docs/canonical/REFERENCE_STANDARDS.md")}">Reference Standards</a></li>
        <li><a href="${gh("docs/governance/ARCHITECTURE_PRINCIPLES.md")}">Architecture Principles</a></li>
        <li><a href="${gh("docs/governance/SYSTEM_OF_RECORDS.md")}">System of Records</a></li>
        <li><a href="${gh("docs/canonical/CHANGE_CONTROL_POLICY.md")}">Change Control Policy</a></li>
      </ul>
    </div>
  </div></section>`,
      "Standards — RAE Canonical Repository",
    ),
  );

  writePage(
    "adr/index.html",
    shell(
      sub,
      "adr",
      `
  <section class="page-hero"><div class="container"><h1>Architecture Decision Records</h1><p>9 Accepted ADRs · Frozen decisions</p></div></section>
  <section class="section"><div class="container">
    <div class="content-card"><h2>Accepted ADRs</h2><ul>
      <li><a href="${gh("docs/adr/ADR-001-m365-source-of-truth.md")}">ADR-001 Microsoft 365 as Source of Truth</a></li>
      <li><a href="${gh("docs/adr/ADR-002-website-presentation-layer.md")}">ADR-002 Website is Presentation Layer</a></li>
      <li><a href="${gh("docs/adr/ADR-003-registry-pattern.md")}">ADR-003 Registry Pattern</a></li>
      <li><a href="${gh("docs/adr/ADR-004-sharepoint-library-strategy.md")}">ADR-004 SharePoint Library Strategy</a></li>
      <li><a href="${gh("docs/adr/ADR-005-metadata-first-architecture.md")}">ADR-005 Metadata First Architecture</a></li>
      <li><a href="${gh("docs/adr/ADR-006-governance-deferred-model.md")}">ADR-006 Governance Deferred Model</a></li>
      <li><a href="${gh("docs/adr/ADR-007-migration-strategy.md")}">ADR-007 Migration Strategy</a></li>
      <li><a href="${gh("docs/adr/ADR-008-production-freeze.md")}">ADR-008 Production Freeze</a></li>
      <li><a href="${gh("docs/adr/ADR-009-public-experience-separation.md")}">ADR-009 Public Experience Separation</a></li>
    </ul></div>
    <p><a href="${gh("docs/adr/README.md")}">Full ADR index on GitHub →</a></p>
  </div></section>`,
      "ADRs — RAE Canonical Repository",
    ),
  );

  writePage(
    "roadmap/index.html",
    shell(
      sub,
      "roadmap",
      `
  <section class="page-hero"><div class="container"><h1>Enterprise Roadmap</h1><p>Future platforms consume canonical standards</p></div></section>
  <section class="section"><div class="container">
    <ul class="roadmap-list">
      <li class="roadmap-item"><span class="roadmap-status status-done">Completed</span><div><h3>Document Center</h3><p>627 files · 627 Registry · Production frozen v1.0.0</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-consumer">Consumer</span><div><h3>Research Portal</h3><p>Consumes Research library metadata + Registry export</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-consumer">Consumer</span><div><h3>Learning Center</h3><p>AcademicServices + SOPManuals metadata</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-consumer">Consumer</span><div><h3>Green Office</h3><p>Taxonomy extension via ADR</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-future">Future</span><div><h3>Public Experience Portal</h3><p>Next.js · Registry export JSON</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-future">Future</span><div><h3>AI Knowledge Platform</h3><p>Governed RAG · DocumentID index</p></div></li>
      <li class="roadmap-item"><span class="roadmap-status status-future">Future</span><div><h3>Unified Integration Layer</h3><p>Enterprise export + monitoring</p></div></li>
    </ul>
    <p style="margin-top:1rem"><a href="${gh("docs/governance/RAE_ENTERPRISE_PLATFORM_ROADMAP.md")}">Full roadmap document →</a></p>
  </div></section>`,
      "Roadmap — RAE Canonical Repository",
    ),
  );

  writePage(
    "release/index.html",
    shell(
      sub,
      "release",
      `
  <section class="page-hero"><div class="container"><h1>Release Baseline</h1><p>Production v1.0.0 · Canonical v${VERSION}</p></div></section>
  <section class="section"><div class="container">
    <div class="stats-grid" style="margin-top:0">
      <div class="stat-card"><strong>1.0.0</strong><span>Production freeze</span></div>
      <div class="stat-card"><strong>1.0.1</strong><span>Canonical elevation</span></div>
      <div class="stat-card"><strong>1.0.2</strong><span>Enterprise governance</span></div>
      <div class="stat-card"><strong>${VERSION}</strong><span>Pages activation</span></div>
    </div>
    <div class="content-card" style="margin-top:1.5rem"><h2>Production Baseline (Frozen)</h2>
    <ul>
      <li>627 SharePoint files · 627 Registry rows</li>
      <li>0 duplicates · 0 broken URLs</li>
      <li>Tag: <code>document-center-v1.0.0</code></li>
    </ul></div>
    <div class="content-card"><h2>Release Documents</h2><ul>
      <li><a href="${gh("docs/release/DOCUMENT_CENTER_v1.0_PRODUCTION_FREEZE.md")}">Production Freeze</a></li>
      <li><a href="${gh("docs/release/ARCHITECTURE_BASELINE_v1.0.md")}">Architecture Baseline v1.0</a></li>
      <li><a href="${gh("docs/release/PRODUCTION_ACCEPTANCE_CERTIFICATE.md")}">Acceptance Certificate</a></li>
      <li><a href="${gh("docs/release/OPERATION_RUNBOOK_v1.0.md")}">Operation Runbook</a></li>
      <li><a href="${gh("docs/release/PROJECT_CLOSEOUT_REPORT.md")}">Project Closeout</a></li>
      <li><a href="${gh("docs/release/RELEASE_NOTES_v1.0.md")}">Release Notes v1.0</a></li>
    </ul></div>
  </div></section>`,
      "Release — RAE Canonical Repository",
    ),
  );

  writePage(
    "operations/index.html",
    shell(
      sub,
      "operations",
      `
  <section class="page-hero"><div class="container"><h1>Operations</h1><p>READ-MOSTLY mode · Repository operation policy</p></div></section>
  <section class="section"><div class="container">
    <div class="hero-badges" style="margin-bottom:1.5rem">
      <span class="badge badge-gold" style="color:var(--primary-dark)">READ-MOSTLY</span>
      <span class="badge badge-outline" style="border-color:var(--primary);color:var(--primary)">NO PRODUCTION CHANGES</span>
    </div>
    <div class="content-card"><h2>Allowed Changes</h2><ul>
      <li>Documentation updates</li>
      <li>New ADRs for future platforms</li>
      <li>Bug fixes and security fixes</li>
      <li>Runbook maintenance</li>
    </ul></div>
    <div class="content-card"><h2>Requires Architecture Review</h2><ul>
      <li>Baseline amendments</li>
      <li>New SharePoint libraries</li>
      <li>Registry schema changes</li>
      <li>ADR reversals</li>
    </ul></div>
    <div class="content-card"><h2>Operational Runbook</h2>
    <p>Monthly QA: Registry sync, corpus reconcile 627/627/627</p>
    <p><a href="${gh("docs/release/OPERATION_RUNBOOK_v1.0.md")}">Operation Runbook v1.0 →</a></p>
    <p><a href="${gh("docs/governance/REPOSITORY_OPERATION_POLICY.md")}">Repository Operation Policy →</a></p>
    </div>
  </div></section>`,
      "Operations — RAE Canonical Repository",
    ),
  );

  writePage(
    "404.html",
    shell(
      "./",
      "",
      `
  <section class="error-page">
    <div class="container">
      <h1>404</h1>
      <p>ไม่พบหน้าที่ต้องการ · Page not found</p>
      <p style="margin-top:1.5rem"><a class="btn btn-primary" href="./" style="display:inline-flex">กลับหน้าแรก</a>
      <a class="btn btn-ghost" href="./preview/" style="display:inline-flex;margin-left:0.5rem">UI Preview</a></p>
    </div>
  </section>`,
      "404 — RAE Canonical Repository",
    ),
  );
}

function copyAssets(): void {
  cpSync(resolve(SITE, "assets"), resolve(DIST, "assets"), { recursive: true });
  if (!existsSync(LOGO)) throw new Error("Missing logo: docs/logorae.png");
  cpSync(LOGO, resolve(DIST, "assets/logorae.png"));
}

function copyPreview(): void {
  cpSync(PREVIEW, resolve(DIST, "preview"), { recursive: true });
  updatePreviewIndex();
}

function updatePreviewIndex(): void {
  const indexPath = resolve(DIST, "preview/index.html");
  let html = readFileSync(indexPath, "utf8");
  const banner =
    '<div class="banner banner-demo" role="status" style="margin-bottom:0.75rem">' +
    "⚠️ UI PREVIEW ONLY — 3 mock records · preview_mode: true · " +
    '<a href="../" style="color:inherit">← กลับ Canonical Repository</a></div>';
  if (!html.includes("กลับ Canonical Repository")) {
    html = html.replace(
      '<header class="site-header">',
      '<div style="background:#005C3B;color:#fff;padding:0.5rem 1rem;text-align:center;font-size:0.85rem">' +
        '<strong>UI PREVIEW</strong> — ไม่ใช่ production portal · ' +
        '<a href="../" style="color:#FFDE00">Canonical Repository Home</a></div>' +
        banner +
        '<header class="site-header">',
    );
    html = html.replace(
      "Production UI lives in",
      "Canonical repository home: <a href=\"../\">../</a> · Production UI:",
    );
  }
  writeFileSync(indexPath, html, "utf8");
}

function validateDist(): void {
  const required = [
    "index.html",
    "404.html",
    "assets/canonical.css",
    "assets/canonical.js",
    "assets/logorae.png",
    "architecture/index.html",
    "standards/index.html",
    "adr/index.html",
    "roadmap/index.html",
    "release/index.html",
    "operations/index.html",
    "preview/index.html",
    "preview/data/public-registry.sample.json",
  ];
  for (const rel of required) {
    if (!existsSync(resolve(DIST, rel))) {
      throw new Error(`Missing required route/asset: ${rel}`);
    }
  }
  const sample = JSON.parse(
    readFileSync(resolve(DIST, "preview/data/public-registry.sample.json"), "utf8"),
  );
  if (!sample.preview_mode) throw new Error("preview_mode must be true in dist");
  if (sample.documents.length !== 3) throw new Error(`Expected 3 preview records, got ${sample.documents.length}`);
  const index = readFileSync(resolve(DIST, "index.html"), "utf8");
  if (index.includes("public-registry.sample.json") && index.includes("document-grid")) {
    throw new Error("Root must not contain demo document grid");
  }
  if (!index.includes("Canonical Repository")) {
    throw new Error("Root must be canonical landing page");
  }
  if (!index.includes(VERSION)) throw new Error(`Root must display version ${VERSION}`);
  console.log("PAGES_VALIDATE: OK — all routes and assets present");
}

function main(): void {
  assertPublicSampleOnly();
  rmSync(DIST, { recursive: true, force: true });
  mkdirSync(DIST, { recursive: true });
  buildPages();
  copyAssets();
  copyPreview();
  writeFileSync(resolve(DIST, ".nojekyll"), "\n", "utf8");
  validateDist();
  console.log(`PAGES_BUILD: OK — canonical portal v${VERSION} in dist/`);
}

main();
