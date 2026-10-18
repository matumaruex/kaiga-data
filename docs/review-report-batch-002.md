# 追加15作品：候補一次レビュー（2026-10-18）

## 今回の実績
- シカゴ美術館が公式に提供するサンプルCSV `getting-started/someArtworks.csv` と照合し、**15作品の作品ID・原題・作者**を確認。
- 15作品の感情とのつながりを暫定的に記録し、すべてに別の読み方と注意点を記した。
- 最初の4作品が入っている `data/artworks.json` は変更していない。候補は `data/candidates-batch-002.json` に分離。
- 公式APIへの新規リクエストがこの作業環境では失敗したため、**PDフラグ・画像ID・作品分類・制作年代の照合は未完了**。
- 未確認作品がアプリに混ざらないよう、候補は `status=candidate_unverified`。自動公開・本登録しない。

## 確認先
- [シカゴ美術館公式サンプルCSV](https://github.com/art-institute-of-chicago/api-data/blob/master/getting-started/someArtworks.csv)
- [API公式ドキュメント](https://api.artic.edu/docs/)
- [ロセッティ『Beata Beatrix』公式解説](https://archive.artic.edu/apostlesbeauty/artwork/16551)
- [ホーマー『The Herring Net』公式解説](https://archive.artic.edu/homer_exhb/artwork/25865)
- [ルノワール『Two Sisters』公式研究カタログ](https://publications.artic.edu/renoir/api/epub/135446/135639/print_view)
- [マネ『Woman Reading』公式記録](https://archive.artic.edu/500ways/artwork/14591)

## 絵画候補（15）
| ID | 作品 | 仮の選定軸 |
|---|---|---|
| 16551 | Beata Beatrix | 死別、喪失、未練 |
| 25865 | The Herring Net | 不安の中の協力、踏ん張ること |
| 111442 | The Child's Bath | 親密さ、守られた記憶 |
| 14655 | Two Sisters (On the Terrace) | 一緒にいる喜び |
| 11723 | Woman at Her Toilette | 一人の時間、内省 |
| 14591 | Woman Reading | 読書と静けさ |
| 61128 | At the Moulin Rouge | 群衆の中の孤独 |
| 111436 | The Basket of Apples | 日常への集中 |
| 4575 | Judith | 怒り、葛藤、危険 |
| 16327 | The Annunciation | 思いがけない知らせ |
| 64729 | Early Morning, Tarpon Springs | 新しい朝、期待 |
| 80607 | Self-Portrait | 自己との対話 |
| 869 | The Watermill with the Great Red Roof | 故郷や居場所 |
| 4758 | Stoke-by-Nayland | 風景、郷愁 |
| 4796 | Fishing Boats with Hucksters Bargaining for Fish | 生きる営み、緊張 |

## 自己批評
- 有名な西洋絵画への偏りはまだ強い。時代・地域・作家の多様性が不足。
- 『怒り』に強く関連する作品は候補に入れたが、実際の画面の印象は未検証。
- 画像を直接見ていない作品の感情スコアは暫定的。数字の精密さを過信しない。
- 全15件が本登録条件を満たすとは限らず、公開条件で除外されることがある。
- 感情タグと作者の意図は区別し、身体・精神の状態を作品から診断しない。

## 次の作業
1. `python3 scripts/validate_candidates.py`：候補の構造・形式をチェック
2. `python3 scripts/enrich_candidates.py`：公式APIから実データを照合（dry-run）
3. `python3 scripts/enrich_candidates.py --write`：合格したものだけ本登録（手元のJSONへ追記）
4. 画像URLをブラウザで表示確認し、解釈をレビュー
5. 問題なしならGitHubへコミット

今回は **GitHubへの候補登録まで** を実施。ネットワーク未検証の作品を確定扱いしない。
