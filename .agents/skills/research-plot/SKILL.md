---
name: research-plot
description: Create, export, or review physics research plots with shared Python/ROOT styles and publication-aware visual QA.
---

# Research plot workflow

Use this guidance when creating or reviewing figures in this repository or when adapting its shared style to an analysis. Follow explicit collaboration, journal, and institutional requirements first; express them as overrides. The included `classic`, `clean`, and `ink` styles are personal candidates, not an official STAR style. Do not apply a candidate across another repository before the user selects it.

Read `references/checklist.md` before approving an output. Keep semantic series mapping stable across data order, preserve units and normalization, and choose ranges from the data and scientific question. Distinguish statistical from systematic uncertainty. Handle zeros and negative values explicitly on logarithmic axes. Report visible range, underflow/overflow, and sparse-statistics limitations.

Inspect rendered PNG and PDF pages at their intended physical display size. Numeric metadata and extracted text are not visual inspection. Check legends against peaks and data, ticks and labels against each other, all panel boundaries, fonts, glyphs, and contrast. Compare backend outputs visually; Matplotlib point sizes and ROOT pixel/font modes have different units. A ROOT PNG does not establish ROOT vector-PDF quality. Check actual embedded fonts and text mapping in exported files when portability matters.

The gallery and example CSVs are synthetic. Do not describe them as measured results. The example fit fixes peak mean and width and uses weighted linear least squares; its independent Poisson errors omit systematic uncertainty. Do not generalize its error bars or pull to sparse bins without checking the approximation.

## Repository references

- `references/checklist.md`: reusable preflight and visual QA checklist.
- `../../../config/styles.json`: canonical style values and condition mapping.
- `../../../SELECTION.md`: short guide to the visual candidates and their limits.

## 採用済み方針

作図はPython／Matplotlibを標準とする。ROOT描画はPythonが使えない場合、または計算連携上ROOT描画が適切な場合に使い、例外理由を記録する。計算backendは研究上の都合で選び、ROOTで計算・解析した結果をCSV/配列等でPython描画へ渡してよい。描画標準を理由に計算backendを強制変更しない。

白背景・セリフ体・グリッドなしのレイアウト（内部名classic）を使い、密度linear/logはviridis、符号付き差分は0中心RdBu_r（負blue・正red）を採用。paper/slidesは最終用途で選ぶ。1D系列は役割別に主データ（observed）を黒、比較データ（reference）を青、モデル（model）を朱色に固定する。config/selection.jsonを参照。4条件以上では色を自動循環しない。条件キーごとに色・線種・markerの対応を明示し、既存3色の再利用を含む追加対応はレビューしてから設定する。無断で新色を採用しない。旧候補は比較資料として保持し、他repoは変更しない。

## 図の目的・説明・可読性

- 作図前に、この図で伝えることと、根拠として使う比較を一文で決める。読者が図から判断できる内容に絞り、結論に不要なパネルや装飾を減らす。
- 初めて読む人を想定し、理解に必要な略語・変数・規格化・比較対象を図または近くの説明で示す。すべての語を詳説するのではなく、目的を理解するための最小限の説明を置く。
- 結論に必要な精度に対し、事象数・有効統計・誤差・相関が十分か確認する。統計不足の図から傾向や優劣を議論しない。根拠が不足する場合は結論を保留し、図を探索的なものと明記するか、議論から外す。見た目を整えて統計不足を隠さない。
- 統計データ・比・残差は点と必要な誤差棒で描き、データ点同士を線で結ばない。理論・モデルの曲線と水平の基準線は明確に区別する。誤差なしのデータ点も接続しない。
- 最終掲載幅・投影サイズで、軸・目盛り・タイトル・凡例・点・誤差棒が読めるか実出力を確認する。小さい文字を読むのが苦手な読者や会場後方の聴衆が、拡大や過度な努力なしに内容を追えることを目標とする。スマートフォン対応を前提にしない。
- 読みにくければ文字や点を大きくする、説明を短くする、図を大きくする、パネルを分ける。設定のフォントサイズや機械的な重なり・埋込検査が通っただけで資料完成と判断しない。
