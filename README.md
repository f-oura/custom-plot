# custom-plot

研究用の図を、毎回同じ色・文字サイズ・線幅で作るための作図設定集です。PythonのMatplotlibで使える設定と補助関数、ROOTでの作図例、見本のPDF・PNG、図を作るAI向けの確認手順をまとめています。

標準の描画には **Python／Matplotlib** を使います。ROOTで計算した結果をPythonへ渡して描画する使い方もできます。Pythonが使えない場合や、計算との連携上ROOTで描く方が適切な場合には、ROOTで描画します。

共同研究や投稿先が指定する書式がある場合は、そちらを優先してください。このリポジトリは個人用の作図設定で、STARなどの共同研究が定める公式書式ではありません。

## 標準の見た目

白い背景、セリフ体の文字、グリッドなしのレイアウトを使います。色は表示する役割に固定し、データを渡す順番で変えません。

| 表示するもの | 色・配色 | 補助関数に渡す名前 |
|---|---|---|
| 観測値・主となるデータ | 黒 `#222222` | `observed` |
| 比較対象のデータ | 青 `#0072B2` | `reference` |
| モデル・予測曲線 | 朱色 `#D55E00` | `model` |
| 2次元の密度・件数 | viridis：低い値が紫、高い値が黄 | `density` |
| 正負のある差分 | RdBu_r：負が青、0付近が白、正が赤 | `signed` |

系列は色だけでなく、実線・破線・点線、誤差棒がある場合は丸・四角などでも区別します。4条件以上を表示する場合は、色を自動で繰り返さず、各条件の色・線種・マーカーを明示して決めます。

[標準設定の見本PDF](output/selected-style.pdf)には、1次元の重ね描きと比、2次元の密度と差分を、論文用・スライド用の両方で収録しています。見本とCSVはすべて**合成データ**で、実験の測定結果ではありません。

## 最初の図を作る

### 必要な環境

通常の作図にはPython 3.10以上、NumPy、Matplotlibが必要です。ROOTやGhostscriptは不要です。既存のPython環境で、次のコマンドが通ることを確認してください。

```sh
python3 -c 'import numpy, matplotlib'
```

確認済みの環境はPython 3.11、NumPy 2.4.6、Matplotlib 3.11.0です。依存ソフトを自動でインストールする処理は含めていません。複数のPython環境がある場合は、以下の`python3`を必要なライブラリが入っているPythonに置き換えてください。

### 取得して見本を動かす

```sh
git clone https://github.com/f-oura/custom-plot.git
cd custom-plot
python3 python/selected_counts.py
python3 python/selected_density.py
```

`output/`に次のファイルを生成します。各図はPDFとPNGの両方で保存されます。

- `selected-counts-paper`、`selected-counts-slides`：1次元の重ね描きと比。
- `selected-density-paper`、`selected-density-slides`：密度の線形・対数表示と、0を中心にした差分。

### 補助関数を使う最小例

以下をリポジトリの直下に`first_plot.py`として保存し、`python3 first_plot.py`で実行してください。合成CSVを読み、黒・青・朱色の図を`output/first-plot.pdf`と`output/first-plot.png`に保存します。

```python
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "python")
from plotstyle import apply_selected, semantic

style, _ = apply_selected("paper")
x, observed, reference, background, model = np.loadtxt(
    "data/counts.csv", delimiter=","
).T

fig, ax = plt.subplots(figsize=(6.8, 4.2))
semantic(ax, x, observed, "observed", style, errors=np.sqrt(observed))
semantic(ax, x, reference, "reference", style, errors=np.sqrt(reference))
semantic(ax, x, model, "model", style)
ax.set(xlabel="Mass [GeV]", ylabel="Counts / 0.2 GeV",
       xlim=(0, 8), ylim=(0, 210), title="Synthetic example")
ax.legend(loc="upper right", frameon=False)
fig.tight_layout()
Path("output").mkdir(exist_ok=True)
fig.savefig("output/first-plot.pdf")
fig.savefig("output/first-plot.png")
plt.close(fig)
```

