#!/bin/sh
# Regenerates every Lottie file + the per-animation pages, then rebuilds ../index.html (the single shareable page).
set -e
cd "$(dirname "$0")"
for g in make_*_lottie.py make_movie_reel.py; do python3 "$g"; done
python3 pages.py
python3 build.py
