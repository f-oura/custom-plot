# ROOT vector PDF follow-up

既存Ghostscript 10.00.0の本体と一致するResourceが 既存のGhostscript installation に見つかった。default gsは9.27でresource参照が壊れていた。10の欠損libtiff.5は既存Anacondaから、temporary directory内のlinkとprocess限定DYLD_LIBRARY_PATHで参照。Anacondaのlib全体は古いlibc++を含み衝突するため使わない。global設定・binary・ライブラリは変更せず、installなし。

ROOT原PDFはそのまま保持。`root/embed_vector_pdf.py` はGS pdfwriteで標準fontのNeverEmbedリストを明示的に空にし、既存Nimbusfontをsubset埋込する。fontのembedding例外は `licenses/Ghostscript-font-embedding.txt` に記録。WinAnsiの1byte文字をCP1252からUnicodeへ正確に対応するToUnicodeを付与。追加比較で確認したSymbolの `[45 /minus]` のみU+2212へ対応。その他のSymbol、Japanese、未知Encoding Differencesは推測せず停止する。

ROOT原PDFはA4ページ・CropBox・Rotateを使うため、実寸比較に適したpage boxへ正規化。canvasの縦横比を保ち、残りは余白とする。single paper3.4×2.8inch、slides10×7inch、overlay paper6.8×5.2inch、slides10×7.6inch。style候補やdataを変更しない。

初版4つ＋追加比較2つの `*-embedded.pdf` を生成してpdffontsでembedded/subset/Unicodeの全てyesを確認。ベクトルのpath strokeとtext operationを確認、Imageオブジェクト0。現在の件数はqa/vector/results.jsonを参照。pathとtextを保持し、全raster化していない。対象語SYNTHETIC、Mass [GeV]、observed、reference、Ratioも実textとして抽出可能。4つのPDFをPopplerで実renderして全panelを目視し、peakとlegendの重なり、tickとlabelの重なり、clipがないことを確認。外部fontが空のFontconfig設定でも4図をrenderし、通常renderとのpixel差分0。

実寸で抽出した横書きfontはsingle paperのtick8.01pt、axis/title9.47pt、slidesのtick12.29pt、axis/title13.73pt。ROOT font43/133のpixel指定とPDF canvas/crop変換の結果であり、Matplotlibの10/15ptと同一ではない。見本の実pixelも確認したが、投影距離・印刷機での最終読めるサイズはユーザー確認待ち。

既存Anaconda Python3.7 + PyYAML5.1.2でskill-creatorの公式quick_validate.pyを実行し `Skill is valid!` を確認。初版で未検証だったvalidatorは解消。

実行：

```sh
python3 root/embed_vector_pdf.py --gs /path/to/gs --resource /path/to/matching/resources
```

pypdf6.10.0を使用。`--gs`、`--resource`、`--libtiff` で確認済み別環境を指定可能。この救済経路は今のMac用で、任意の新環境へそのまま動くと主張しない。raw ROOT PDFは未埋込のままなので、提出候補はembedded版を使う。

追加color比較2図もtext/path保持、画像0で埋込成功。最終合本4＋4ページを外部font空で実renderしpixel差0。詳細はqa/COLOR_REPORT.md。