この例の`sqrt(counts)`は合成データの統計誤差を示すための近似です。実際の解析では、求めた誤差や共分散をそのまま渡してください。既存の誤差を勝手に`sqrt(counts)`へ置き換えないでください。

## 論文用・スライド用とAPI

`apply_selected("paper")`は論文用、`apply_selected("slides")`はスライド用の文字・線幅などを設定します。基本の文字サイズはそれぞれ10 pt、15 ptです。掲載幅や投影距離に合わせて図全体の寸法を決め、縮小後も読めるか確認してください。見本の多パネル一覧を、そのまま論文の単図幅へ縮小することは想定していません。

| 関数 | 用途 |
|---|---|
| `apply_selected(preset)` | 標準設定を適用し、系列の色設定と寸法設定を返す。 |
| `semantic(ax, x, y, key, style, errors=None)` | 役割名に対応する色・線種で描く。`errors`を渡すと誤差棒を付ける。 |
| `selected_palette("density")` | 密度用のviridisを返す。 |
| `selected_palette("signed")` | 差分用のRdBu_rを返す。 |

`semantic`に渡せる役割名は上の表の3種類です。未知の名前はエラーになります。補助関数を使わずにMatplotlibで直接描く場合も、標準の自動色順をこのリポジトリの役割別の配色と混同しないでください。

差分では配色だけでなく、例えば`matplotlib.colors.TwoSlopeNorm(vmin=-30, vcenter=0, vmax=30)`で0を中心にします。上下限は実データと目的に合わせて決めます。対数表示の0・負値は黙って除外せず、マスクした範囲と件数を説明します。凡例の場所や表示範囲は図ごとに確認してください。

## 設定を変える

- [`config/selection.json`](config/selection.json)：現在使うレイアウト、配色、描画方針。
- [`config/styles.json`](config/styles.json)：文字サイズ、線幅、余白、論文用・スライド用の寸法など。
- [`config/color_options.json`](config/color_options.json)：役割別の色と、Python／ROOTで共通に使う色の数値表。

`styles.json`を変更した場合は、`python3 python/export_styles.py`でMatplotlibの`.mplstyle`とROOT用ヘッダーを再生成します。現在の設定では、系列色は`selection.json`が指定する`color_options.json`内の対応表から取得します。JSON内の数値IDや名前は設定を参照するための内部識別子です。

変更後は見本を再生成し、文字・凡例の重なり、軸やパネルからのはみ出し、色の区別、PDFのフォントを確認します。共同研究・投稿先の指定に合わせた一時的な調整は、設定適用後の`plt.rcParams.update(...)`や個々の軸の設定でも行えます。

## 解析プロジェクトへ組み込む

Gitで管理している解析プロジェクトの直下で実行します。

```sh
git submodule add https://github.com/f-oura/custom-plot.git vendor/custom-plot
```

プロジェクト側では`sys.path.insert(0, "vendor/custom-plot/python")`として補助関数を読み込みます。サブモジュールは特定のコミットに固定されるため、図を作ったときの設定を記録できます。更新時は、使うコミットを確認してからサブモジュールの参照を更新してください。

ROOTからCSVや配列を渡す場合も、ビンの境界、単位、規格化、統計誤差・系統誤差、共分散、表示範囲外の件数を保存してください。Pythonを描画の標準にすることは、計算や解析をPythonへ移し替える指示ではありません。

## 図を作るAIに確認手順を読ませる

[作図SKILL](.agents/skills/research-plot/SKILL.md)は、凡例とピークの重なり、文字の切れ、色の意味、誤差、PDFのフォントなどを確認するための指示です。このリポジトリ内では[AGENTS.md](AGENTS.md)から参照しています。

