# 第21群：250→270作品の根拠・留意点

- Met公式Object APIで20点すべての同定・絵画種別・PDフラグを検証。公式画像JPEGを20/20実ダウンロードしSHA256・Content-Type・JPEG末尾まで検証。
- [公式検証ジョブ](https://github.com/matumaruex/kaiga-data/actions/runs/39344744217)。
- met-436065は「Attributed to Aelbert Cuyp」、met-57282は「School of Katsushika Hokusai」、met-437949は「Style of Jacob de Wit」。公式Object APIの単純化されたartistDisplayNameで作者本人の確定作品と誤表示しない。
- met-20129のAPI classificationは空欄だがobjectName Painting, medium Oil on canvasから絵画と確認。
- 無理に感情タグを付けず、仮の画面・背景解釈と作者の直接発言を区別。人間審査、公開権利の最終判定は未実施。
- 展示体験・選定プログラムには変更を加えない。

## 第12群からの保留履歴の尊重

- `met-45647`《晴川送客図》は当時『寂しさ・未練』の根拠不足で保留。今回の登録後に過去の保留履歴を再発見したため、寂しさタグを削除して主0・補助0の作品に変更した。
- 登録そのものはMet公式API・絵画分類・PD・完全JPEG SHA256の独立検証に合格。歴史的な`data/candidates-batch-012.json`は変更しない。
- 過去の保留品が意図せず登録されないよう、`scripts/validate_batch012.py`には**今回1件だけ**の証拠付き再評価条件を設ける。他の保留作品は引き続き拒否する。
