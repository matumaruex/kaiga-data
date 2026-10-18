# 公式作品情報と画像配信の検証（2026-10-18）

## 結果と区別
| 対象 | 現行公式作品APIの照合 | 公式画像配信のJPEG HTTP取得 | 絵の内容を視認 | 展示に昇格 |
|---|---:|---:|---|---|
| 既存の本登録4点 | 4/4 | 0/4（HTTP 403） | 未確認 | 今回は変更せず、公開前に再確認 |
| 追加候補15点 | 15/15 | 0/15（HTTP 403） | 未確認 | **未昇格・候補のまま** |
| **合計** | **19/19** | **0/19** | **未確認** | **15件は候補** |

- 検証実行：[GitHub Actions / 2026-10-18](https://github.com/matumaruex/kaiga-data/actions/runs/39097828166)
- 作品API：`https://api.artic.edu/api/v1/artworks/{id}`
- IIIF画像：`https://www.artic.edu/iiif/2/{image_id}/full/400,/0/default.jpg` をテスト（画面表示用URLは843幅）
- 公式APIの作品ID、名称、作者、Painting分類、PDフラグ、画像ID、年代表示は一致・有効と確認。
- 画像は19点すべてHTTP 403となり、JPEGを取得できなかった。**画像が存在しないと確認されたわけではない**。
- 現行APIで画像IDが確定したため、過去の複製間で一致しなかった2点は現在の公式画像IDを候補JSONに記録した。
- 作品の背景や感情への適合の最終審査、実際の画面表示、画像権利の総合判断は未了。

## 原因についての外部報告

美術館自身のGitHubリポジトリで、`www.artic.edu` のIIIF画像がCloudflareの認証チャレンジにより非ブラウザアクセスからHTTP 403となる問題が2026年6月以降報告されている。

- https://github.com/art-institute-of-chicago/api-data/issues/9
- https://github.com/art-institute-of-chicago/data-aggregator/issues/151

API取得成功と画像配信成功は別。画像を必要とするWebアプリで、シカゴ美術館のIIIFを無検証で直接読み込む構成は採用しない。
取得制限を技術的に回避するのではなく、正当に公開配信されている別の画像ソースを検証する。

## 代替画像ホストの小規模確認

[GitHub Actions / 画像ホストを確認](https://github.com/matumaruex/kaiga-data/actions/runs/39097983295)

- **Cleveland Museum of Art**：公式ドキュメントにあるCC0画像1点をGitHub Actions上から取得しHTTP 200/JPEGと確認。
- **Metropolitan Museum of Art**：サンプル画像URL1件がHTTP 404。URLが古い・変更された可能性があり、美術館全体が使えないとは結論しない。
- 1点のHTTP成功だけでは、すべての画像の利用可能性、長期安定性は保証されない。

## 次の意思決定

1. **画像配信が実際に使える公式美術館を基本の作品追加先に選ぶ**。現状、Cleveland Museum of Artが有力。
2. 現在のAICの19点は削除せず、別の正当な画像ソースが確認できた作品だけ展示候補として検討。絵の版・所蔵館を取り違えないこと。
3. 以後、作品を10〜20点調査 → 公式作品情報・権利と画像実取得を確認 → タグや解説を見直す → 自動テスト → 次の作品群へ。
4. **AI選定プログラム・有料APIの導入は今はしない**。作品情報と選定方式を切り離す。

## 自動テストの区別

- 通常のデータ更新：形式・必須項目・重複を自動で確認。
- 手動`workflow_dispatch`、またはコミットメッセージに`[verify-live]`を付けたとき：公式APIとIIIF画像配信をオンライン確認。HTTP 403などであれば**失敗**と記録。結果JSONはActionsのArtifactに14日保存。
- 検証の最終合格は、画像実取得・人による表示確認・作品背景や感情解釈のレビューを伴う。
