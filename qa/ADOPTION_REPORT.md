# 採用の根拠と検証

Library添付2枚を正規materializeでMacへ取得して実際に表示した。1枚目はviridisのlinear/log density、2枚目は青→neutral→赤の0中心RdBu_r差分。画像には1Doverlayがなく、その時点では線配色1/4を保留、下記の追加回答で確定。paper/slidesも切り抜きから識別できないため両presetを維持。元画像はローカルLibraryで確認済み。個人添付画像はrepoへコピーしない。

Python/Matplotlib描画標準をconfig・README・SELECTION・AGENTS・repo SKILLへ反映。ROOT描画の例外はPython不可または計算連携都合、計算backendは強制しない。ROOT計算→Python描画を許容。既存候補・他repoは変更しない。

python/selected_density.pyを既存Matplotlib環境で実行、paper9×3.7inchとslides15×6.1inchのPDF/PNGを生成。共有JSON LUTをselected_paletteから使用。同一synthetic CSV、linear0–60/log1–60（261zeroをgray）、差分−30…+30を0中心。両PDFをPoppler100dpiでrenderして全panelを実目視、tick/label/title/colorbarの重なりや切れなし。pdffontsはDejaVuSerif埋込・subset・ToUnicodeすべてyes、font空環境renderとのpixel差0。密度画像はimshowのraster mesh＋vector textとして保存し、全vectorとは呼ばない。公式skill validator PASS。

追加のユーザー回答「それは4かな」により1D線色④を採用。observed black / reference blue / model vermilion、3色のみ。4条件以上は自動色循環をせずexplicit semantic mappingを要求。未検証：実研究dataでのranges/legend、印刷機/projector、会場の可読性。これはSYNTHETIC見本で、誤差・相関・sparse statisticsの研究結論には使わない。

採用1D見本python/selected_counts.pyも実行。paper6.8×5.2inch、slides10×7.6inch。同一CSVの列schema x/observed/reference/background/modelを照合。option4 semantic mapping exact black#222222 / blue#0072B2 / vermilion#D55E00をassert。ratioはobserved/referenceで独立Poisson誤差。両PDFを100dpi実render目視しlegend/peakの重なり、文字切れなし。font embedded/subset/Unicode yes、外部font空render差0。合本selected-style.pdfは1Dpaper→2Dpaper→1Dslides→2Dslidesの4ページ。
