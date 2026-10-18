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
3. `python3 scripts/enrich_candidates.py --write`：合格したものを**審査用の別ファイル**に保存（本登録は変更しない）
4. 画像URLをブラウザで表示確認し、出典・解釈を人間がレビュー
5. 承認できた作品だけを本登録し、GitHubへコミット

今回は **GitHubへの候補登録まで** を実施。ネットワーク未検証の作品を確定扱いしない。


## 追加調査（2026-10-18）

### 作品画像IDと権利情報をさらに照合
公式APIへの直接アクセスがこの環境からできなかったため、第三者が保存した**過去のシカゴ美術館APIレスポンス2組**を照合した。

- [過去APIレスポンス複製A](https://github.com/monocle/musee/blob/main/backend/src/artworks_response_1.json)
- [過去APIレスポンス複製B](https://github.com/max881230/mp2/blob/main/public/data/paintings.json)

調査結果：
- 15作品すべて、2つの複製で「Painting」「is_public_domain=true」が一致
- **13作品**：画像IDまで一致。画像URLの候補を生成して候補データに保存
- **2作品**：画像IDに相違があり、混同の可能性があるため保留
  - Mary Cassatt `aic-111442` The Child's Bath
  - Vincent van Gogh `aic-80607` Self-Portrait

**重要：** この突合は過去のAPIコピー同士の照合であり、現在の公式APIが返す画像IDや公開状態の確認ではない。URLは未疎通確認。ゆえにすべて `candidate_unverified` のまま本登録は保留。

### 感情解釈の再チェック

**ロセッティ『Beata Beatrix』（16551）**
- [シカゴ美術館所蔵版の公式解説](https://archive.artic.edu/apostlesbeauty/artwork/16551)が、死んだベアトリーチェと画家の亡妻への個人的な思いを説明。喪失・未練との結び付けは強い。
- ロンドンのテート所蔵初版とシカゴ所蔵の複製版を混同しない。

**ホーマー『The Herring Net』（25865）**
- [シカゴ美術館公式解説](https://archive.artic.edu/homer_exhb/artwork/25865)で、2人の漁師の協働・海の危険・生き抜く努力を確認。不安だけではなく、協力や耐える力を読むことができる。

**ルノワール『Two Sisters』（14655）**
- [美術館の学術カタログ](https://publications.artic.edu/renoir/api/epub/135446/135639/print_view)によると2人は実際の姉妹ではなく、温かい交流を明確に描いた作品とも言えない。
- もともとの「2人の親密さ、喜び」の解釈を弱め、**人物間の距離**を主題に追加した。

**ロートレック『At the Moulin Rouge』（61128）**
- [美術館展覧会の公式解説](https://archive.artic.edu/toulouse_lautrec/themes.html)が、歪んだ遠近・きつい色調・疎外的な社交関係を説明。**群衆の中の孤独**を2から3に変更。

**カサット『The Child's Bath』（111442）**
- [美術館が提供したGoogle Arts & Culture上の作品解説](https://artsandculture.google.com/asset/the-child-s-bath/FQGpjnFFEcrMyw?hl=en-GB)で、子を世話する人物と子どもの親密な場面を確認。
- しかし人物が実際の母と子と断定できるわけではないため、家族関係の事実を作らない。

**ユディト（4575）**
- 題材に斬首が含まれるため、将来の展示アプリ向けに「暴力的題材」の注意タグを追加。実画像の描写については未確認。

### 自動チェック
- `scripts/validate_candidates.py` に過去APIスナップショット2件の一致検査、画像IDの不一致検出、未検証状態のチェックを追加。
- `scripts/enrich_candidates.py` は美術館APIの推奨アクセス間隔を考慮し、1作品ごとに1.1秒の待ち時間を設定。
- [GitHub Actionsの確認ワークフロー](../.github/workflows/check-artworks.yml)を追加。実行時に静的チェックと公式APIへの照合（dry-run）を行う。**実際のワークフロー成功は未確認**。

### 次の優先事項
1. GitHub Actionsで現在の美術館公式APIを照合できるか確認。
2. 画像ID不一致の2作品は**現在の公式API値**を使って解決。
3. IIIF画像を実際に表示して内容・比率・暴力表現などを確認。
4. 良好な作品のみ人間のチェックを経て本登録する。
