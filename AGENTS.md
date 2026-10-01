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

白背景・セリフ体・グリッドなしのレイアウト（内部名classic）を使い、密度linear/logはviridis、符号付き差分は0中心RdBu_r（負blue・正red）を採用。paper/slidesは最終用途で選ぶ。1D系列は役割別に主データ（observed）を黒、比較データ（reference）を青、モデル（model）を朱色に固定する。config/selection.jsonを参照。4条件以上では色を自動循環しない。条件キーごとに色・線種・markerの対応を明示し、既存3色の再利用を含む追加対応はレビューしてから設定する。無断で新色を採用しない。旧候補は比較資料として保持し、他repoは変更しない。

## 図の目的・説明・可読性

- 作図前に、この図で伝えることと、根拠として使う比較を一文で決める。読者が図から判断できる内容に絞り、結論に不要なパネルや装飾を減らす。
- 初めて読む人を想定し、理解に必要な略語・変数・規格化・比較対象を図または近くの説明で示す。すべての語を詳説するのではなく、目的を理解するための最小限の説明を置く。
- 結論に必要な精度に対し、事象数・有効統計・誤差・相関が十分か確認する。統計不足の図から傾向や優劣を議論しない。根拠が不足する場合は結論を保留し、図を探索的なものと明記するか、議論から外す。見た目を整えて統計不足を隠さない。
- 統計データ・比・残差は点と必要な誤差棒で描き、データ点同士を線で結ばない。理論・モデルの曲線と水平の基準線は明確に区別する。誤差なしのデータ点も接続しない。
- 最終掲載幅・投影サイズで、軸・目盛り・タイトル・凡例・点・誤差棒が読めるか実出力を確認する。小さい文字を読むのが苦手な読者や会場後方の聴衆が、拡大や過度な努力なしに内容を追えることを目標とする。スマートフォン対応を前提にしない。
- 読みにくければ文字や点を大きくする、説明を短くする、図を大きくする、パネルを分ける。設定のフォントサイズや機械的な重なり・埋込検査が通っただけで資料完成と判断しない。
