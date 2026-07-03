#!/bin/sh
# Celestial Electric - MPT repo v2.0 finisher
# Run from anywhere inside the repo:  sh finish.sh
# Idempotent: safe to run twice. Self-removing: deletes itself in the final commit.

set -e
cd "$(git rev-parse --show-toplevel)"

echo "== Unpacking patches =="
[ -f v2-assets-patch.zip ] && unzip -o v2-assets-patch.zip
[ -f v2-final-patch.zip ]  && unzip -o v2-final-patch.zip

echo "== Cleanup =="
rm -f v2-assets-patch.zip v2-final-patch.zip
rm -f docs/assets/pdfs/README.md
rm -f finish.sh

echo "== Commit + push =="
git add -A
git commit -m "v2.0 complete: assets, tools, changelog, README, gitignore" || echo "(nothing new to commit)"
git push

echo "=================================="
echo "TRACKED FILE COUNT (target is 37):"
git ls-files | wc -l
echo "=================================="
