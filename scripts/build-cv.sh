#!/usr/bin/env bash
# Rebuild public/cv.pdf from the Overleaf CV source.
#
# The CV lives in Overleaf and is cloned locally over Overleaf's git bridge.
# This compiles it and drops the result where the site serves it. Tectonic is
# used rather than a TeX Live install: it is a single binary that fetches the
# packages the document asks for, which matters here because this machine has
# no TeX distribution at all.
#
#   ./scripts/build-cv.sh [path-to-clone]
#
# To refresh the source first:  git -C ~/Documents/cv-overleaf pull
set -euo pipefail

SRC="${1:-$HOME/Documents/cv-overleaf/My-CV-master}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$HERE/public/cv.pdf"

[ -f "$SRC/z.tex" ] || { echo "no z.tex under $SRC" >&2; exit 1; }
command -v tectonic >/dev/null || { echo "tectonic not on PATH (brew install tectonic)" >&2; exit 1; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cp -R "$SRC"/. "$WORK"/
mkdir -p "$WORK/out"
# Quiet unless it fails: the document throws a few dozen overfull-hbox
# warnings every run, which say nothing about whether the build worked.
if ! tectonic -X compile "$WORK/z.tex" --outdir "$WORK/out" >"$WORK/log" 2>&1; then
  tail -30 "$WORK/log" >&2
  exit 1
fi

pages=$(pdfinfo "$WORK/out/z.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
# A CV that suddenly builds to one page means the bibliography silently
# failed. Refuse rather than publish a truncated document.
if [ "${pages:-0}" -lt 4 ]; then
  echo "built only ${pages:-0} pages, refusing to publish" >&2
  exit 1
fi

cp "$WORK/out/z.pdf" "$OUT"
echo "wrote $OUT: $pages pages, $(wc -c < "$OUT" | tr -d ' ') bytes"
