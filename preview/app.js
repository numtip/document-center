const BASE = new URL("./", import.meta.url);

const categoryFilter = document.getElementById("category-filter");
const searchInput = document.getElementById("search");
const documentList = document.getElementById("document-list");
const emptyState = document.getElementById("empty-state");
const kpis = document.getElementById("kpis");
const categoriesEl = document.getElementById("categories");

let taxonomy = { categories: [] };
let registry = { documents: [] };
let activeCategory = "";
let sourceMode = "demo"; // "live" | "demo"

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

async function loadJson(path) {
  const res = await fetch(new URL(path, BASE));
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
  return res.json();
}

/**
 * Normalise PXP-1 contract field names to the internal property names
 * used by the render functions.  Safe to call on already-normalised data
 * (unknown source fields are simply passed through).
 */
function normalizePxp1(docs) {
  return docs.map((doc) => ({
    id: doc.DocumentID ?? doc.id,
    title: doc.Title ?? doc.title,
    category: doc.Category ?? doc.category,
    status: doc.Status ?? doc.status ?? "",
    visibility: doc.Visibility ?? doc.visibility ?? "public",
    updated_date: doc.UpdatedDate ?? doc.updated_date ?? "",
    storage_url: doc.StorageURL ?? doc.storage_url ?? "",
    download_mode: doc.DownloadMode ?? doc.download_mode ?? "DIRECT",
    file_type: doc.file_type ?? "",
    tags: doc.tags ?? [],
    version: doc.version ?? "1.0",
  }));
}

function categoryName(id) {
  return taxonomy.categories.find((c) => c.id === id)?.name_th ?? id;
}

/* ------------------------------------------------------------------ */
/*  Render helpers                                                     */
/* ------------------------------------------------------------------ */

function renderKpis(docs) {
  const isLive = sourceMode === "live";
  kpis.innerHTML = `
    <div class="kpi-card"><strong>${docs.length}</strong>${isLive ? "เอกสารสาธารณะ" : "เอกสารสาธารณะ (ตัวอย่าง)"}</div>
    <div class="kpi-card"><strong>${new Set(docs.map((d) => d.category)).size}</strong>หมวดที่มีเอกสาร</div>
    <div class="kpi-card"><strong>${isLive ? "Live" : "Demo"}</strong>${isLive ? "ข้อมูลจากระบบจริง" : "ไม่ใช่ข้อมูลจริง"}</div>
  `;
}

function renderCategories(docs) {
  const counts = docs.reduce((acc, doc) => {
    acc[doc.category] = (acc[doc.category] ?? 0) + 1;
    return acc;
  }, {});

  categoriesEl.innerHTML = taxonomy.categories
    .filter((c) => c.enabled && counts[c.id])
    .map(
      (c) => `
      <button type="button" class="category-chip ${activeCategory === c.id ? "active" : ""}" data-category="${c.id}">
        <strong>${c.name_th}</strong>
        <span>${counts[c.id] ?? 0} เอกสาร</span>
      </button>
    `,
    )
    .join("");

  categoriesEl.querySelectorAll("[data-category]").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeCategory = btn.dataset.category === activeCategory ? "" : btn.dataset.category;
      categoryFilter.value = activeCategory;
      renderDocuments(filterDocuments());
      renderCategories(registry.documents);
    });
  });
}

