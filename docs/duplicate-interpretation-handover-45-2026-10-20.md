# 専門家解釈と制作背景の同文146件・45件精査引き継ぎ（2026-10-20）

## 進捗の正本
- 作品データ正本：[`data/artworks.json`](../data/artworks.json) （作品総数300件を維持）
- **開始時の同文146件のうち最初の45件は、順番通り全件で修正・GitHub反映済み。残り101件。**
- 第1回15件のうちゴーギャン `aic-19339` とピサロ `aic-81548` は当初追加調査が必要だったが、2026-10-20にシカゴ美術館・関連学術資料を調べ直して修正済み。**保留は0件**。
- 第2回（16〜30）と第3回（31〜45）も各15件をMet公式作品ページをもとに修正済み。
- 作品の解釈だけでなく `curation.meaning_basis.creation_context`、旧表示・検索互換の `curation.interpretation`、`curation.source_context_note` を対応させて修正。**原題・作者・年代・感情タグ・画像リンクは変更しない。**
- `review.ai_content_review_status` 内訳：`needs_revision` 101件、`pending` 197件、`verified` 2件。直接出典を再検証できたAICの2件のみ `review.source_evidence_review_status=verified`。ほか298件は `pending`。
- 画像と作品の内容一致は全300件 `review.image_subject_match_status=pending` のまま。**文章の同文解消を美術史的な完全承認・公開権利判定と混同しない。**

