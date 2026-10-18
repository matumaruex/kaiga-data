# 第5群11作品：作者の制作意図優先の選定（2026-10-18）

## 結果
- **新11作品を試験登録**して、共有データベースは **44作品**、画像出典台帳は **45点**（保留1点を含む）。
- 11/11の作品はシカゴ美術館の現行APIから所蔵番号、作品ID、作者、制作年、絵画分類、パブリックドメイン、画像IDを照合済み。
- 11/11のCommons画像について、作品との所蔵番号の照合、JPEGの実取得とSHA256を記録。初回は6/11、別名ファイルの所蔵番号を再確認して残り5/5にも成功。
- 機械的確認と**作者の制作意図の解釈が正しいか**は別問題。人間の鑑賞・公開審査を完了したものとは扱わない。

**証拠：** [第1回公式API 11/11・画像6/11](https://github.com/matumaruex/kaiga-data/actions/runs/39113155150) ／ [追加のCommons画像5/5](https://github.com/matumaruex/kaiga-data/actions/runs/39113384202)。

## 作品ごとの判断

| AIC ID | 作品 | 制作意図の根拠 | 主タグ／補助タグ |
|---|---|---|---|
| 16549 | [Apples and Grapes](https://www.artic.edu/artworks/16549) | 本人の当該作品への言葉は未確認 | 好奇心／喪失感 |
| 81539 | [On the Bank of the Seine, Bennecourt](https://www.artic.edu/artworks/81539) | 本人の当該作品への言葉は未確認 | 好奇心／不安 |
| 16554 | [The Artist's House at Argenteuil](https://www.artic.edu/artworks/16554) | 本人の当該作品への言葉は未確認 | 安心／喜び |
| 14598 | [The Beach at Sainte-Adresse](https://www.artic.edu/artworks/14598) | 本人の当該作品への言葉は未確認 | 好奇心／懐かしさ |
| 16571 | [Arrival of the Normandy Train, Gare Saint-Lazare](https://www.artic.edu/artworks/16571) | 本人の当該作品への言葉は未確認 | 好奇心／期待 |
| 81548 | [Young Peasant Having Her Coffee](https://www.artic.edu/artworks/81548) | 本人が個別作品に言及 | 安心／好奇心 |
| 81552 | [Woman and Child at the Well](https://www.artic.edu/artworks/81552) | 本人の当該作品への言葉は未確認 | 好奇心／安心 |
| 81551 | [The Place du Havre, Paris](https://www.artic.edu/artworks/81551) | 本人が個別作品に言及 | 好奇心／期待 |
| 11312 | [Woman Mending](https://www.artic.edu/artworks/11312) | 本人が個別作品に言及 | 好奇心／安心 |
| 27949 | [Madame Roulin Rocking the Cradle (La berceuse)](https://www.artic.edu/artworks/27949) | 本人の連作・同題への発言 | 安心、懐かしさ／希望 |
| 19339 | [Arlésiennes (Mistral)](https://www.artic.edu/artworks/19339) | 本人の当該作品への言葉は未確認 | 好奇心／不安 |

## 制作意図を確認できた重要な例
- **ピサロ『繕い物をする女性』（aic-11312）**：1895年12月4日の息子ルシアン宛て書簡に作品題名が現れ、人物表現の完成度への手応えを本人が説明。これはモデル自身が安らいでいた証拠ではない。[シカゴ美術館学術研究](https://publications.artic.edu/pissarro/api/epub/7/27/print_view)
- **ピサロ『パリ、アーヴル広場』（aic-81551）**：1893年の制作計画とこの作品への言及が書簡に残る。賑わう都市に作者が孤独を感じたという意味ではない。[シカゴ美術館研究](https://publications.artic.edu/pissarro/reader/paintingsandpaper/section/25)
- **ピサロ『コーヒーを飲む若い農婦』（aic-81548）**：本人はこの絵の丁寧な制作・完成を評価した。農婦の生活が幸福だったと決めつけない。[シカゴ美術館](https://publications.artic.edu/pissarro/reader/paintingsandpaper/section/1069)
- **ゴッホ『ラ・ベルスーズ』（aic-27949）**：子守歌を色彩で実現しようとする制作方針を手紙に残した。ただし複数の版を描いており、ここでは同題の作品群への発言として記録。[本人の手紙](https://vangoghletters.org/vg/letters/let745/letter.html)
- **モネ『リンゴとブドウ』（aic-16549）**：妻の死と収入・家族の変化は制作背景に関係する。ただし果物そのものが悲しみを象徴するという根拠ではない。[シカゴ美術館学術研究](https://publications.artic.edu/monet/api/epub/135466/135552/print_view)

## 画像の別名を確認した5作品

作品名や所蔵番号が画像ファイル名に書かれていない場合があるため、**Wikimedia Commonsのファイルページにある「所蔵番号」まで照合**した。

- 1933.1158 モネ・サン＝ラザール駅：[Google Art Project版](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Arrival_of_the_Normandy_Train,_Gare_Saint-Lazare_-_Google_Art_Project.jpg)
- 1922.433 ピサロ・コーヒーを飲む農婦：[ファイルページ](https://commons.wikimedia.org/wiki/File:Young_Peasant_Having_Her_Coffee.jpg)
- 1922.436 ピサロ・井戸端の女性と子ども：[ファイルページ](https://commons.wikimedia.org/wiki/File:Young-woman-and-child-at-the-well-1882.jpg)
- 1922.434 ピサロ・アーヴル広場：[ファイルページ](https://commons.wikimedia.org/wiki/File:Camille_Pissarro_-_Place_du_Havre,_Paris_-_Art_Institute_of_Chicago.jpg)
- 1959.636 ピサロ・繕い物をする女性：[ファイルページ](https://commons.wikimedia.org/wiki/File:Kvinde_der_lapper.jpg)

## 未了
- 個別の全画像の人による最終目視・表現の多義性の検討・アプリへの同梱時の権利判断は別。
- 本人の発言がない残りの作品には「制作意図を直接確認できない」を記録。**専門家の読解はあくまで研究者のもの**。
- モネが多くなっているため、次の群では時代と画家の多様性、弱い感情カテゴリー（怒り・喜び・期待・未練など）に根拠ある作品を探す。ただし不足タグを補うために強引な連想は付けない。
- **展示体験は約100作品になってから**。