function filterDocuments() {
  const q = searchInput.value.trim().toLowerCase();
  const cat = categoryFilter.value || activeCategory;

  return registry.documents.filter((doc) => {
    if (cat && doc.category !== cat) return false;
    if (!q) return true;
    const haystack = [
      doc.id,
      doc.title,
      doc.category,
      categoryName(doc.category),
      ...(doc.tags ?? []),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(q);
  });
}

function renderDocuments(docs) {
  documentList.innerHTML = docs
    .map((doc) => {
      const isDemoUrl = (doc.storage_url ?? "").includes("example.sharepoint.com");
      const isAuthenticated = doc.download_mode === "AUTHENTICATED_SHAREPOINT";

      let downloadHtml;
      if (isDemoUrl) {
        downloadHtml = `<a href="#demo-download" aria-disabled="true" title="Demo only — not a real download link">ดาวน์โหลด (ตัวอย่าง — ไม่ใช่ลิงก์จริง)</a>`;
      } else if (isAuthenticated) {
        downloadHtml = `
          <div class="auth-download">
            <a href="${doc.storage_url}" target="_blank" rel="noopener noreferrer">ดาวน์โหลดเอกสาร</a>
            <span class="auth-note">อาจต้องลงชื่อเข้าใช้บัญชี Microsoft 365 ของมหาวิทยาลัย</span>
          </div>`;
      } else {
        downloadHtml = `<a href="${doc.storage_url}" target="_blank" rel="noopener noreferrer">ดาวน์โหลด</a>`;
      }

      return `
      <article class="doc-card">
        <header>
          <span class="doc-id">${doc.id}</span>
          <span class="badge">${doc.file_type?.toUpperCase() ?? "FILE"} · ${doc.visibility ?? "public"}</span>
        </header>
        <h3 class="doc-title">${doc.title}</h3>
        <p class="meta">${categoryName(doc.category)} · v${doc.version ?? "1.0"} · ${doc.updated_date ?? ""}</p>
        <div class="tags">${(doc.tags ?? []).map((t) => `<span class="tag">${t}</span>`).join("")}</div>
        ${downloadHtml}
      </article>
    `;
    })
    .join("");

  /* Empty-state messaging */
  emptyState.classList.toggle("hidden", docs.length > 0);
  if (docs.length === 0) {
    const q = searchInput.value.trim().toLowerCase();
    const cat = categoryFilter.value || activeCategory;
    if (!q && !cat && sourceMode === "live") {
      emptyState.textContent = "ยังไม่มีเอกสารสาธารณะในระบบในขณะนี้";
    } else {
      emptyState.textContent = "ไม่พบเอกสารที่ตรงกับการค้นหา";
    }
  }
}

function populateCategoryFilter() {
  taxonomy.categories
    .filter((c) => c.enabled)
    .forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name_th;
      categoryFilter.appendChild(opt);
    });
}

/* ------------------------------------------------------------------ */
/*  Init                                                               */
/* ------------------------------------------------------------------ */

async function init() {
  /* 1. Try loading the live public export */
  try {
    registry = await loadJson("../data/document-registry.public.json");
    if (registry.documents && registry.documents.length > 0) {
      registry.documents = normalizePxp1(registry.documents);
      sourceMode = "live";
    } else {
      throw new Error("live export is empty");
    }
  } catch {
    /* 2. Fall back to demo fixtures */
    registry = await loadJson("./data/public-registry.sample.json");
    sourceMode = "demo";
  }

  /* 3. Update data-source status banner */
  const statusBanner = document.getElementById("data-source-status");
  if (statusBanner) {
    if (sourceMode === "live") {
      statusBanner.textContent = "กำลังแสดงข้อมูลจากระบบจริง";
      statusBanner.className = "banner banner-live";
    } else {
      statusBanner.textContent = "กำลังแสดงข้อมูลตัวอย่าง (Demo) — ไม่ใช่ข้อมูลจริง";
      statusBanner.className = "banner banner-demo";
    }
  }

  /* 4. Update documents heading */
  const docsHeading = document.getElementById("documents-heading");
  if (docsHeading) {
    docsHeading.textContent =
      sourceMode === "live" ? "เอกสารสาธารณะ" : "เอกสารสาธารณะ (ตัวอย่าง)";
  }

  /* 5. Load taxonomy (always from the local preview fixture) */
  taxonomy = await loadJson("./data/taxonomy.sample.json");

  populateCategoryFilter();
  renderKpis(registry.documents);
  renderCategories(registry.documents);
  renderDocuments(registry.documents);

  searchInput.addEventListener("input", () => renderDocuments(filterDocuments()));
  categoryFilter.addEventListener("change", () => {
    activeCategory = categoryFilter.value;
    renderDocuments(filterDocuments());
    renderCategories(registry.documents);
  });
}

init().catch((err) => {
  document.body.innerHTML = `<main class="container"><h1>Preview failed to load</h1><pre>${err.message}</pre></main>`;
});
