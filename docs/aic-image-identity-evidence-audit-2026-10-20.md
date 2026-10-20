# シカゴ美術館51作品：画像と作品の同定調査（2026-10-20、読み取り専用・一次結果）

> **結論：51件とも登録作品ID・画像台帳・画像ハッシュの内部整合は確認。公式画像との全件直接目視照合は未完了。よって本報告では51件を「作品画像一致 verified」と断定しない。** この調査では `data/artworks.json`、`data/image-sources.json`、レビューの `image_subject_match_status` を一切更新しない。別チャットの同文修正と衝突しない。

## 検査したファイルの固定版
- 作品データ：`data/artworks.json` blob SHA `bd5acc08795fe1972fb91ddc5cb1c6a9b7ced5e6`
- 画像台帳：`data/image-sources.json` blob SHA `ef9803129b09c61e1ebafeb3faf67204759a27d9`
- 作品：AIC 51件（Commons由来35件／公開ミラー由来16件）。画像台帳の `aic-4575` は登録外の保留作品なので本件から除外。

## 実施済み
1. 51件の登録作品ID、タイトル、公式作品ページURL、所蔵番号、画像URL、画像ハッシュを画像台帳と照合し、**内部不一致0件**。
2. Commons 35件のうち30件は画像ファイル名に作品の所蔵番号が明示され、登録値と一致。
3. 残りのCommons 5件はファイル名が所蔵番号を示さないため、Commonsのファイル説明と作品ID・所蔵番号を追加照合した：`aic-11312`（1959.636）、`aic-16571`（1933.1158）、`aic-81548`（1922.433）、`aic-81551`（1922.434）、`aic-81552`（1922.436）。各画像出典ページおよび [シカゴ美術館公式研究資料（Place du Havre）](https://publications.artic.edu/node/134687)、[Pissarroの Woman Mending](https://publications.artic.edu/pissarro/api/epub/7/27/print_view)、[Monetの駅風景](https://publications.artic.edu/node/135550) を確認した。**これも公式画像とのピクセル照合ではない。**
4. 公開ミラー16件の画像はGitHub上の固定コミットから取得し、その絵柄・作品名に明白な食い違いがないことを目視確認した。少なくとも `aic-11723` の実取得画像については登録済みSHA-256と一致を再計算した。ほかのミラー画像は以前の台帳のハッシュ検証記録があり、今回は全16件のハッシュを再計算したとは主張しない。
5. シカゴ美術館の公式作品ページ/IIIF画像にはHTTP 403などの制約があり、今回の検査では**独立した公式画像と登録画像を全51件で直接並べることができなかった**。

## 判定
- 登録作品と画像出典の**書誌的・構造的な同定**：51/51に整合する根拠あり（30件Commonsファイル名一致、5件Commons説明の所蔵番号一致、16件固定IDの公開ミラー＋台帳と目視整合）。
- **公式美術館の画像と登録画像が同じ絵であることを確定する全件目視照合**：未完了（51件の `image_subject_match_status` は変更せず保留）。
- **確定的な画像取り違え**：今回の範囲で検出なし。ただし未検出は不存在の証明ではない。
- **画像の色精度、修復差、トリミング、画像利用権利の最終確認**：対象外。
- `aic-81539` は過去のCommonsサムネイル再符号化問題として別途再確認済み：[既存の照合記録](aic-81539-thumbnail-recheck.json)。この件を別の作品への取り違えと解釈しない。

## 51件の個別記録
以下の各行の「未確定」は**公式画像との厳密な比較について**であり、台帳内部のID・ハッシュのエラーを示さない。

| 作品ID | 登録作品の原題 | 所蔵番号 | 出典からの根拠 | 出典ページ | 公式画像との直接比較 |
|---|---|---|---|---|---|
| aic-869 | The Watermill with the Great Red Roof | 1894.1031 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Meindert%20Hobbema%20-%20The%20Watermill%20with%20the%20Great%20Red%20Roof%20-%201894.1031%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-4758 | Stoke-by-Nayland | 1922.4453 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:John%20Constable%20-%20Stoke-by-Nayland%20-%201922.4453%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-4796 | Fishing Boats with Hucksters Bargaining for Fish | 1922.4472 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Joseph%20Mallord%20William%20Turner%20-%20Fishing%20Boats%20with%20Hucksters%20Bargaining%20for%20Fish%20-%201922.4472%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-8991 | Improvisation No. 30 (Cannons) | 1931.511 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Vasily%20Kandinsky%20-%20Improvisation%20No.%2030%20(Cannons)%20-%201931.511%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-11312 | Woman Mending | 1959.636 | Commonsのファイル説明に所蔵番号・作品ID（外部資料照合） | [画像出典](https://commons.wikimedia.org/wiki/File:Kvinde_der_lapper.jpg) | 未確定 |
| aic-11723 | Woman at Her Toilette | 1924.127 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Berthe_Morisot_-_Woman_at_Her_Toilette_-_1924.127_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-14591 | Woman Reading | 1933.435 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:%C3%89douard%20Manet%20-%20Woman%20Reading%20-%201933.435%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-14598 | The Beach at Sainte-Adresse | 1933.439 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Beach_at_Sainte-Adresse_-_1933.439_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-14620 | Cliff Walk at Pourville | 1933.443 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Cliff_Walk_at_Pourville_-_Google_Art_Project.jpg) | 未確定 |
| aic-14624 | Stacks of Wheat (End of Day, Autumn) | 1933.444 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude%20Monet%20-%20Stacks%20of%20Wheat%20(End%20of%20Day%2C%20Autumn)%20-%201933.444%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-14655 | Two Sisters (On the Terrace) | 1933.455 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Two_Sisters_(On_the_Terrace)_-_Google_Art_Project.jpg) | 未確定 |
| aic-16327 | The Annunciation | 1933.1062 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Jean%20Hey%2C%20(the%20Master%20of%20Moulins)%20-%20The%20Annunciation%20-%201933.1062%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-16549 | Apples and Grapes | 1933.1152 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Apples_and_Grapes_-_1933.1152_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-16551 | Beata Beatrix | 1925.722 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Dante%20Gabriel%20Rossetti%20-%20Beata%20Beatrix%20-%201925.722%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-16554 | The Artist's House at Argenteuil | 1933.1153 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Artist's_House_at_Argenteuil_-_1933.1153_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-16568 | Water Lilies | 1933.1157 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Water_Lilies_-_1933.1157_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-16571 | Arrival of the Normandy Train, Gare Saint-Lazare | 1933.1158 | Commonsのファイル説明に所蔵番号・作品ID（外部資料照合） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Arrival_of_the_Normandy_Train%2C_Gare_Saint-Lazare_-_Google_Art_Project.jpg) | 未確定 |
| aic-16622 | Madame Léon Clapisson | 1933.1174 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Madame_L%C3%A9on_Clapisson_-_1933.1174_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-19339 | Arlésiennes (Mistral) | 1934.391 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Paul_Gauguin_-_Arl%C3%A9siennes_(Mistral)_-_1934.391_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-20684 | Paris Street; Rainy Day | 1964.336 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Gustave_Caillebotte_-_Paris_Street,_Rainy_Day_-_1964.336_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-20692 | El Maragato Threatens Friar Pedro de Zaldivia with His Gun | 1933.1071 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Francisco%20Jos%C3%A9%20de%20Goya%20y%20Lucientes%20-%20El%20Maragato%20Threatens%20Friar%20Pedro%20de%20Zaldivia%20with%20His%20Gun%20-%201933.1071%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-25825 | Woman at the Piano | 1937.1025 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Woman_at_the_Piano_-_1937.1025_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-25865 | The Herring Net | 1937.1039 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Winslow_Homer_-_The_Herring_Net_-_Google_Art_Project.jpg) | 未確定 |
| aic-27943 | Mahana no atua (Day of the God) | 1926.198 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Paul%20Gauguin%20-%20Mahana%20no%20atua%20(Day%20of%20the%20God)%20-%201926.198%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-27949 | Madame Roulin Rocking the Cradle (La berceuse) | 1926.200 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Madame_Roulin_Rocking_the_Cradle_(La_berceuse)_-_1926.200_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-27992 | A Sunday on La Grande Jatte — 1884 | 1926.224 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Georges_Seurat_-_A_Sunday_on_La_Grande_Jatte_--_1884_-_Google_Art_Project.jpg) | 未確定 |
| aic-28560 | The Bedroom | 1926.417 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_The_Bedroom_-_1926.417_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-30901 | The Denial of Saint Peter | 1969.3 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Hendrick_Terbrugghen_-_The_Denial_of_Saint_Peter_-_1969.3_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-35195 | The Lamentation | 1970.1013 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Andrea_Vaccaro_-_The_Lamentation_-_1970.1013_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-56905 | Nocturne: Blue and Gold—Southampton Water | 1900.52 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:James%20McNeill%20Whistler%20-%20Nocturne%2C%20Blue%20and%20Gold%E2%80%94Southampton%20Water%20-%201900.52%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-57148 | The Death of Procris | 1900.445 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Benjamin_West_-_The_Death_of_Procris_-_1900.445_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-61128 | At the Moulin Rouge | 1928.610 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Henri_de_Toulouse-Lautrec_-_At_the_Moulin_Rouge_-_1928.610_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-64729 | Early Morning, Tarpon Springs | 1911.32 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:George%20Inness%20-%20Early%20Morning%2C%20Tarpon%20Springs%20-%201911.32%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-79349 | The Drinkers | 1953.178 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Vincent%20van%20Gogh%20-%20The%20Drinkers%20-%201953.178%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-80607 | Self-Portrait | 1954.326 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Self-Portrait_-_1954.326_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-81539 | On the Bank of the Seine, Bennecourt | 1922.427 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_On_the_Bank_of_the_Seine%2C_Bennecourt_-_1922.427_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-81545 | Stacks of Wheat (Sunset, Snow Effect) | 1922.431 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Claude%20Monet%20-%20Stacks%20of%20Wheat%20(Sunset%2C%20Snow%20Effect)%20-%201922.431%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-81548 | Young Peasant Having Her Coffee | 1922.433 | Commonsのファイル説明に所蔵番号・作品ID（外部資料照合） | [画像出典](https://commons.wikimedia.org/wiki/File:Young_Peasant_Having_Her_Coffee.jpg) | 未確定 |
| aic-81551 | The Place du Havre, Paris | 1922.434 | Commonsのファイル説明に所蔵番号・作品ID（外部資料照合） | [画像出典](https://commons.wikimedia.org/wiki/File:Camille_Pissarro_-_Place_du_Havre%2C_Paris_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-81552 | Woman and Child at the Well | 1922.436 | Commonsのファイル説明に所蔵番号・作品ID（外部資料照合） | [画像出典](https://commons.wikimedia.org/wiki/File:Young-woman-and-child-at-the-well-1882.jpg) | 未確定 |
| aic-81558 | Acrobats at the Cirque Fernando (Francisca and Angelina Wartenberg) | 1922.440 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Pierre-Auguste%20Renoir%20-%20Acrobats%20at%20the%20Cirque%20Fernando%20(Francisca%20and%20Angelina%20Wartenberg)%20-%201922.440%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-87479 | The Assumption of the Virgin | 1906.99 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Domenico%20Theotok%C3%B3poulos%2C%20called%20El%20Greco%20-%20The%20Assumption%20of%20the%20Virgin%20-%201906.99%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-90048 | Distant View of Niagara Falls | 1946.396 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Distant_View_of_Niagara_Falls_1830_Thomas_Cole.jpg) | 未確定 |
| aic-93450 | Winter Scene | 1990.558 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Francisco%20Jos%C3%A9%20de%20Goya%20y%20Lucientes%20-%20Winter%20Scene%20-%201990.558%20-%20Art%20Institute%20of%20Chicago.jpg) | 未確定 |
| aic-93782 | The Death of Orpheus | 1977.4 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Henri_Leopold_L%C3%A9vy_-_The_Death_of_Orpheus_-_1977.4_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-94841 | The Song of the Lark | 1894.1033 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Jules_Breton,_le_chant_de_l%27alouette.1884.jpg) | 未確定 |
| aic-95998 | Old Man with a Gold Chain | 1922.4467 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmenszoon_van_Rijn_-_Old_Man_with_a_Gold_Chain_-_1922.4467_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-102227 | The Expulsion of Adam and Eve from Paradise | 1984.175 | Commonsのファイル名に所蔵番号（内部一致） | [画像出典](https://commons.wikimedia.org/wiki/File:Benjamin_West_-_The_Expulsion_of_Adam_and_Eve_from_Paradise_-_1984.175_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-111436 | The Basket of Apples | 1926.252 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Paul_C%C3%A9zanne_-_The_Basket_of_Apples_-_1926.252_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-111442 | The Child's Bath | 1910.2 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Mary_Cassatt_-_The_Child%27s_Bath_-_1910.2_-_Art_Institute_of_Chicago.jpg) | 未確定 |
| aic-154235 | The Girl by the Window | 2000.50 | 作品ID名の公開ミラー画像・目視で題材は矛盾なし | [画像出典](https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_The_Girl_by_the_Window_-_2000.50_-_Art_Institute_of_Chicago.jpg) | 未確定 |

## 今後の処理（作品データを書き換えない）
公式画像のアクセス制限が解消するか、所蔵館の信頼できる図版が別途取得できた作品ごとに**画像そのものを左右比較**し、構図・人物・描かれている要素、同一画題の異作品との取り違えを判断する。証拠とともに個別に結果を記録したときだけ `image_subject_match_status` を更新する。勝手に一括 `verified` にしない。

**内容解説、感情タグ、作品の同文修正はこの監査の対象外。**
