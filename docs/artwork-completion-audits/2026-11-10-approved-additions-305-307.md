# 2026-11-10 承認済み305〜307作品の登録検証メモ

- 承認を受けた作品: `met-48893` 歌川広重《雪中を歩く女性》、`met-694642` William A. Harper《フランスの木々、午後の早い時間》、`met-765654` インド作者不詳《ヤムナー川岸のクリシュナと牧女たち》。
- 正式作品ID・原題・年代・作者または作者不詳・所蔵番号・作品PD表示は個々のMet公式作品ページと公開Object APIで照合した。
- 公式Open Access画像はMet公式のoriginalおよびweb-large JPEGについてバイト数・SHA256・寸法・縮小画の一致を [GitHub Actions run 42753854022](https://github.com/matumaruex/kaiga-data/actions/runs/42753854022) で検証。画像の構図と主題はMet公開画像との別工程の視覚照合を実施した。met-694642のAPI classification空欄は作品名Paintingと公式展示ページで補完、met-765654の原画URL内の空白は%20符号化して実取得した。見ていない画像バイトを見たと偽らない。
- 制作意図を独断で補わず、Met専門家の読み、制作の背景、画面からの観察、観客が持つ感情の入口を区別。主要感情は広重「孤独」強度2、ハーパー感情0件、インド作品「喜び」強度2。ナインスーク本人の制作・王室婚礼の確定を主張しない。感情タグは作者や描かれた人物の感情診断ではない。
- 絵画本体PD／Met画像CC0／現代の美術館解説文を区別し、文章は日本語で新規執筆。完全な法律上の適法性証明を行ったものとは扱わない。
- 同一AIの制作と別工程のチェックを各作品監査へ保存。独立した外部の人間や別AIの審査を行ったとは主張しない。
- `scripts/add_artwork.py preview→save→check` は3作品を順に登録するジョブ [GitHub Actions run 42754336591](https://github.com/matumaruex/kaiga-data/actions/runs/42754336591) で全作品PASS。既存304作品と元300作品スナップショットを維持し、正式DB件数を307作品へ更新した。
- 最終の「Check artwork data」「Check visitor explanation drafts」のCIが成功し、PR #220 をmainへ統合するまで完成数へ正式に算入しない。展示アプリへの反映は別工程。
