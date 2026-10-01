# 見本の選び方

まず [output/comparison.pdf](output/comparison.pdf) を100%表示し、論文用とスライド用をそれぞれ確認してください。候補名は `classic`、`clean`、`ink` です。これは個人用の比較案で、公式STAR形式ではありません。

| 候補 | 色と見た目 | 見る点 |
|---|---|---|
| classic | 青・朱・緑、セリフ体、グリッドなし | 密度palette viridis、符号付きpalette RdBu_r |
| clean | 青・茶・紫、サンセリフ体、薄いグリッド | 密度palette cividis、符号付きpalette PuOr |
| ink | 黒・灰・赤紫、サンセリフ体、グリッドなし | 密度palette magma、符号付きpalette BrBG |

各図の系列色はデータ順でなく条件名に固定されています。marker形状と実線/破線も条件ごとに異なります。2D差分は0を中央に置き、相関行列は全て同じ -1〜1 のscaleで比べます。論文用は10 pt/単図3.4×2.8 inch、スライド用は15 pt/単図10×7 inchを基本にしています。スライドの投影距離、論文の実際の掲載幅に合わせて確認してください。

比較PDFの9-panel一覧にはcountsと統計誤差、log Y、複数条件overlay、ratio、背景差し引き、fit residual、log 2D密度、符号付き差分、相関heatmapがあります。linear 2D密度、上下段overlay+ratio、共通軸panelと実寸単図はoutput内の別PNG/PDFで比較できます。比較PDFではROOTの図はPNGのpreviewです。MatplotlibとROOTは同じデータとsemantic mappingを使いますが、文字やlayoutが完全に同じとは限りません。ROOTのPNG表示をROOTのvector PDF品質の証拠にしないでください。ROOT単体PDFはType 1 font未埋め込みです。比較PDFの文字部分は埋め込みDejaVu Sansです。日本語PDFと日本語フォント埋め込み/ToUnicodeは未検証です。

このデータはSYNTHETICで、独立Poisson誤差のみです。fitは平均と幅を固定した重み付き線形fitです。疎なbinでの対称Poisson誤差・pullは漸近近似の限界を持ち、実データの統計処理を規定しません。systematicも入っていません。ここでは図の見やすさを選び、解析上の定義は各分析で決めてください。

選ぶときはテイストに加えて、paper/slidesそれぞれの文字サイズ、palette、凡例位置や条件markerの好みを記録してください。候補の採否はまだ確定していません。共同研究・投稿先固有のルールがあれば、そのルールを優先するoverrideが必要です。

## 現在の選択と次の比較

layoutはclassicをユーザー選択済み。現在の採用設定は末尾参照。`output/classic-color-comparison.pdf`（4ページ）で、1のblue/orange/teal＋viridisと、4のblack/blue/vermilion＋BluesまたはYlGnBuを見比べてください。4は3色だけ、1のmagentaは補助条件用予約色です。差分は全候補共通の0中心RdBu_r。比較資料は保持し、採用は線④／density viridis／差分RdBu_rで確定。他repoへの適用はまだ行っていません。

## 採用済み方針

作図はPython／Matplotlibを標準とする。ROOT描画はPythonが使えない場合、または計算連携上ROOT描画が適切な場合に使い、例外理由を記録する。計算backendは研究上の都合で選び、ROOTで計算・解析した結果をCSV/配列等でPython描画へ渡してよい。描画標準を理由に計算backendを強制変更しない。

layoutはclassic、密度linear/logはviridis、符号付き差分は0中心RdBu_r（負blue・正red）を採用。paper/slidesは最終用途で選ぶ。1D線色は追加のユーザー回答で④黒・青・朱色を採用。observed=black、reference=blue、model=vermilion。config/selection.jsonを参照。4条件以上では色を自動循環しない。条件キーごとに色・線種・markerの対応を明示し、既存3色の再利用を含む追加対応はレビューしてから設定する。無断で新色を採用しない。旧候補は比較資料として保持し、他repoは変更しない。
