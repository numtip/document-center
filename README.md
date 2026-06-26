# RAE Document Center

Metadata registry, validation scripts, and migration tooling for the RAE Document Center project (Maejo University — Research and Academic Extension).

This repository holds **metadata only**. Document files live in OneDrive; they are never stored in Git.

## What is in this repo

| Path | Purpose |
|------|---------|
| `docs/document-center/` | Taxonomy, registry schemas, migration matrices, audit reports |
| `scripts/` | Validation and registry generation scripts |
| `preview/` | Static GitHub Pages preview (sample data only) |

## Scripts

```bash
rtk npm install
rtk npm run validate:all
rtk npm run build
```

| Command | Description |
|---------|-------------|
| `npm run validate:matrix` | Validate migration matrix CSV |
| `npm run validate:registry` | Validate registry draft JSON |
| `npm run validate:all` | Run all validators |
| `npm run build` | Build static Pages preview into `dist/` |
| `npm run lint` | Placeholder (no linter configured yet) |

## GitHub Pages — preview / demo only

> **Important:** The GitHub Pages site is a **preview/demo UI only**. It does **not** serve real documents, internal records, or production OneDrive links.

| Item | Detail |
|------|--------|
| **Preview URL** | https://numtip.github.io/document-center/ |
| **Data source** | `preview/data/public-registry.sample.json` (3 mock public records) |
| **Excluded** | Internal, restricted, draft, and production registry files |
| **Download links** | Example URLs only (`example.sharepoint.com`) — not real files |
| **Production UI** | Implemented in [`rae-nextjs-main`](https://github.com/numtip/rae-nextjs-main) |

### Enable GitHub Pages (one-time, repo admin)

1. Repository **Settings → Pages**
2. **Build and deployment → Source:** GitHub Actions
3. Push to `main` — workflow `.github/workflows/pages.yml` deploys automatically

### Local preview

```bash
rtk npm run build
# Serve dist/ with any static server, e.g.:
rtk npx --yes serve dist -p 4173
```

Open http://localhost:4173/ (local base path `/`; GitHub Pages uses `/document-center/`).

## Architecture

```
OneDrive (files)
      ↓
storage-map / migration matrix (authoring)
      ↓
document-registry.json (metadata in Git)
      ↓
Next.js Document Center (production — rae-nextjs-main)
```

## Security

- Do not commit `.env`, certificates, tokens, or real OneDrive share URLs
- Do not add real document binaries to this repository
- Preview build validates that only `visibility=public` + `status=current` sample records ship to Pages

## License

Internal RAE project — confirm governance policy before external distribution.
