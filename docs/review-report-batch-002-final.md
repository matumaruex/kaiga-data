# 第2群15作品の再レビューと試験用本登録（2026-10-18）

## 今回の確定結果

- **14作品を `data/artworks.json` に試験用・暫定キュレーションとして登録**。従来の4作品と合わせて計18作品。
- **1作品（`aic-4575` ユディト）はセンシティブな描写のため自動展示候補に追加せず保留**。
- 本登録18作品の表示用URLはシカゴ美術館IIIF（403）から、外部で再配信可能なCommons由来の画像／コミット固定の公開ミラーへ変更。公式の画像IDは`image.image_id`、参照用URLは`image.iiif_reference_url`として残した。
- 24画像のHTTP取得／JPEG検査に成功、既存アプリ16画像は既知のSHA256と一致。追加8作品は取得時のSHA256を台帳で管理。[画像検証の成功記録](https://github.com/matumaruex/kaiga-data/actions/runs/39104528012)
- **作品選定用の解釈と事実説明を区別し、誤解されやすい感情タグを下方修正**。AIには短い検索用要約／具体的状況／注意を渡す形式。
- 形式検証はGitHub Actionsで確認。ただし、これは**人間による最終レビューの代わりにはならない**。すべて `review.interpretation_human_approved=false` とし、`review.curatorial_review_status=provisional` のまま。

## 15作品の判断

| ID | 作品 | 扱い | 主な見直し |
|---|---|---|---|
| 16551 | Beata Beatrix | 暫定登録 | シカゴ版はロンドンの先行作と別版。下部の小画面（天国での再会）も評価。喪失と再会を両方扱う |
| 25865 | The Herring Net | 暫定登録 | 波のある海で2人の漁師が協働。希望を一方的に押しつけない |
| 111442 | The Child's Bath | 暫定登録 | 子どもの足を洗う行為と日本版画の構図。描かれた2人が実際の親子と断定しない |
| 14655 | Two Sisters (On the Terrace) | 暫定登録 | モデルは姉妹ではない。『一緒にいるのに孤独』の憶測を外し、色彩・余暇・穏やかさを重視 |
| 11723 | Woman at Her Toilette | 暫定登録 | 私的な身支度の場面であって、苦痛としての孤独とは限らない。『孤独』タグを削除 |
| 14591 | Woman Reading | 暫定登録 | **室内の読書ではなくカフェ風の場面**。身なりと飲み物にも着目。『孤独』を削除・『安心』を弱めた |
| 61128 | At the Moulin Rouge | 暫定登録 | にぎわいの中の疎外感に強い関連。単純に「楽しい夜」と決めつけない |
| 111436 | The Basket of Apples | 暫定登録 | 単なる安心できる静物ではなく、不安定な視点と構図を重視。『好奇心』を強めた |
| 4575 | Judith | **自動展示から保留** | ユディトが示す切断された敵将の頭と身体の露出。怒りへの無条件の自動推薦を避ける |
| 16327 | The Annunciation | 暫定登録 | キリスト教の受胎告知と元の祭壇画の文脈を維持。普通の『嬉しい知らせ』との関連を弱めた |
| 64729 | Early Morning, Tarpon Springs | 暫定登録 | 木々・小さな建物・人影のある朝。『朝＝希望』という飛躍を弱めた |
| 80607 | Self-Portrait | 暫定登録 | 自画像は自己像の表現研究。『孤独』『不安』を強く断定せず弱めた |
| 869 | The Watermill with the Great Red Roof | 暫定登録 | 田園の水車・水辺の落ち着きを中心に。『故郷』は鑑賞者の連想なので弱めた |
| 4758 | Stoke-by-Nayland | 暫定登録 | サフォークの教会と自然、習作性を加筆。メトロポリタン美術館の同名別作品とは混同しない |
| 4796 | Fishing Boats with Hucksters Bargaining for Fish | 暫定登録 | 帆船・波・光の海景を重視。売買だけで対人交渉の不安と断定しない。『希望』タグを削除 |

## 確認資料（抜粋）

- ロセッティ・所蔵版と下部パネル：[シカゴ美術館](https://archive.artic.edu/apostlesbeauty/artwork/16551)
- ホーマー・漁師の2人の協力：[シカゴ美術館](https://archive.artic.edu/homer_exhb/artwork/25865)
- カサット・子どものケアと日本版画：[シカゴ美術館ショップ解説](https://shop.artic.edu/collections/post-impressionism/products/292372)
- ルノワール・画家のモデルとタイトルの由来：[シカゴ美術館学術カタログ](https://publications.artic.edu/renoir/api/epub/135446/135639/print_view)
- モリゾ・身支度と女性の私的空間：[オルセー美術館研究展示](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/presentation/berthe-morisot-1841-1895)
- マネ・読み物と飲み物、カフェ風の場面：[ゲティ美術館学芸員解説](https://www.getty.edu/art/mobile/center/manet/stop.php?id=370075)
- ロートレック・社交の疎外：[シカゴ美術館](https://archive.artic.edu/toulouse_lautrec/themes.html)
- セザンヌ・構図：[シカゴ美術館](https://archive.artic.edu/cezannetopicasso/works.html)
- ユディト・原画所蔵番号とCC0：[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Jan_Sanders_van_Hemessen_-_Judith_-_1956.1109_-_Art_Institute_of_Chicago.jpg)
- ジャン・エイ・元祭壇画との関係：[シカゴ美術館](https://archive.artic.edu/kings-queens/artwork/16327)
- イネス・所在地と景観：[スミソニアン](https://www.si.edu/object/early-morning-tarpon-springs-painting%3Asiris_ari_254879)
- ゴッホ・1887年の自画像：[シカゴ美術館](https://www.artic.edu/artworks/80607)
- ホッベマ・赤い水車小屋：[シカゴ美術館](https://www.artic.edu/artworks/869)
- コンスタブル・サフォークの風景：[シカゴ美術館](https://www.artic.edu/artworks/4758/stoke-by-nayland)
- ターナー・魚を売る船と海景：[Commonsの個別所蔵版](https://commons.wikimedia.org/wiki/File:Joseph_Mallord_William_Turner_-_Fishing_Boats_with_Hucksters_Bargaining_for_Fish_-_1922.4472_-_Art_Institute_of_Chicago.jpg)

## 現段階の未了項目

1. AIは作品の概要と代表画像、外部研究資料を調査したが、**全JPEGファイルを個別に人間の目で実物確認したわけではない**。画像IDと所蔵番号、HTTP/JPEG/ハッシュで一致を調べている段階。
2. 権利はシカゴの公式パブリックドメイン表示とCommons個別ページで記録。再配布するアプリの公開前に、各画像ページの状態と適用法域の規定を再確認する。
3. 人間による解釈の最終承認は行っていない。AIの主観的なタグ強度は測定された心理学データではない。
4. ユディトは保存せず消すのではなく、作品候補と画像台帳に残して、**展示前に利用者による明確な選択・年齢相応の注意表示ができる仕組みが整った場合のみ再検討**する。
5. 次の作品群に進む際は同じ手順（作品事実 → 画像出典とハッシュ → 背景と具体的状況 → 自動テスト → 人間の鑑賞チェック）で増やす。

## 重要な区別

- **作品登録（今回の18件）**：データが作品IDに正しく結びついており、アプリでの試験表示・選定実験をできる状態。
- **人間の最終承認（未了）**：感情との適合、画像の細部、公開状態を人間が承認した状態。まだ登録された作品でも`review.interpretation_human_approved=false`。
- **アプリ公開（未実施）**：共有データの変更だけでは既存2アプリの展示内容は切り替わらない。
