# 300作品の基礎資料・将来の鑑賞者向け解説への準備状況：全件一次監査（2026-10-20）

> **これは一次監査（全300レコードの機械的・文章上の点検＋5作品の公式ページ標本照合）であり、300件の内容・美術史・画像真正性を原資料と全件照合した最終監査ではない。** 作品データは変更していない。別チャットで同文の修正が継続しうるため、ここに記した数値は**以下のGit blob SHA時点の固定スナップショット**。新しい進捗には再計算が必要。

- 作品の正本：`data/artworks.json` blob `4dee6db08d5cda6b24fb57efe1b2478612184862`
- 画像台帳：`data/image-sources.json` blob `ef9803129b09c61e1ebafeb3faf67204759a27d9`
- 調査対象：登録作品全300件。画像台帳301件（うち登録外は保留中の `aic-4575`《Judith》）。
- 方針：[`data-policy.md`](data-policy.md#鑑賞者向け解説の制作準備2026-10-20追加)・[`review-guide.md`](review-guide.md)。
- データ変更は行わず、修正作業中の別チャットと競合しない。未確認内容を `verified` にしない。

## 監査結果の概要

| 横断項目 | 件数・結果 | 意味 |
|---|---:|---|
| 登録作品 | 300 | シカゴ51件・Met249件 |
| 専門家解釈と制作背景の**完全同文** | **86** | 役割分離を要する強い修正候補。別チャットで修正中 |
| 解釈＋制作背景＋視覚ヒントが合計**100字未満** | **63** | 鑑賞者向け文章の根拠が薄い可能性がある。短さだけで誤り・不合格とは断定しない |
| 上記2条件のいずれか（重複除外） | **93** | 優先的に個別精査する候補。うち両条件に該当 56 件 |
| 上記2条件に該当しない | 207 | 合格・内容確認済みとは意味しない |
| 原資料との内容照合：`verified` | **2** | 原資料の記述とDB主張の実照合を登録している件数 |
| 原資料との内容照合：`pending` | **298** | 確定した間違いの件数ではなく、検証記録が不足 |
| 実画像と絵の内容同定：`pending` | **300** | 過去の画像SHA成功とは別の点検 |
| 作品IDと画像台帳・画像ハッシュの内部突合 | **0件の不整合** | 今回のデータ内対応のみを検査。画像の美術史的同定は保証しない |
| 感情タグ0件 | 88 | 仕様どおり許容、欠陥ではない |

**文字数は不十分さを推定する警告指標にすぎない。** 長文でも誤りがありうるし、短くても出典・具体性が優れている作品はある。作品ごとの作成可否判定には、出典本文の照合と意味の質の判断が必要。

### 出典URLの内訳（存在・形だけの点検）
- Met公式作品ページ：249件
- AIC学術出版：20件
- AIC作品・関連ページ：24件
- その他：7件

同じ公式作品ページでも、研究的な長文が掲載されている場合と、ほぼメタデータだけの場合がある。**「公式URLあり＝解説の出典照合済み」ではない**。

## 公式の作品ページを実際に開いた個別の標本照合（5作品）

1. **`met-670896`《Plum Blossoms》** — DBの解釈・制作背景はどちらも「室町時代の禅僧が描く梅の水墨画。」の同文（各16字）。[Met公式ページ](https://www.metmuseum.org/art/collection/search/670896)には、梅が禅画で広まった背景、円相の解釈、師の一休宗純との関係、画中の賛文の内容など、鑑賞者向けに使える固有情報がある。**資料不足ではなく、原資料からDBへの情報抽出不足**の典型例。主張の確度に応じて再整理すべき。
2. **`met-57280`《Mother and Children in Summer Night》** — DBは「北斎派による夏夜の親子を描く墨画。」の同文（各17字）。[Met公式ページ](https://www.metmuseum.org/art/collection/search/57280)では北斎派の帰属・媒体・年代等は確認できるが、現行ページに個別の解釈本文は見当たらない。**同じURLを再読するだけでは豊かな解説材料は得にくい**。別の信頼できる資料か、画面上の慎重な記述が必要。無理な背景物語は作らない。
3. **`met-437422`《Charity》** — DBは慈愛の寓意画という説明が解釈・背景の両方に反復。[Met公式ページ](https://www.metmuseum.org/art/collection/search/437422)は構図の反復、1629年のフレスコとの関係、当時の高い評価、リヒテンシュタイン家の購入可能性まで解説。**資料は存在しており、役割別に抽出可能**。
4. **`met-73161`《Drenched in Moonlight》** — DBは既に本人の詩・月夜の梅・解釈上の注意を区別。[Met公式ページ](https://www.metmuseum.org/art/collection/search/73161)でも画中の詩、枝の構成、地域の梅図の伝統が確認できる。短いからといって「内容が足りない」と断定しない例。将来の解説には詩と画面をどう結び付けるかが役立つ。
5. **`met-436535`《Wheat Field with Cypresses》** — DBには1889年の制作背景、作品の比較、筆触の動きと作者の評価が複数の欄に保存されている。[Met公式ページ](https://www.metmuseum.org/art/collection/search/436535)には本人の評価、弟への手紙、後の別制作に加え音声解説の書き起こしもある。**比較的資料が豊かで解説を構成しやすそうな候補**だが、すべての記述を正式に `verified` とするには独立検査記録を残す必要がある。

> この標本確認は**5件に限る**。残り295件の外部ページ本文は、この監査で個別には開いていない。したがって本レポートをもって300件が学術的に検証済みと評価しない。

## 今後の修正を最小化するための方針

1. 別チャットは引き続き**同文修正**を担当してよい。ただし、同文の解消だけで原資料検証済みにはしない。
2. 原資料に豊富な内容がある作品は、原資料から「制作背景」「専門的解釈」「画面の根拠」を切り分けて**既存の基礎資料欄**を充実させる。単に字数を増やさない。
3. 原資料が作品同定程度の情報しか持たない作品は、信頼できる補足資料があるかを探す。資料がなければ推測で補わず「未確認・根拠不足」を維持する。
4. 全300件について、各資料の主張を実際に原資料と突合する工程は**未完了**。優先候補93件だけ終えても、残りは学術的な内容が保証されない。
5. その後に限り、少数作品で**鑑賞者向けの独立した1種類の解説**を試作する。AI選定用の短文をそのまま再利用しない。複数段階の詳細解説は作らない。

## 全300作品の機械点検表（固定スナップショット）

「字数」は**専門家解釈 / 制作背景 / 画面のヒント**の各日本語文字数（空白等含む）。「同文」は2欄の完全一致、「素材短め」は3欄の合計100字未満を意味する。「出典未照合」は `source_evidence_review_status=pending` を指す。**一行の判定は作品の学術的な合否ではない。**

| No. | ID | 原題 | 字数（解釈/背景/画面） | 一次監査の旗 |
|---:|---|---|---:|---|
| 1 | `aic-869` | The Watermill with the Great Red Roof | 71/56/28 | 出典未照合 |
| 2 | `aic-4758` | Stoke-by-Nayland | 87/53/25 | 出典未照合 |
| 3 | `aic-4796` | Fishing Boats with Hucksters Bargaining for Fish | 65/51/21 | 出典未照合 |
| 4 | `aic-8991` | Improvisation No. 30 (Cannons) | 89/54/26 | 出典未照合 |
| 5 | `aic-11312` | Woman Mending | 106/79/34 | 出典未照合 |
| 6 | `aic-11723` | Woman at Her Toilette | 60/47/26 | 出典未照合 |
| 7 | `aic-14591` | Woman Reading | 88/52/29 | 出典未照合 |
| 8 | `aic-14598` | The Beach at Sainte-Adresse | 99/102/27 | 出典未照合 |
| 9 | `aic-14620` | Cliff Walk at Pourville | 76/55/25 | 出典未照合 |
| 10 | `aic-14624` | Stacks of Wheat (End of Day, Autumn) | 75/33/21 | 出典未照合 |
| 11 | `aic-14655` | Two Sisters (On the Terrace) | 89/51/24 | 出典未照合 |
| 12 | `aic-16327` | The Annunciation | 62/59/21 | 出典未照合 |
| 13 | `aic-16549` | Apples and Grapes | 107/101/32 | 出典未照合 |
| 14 | `aic-16551` | Beata Beatrix | 88/64/24 | 出典未照合 |
| 15 | `aic-16554` | The Artist's House at Argenteuil | 97/103/26 | 出典未照合 |
| 16 | `aic-16568` | Water Lilies | 79/59/26 | 出典未照合 |
| 17 | `aic-16571` | Arrival of the Normandy Train, Gare Saint-Lazare | 95/77/24 | 出典未照合 |
| 18 | `aic-16622` | Madame Léon Clapisson | 82/54/38 | 出典未照合 |
| 19 | `aic-19339` | Arlésiennes (Mistral) | 125/133/27 | — |
| 20 | `aic-20684` | Paris Street; Rainy Day | 93/56/31 | 出典未照合 |
| 21 | `aic-20692` | El Maragato Threatens Friar Pedro de Zaldivia with His Gun | 73/45/23 | 出典未照合 |
| 22 | `aic-25825` | Woman at the Piano | 77/56/24 | 出典未照合 |
| 23 | `aic-25865` | The Herring Net | 67/48/24 | 出典未照合 |
| 24 | `aic-27943` | Mahana no atua (Day of the God) | 83/80/25 | 出典未照合 |
| 25 | `aic-27949` | Madame Roulin Rocking the Cradle (La berceuse) | 102/103/28 | 出典未照合 |
| 26 | `aic-27992` | A Sunday on La Grande Jatte — 1884 | 79/45/32 | 出典未照合 |
| 27 | `aic-28560` | The Bedroom | 93/49/34 | 出典未照合 |
| 28 | `aic-30901` | The Denial of Saint Peter | 59/41/20 | 出典未照合 |
| 29 | `aic-35195` | The Lamentation | 74/52/19 | 出典未照合 |
| 30 | `aic-56905` | Nocturne: Blue and Gold—Southampton Water | 79/49/31 | 出典未照合 |
| 31 | `aic-57148` | The Death of Procris | 58/58/22 | 出典未照合 |
| 32 | `aic-61128` | At the Moulin Rouge | 62/58/30 | 出典未照合 |
| 33 | `aic-64729` | Early Morning, Tarpon Springs | 88/63/22 | 出典未照合 |
| 34 | `aic-79349` | The Drinkers | 76/43/26 | 出典未照合 |
| 35 | `aic-80607` | Self-Portrait | 68/37/24 | 出典未照合 |
| 36 | `aic-81539` | On the Bank of the Seine, Bennecourt | 93/84/35 | 出典未照合 |
| 37 | `aic-81545` | Stacks of Wheat (Sunset, Snow Effect) | 73/36/26 | 出典未照合 |
| 38 | `aic-81548` | Young Peasant Having Her Coffee | 130/121/22 | — |
| 39 | `aic-81551` | The Place du Havre, Paris | 111/78/30 | 出典未照合 |
| 40 | `aic-81552` | Woman and Child at the Well | 95/75/25 | 出典未照合 |
| 41 | `aic-81558` | Acrobats at the Cirque Fernando (Francisca and Angelina Wartenberg) | 79/54/35 | 出典未照合 |
| 42 | `aic-87479` | The Assumption of the Virgin | 67/47/24 | 出典未照合 |
| 43 | `aic-90048` | Distant View of Niagara Falls | 79/77/26 | 出典未照合 |
| 44 | `aic-93450` | Winter Scene | 82/41/26 | 出典未照合 |
| 45 | `aic-93782` | The Death of Orpheus | 72/47/15 | 出典未照合 |
| 46 | `aic-94841` | The Song of the Lark | 88/58/21 | 出典未照合 |
| 47 | `aic-95998` | Old Man with a Gold Chain | 83/63/27 | 出典未照合 |
| 48 | `aic-102227` | The Expulsion of Adam and Eve from Paradise | 56/38/20 | 出典未照合 |
| 49 | `aic-111436` | The Basket of Apples | 61/54/32 | 出典未照合 |
| 50 | `aic-111442` | The Child's Bath | 68/51/29 | 出典未照合 |
| 51 | `aic-154235` | The Girl by the Window | 67/45/22 | 出典未照合 |
| 52 | `met-749407` | The Fury of Monk Raigō | 51/38/41 | 出典未照合 |
| 53 | `met-737735` | Viewing the Moon in an Empty Room | 50/36/31 | 出典未照合 |
| 54 | `met-816203` | Festive Dancing at a Samurai Residence (Fūryū odori zu byōbu) | 51/43/38 | 出典未照合 |
| 55 | `met-42346` | Landscape with Pavilion | 41/49/35 | 出典未照合 |
| 56 | `met-73161` | Drenched in Moonlight | 42/31/18 | 素材短め・出典未照合 |
| 57 | `met-74692` | Woman Leaving Her Lover | 40/48/24 | 出典未照合 |
| 58 | `met-37941` | A Courtesan and Her Lover Estranged by a Quarrel:  Page from a Rasamanjari series | 56/43/33 | 出典未照合 |
| 59 | `met-12110` | The Hermit (Il solitario) | 54/49/23 | 出典未照合 |
| 60 | `met-40429` | Pavilion by the Lake | 48/33/29 | 出典未照合 |
| 61 | `met-55034` | Shiva Carries the Corpse of Sati | 44/57/39 | 出典未照合 |
| 62 | `met-823278` | Shiva enraged by Parvati's interruption of his meditation | 47/55/44 | 出典未照合 |
| 63 | `met-439333` | Wanderer in the Storm | 49/52/17 | 出典未照合 |
| 64 | `met-37852` | Ramkali Ragini: Folio from a ragamala series (Garland of Musical Modes) | 49/50/26 | 出典未照合 |
| 65 | `met-37907` | Kakubha Ragini:  Page from a Dispersed Ragamala Series (Garland of Musical Modes) | 37/47/26 | 出典未照合 |
| 66 | `met-436530` | Oleanders | 44/51/19 | 出典未照合 |
| 67 | `met-44702` | Sparse trees and pavilion | 39/47/30 | 出典未照合 |
| 68 | `met-49454` | Landscape | 36/50/29 | 出典未照合 |
| 69 | `met-39551` | Mandarin ducks and cotton rose hibiscus | 37/43/33 | 出典未照合 |
| 70 | `met-41154` | Wind among the Trees on the Riverbank | 41/53/44 | 出典未照合 |
| 71 | `met-10070` | The Spanish Girl in Reverie | 55/60/23 | 出典未照合 |
| 72 | `met-11145` | The Veteran in a New Field | 54/55/30 | 出典未照合 |
| 73 | `met-435962` | Hagar in the Wilderness | 64/65/28 | 出典未照合 |
| 74 | `met-435967` | The Burning of Sodom (formerly "The Destruction of Sodom") | 49/59/28 | 出典未照合 |
| 75 | `met-436840` | Self-Portrait with Two Pupils, Marie Gabrielle Capet (1761–1818) and Marie Marguerite Carraux de Rosemond (1765–1788) | 75/64/28 | 出典未照合 |
| 76 | `met-437903` | Marie Joséphine Charlotte du Val d'Ognes (1786–1868) | 75/78/32 | 出典未照合 |
| 77 | `met-436869` | Lachrymae | 40/57/27 | 出典未照合 |
| 78 | `met-436582` | Head of a Young Woman | 40/41/30 | 出典未照合 |
| 79 | `met-437323` | A Brazilian Landscape | 59/61/36 | 出典未照合 |
| 80 | `met-764092` | Our Lady of Mercy, called “The Pilgrim of Quito” | 47/68/46 | 出典未照合 |
| 81 | `met-847023` | The Return of Persephone | 50/50/29 | 出典未照合 |
| 82 | `met-439122` | Gothic Windows in the Ruins of the Monastery at Oybin | 43/51/30 | 出典未照合 |
| 83 | `met-435702` | The Horse Fair | 61/56/28 | 出典未照合 |
| 84 | `met-10790` | In the Woods | 54/37/23 | 出典未照合 |
| 85 | `met-11116` | Dressing for the Carnival | 47/26/27 | 出典未照合 |
| 86 | `met-20888` | Preparing for Christmas (Plucking Turkeys) | 42/27/23 | 素材短め・出典未照合 |
| 87 | `met-37881` | A Heroine Plucking a Flower:  Page from a Dispersed Nayikabheda | 50/41/37 | 出典未照合 |
| 88 | `met-37992` | Abhisarika Nayika, a Heroine Longing for Her Lover | 33/35/27 | 素材短め・出典未照合 |
| 89 | `met-38012` | Melancholy Courtesan | 46/38/20 | 出典未照合 |
| 90 | `met-38017` | Desvarati Ragini: Folio from a ragamala series (Garland of Musical Modes) | 31/41/27 | 素材短め・出典未照合 |
| 91 | `met-48932` | Orchid and rock | 55/45/23 | 出典未照合 |
| 92 | `met-53460` | On a Rustic Bridge, Carrying a Zither | 46/42/30 | 出典未照合 |
| 93 | `met-74983` | Queen Trisala's Grief (at the Stillness of the Unborn): Folio from a Kalpasutra Manuscript | 46/40/34 | 出典未照合 |
| 94 | `met-435650` | Madame Philippe Panon Desbassayns de Richemont (Jeanne Eglé Mourgue, 1778–1855) and Her Son, Eugène (1800–1859) | 44/50/19 | 出典未照合 |
| 95 | `met-435727` | The Departure of Saints Paula and Eustochium for the Holy Land | 24/33/26 | 素材短め・出典未照合 |
| 96 | `met-435978` | The Muse: History | 37/42/24 | 出典未照合 |
| 97 | `met-437035` | The Lamentation | 35/32/23 | 素材短め・出典未照合 |
| 98 | `met-439553` | The Lamentation | 36/39/19 | 素材短め・出典未照合 |
| 99 | `met-441352` | The Sultan's Tiger | 49/37/17 | 出典未照合 |
| 100 | `met-898196` | Bélizaire and the Frey Children | 48/56/48 | 出典未照合 |
| 101 | `met-436105` | The Death of Socrates | 109/92/44 | 出典未照合 |
| 102 | `met-11122` | The Gulf Stream | 89/95/27 | 出典未照合 |
| 103 | `met-435621` | Joan of Arc | 91/91/37 | 出典未照合 |
| 104 | `met-12127` | Madame X (Virginie Amélie Avegno Gautreau) | 89/87/37 | 出典未照合 |
| 105 | `met-436322` | The Love Letter | 87/75/32 | 出典未照合 |
| 106 | `met-435809` | The Harvesters | 83/54/31 | 出典未照合 |
| 107 | `met-53410` | Lions at the Stone Bridge of Mount Tiantai | 69/70/21 | 出典未照合 |
| 108 | `met-676034` | Mountain God with Tiger and Attendants | 62/59/42 | 出典未照合 |
| 109 | `met-39540` | Two eagles | 60/63/22 | 出典未照合 |
| 110 | `met-40086` | Scholar viewing a waterfall | 55/47/33 | 出典未照合 |
| 111 | `met-49001` | Cherry Blossoms at Yoshino | 110/107/36 | 出典未照合 |
| 112 | `met-44699` | Returning home through the snow | 90/53/29 | 出典未照合 |
| 113 | `met-829379` | Herdboys and Buffalos | 89/91/39 | 出典未照合 |
| 114 | `met-37897` | Malkos Raga: Page from a Dispersed Ragamala Series (Garland of Musical Modes) | 86/56/36 | 出典未照合 |
| 115 | `met-11160` | The Last Moments of John Brown | 102/79/34 | 出典未照合 |
| 116 | `met-436141` | The Dancing Class | 122/51/35 | 出典未照合 |
| 117 | `met-437156` | The Entombment | 103/57/44 | 出典未照合 |
| 118 | `met-45620` | Kongōyasha Myōō | 81/61/30 | 出典未照合 |
| 119 | `met-906843` | Kannon by a Lotus Pond | 76/57/29 | 出典未照合 |
| 120 | `met-41475` | Guanyin the Bringer of Sons | 51/51/36 | 出典未照合 |
| 121 | `met-10497` | View from Mount Holyoke, Northampton, Massachusetts, after a Thunderstorm—The Oxbow | 72/51/38 | 出典未照合 |
| 122 | `met-10480` | The Aegean Sea | 56/79/35 | 出典未照合 |
| 123 | `met-10946` | A Gorge in the Mountains (Kauterskill Clove) | 68/47/27 | 出典未照合 |
| 124 | `met-435838` | Virgin and Child in an Apse | 52/60/33 | 出典未照合 |
| 125 | `met-438754` | Madonna and Child | 57/50/33 | 出典未照合 |
| 126 | `met-437023` | Madonna and Child Enthroned with Angels | 80/44/28 | 出典未照合 |
| 127 | `met-438427` | The Lamentation | 61/56/34 | 出典未照合 |
| 128 | `met-829381` | Portrait of Minamoto no Muneyuki, from the “Fujifusa Version of the Handscroll of Thirty-Six Poetic Immortals” | 65/41/24 | 出典未照合 |
| 129 | `met-44863` | Yukihira and Two Brinemaidens at Suma | 48/49/31 | 出典未照合 |
| 130 | `met-40020` | The Sound of Spring in a Lonely Valley | 74/65/24 | 出典未照合 |
| 131 | `met-437033` | Virgin and Child | 63/47/30 | 出典未照合 |
| 132 | `met-435765` | Virgin and Child | 74/51/31 | 出典未照合 |
| 133 | `met-459070` | The Lamentation of Christ | 58/47/37 | 出典未照合 |
| 134 | `met-437897` | Abraham's Parting from the Family of Lot | 63/49/23 | 出典未照合 |
| 135 | `met-831188` | Icon of the Virgin and Child, Hodegetria variant | 58/53/32 | 出典未照合 |
| 136 | `met-435673` | The Outer Harbor of Brest | 53/55/24 | 出典未照合 |
| 137 | `met-435977` | Mother and Child | 82/38/15 | 出典未照合 |
| 138 | `met-435752` | Young Mother Gazing at Her Child | 91/48/25 | 出典未照合 |
| 139 | `met-74984` | Queen Trisala's Joy (at the Confirmation of Her Conception): Folio from a Kalpasutra Manuscript | 77/42/29 | 出典未照合 |
| 140 | `met-436721` | Christ Crowned with Thorns (Ecce Homo), and the Mourning Virgin (Mater Dolorosa) | 81/40/31 | 出典未照合 |
| 141 | `met-438952` | View from the Citadel Ramparts in Copenhagen by Moonlight | 69/46/30 | 出典未照合 |
| 142 | `met-437227` | The Love Letter | 87/31/26 | 出典未照合 |
| 143 | `met-435714` | Curiosity | 78/44/30 | 出典未照合 |
| 144 | `met-435743` | The Dispatch of the Messenger | 84/47/24 | 出典未照合 |
| 145 | `met-36141` | Returning Home in a Driving Rain | 83/34/32 | 出典未照合 |
| 146 | `met-770595` | The Crucifixion | 76/36/37 | 出典未照合 |
| 147 | `met-52988` | “Mount Utsu” (Utsu no yama), from The Tales of Ise (Ise monogatari) | 83/40/28 | 出典未照合 |
| 148 | `met-74846` | Krishna Woos Radha: Page from the  Dispersed "Boston" Rasikapriya (Lover's Breviary) | 75/41/26 | 出典未照合 |
| 149 | `met-37872` | Four Love Scenes and a Landscape: Page from a Dispersed Raskapriya | 78/37/31 | 出典未照合 |
| 150 | `met-77799` | Scene from the Tales of Ise: “Mount Utsu” | 72/31/26 | 出典未照合 |
| 151 | `met-436053` | Pietà | 72/39/33 | 出典未照合 |
| 152 | `met-13132` | The Coppersmith | 81/42/20 | 出典未照合 |
| 153 | `met-435762` | Virgin and Child | 65/54/38 | 出典未照合 |
| 154 | `met-435879` | The Pool at Jas de Bouffan | 96/56/33 | 出典未照合 |
| 155 | `met-438848` | Parochialstrasse in Berlin | 80/49/32 | 出典未照合 |
| 156 | `met-40063` | Sparrows, plum blossoms, and bamboo | 71/52/32 | 出典未照合 |
| 157 | `met-77204` | Waxwings, Cherry Blossoms, and Bamboo | 80/46/25 | 出典未照合 |
| 158 | `met-853216` | Unexpected Meeting on the Yodo River | 91/48/31 | 出典未照合 |
| 159 | `met-10819` | The Champion Single Sculls (Max Schmitt in a Single Scull) | 70/46/41 | 出典未照合 |
| 160 | `met-10154` | The Rocky Mountains, Lander's Peak | 96/51/36 | 出典未照合 |
| 161 | `met-10159` | Fur Traders Descending the Missouri | 89/44/30 | 出典未照合 |
| 162 | `met-436724` | Expectation | 90/45/19 | 出典未照合 |
| 163 | `met-37906` | Krishna and Radha with Their Confidantes: Page from a Dispersed Gita Govinda | 108/41/38 | 出典未照合 |
| 164 | `met-437749` | Merry Company on a Terrace | 93/48/31 | 出典未照合 |
| 165 | `met-39543` | Palace banquet | 89/86/14 | 出典未照合 |
| 166 | `met-45417` | Death of the Historical Buddha (Nehan-zu) | 100/63/22 | 出典未照合 |
| 167 | `met-44841` | Death of the Historical Buddha (Nehan-zu) | 97/74/21 | 出典未照合 |
| 168 | `met-45595` | Descent of Eleven-Headed Kannon | 87/83/19 | 出典未照合 |
| 169 | `met-45524` | White-Robed Kannon | 88/67/13 | 出典未照合 |
| 170 | `met-670929` | Hanshan and Shide (Japanese: Kanzan and Jittoku) | 98/87/19 | 出典未照合 |
| 171 | `met-11140` | Snap the Whip | 98/74/20 | 出典未照合 |
| 172 | `met-44984` | Descent of Eleven-Headed Kannon | 98/92/14 | 出典未照合 |
| 173 | `met-829407` | High Mountains, Flowing Water: Yu Boya and Zhong Ziqi | 106/72/20 | 出典未照合 |
| 174 | `met-438545` | Léon Pallière (1787–1820) in His Room at the Villa Medici, Rome | 93/90/18 | 出典未照合 |
| 175 | `met-437887` | Bertel Thorvaldsen (1768–1844) with the Bust of Horace Vernet | 83/108/16 | 出典未照合 |
| 176 | `met-436329` | Gathering Olives at Tivoli | 100/110/15 | 出典未照合 |
| 177 | `met-73188` | Rainy Landscape | 95/81/22 | 出典未照合 |
| 178 | `met-40451` | Rainy Landscape with Travelers | 100/77/19 | 出典未照合 |
| 179 | `met-40432` | Scholar in a Lakeside Pavilion | 94/88/15 | 出典未照合 |
| 180 | `met-74448` | Gathering of government officials | 98/68/16 | 出典未照合 |
| 181 | `met-35968` | Forts Zeelandia and Provintia and the City of Tainan | 96/95/20 | 出典未照合 |
| 182 | `met-38056` | Panchama Ragini: Page from a Ragamala Series (Garland of Musical Modes) | 66/78/50 | 出典未照合 |
| 183 | `met-435997` | The Storm | 116/91/24 | 出典未照合 |
| 184 | `met-436453` | Esther before Ahasuerus | 107/92/33 | 出典未照合 |
| 185 | `met-435844` | The Musicians | 109/114/34 | 出典未照合 |
| 186 | `met-437881` | Young Woman with a Water Pitcher | 108/105/23 | 出典未照合 |
| 187 | `met-437394` | Aristotle with a Bust of Homer | 105/94/24 | 出典未照合 |
| 188 | `met-437878` | A Maid Asleep | 116/105/25 | 出典未照合 |
| 189 | `met-436576` | The Vision of Saint John | 99/110/23 | 出典未照合 |
| 190 | `met-436947` | Boating | 101/120/26 | 出典未照合 |
| 191 | `met-436839` | The Penitent Magdalen | 118/111/25 | 出典未照合 |
| 192 | `met-11417` | Washington Crossing the Delaware | 122/97/29 | 出典未照合 |
| 193 | `met-436535` | Wheat Field with Cypresses | 104/91/20 | 出典未照合 |
| 194 | `met-437588` | Drawing the Eel | 114/100/25 | 出典未照合 |
| 195 | `met-436005` | The Calm Sea | 106/72/24 | 出典未照合 |
| 196 | `met-437549` | Wheat Fields | 100/107/23 | 出典未照合 |
| 197 | `met-435739` | The Toilette of Venus | 118/111/22 | 出典未照合 |
| 198 | `met-436622` | Merrymakers at Shrovetide | 100/96/25 | 出典未照合 |
| 199 | `met-435888` | Soap Bubbles | 101/98/24 | 出典未照合 |
| 200 | `met-436579` | Broken Eggs | 74/88/27 | 出典未照合 |
| 201 | `met-436678` | The Visit | 62/81/26 | 出典未照合 |
| 202 | `met-438817` | The Dance Class | 93/72/32 | 出典未照合 |
| 203 | `met-436838` | The Fortune-Teller | 88/97/23 | 出典未照合 |
| 204 | `met-437329` | The Abduction of the Sabine Women | 91/94/23 | 出典未照合 |
| 205 | `met-438779` | A Peasant Family | 85/95/23 | 出典未照合 |
| 206 | `met-438629` | First Steps | 82/118/17 | 出典未照合 |
| 207 | `met-437990` | Seated Peasant | 94/92/17 | 出典未照合 |
| 208 | `met-437842` | Teasing a Sleeping Girl | 77/80/21 | 出典未照合 |
| 209 | `met-437439` | A Young Girl with Daisies | 86/82/20 | 出典未照合 |
| 210 | `met-436952` | The Funeral | 87/93/21 | 出典未照合 |
| 211 | `met-436449` | The Siesta | 79/122/23 | 出典未照合 |
| 212 | `met-459016` | The Annunciation | 78/100/22 | 出典未照合 |
| 213 | `met-437490` | The Annunciation | 85/115/23 | 出典未照合 |
| 214 | `met-436791` | The Annunciation | 89/101/22 | 出典未照合 |
| 215 | `met-435640` | Madonna Adoring the Sleeping Child | 43/43/14 | 同文・出典未照合 |
| 216 | `met-437422` | Charity | 39/39/17 | 同文・素材短め・出典未照合 |
| 217 | `met-459131` | The Last Supper | 39/39/17 | 同文・素材短め・出典未照合 |
| 218 | `met-437286` | The Death of Harmonia | 62/62/36 | 同文・出典未照合 |
| 219 | `met-459110` | Young Girl Bathing | 39/39/16 | 同文・素材短め・出典未照合 |
| 220 | `met-437438` | Young Girl in a Pink-and-Black Hat | 56/56/16 | 同文・出典未照合 |
| 221 | `met-437638` | The Marriage of Cupid and Psyche | 31/31/13 | 同文・素材短め・出典未照合 |
| 222 | `met-437083` | The Marriage of the Virgin | 32/32/15 | 同文・素材短め・出典未照合 |
| 223 | `met-436801` | The Marriage Feast at Cana | 36/36/14 | 同文・素材短め・出典未照合 |
| 224 | `met-459079` | Mary of Burgundy | 34/34/14 | 同文・素材短め・出典未照合 |
| 225 | `met-436808` | Edward Smith Stanley (1752–1834), Twelfth Earl of Derby, Elizabeth, Countess of Derby (Lady Elizabeth Hamilton, 1753–1797), and Their Son (Edward Smith Stanley, 1775–1851) | 32/32/12 | 同文・素材短め・出典未照合 |
| 226 | `met-74996` | Aristanemi's Bridal Pavilion (top) and Witnessing Animals for Slaughter (bottom): Folio from a Kalpasutra Manuscript | 39/39/14 | 同文・素材短め・出典未照合 |
| 227 | `met-437284` | The Return from the Hunt | 32/32/14 | 同文・素材短め・出典未照合 |
| 228 | `met-437042` | The Return to the Fold | 32/32/15 | 同文・素材短め・出典未照合 |
| 229 | `met-436186` | Still Life with Silver | 29/29/10 | 同文・素材短め・出典未照合 |
| 230 | `met-435883` | Still Life with Apples and Pears | 31/31/16 | 同文・素材短め・出典未照合 |
| 231 | `met-816519` | Still Life of Grapes and Peaches | 33/33/17 | 同文・素材短め・出典未照合 |
| 232 | `met-436805` | Still Life with Fruit, Glassware, and a Wanli Bowl | 33/33/16 | 同文・素材短め・出典未照合 |
| 233 | `met-670896` | Plum Blossoms | 16/16/10 | 同文・素材短め・出典未照合 |
| 234 | `met-78149` | Plum Blossoms | 22/22/8 | 同文・素材短め・出典未照合 |
| 235 | `met-916604` | Plum Blossoms under the Moon at Dawn | 21/21/10 | 同文・素材短め・出典未照合 |
| 236 | `met-36000` | River landscape | 21/21/14 | 同文・素材短め・出典未照合 |
| 237 | `met-57280` | Mother and Children in Summer Night | 17/17/12 | 同文・素材短め・出典未照合 |
| 238 | `met-45805` | Mother and Children at the New Year | 33/33/16 | 同文・素材短め・出典未照合 |
| 239 | `met-670902` | Pilgrims Travelling to Ise | 22/22/11 | 同文・素材短め・出典未照合 |
| 240 | `met-437757` | Old Woman Praying | 24/24/10 | 同文・素材短め・出典未照合 |
| 241 | `met-437412` | Old Woman Cutting Her Nails | 34/34/14 | 同文・素材短め・出典未照合 |
| 242 | `met-437246` | Interior of Saint Peter's, Rome | 25/25/13 | 同文・素材短め・出典未照合 |
| 243 | `met-437802` | Neptune and the Winds | 32/32/13 | 同文・素材短め・出典未照合 |
| 244 | `met-435972` | Honfleur: Calvary | 26/26/13 | 同文・素材短め・出典未照合 |
| 245 | `met-857030` | The avatar Narasimha | 25/25/14 | 同文・素材短め・出典未照合 |
| 246 | `met-437429` | Still Life with Peaches | 33/33/11 | 同文・素材短め・出典未照合 |
| 247 | `met-888924` | Still Life with a Vase of Flowers, Melon, Peaches, and Grapes | 29/29/13 | 同文・素材短め・出典未照合 |
| 248 | `met-437479` | The Return of the Cattle | 29/29/15 | 同文・素材短め・出典未照合 |
| 249 | `met-438130` | The Departure of the Gondola | 26/26/11 | 同文・素材短め・出典未照合 |
| 250 | `met-436502` | The Annunciation | 50/50/19 | 同文・出典未照合 |
| 251 | `met-45647` | Farewell by a Stream on a Clear Day | 43/43/21 | 同文・出典未照合 |
| 252 | `met-823663` | “Taira no Koremori’s Farewell,”  from The Tale of the Heike (Heike monogatari) | 56/56/21 | 同文・出典未照合 |
| 253 | `met-816515` | Allegory of Sacred and Profane Love | 45/45/22 | 同文・出典未照合 |
| 254 | `met-438127` | The Declaration of Love | 39/39/15 | 同文・素材短め・出典未照合 |
| 255 | `met-437354` | The Drummond Children | 51/51/20 | 同文・出典未照合 |
| 256 | `met-436065` | Children and a Cow | 49/49/13 | 同文・出典未照合 |
| 257 | `met-436217` | Boy with a Black Spaniel | 40/40/17 | 同文・素材短め・出典未照合 |
| 258 | `met-57282` | Benten (Goddess of Love) | 35/35/13 | 同文・素材短め・出典未照合 |
| 259 | `met-437949` | Children Playing with a Goat | 36/36/12 | 同文・素材短め・出典未照合 |
| 260 | `met-57171` | Kusunoki Masashige Bidding Farewell to His Son Masatsura | 32/32/13 | 同文・素材短め・出典未照合 |
| 261 | `met-45217` | Seven Gods of Good Fortune and Chinese Children | 29/29/15 | 同文・素材短め・出典未照合 |
| 262 | `met-45656` | Children playing in the palace garden | 56/56/19 | 同文・出典未照合 |
| 263 | `met-45697` | Chinese Children at Play | 27/27/11 | 同文・素材短め・出典未照合 |
| 264 | `met-436692` | The Sackville Children | 53/53/18 | 同文・出典未照合 |
| 265 | `met-438815` | Madame Georges Charpentier (Marguerite-Louise Lemonnier, 1848–1904) and Her Children, Georgette-Berthe (1872–1945) and Paul-Emile-Charles (1875–1895) | 42/42/13 | 同文・素材短め・出典未照合 |
| 266 | `met-20129` | Story of Golden Locks | 54/54/22 | 同文・出典未照合 |
| 267 | `met-670921` | Farewell Gift to Tani Bunji | 28/28/15 | 同文・素材短め・出典未照合 |
| 268 | `met-436534` | Roses | 69/69/23 | 同文・出典未照合 |
| 269 | `met-437170` | The Music Room | 47/47/12 | 同文・出典未照合 |
| 270 | `met-436866` | Graziella | 61/61/26 | 同文・出典未照合 |
| 271 | `met-437508` | Self-Portrait | 49/49/18 | 同文・出典未照合 |
| 272 | `met-435627` | In the Sun | 28/28/13 | 同文・素材短め・出典未照合 |
| 273 | `met-440729` | Spring Morning | 28/28/13 | 同文・素材短め・出典未照合 |
| 274 | `met-436086` | The Seine: Morning | 28/28/13 | 同文・素材短め・出典未照合 |
| 275 | `met-438738` | Haystacks, Morning, Eragny | 28/28/12 | 同文・素材短め・出典未照合 |
| 276 | `met-437308` | Morning, An Overcast Day, Rouen | 28/28/9 | 同文・素材短め・出典未照合 |
| 277 | `met-670765` | The Death of Cleopatra | 54/54/21 | 同文・出典未照合 |
| 278 | `met-437985` | Pansies | 42/42/16 | 同文・出典未照合 |
| 279 | `met-437547` | Grainfields | 28/28/10 | 同文・素材短め・出典未照合 |
| 280 | `met-437915` | Interior of the Oude Kerk, Delft | 28/28/9 | 同文・素材短め・出典未照合 |
| 281 | `met-435807` | The Smokers | 55/55/16 | 同文・出典未照合 |
| 282 | `met-436305` | Still Life | 28/28/12 | 同文・素材短め・出典未照合 |
| 283 | `met-438123` | A Man Leaning on a Parapet | 39/39/22 | 同文・出典未照合 |
| 284 | `met-437168` | Christ Shown to the People | 28/28/14 | 同文・素材短め・出典未照合 |
| 285 | `met-687513` | The Lamentation | 28/28/15 | 同文・素材短め・出典未照合 |
| 286 | `met-435619` | The Betrayal of Christ | 28/28/13 | 同文・素材短め・出典未照合 |
| 287 | `met-436680` | The Annunciation of the Death of the Virgin | 62/62/12 | 同文・出典未照合 |
| 288 | `met-435851` | The Meditation on the Passion | 51/51/21 | 同文・出典未照合 |
| 289 | `met-436078` | Charity | 43/43/16 | 同文・出典未照合 |
| 290 | `met-436176` | Christ Asleep during the Tempest | 60/60/21 | 同文・出典未照合 |
| 291 | `met-436174` | A Woman Ironing | 61/61/26 | 同文・出典未照合 |
| 292 | `met-49475` | Plum | 42/42/20 | 同文・出典未照合 |
| 293 | `met-74673` | Lovers Returning to a Palace | 40/40/19 | 同文・素材短め・出典未照合 |
| 294 | `met-45739` | Jurōjin | 36/36/14 | 同文・素材短め・出典未照合 |
| 295 | `met-44638` | Viewing plum blossoms by moonlight | 24/24/16 | 同文・素材短め・出典未照合 |
| 296 | `met-37905` | Dipak Raga: Folio from a Ragamala Series (Garland of Musical Modes) | 57/57/22 | 同文・出典未照合 |
| 297 | `met-48984` | Old Man and Woman | 26/26/12 | 同文・素材短め・出典未照合 |
| 298 | `met-436123` | The Ballet from "Robert le Diable" | 69/69/23 | 同文・出典未照合 |
| 299 | `met-37851` | Bairadi Ragini: Folio from a ragamala series (Garland of Musical Modes) | 46/46/17 | 同文・出典未照合 |
| 300 | `met-436956` | Jean-Baptiste Faure (1830–1914) | 56/56/24 | 同文・出典未照合 |

