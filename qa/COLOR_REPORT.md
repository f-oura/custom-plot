# Classic 配色比較の検証

ユーザー選択済みlayoutはclassic。配色1/4とdensity viridis/Blues/YlGnBuは未選択。`config/selection.json`に記録し、他repoや既存styleへ適用しない。初版のclassic/clean/inkは保持。

`output/classic-color-comparison.pdf`は4ページ：Matplotlib paper、ROOT paper、Matplotlib slides、ROOT slides。paper12×10inch、slides16×13inch。色選び用一覧で、単図の出版サイズに縮小しない。単図の実寸検証は`root-vector-samples.pdf`と初版のsingle plotを使う。

配色1はobserved blue、reference orange、model teal、magentaは予約色のみ。配色4はblack/blue/vermilionの3色のみ。curve/凡例は同じ3項目、marker circle/squareとsolid/dashed/dottedを併用。実研究dataを使わず、同一CSVから描画。初版commitとのCSV byte一致を検査済み。

counts x0–8GeV、y0–210、0.2GeV/bin、ratio0–5。密度linear0–60、log1–60、差分−30…+30で中心0。同じ128点RGB LUTをJSONからPython/ROOTへ渡す。ROOTのGetColorは近い既存色を再利用するため、新しいTColorへ正確なRGBを登録。実runtime RGBとの最大差は2.98e−8。axis tickの選び方・aspectはbackend間で異なり、同一pixelとは主張しない。ROOT COLZが省略するlinearのzeroセルはframeをzero色に設定、logの261zeroセルはgrayで明示。差分のzeroはneutral色。負値はlog用dataにない。ROOT COL2はbitmapとなるため採用せずCOLZのvectorを使用（[ROOT公式THistPainter](https://root.cern/doc/master/classTHistPainter.html)）。

全8ページ（color4＋vector proof4）をPDFからPopplerで実renderし目視。重要peak上にlegendがなく、軸tick/label、下段、colorbar、noteの切れや重なりを確認。余白・共有軸の上段labelを修正してから最終renderを確認。PNGも両backend/presetで保存。

全PDF fontはembedded/subset/ToUnicode yes。ROOTは既存GS10の救済経路でtext/pathを保持。Matplotlib colorbarの自動raster化を無効化し、最終PDF全8ページのImage objectは0。外部font空設定の実renderと通常renderは全ページpixel差0。Symbolの負号は実Encoding Differences `[45 /minus]`を確認しU+2212へ対応。未知glyphやJapanese encodingは停止し、推測しない。

ROOTcolor paperの横書きfontは7.2–11.5pt、slides11.5–16.5pt。Matplotlib指定10/15ptと同一ではない。高密度一覧は投影用完成slideではなく配色確認用であり、最終投影距離/印刷サイズはユーザー確認待ち。統計誤差のみ、独立Poissonの対称近似、fit shape固定。小統計binやratio誤差の科学的限界は初版README参照。color gamut、printer/projectorでの見え方は未検証。

`qa/color_checks.py`はdata不変、runtime LUT、PDF page数/font/vector/外部font無しrenderを検査。目視合格は自動化しない。詳細は`qa/color/results.json`と`qa/vector/results.json`。
