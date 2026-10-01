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

layoutはclassic、密度linear/logはviridis、符号付き差分は0中心RdBu_r（負blue・正red）を採用。paper/slidesは最終用途で選ぶ。1D線色は追加のユーザー回答で④黒・青・朱色を採用。observed=black、reference=blue、model=vermilion。config/selection.jsonを参照。4条件以上では色を自動循環しない。条件キーごとに色・線種・markerの対応を明示し、既存3色の再利用を含む追加対応はレビューしてから設定する。無断で新色を採用しない。旧候補は比較資料として保持し、他repoは変更しない。
