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

async function loadJson(path) {
  const res = await fetch(new URL(path, BASE));
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
  return res.json();
}

function categoryName(id) {
  return taxonomy.categories.find((c) => c.id === id)?.name_th ?? id;
}

function renderKpis(docs) {
  kpis.innerHTML = `
    <div class="kpi-card"><strong>${docs.length}</strong>เอกสารสาธารณะ (ตัวอย่าง)</div>
    <div class="kpi-card"><strong>${new Set(docs.map((d) => d.category)).size}</strong>หมวดที่มีเอกสาร</div>
    <div class="kpi-card"><strong>Demo</strong>ไม่ใช่ข้อมูลจริง</div>
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
      return `
      <article class="doc-card">
        <header>
          <span class="doc-id">${doc.id}</span>
          <span class="badge">${doc.file_type?.toUpperCase() ?? "FILE"} · public</span>
        </header>
        <h3 class="doc-title">${doc.title}</h3>
        <p class="meta">${categoryName(doc.category)} · v${doc.version ?? "1.0"} · ${doc.updated_date ?? ""}</p>
        <div class="tags">${(doc.tags ?? []).map((t) => `<span class="tag">${t}</span>`).join("")}</div>
        <a href="${isDemoUrl ? "#demo-download" : doc.storage_url}" ${isDemoUrl ? 'aria-disabled="true" title="Demo only — not a real download link"' : 'target="_blank" rel="noopener noreferrer"'}>
          ${isDemoUrl ? "ดาวน์โหลด (ตัวอย่าง — ไม่ใช่ลิงก์จริง)" : "ดาวน์โหลด"}
        </a>
      </article>
    `;
    })
    .join("");

  emptyState.classList.toggle("hidden", docs.length > 0);
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

async function init() {
  [registry, taxonomy] = await Promise.all([
    loadJson("./data/public-registry.sample.json"),
    loadJson("./data/taxonomy.sample.json"),
  ]);

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
