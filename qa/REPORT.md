# 初版QA報告

対象は全てSYNTHETIC。ユーザーの研究データ・他の研究repo・global設定・global skillは変更していない。独立repo初版で、候補の採用はユーザーの判断待ち。

## 実行と確認

- 既存Python環境：Python 3.11、NumPy 2.4.6、Matplotlib 3.11.0、Pillow。ROOT 6.32.08。新規installなし。
- `run.sh` でJSONから両backend styleを生成し、PythonとROOTを実行。同一CSVで3候補×2preset×2backendの12PNGと12ページ比較PDFを作成。
- counts40bin、density24×24bin、対称positive-definite correlation、固定shape fit（3parameter、37ndof）、ratio error rangeを数値検査。fitのchi2=38.0169。詳細 `automated.json`、`fit.json`。
- 見本：stat counts、logY、overlay、ratio、background subtraction、fit residual、log density＋明示された261zero bins、0中心signed差分、correlation。別見本でlinear density、上下段overlay/ratio、共通軸、single paper/slides。
- 比較するcounts/range/bin幅/単位/normalizationを共通化。densityはlinear0-60、log1-60、signedは-30..30、correlationは-1..1。underflow/overflowは合成モデルの定義により0。ratioは0..5に共通化。
- 図作成担当がPDFのPoppler renderとPNGの実pixelを目視した。重要な3GeV peakに凡例文字が被らず、tick/axis labelの重なりやpanelの切れがないことを確認。単図paper（3.4×2.8inch）とslides（10×7inch）も目視。galleryは候補比較用の大きな紙面で、単欄サイズに縮小する用途ではない。
- 明示条件で色/marker/lineを固定。observed/reference/model。色だけに依存しない。ただし灰色referenceは高contrastな線色より淡く、投影環境での確認はユーザー選択後に必要。
- 修正した不具合：ROOT paletteが他panelへ伝播（pad内TExecで各paletteを再設定）、Python下端注記のaxis-labelとの重なり（専用余白）、ratio errorsのrange外、color maxのデータ超過（density max52、差分max24.25を含む範囲へ修正）。

## フォント・PDF

- 比較PDFとMatplotlibの10PDFは `pdffonts` でCID TrueType / embedded=yes / subset=yes / Unicode=yesを確認。`*-fonts.txt` に実出力を保存。DejaVu licenseの埋込許可を確認し `licenses/DejaVu.txt` に同梱。
- 比較PDF全12ページを、外部font directoryが空のFontconfig設定でもrender。通常renderとのpixel差分0。比較PDFのROOT panelはPNG、見出しは埋込DejaVu。これはROOT vector exportの埋込検証を代替しない。
- 数字・負号・φ・nσを見本注記とtickで実pixel確認。今回日本語PDFは作っていない。日本語Markdownガイドを同梱。日本語実体font＋ToUnicode＋license＋外部font無しrenderは将来の日本語PDF作成時に必須。
- ROOT raw vector PDF（single/overlay-ratio）の生成自体は成功。ただしType1 fontが未埋込、ToUnicodeなし。論文用PDFの移植性は **FAIL**。ROOT PNGは見本として確認済み。埋込ベクトルPDFは未完成。
- 既存Ghostscript9.27はgs_init.ps欠損でfont embedding後処理を実行できなかった。新software installやfont差替は行っていない。必要なら次段階で修復またはROOTベクトルexport経路を選ぶ。

## 統計と範囲の制約

対称sqrt(N)とGaussian ratio errorは例示。少数counts/zero countsの精密な推論には不十分。背景variance=背景期待値と独立controlを仮定するが、背景CSVは解析式の平均でcontrol実測ではない。fitはmean=3,width=.38固定のweighted linear least squares。残差のparameter covariance補正は未実施。systematicなし（stat only明記）。任意実データの負値・log下限・bin range・sparse uncertainty・legend位置は各解析で判断する。外部投影・印刷機・ユーザー端末での最終読めるサイズは未確認。

## Skill・作業境界



この初版レポートの埋込未完了・validator未検証は歴史的記録。現在の成功検証はVECTOR_REPORT.md、COLOR_REPORT.md、ADOPTION_REPORT.mdを参照。
