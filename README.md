# Portfolio Guide (interactive HTML)

An interactive HTML version of "Build & Deploy Your Professional Portfolio Website": 24 sections, copy-ready prompts, checklists and search. Plain HTML/CSS/JS, no build step, no dependencies.

## Open locally
Double-click `index.html`, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

## Screenshots
The guide uses 10 real screenshots from `assets/screenshots/`. Section 23 lists them. To swap one, replace the file with the same name.

## PDF
The Download buttons use `assets/pdf/GLEEBOI_Portfolio_Build_and_Deploy_Guide.pdf`.

## Deploy on GitHub Pages
Upload the contents of this folder to a repository, then Settings → Pages → Deploy from a branch → `main` → `/(root)` → Save.

## How it works
- **Contents:** the sidebar (a drawer on screens ≤1024px) links to each section; the current section is highlighted.
- **Search:** `js/search.js` searches the page text in the browser. Press `/` or click Search.
- **Checklists:** ticks are saved in `localStorage`; "Reset checklist" clears them.
- **Theme:** saved in `localStorage`.
