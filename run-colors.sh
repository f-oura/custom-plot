#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
PLOT_PYTHON=${PLOT_PYTHON:-python3}
PDF_PYTHON=${PDF_PYTHON:-python3}
export MPLCONFIGDIR=${MPLCONFIGDIR:-/tmp/research-plot-mpl}
"$PLOT_PYTHON" python/color_compare.py
root -l -b -q root/color_compare.C
"$PDF_PYTHON" root/embed_vector_pdf.py
"$PDF_PYTHON" qa/color_checks.py
