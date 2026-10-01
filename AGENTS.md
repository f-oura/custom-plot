# Repository guidance

- Treat every checked-in plot and CSV as synthetic demonstration material. Never present it as research evidence.
- Keep `config/styles.json` as the shared source of truth. After changing it, regenerate the Matplotlib and ROOT exports with `python3 python/export_styles.py`.
- Keep Python and ROOT mappings semantically aligned, but judge the rendered output rather than assuming equal settings produce equal appearance.
- Follow the reusable plot review instructions in [`.agents/skills/research-plot/SKILL.md`](.agents/skills/research-plot/SKILL.md), including its checklist.
- Do not call a candidate an official STAR style. Respect collaboration, journal, and institutional requirements through explicit overrides.
- Do not apply a candidate to another analysis repository until the user selects it. Do not add remotes, publish, or push this repository without an explicit request.
- For ROOT vector output, Japanese text, or embedded fonts, state what was actually rendered and inspected. A ROOT PNG preview does not validate its PDF output.

## 採用済み方針

作図はPython／Matplotlibを標準とする。ROOT描画はPythonが使えない場合、または計算連携上ROOT描画が適切な場合に使い、例外理由を記録する。計算backendは研究上の都合で選び、ROOTで計算・解析した結果をCSV/配列等でPython描画へ渡してよい。描画標準を理由に計算backendを強制変更しない。

layoutはclassic、密度linear/logはviridis、符号付き差分は0中心RdBu_r（負blue・正red）を採用。paper/slidesは最終用途で選ぶ。1D線色は追加のユーザー回答で④黒・青・朱色を採用。observed=black、reference=blue、model=vermilion。config/selection.jsonを参照。4条件以上では色を自動循環しない。条件キーごとに色・線種・markerの対応を明示し、既存3色の再利用を含む追加対応はレビューしてから設定する。無断で新色を採用しない。旧候補は比較資料として保持し、他repoは変更しない。
