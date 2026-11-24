# Loom motion library

Loading-animation concepts built from the Loom logo's own shapes (12 legs + a ring).

- **`index.html`** — the whole library as one self-contained page. Open it in a browser or host it as a static site.
- **`lottie/`** — each animation as Lottie JSON: Movie reel, Shutter, Tracking, Arrival, Depth of field, Surfacing, Unfold, Tunnel, Assemble.
  Film strip (canvas) and the 3D spin (WebGL) are code-only, so they have no JSON.
- **`src/`** — page source, one page per animation, and the Python generators (`make_*.py`) that write the Lottie files.
  Rebuild everything with `src/build_all.sh`.
- **`favicon-black.svg`** — black tile, white Loom mark (also embedded in the page).

Notes
- Depth of field uses Lottie's Gaussian Blur effect, so it needs the full lottie-web player; some native players (e.g. iOS) may ignore it.
- Movie reel is the product's paid Jitter export plus a soft fade at the loop point; the export itself shows a few cut-off frames around 1.2–1.5s.
- To add an animation: put a page in `src/items/`, add a line to `GROUPS` in `src/index-src.html`, run `src/build_all.sh`.