## 第1回の再調査に利用した主な出典
- `aic-19339` ゴーギャン《Arlésiennes (Mistral)》：[AIC学術カタログ](https://publications.artic.edu/gauguin/reader/gauguinart/section/140235)、[AIC提供のGoogle Arts & Culture解説](https://artsandculture.google.com/asset/arl%C3%A9siennes-mistral-0108/igHNVuS1eNsxdw)、[ゴッホ美術館の研究](https://catalogues.vangoghmuseum.com/contemporaries-of-van-gogh-1/introductory-essay)。
- `aic-81548` ピサロ《Young Peasant Having Her Coffee》：[AIC学術カタログ（準備素描と油彩の比較）](https://publications.artic.edu/pissarro/api/epub/7/20/print_view)、[AIC館長序文](https://publications.artic.edu/pissarro/reader/paintingsandpaper/section/1069)。

## 完了した45作品（初期146件からの固定順序）
| 当初順番 | 作品ID | 作品 | 精査群 | 状態 |
|---:|---|---|---|---|
| 1 | aic-11312 | [Woman Mending](https://www.artic.edu/artworks/11312) | 第1回 | 修正済み |
| 2 | aic-14598 | [The Beach at Sainte-Adresse](https://www.artic.edu/artworks/14598) | 第1回 | 修正済み |
| 3 | aic-16549 | [Apples and Grapes](https://www.artic.edu/artworks/16549) | 第1回 | 修正済み |
| 4 | aic-16554 | [The Artist's House at Argenteuil](https://www.artic.edu/artworks/16554) | 第1回 | 修正済み |
| 5 | aic-16571 | [Arrival of the Normandy Train, Gare Saint-Lazare](https://www.artic.edu/artworks/16571) | 第1回 | 修正済み |
| 6 | aic-19339 | [Arlésiennes (Mistral)](https://www.artic.edu/artworks/19339) | 第1回 | 修正済み |
| 7 | aic-27949 | [Madame Roulin Rocking the Cradle (La berceuse)](https://www.artic.edu/artworks/27949) | 第1回 | 修正済み |
| 8 | aic-81539 | [On the Bank of the Seine, Bennecourt](https://www.artic.edu/artworks/81539) | 第1回 | 修正済み |
| 9 | aic-81548 | [Young Peasant Having Her Coffee](https://www.artic.edu/artworks/81548) | 第1回 | 修正済み |
| 10 | aic-81551 | [The Place du Havre, Paris](https://www.artic.edu/artworks/81551) | 第1回 | 修正済み |
| 11 | aic-81552 | [Woman and Child at the Well](https://www.artic.edu/artworks/81552) | 第1回 | 修正済み |
| 12 | met-39543 | [Palace banquet](https://www.metmuseum.org/art/collection/search/39543) | 第1回 | 修正済み |
| 13 | met-45417 | [Death of the Historical Buddha (Nehan-zu)](https://www.metmuseum.org/art/collection/search/45417) | 第1回 | 修正済み |
| 14 | met-44841 | [Death of the Historical Buddha (Nehan-zu)](https://www.metmuseum.org/art/collection/search/44841) | 第1回 | 修正済み |
| 15 | met-45595 | [Descent of Eleven-Headed Kannon](https://www.metmuseum.org/art/collection/search/45595) | 第1回 | 修正済み |
| 16 | met-45524 | [White-Robed Kannon](https://www.metmuseum.org/art/collection/search/45524) | 第2回 | 修正済み |
| 17 | met-670929 | [Hanshan and Shide (Japanese: Kanzan and Jittoku)](https://www.metmuseum.org/art/collection/search/670929) | 第2回 | 修正済み |
| 18 | met-11140 | [Snap the Whip](https://www.metmuseum.org/art/collection/search/11140) | 第2回 | 修正済み |
| 19 | met-44984 | [Descent of Eleven-Headed Kannon](https://www.metmuseum.org/art/collection/search/44984) | 第2回 | 修正済み |
| 20 | met-829407 | [High Mountains, Flowing Water: Yu Boya and Zhong Ziqi](https://www.metmuseum.org/art/collection/search/829407) | 第2回 | 修正済み |
| 21 | met-438545 | [Léon Pallière (1787–1820) in His Room at the Villa Medici, Rome](https://www.metmuseum.org/art/collection/search/438545) | 第2回 | 修正済み |
| 22 | met-437887 | [Bertel Thorvaldsen (1768–1844) with the Bust of Horace Vernet](https://www.metmuseum.org/art/collection/search/437887) | 第2回 | 修正済み |
| 23 | met-436329 | [Gathering Olives at Tivoli](https://www.metmuseum.org/art/collection/search/436329) | 第2回 | 修正済み |
| 24 | met-73188 | [Rainy Landscape](https://www.metmuseum.org/art/collection/search/73188) | 第2回 | 修正済み |
| 25 | met-40451 | [Rainy Landscape with Travelers](https://www.metmuseum.org/art/collection/search/40451) | 第2回 | 修正済み |
| 26 | met-40432 | [Scholar in a Lakeside Pavilion](https://www.metmuseum.org/art/collection/search/40432) | 第2回 | 修正済み |
| 27 | met-74448 | [Gathering of government officials](https://www.metmuseum.org/art/collection/search/74448) | 第2回 | 修正済み |
| 28 | met-35968 | [Forts Zeelandia and Provintia and the City of Tainan](https://www.metmuseum.org/art/collection/search/35968) | 第2回 | 修正済み |
| 29 | met-435997 | [The Storm](https://www.metmuseum.org/art/collection/search/435997) | 第2回 | 修正済み |
| 30 | met-436453 | [Esther before Ahasuerus](https://www.metmuseum.org/art/collection/search/436453) | 第2回 | 修正済み |
| 31 | met-435844 | [The Musicians](https://www.metmuseum.org/art/collection/search/435844) | 第3回 | 修正済み |
| 32 | met-437881 | [Young Woman with a Water Pitcher](https://www.metmuseum.org/art/collection/search/437881) | 第3回 | 修正済み |
| 33 | met-437394 | [Aristotle with a Bust of Homer](https://www.metmuseum.org/art/collection/search/437394) | 第3回 | 修正済み |
| 34 | met-437878 | [A Maid Asleep](https://www.metmuseum.org/art/collection/search/437878) | 第3回 | 修正済み |
| 35 | met-436576 | [The Vision of Saint John](https://www.metmuseum.org/art/collection/search/436576) | 第3回 | 修正済み |
| 36 | met-436947 | [Boating](https://www.metmuseum.org/art/collection/search/436947) | 第3回 | 修正済み |
| 37 | met-436839 | [The Penitent Magdalen](https://www.metmuseum.org/art/collection/search/436839) | 第3回 | 修正済み |
| 38 | met-11417 | [Washington Crossing the Delaware](https://www.metmuseum.org/art/collection/search/11417) | 第3回 | 修正済み |
| 39 | met-436535 | [Wheat Field with Cypresses](https://www.metmuseum.org/art/collection/search/436535) | 第3回 | 修正済み |
| 40 | met-437588 | [Drawing the Eel](https://www.metmuseum.org/art/collection/search/437588) | 第3回 | 修正済み |
| 41 | met-436005 | [The Calm Sea](https://www.metmuseum.org/art/collection/search/436005) | 第3回 | 修正済み |
| 42 | met-437549 | [Wheat Fields](https://www.metmuseum.org/art/collection/search/437549) | 第3回 | 修正済み |
| 43 | met-435739 | [The Toilette of Venus](https://www.metmuseum.org/art/collection/search/435739) | 第3回 | 修正済み |
| 44 | met-436622 | [Merrymakers at Shrovetide](https://www.metmuseum.org/art/collection/search/436622) | 第3回 | 修正済み |
| 45 | met-435888 | [Soap Bubbles](https://www.metmuseum.org/art/collection/search/435888) | 第3回 | 修正済み |

## 次のチャットで着手する46〜60件目（第4回）
| 順番 | 作品ID | 作品 |
|---:|---|---|
| 46 | met-436579 | [Broken Eggs](https://www.metmuseum.org/art/collection/search/436579) |
| 47 | met-436678 | [The Visit](https://www.metmuseum.org/art/collection/search/436678) |
| 48 | met-438817 | [The Dance Class](https://www.metmuseum.org/art/collection/search/438817) |
| 49 | met-436838 | [The Fortune-Teller](https://www.metmuseum.org/art/collection/search/436838) |
| 50 | met-437329 | [The Abduction of the Sabine Women](https://www.metmuseum.org/art/collection/search/437329) |
| 51 | met-438779 | [A Peasant Family](https://www.metmuseum.org/art/collection/search/438779) |
| 52 | met-438629 | [First Steps](https://www.metmuseum.org/art/collection/search/438629) |
| 53 | met-437990 | [Seated Peasant](https://www.metmuseum.org/art/collection/search/437990) |
| 54 | met-437842 | [Teasing a Sleeping Girl](https://www.metmuseum.org/art/collection/search/437842) |
| 55 | met-437439 | [A Young Girl with Daisies](https://www.metmuseum.org/art/collection/search/437439) |
| 56 | met-436952 | [The Funeral](https://www.metmuseum.org/art/collection/search/436952) |
| 57 | met-436449 | [The Siesta](https://www.metmuseum.org/art/collection/search/436449) |
| 58 | met-459016 | [The Annunciation](https://www.metmuseum.org/art/collection/search/459016) |
| 59 | met-437490 | [The Annunciation](https://www.metmuseum.org/art/collection/search/437490) |
| 60 | met-436791 | [The Annunciation](https://www.metmuseum.org/art/collection/search/436791) |

## 変更・検査の原則
1. 15件単位で**作品固有の一次出典・美術館の学術解説を再確認**し、専門家の解釈と制作背景を別々に書く。修辞的な言い換えで埋めない。
2. 出典の読みが不確かな場合は `pending` や `needs_revision` を維持し、作者の感情・心理を推測して書かない。
3. 最新のGitHubの `main` を読み直して対象を同定する。最初の45件を飛ばし、開始時の46〜60件を参照する（修正後の同文検索の先頭と混同しない）。
4. GitHubへの反映後は GitHub Actions の `museum-data/validate-format` コミットステータスを取得して合否を確認する。
5. **45件処理完了時点でチャットを切り替える**というユーザー指定に従い、次は第4回（46〜60件目）から。

## 更新時の注意
この文書の45件と101件は2026-10-20時点のスナップショット。進捗は必ずGitHub最新版の `data/artworks.json` から数え直す。