解析プロジェクトで使う場合は、プロジェクト内の`.agents/skills/custom-plot/SKILL.md`などに、次のような入口を置きます。利用するAIツールがプロジェクト内のSKILLを読むことを前提とした例です。

```markdown
---
name: custom-plot
description: 研究データの図を作成・修正・レビューするときに使う。
---

作図前に vendor/custom-plot/.agents/skills/research-plot/SKILL.md を読み、
その手順とチェックリストに従う。
```

AIツールがSKILLの自動読み込みに対応しない場合は、同じファイルを読む指示をプロジェクトの作業規則や依頼文へ入れてください。サブモジュール内のSKILLや全プロジェクト共通の設定を直接上書きする必要はありません。

## ROOTで描画する場合

ROOTの例は[`root/`](root/)にあります。ROOT 6.32.08で実行確認済みです。PythonとROOTでは文字サイズの単位や配置が異なるため、同じ設定名でも同じ見た目になるとは限りません。

```sh
./run.sh  # 初期スタイルのPython／ROOT比較を再生成
```

この比較にはNumPy・Matplotlib・Pillow・pypdf、ROOT、Popplerの`pdffonts`・`pdfinfo`・`pdftoppm`、`rg`を使います。Pythonの実行環境は`PLOT_PYTHON`で指定できます。追加の色比較は`./run-colors.sh`で生成します。色比較のPDF処理には、pypdfを使える`PDF_PYTHON`と、下記のGhostscript設定も必要です。

ROOTの未処理PDFはフォントが埋め込まれていません。提出には`*-embedded.pdf`を使います。既存のGhostscript本体と対応するリソースがある環境では、次の処理でフォントを埋め込みます。

```sh
python3 root/embed_vector_pdf.py \
  --gs /path/to/gs \
  --resource /path/to/matching/ghostscript/resources
```

`run-colors.sh`から同じ処理を呼ぶ場合は`GS_BINARY`・`GS_RESOURCE`で指定します。Macで既存のlibtiff 5を補う必要がある場合だけ、`--libtiff`または`GS_LIBTIFF5`を指定します。環境設定はその処理内に限り、全体の設定を変更しません。この経路はMacのGhostscript 10で確認済みですが、他環境での動作は未検証です。

## 検証と見本の限界

Pythonの見本を生成した後、Pillow・pypdfもある環境で次を実行すると、役割別の配色、合成データのハッシュ、PDFのフォント埋め込みと文字対応を検査できます。GitHub Actionsでも同じ検査を実行します。

```sh
python3 qa/publication_checks.py
```

標準設定の4図はPDFから描画し、全パネルを目視確認済みです。フォントは埋め込み済みで、文字コードとUnicodeの対応表（ToUnicode）もあります。外部フォントのない環境での描画との差は0でした。ただし、自動検査は目視確認の代わりにはなりません。

2次元のPython見本は画像としての密度図と、ベクトル形式の文字を組み合わせています。ROOTのフォント埋め込み版は線や文字をベクトル形式で保持しています。日本語PDFは作成しておらず、ROOTの日本語や未対応の記号は未検証です。日本語を使う場合は、フォントの利用許諾・実体の埋め込み・ToUnicode・外部フォントなしでの実描画を確認してください。

合成データの誤差棒や比は、独立Poisson分布の近似を使っています。少数カウントの精密な推論には不十分です。モデルの平均・幅は固定しており、系統誤差やフィットパラメータの共分散も含めていません。実解析の統計処理、最終的な印刷・投影での可読性は、それぞれのプロジェクトで確認してください。

詳しい記録は[標準設定の検証](qa/ADOPTION_REPORT.md)、[配色比較の検証](qa/COLOR_REPORT.md)、[ROOTのPDF検証](qa/VECTOR_REPORT.md)にあります。フォントのライセンスは[`licenses/`](licenses/)に同梱しています。過去の比較見本については[見本ガイド](SELECTION.md)を参照してください。
