# Research plot QA checklist

## Scientific meaning

- [ ] Series colors come from explicit semantic mapping, never incidental input order; markers and line styles also distinguish conditions.
- [ ] Legend entries correspond exactly to curves and uncertainties shown.
- [ ] Units, normalization, bin width, and range match across panels being compared.
- [ ] Statistical and systematic uncertainty are named and shown distinctly; assumptions and correlations are stated.
- [ ] Underflow, overflow, visible range, and sparse-bin treatment are reported.
- [ ] Log axes handle zero and negative values explicitly; nothing is silently clipped or omitted.
- [ ] Signed differences use a diverging scale centered at zero; comparable maps share limits and units.

## Visual rendering

- [ ] Render and inspect every page/panel in the actual PNG/PDF output at its intended physical size; text extraction or numeric checks do not count as pixel inspection.
- [ ] Legend text does not cover a peak, data points, or important uncertainty.
- [ ] Text does not overlap ticks, axis labels, neighboring panels, or the figure edge.
- [ ] Font sizes are readable at final print size or slide viewing distance; contrast, markers, and lines remain distinguishable without color alone.
- [ ] Every panel is visible, with no clipped labels, colorbars, legends, or content beyond the canvas.
- [ ] Compare Python and ROOT rendered output directly; do not infer visual equivalence from style names or equal numeric font sizes.
- [ ] For portable PDFs, inspect embedded font records and Unicode mapping (including ToUnicode); confirm font licensing permits embedding.
- [ ] If Japanese appears, verify Japanese glyphs are physically present in the rendered output and test viewing without external fonts. Inspect digits, minus sign, φ, and nσ too. Text extraction alone does not prove glyph rendering.
- [ ] Treat ROOT vector PDF and ROOT PNG as separate outputs: inspect the actual PDF before claiming vector publication readiness.

## Synthetic and statistical limits

- [ ] Clearly mark synthetic examples; never imply generated values came from an experiment.
- [ ] State the generating model and error assumptions. Check whether Gaussian/asymptotic error approximations are suitable for sparse counts.
- [ ] State when systematics or correlations are absent. Do not reuse example fit or uncertainty choices as analysis defaults without justification.

## ROOT vectorと共通palette

- ROOT GetColor(float RGB)は近い既存色へ寄せることがある。厳密なLUT比較は新規TColorへ登録し、runtime RGBを検査する。
- COLZで省略されるzeroはlinear/differenceのzero色をframeへ、logは明示masked色を指定。COL2のbitmap化をvectorと呼ばない。
- raw ROOT PDFを提出扱いにしない。font embed＋ToUnicodeを確認し、canvas CropBox/Rotateを実寸へ正規化、path/text保持と画像objectの有無を確認。
- Unicode mappingは実Encodingを根拠にする。今回WinAnsiとSymbol `[45 /minus]`のみ対応。他encodingは停止。
- 配色選択状態はconfig/selection.json、追加QAはqa/COLOR_REPORT.mdとqa/VECTOR_REPORT.mdを参照。未知環境のGS設定をglobalへ変更しない。
