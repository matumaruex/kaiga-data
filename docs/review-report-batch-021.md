# 第21群：250→270作品の根拠・留意点

- Met公式Object APIで20点すべての同定・絵画種別・PDフラグを検証。公式画像JPEGを20/20実ダウンロードしSHA256・Content-Type・JPEG末尾まで検証。
- [公式検証ジョブ](https://github.com/matumaruex/kaiga-data/actions/runs/39344744217)。
- met-436065は「Attributed to Aelbert Cuyp」、met-57282は「School of Katsushika Hokusai」、met-437949は「Style of Jacob de Wit」。公式Object APIの単純化されたartistDisplayNameで作者本人の確定作品と誤表示しない。
- met-20129のAPI classificationは空欄だがobjectName Painting, medium Oil on canvasから絵画と確認。
- 無理に感情タグを付けず、仮の画面・背景解釈と作者の直接発言を区別。人間審査、公開権利の最終判定は未実施。
- 展示体験・選定プログラムには変更を加えない。
