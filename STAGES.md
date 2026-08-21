# Project Stages

A sequential checklist for building the archive. Each stage has a concrete "done when" so you always know whether to move on or keep working on the current one. References point back to sections in `illustration-archive-plan.md`.

Work through these roughly in order — later stages assume earlier ones are actually done, not just started.

---

## Stage 0 — Consolidate the project into one folder

- [ ] Pick the one folder this whole project will live in (e.g. `C:\Users\nikala\Documents\illustration-archive\`)
- [ ] Copy `setup-project.ps1`, `prep_batch.py`, and this file into it
- [ ] Run `.\setup-project.ps1` from inside that folder
- [ ] Move `prep_batch.py` into `.\scripts\`
- [ ] Delete (or just stop using) the old scattered folders under `Users\nikala\`
- [ ] `git init`, create the GitHub repo, push once (even with just the empty folder structure + `.gitignore`)

**Done when:** everything for this project lives under one folder, that folder is a git repo, and it's pushed to GitHub at least once.

---

## Stage 1 — Naming & metadata scaffolding

- [ ] Add your first journal(s) to `data/journals.yml` — Georgian name + a Latin slug you choose by hand (Plan §1, §2)
- [ ] Pick 2–3 real scanned images and manually work out what their filename *would* be under the naming convention, without running the script

**Done when:** you can look at a real image and confidently name it per §1 without hesitating or re-reading the plan.

---

## Stage 2 — First batch run (small, ~5 images)

- [ ] Run `prep_batch.py` against a tiny real test batch (5 images is plenty)
- [ ] Check the generated files in `_illustrations\` — do the pre-filled fields look right?
- [ ] Check `assets\images\illustrations\full\` and `\thumb\` — do the derivatives look right (size, quality, both jpg + webp)?
- [ ] Hand-fill `caption`, `theme_tags` (add more if one wasn't enough), and `artist` on those 5 stubs

**Done when:** 5 real illustrations have complete, correct metadata files and derivative images, committed to the repo.

---

## Stage 3 — Minimal Jekyll site skeleton

- [ ] Set up `_config.yml` with the `illustrations` collection defined
- [ ] Build the illustration detail page layout (renders one `_illustrations/*.md` item) — Plan §4
- [ ] Build the `illustrations.json` generator page (the Liquid template in §4)
- [ ] Confirm it runs locally via Docker (Plan §3, "Previewing the site locally on Windows")

**Done when:** `docker run ... jekyll serve` shows at least one working detail page locally, and `/illustrations.json` returns your 5 test records correctly.

---

## Stage 4 — Mosaic view

- [ ] Build `mosaic.js` + the CSS from §5 (card-catalog tabs, column layout)
- [ ] Wire up infinite-scroll batching (`IntersectionObserver`, §4)
- [ ] Build the lightbox (prev/next, "view full record" link)

**Done when:** the homepage shows all 5 test images in the mosaic, scrolling and the lightbox both work locally.

---

## Stage 5 — Catalogue & search

- [ ] Build the facet filters (journal, tags) wired to `illustrations.json`
- [ ] Build the date-range slider (also against the JSON index, not Pagefind — §4)
- [ ] Add Pagefind to the local build, wire up the text search box

**Done when:** you can filter by journal/tag, drag the date range, and free-text search — all three return correct results for your 5 test images.

---

## Stage 6 — Visual design pass

- [ ] Apply the palette, `Noto Serif Georgian` / `IBM Plex Mono` typography, and `lang="ka"` across every page
- [ ] Confirm Georgian text actually renders correctly everywhere (no tofu boxes, no fallback font creeping in)

**Done when:** it doesn't look like a default Jekyll theme, is visually consistent across mosaic/catalogue/detail pages, and every fragment of Georgian text renders in the intended typeface.

---

## Stage 7 — Deploy

- [ ] Add `.github/workflows/deploy.yml` (Plan §6)
- [ ] Push to GitHub, switch Pages source to "GitHub Actions" in repo settings
- [ ] Confirm the live URL works, including search

**Done when:** your 5 test images are live and fully functional (mosaic, catalogue, search) at your real GitHub Pages URL — not just localhost.

---

## Stage 8 — First real batch (50–100 images)

- [ ] Run the entire documented workflow (Plan §6) end to end, at real scale
- [ ] Note anywhere the process felt slower or more manual than it should — that's your Stage 9 priority list

**Done when:** a full real batch goes from PDF crop to live site using only the documented workflow, with no manual troubleshooting or one-off fixes.

---

## Stage 9 — Automation (later, as it starts to feel worth it)

Not urgent — revisit this once Stage 8 has happened a few times and the repetitive parts are obvious. Candidates are in Plan §7: AI-assisted tagging/captioning, OCR-seeded captions, session-level CSV pre-fill, the tag-vocabulary linter, duplicate detection.

**Done when:** never, really — this stage is ongoing. Pick one item at a time, only when the manual version has actually become annoying.
