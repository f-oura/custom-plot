#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PLOT_PYTHON=${PLOT_PYTHON:-python3}
export MPLCONFIGDIR="$PWD/qa/cache/matplotlib"
mkdir -p "$MPLCONFIGDIR"
"$PLOT_PYTHON" -c 'import numpy,matplotlib,PIL'
command -v root >/dev/null
"$PLOT_PYTHON" python/export_styles.py
"$PLOT_PYTHON" python/build.py > qa/python-run.log 2>&1
root -l -b -q root/gallery.C > qa/root-run.log 2>&1
if rg -i 'error:|fatal error|exception' qa/root-run.log; then exit 1; fi
"$PLOT_PYTHON" python/build.py --comparison
"$PLOT_PYTHON" qa/verify.py > qa/verify-run.log
pdftoppm -scale-to 1400 -png output/comparison.pdf qa/comparison > qa/render.log 2>&1
printf 'Generated comparison.pdf. Inspect every page before approving. ROOT raw PDFs remain unembedded.\n'
