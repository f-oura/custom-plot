# custom-plot

研究図の共通作図スタイルです。採用設定は **classic／線色④黒・青・朱色／密度viridis／符号付き差分0中心RdBu_r**。描画標準はPython／Matplotlibです。ROOT描画はPythonが使えない場合、または計算連携上ROOTが適切な場合の例外とします。計算backendは研究上の都合で選び、ROOTで計算した結果をPythonへ渡して描画しても構いません。

個人の作図設定で、公式STAR形式ではありません。共同研究・journal・institutionの指定は明示的overrideで優先します。他の解析repoへ導入した際も実データの範囲・units・normalization・legend・stat/systを確認してください。

## 使う

Python3.10以上とNumPy／Matplotlib。PDF/画像QAにはPillow／pypdf／Popplerも使用します。確認済みはPython3.11、NumPy2.4.6、Matplotlib3.11.0、ROOT6.32.08。ROOTとGhostscriptはPython標準の描画には不要です。依存を自動installするscriptはありません。

```python
import sys
sys.path.insert(0, "vendor/custom-plot/python")
from plotstyle import apply_selected, semantic, selected_palette

taste, geometry = apply_selected("paper")  # または "slides"
# semantic(ax, x, y, "observed", taste, errors=stat_error)
# density_cmap = selected_palette("density")
# signed_cmap = selected_palette("signed")
```

observed=black、reference=blue、model=vermilion。条件キーの順序で色を変えません。marker circle/square/triangle、線種solid/dashed/dottedも併用。4条件以上は自動で色を循環させず、条件ごとの色・線種・markerを明示してレビューします。新色を無断で採用しません。未知semantic keyはhelperでエラーになります。低水準Matplotlibの自動color cycleを採用済みmappingとして使わないでください。

真の差分に`TwoSlopeNorm(vcenter=0)`を使い、正負rangeと中心を明示。密度logではzero/negativeを黙ってclipせずmaskと件数を表示します。legend/rangeはstyleだけでは決まらず実図で判断します。

## 導入契約

```sh
git submodule add https://github.com/f-oura/custom-plot.git vendor/custom-plot
git -C vendor/custom-plot checkout <approved-commit>
```

解析repoはsubmoduleのcommitを固定します。作図skill entryは [`vendor/custom-plot/.agents/skills/research-plot/SKILL.md`](.agents/skills/research-plot/SKILL.md)。導入先には作図時にこのentryを読む薄いskillを置き、submoduleの内容を直接改変しません。canonical設定は`config/selection.json`、`config/styles.json`、`config/color_options.json`。ROOT計算からexportする場合もbin edges／units／normalization／stat/syst／covariance／underflow/overflowを保持し、Python側でerrorをsqrt(counts)へ置き換えないでください。

## 見本と実行

すべて **SYNTHETIC**。実研究dataを含みません。

- `output/selected-style.pdf`：採用済み1D/2D、paper/slidesの4ページ。
- `output/classic-color-comparison.pdf`：旧候補1/4、viridis/Blues/YlGnBuの比較。
- `output/comparison.pdf`：初期classic/clean/ink、両backendの12ページ。
- `output/root-vector-samples.pdf`：ROOTの実寸embedded vector検証4ページ。

```sh
python3 python/selected_counts.py
python3 python/selected_density.py
```

`PLOT_PYTHON`でPythonを指定して`./run.sh`は初期両backend見本、`./run-colors.sh`は色比較を再生成できます。後者のPDF埋込は`PDF_PYTHON`（pypdfを持つPython）と一致するGS binary/resourcesの指定が必要です。

```sh
python3 root/embed_vector_pdf.py --gs /path/to/gs --resource /path/to/matching/ghostscript/resources
# Macで欠損libtiff5を既存libraryで補う場合のみ --libtiff /path/to/libtiff.5.dylib
```

process限定の環境設定で、global設定を変更しません。このROOT救済経路は確認済みMacのGS10で検証済みで、任意環境で動作するとは主張しません。

## QAと制約

採用4図はPDFから実renderして目視確認済み。font embedded/subset/ToUnicode yes、外部font空renderとのpixel差0。2D見本はraster meshとvector text、ROOTのembedded比較版はpath/textを保持。ROOTのraw PDFはfont未埋込で提出用に使いません。詳細は`qa/ADOPTION_REPORT.md`、`qa/COLOR_REPORT.md`、`qa/VECTOR_REPORT.md`。初版`qa/REPORT.md`の未完了事項は後続レポートで解消しています。

日本語PDFは未作成で、ROOT日本語・未知Symbol glyphは未検証です。WinAnsiと実確認のSymbol /minusのみUnicode対応。日本語を使う場合はfont実体埋込＋ToUnicode＋license＋外部font無し実renderとpixel目視が必要です。

合成dataの対称sqrt(N)・独立Poisson ratio誤差は少数countの精密推論には不十分。fitはmean3・width0.38固定のshapeでsystematic／fit parameter covarianceを含みません。背景varianceは独立Poisson controlの期待値を仮定した例です。印刷機／projector／実研究dataの最終可読性は導入先で確認します。自動QAを目視合格の代用にしません。

font licensesは`licenses/`に同梱。採用・作図手順は[SELECTION.md](SELECTION.md)、[作図SKILL](.agents/skills/research-plot/SKILL.md)を参照。
