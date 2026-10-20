# シカゴ美術館51作品・登録画像と作品同定の追加監査（2026-10-20）

> **読み取り専用の監査結果。** 登録作品・感情タグ・作者の意図・制作背景・画像台帳は**一切編集しない**。現在、別チャットで`data/artworks.json`の同文修正が進行中であり、競合回避のためこの文書以外は変更しない。調査時の作品DB blobは`fa45a84ef2efe78cc8615e4031f96d0aa2722ec6`、画像台帳blobは`ef9803129b09c61e1ebafeb3faf67204759a27d9`。以後の修正で状態が変わる可能性がある。

## 結果を正確に区別する

| 項目 | 件数 | 判定内容 |
|---|---:|---|
| 対象作品 | **51** | シカゴ美術館の登録作品のみ（保留作品は除外） |
| 別アプリ由来の登録JPEG | **16/16** | 保存元`haranishi/hundred-days`の固定コミットからJPEGを取得し、**登録済みSHA-256とファイルサイズが全件一致**。各画像の実際の絵柄を目視し、作品名と明白な取り違えは見つからない |
| Commons画像・ファイル名に所蔵番号あり | **30/35** | 登録画像が指すCommonsファイルのタイトルに、DB登録のシカゴ美術館所蔵番号が含まれる。文字列と出典の照合であって、公式画像同士の画素比較ではない |
| Commons画像・ファイル名に所蔵番号なし | **5/35** | 各Commons作品ページまたは独立した作品一覧で**所蔵番号・作品IDとの対応を確認**した（詳細下記） |
| 画像台帳と公式作品ページ／所蔵番号／登録SHAの構造整合 | **51/51** | 全51件に既存整合検査との矛盾を検出せず |
| **公式AIC画像との直接的な画像比較** | **0/51** | `artic.edu`側の画像アクセス制限により、公式画像そのものを取得してサイド・バイ・サイド比較できていない |
| `review.image_subject_match_status=verified` | **0/51** | **51件とも`pending`維持**。メタデータ・ファイル名・ハッシュ一致だけで作品同定の完全検証としない |

**結論**：今回の範囲で、確定的な作品取り違えや即時差し替えを要する画像は見つかっていない。ただし**51件の画像同定が完全に終わったという意味ではない**。とくにCommons由来35件は登録画像自体と公式画像との直接比較を本セッションでは実施できていない。

### ミラー由来16件の検証手順

1. `data/image-sources.json`の`origin=existing_museum_app`にある元ファイルURLを参照。
2. 公開GitHubリポジトリ`haranishi/hundred-days`の固定コミット`8126fcc488c97e2d3e83926ac7975aedf94c1895`から画像`day-050-art-uncovered/assets/art/{AIC artwork id}.jpg`をバイナリ取得。
3. 16ファイルのSHA-256とバイト数を再計算し、DB台帳と**16件すべて一致**。取得した絵をそれぞれ確認（作品名、特徴的な人物や構図との明白な齟齬なし）。
4. 所蔵館と所蔵番号の関係を、Commonsの参照作品ページ等と照合。**画像を見た事実と、公式画像との直接一致を証明できたかは別である**。

### Commons画像のファイル名に所蔵番号がない5件

| ID | 作品 | 登録所蔵番号 | 別資料で確認した対応 |
|---|---|---|---|
| `aic-11312` | Woman Mending | 1959.636 | [Commons: Kvinde der lapper](https://commons.wikimedia.org/wiki/File:Kvinde_der_lapper.jpg)に同所蔵番号とAIC作品ID |
| `aic-16571` | Arrival of the Normandy Train, Gare Saint-Lazare | 1933.1158 | [Commons: Google Art Project](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Arrival_of_the_Normandy_Train%2C_Gare_Saint-Lazare_-_Google_Art_Project.jpg)に同所蔵番号、他のモネ作「サン＝ラザール駅」と区別 |
| `aic-81548` | Young Peasant Having Her Coffee | 1922.433 | [Commons: Young Peasant Having Her Coffee](https://commons.wikimedia.org/wiki/File:Young_Peasant_Having_Her_Coffee.jpg)に同所蔵番号とAIC作品ID |
| `aic-81551` | The Place du Havre, Paris | 1922.434 | [Commons: 登録ファイル](https://commons.wikimedia.org/wiki/File:Camille_Pissarro_-_Place_du_Havre%2C_Paris_-_Art_Institute_of_Chicago.jpg)に同所蔵番号とAIC作品ID |
| `aic-81552` | Woman and Child at the Well | 1922.436 | [Commons: Young-woman-and-child-at-the-well-1882](https://commons.wikimedia.org/wiki/File:Young-woman-and-child-at-the-well-1882.jpg)に同所蔵番号 |

### 既知の画像差分・保留事項

- `aic-81539`《On the Bank of the Seine, Bennecourt》：旧CommonsサムネイルのSHA変化は[追加調査記録](aic-81539-thumbnail-recheck.json)で調査され、Commons原画像と構図・アスペクト・縮小画像の色差の検査を実施した履歴がある。**旧のSHA変更を直ちに別作品と誤認しない**。
- `aic-4575`《Judith》：**300作品の登録データに含まれない保留作品**で、画像台帳だけにある。しかし`data/image-sources.json`内の`in_shared_catalog`が`true`で、保留状態の意味と不整合。**今回画像台帳は編集しない。** 登録時のフィルタで`in_shared_catalog`を使う別プログラムがある場合、誤流入を起こす余地があるため、今後フラグの訂正を別作業として確認する。現在のアプリが実際に読み込んだ事実は確認されていない。
- `data/artworks.json`に基づく画像同定のレビュー状態は、シカゴ51件**全件`pending`**のままにした。公式画像へのアクセスが回復するか、権利上問題のない公式画像・公式出版物の複製との視覚的比較ができた段階で再評価する。

## 作品別の出典照合一覧（51件）

表の「Commons（ファイル名に所蔵番号）」は**画像ファイルに作品IDが付いているという補強**にとどまり、内容の実照合済みを意味しない。「ミラー画像」は再取得した登録画像JPEGのハッシュまで確認したが、**公式画像との直接照合は未了**。

| 作品ID | 作品名 | 所蔵番号 | 実施した確認 | 参照 |
|---|---|---|---|---|
| `aic-869` | The Watermill with the Great Red Roof | 1894.1031 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Meindert%20Hobbema%20-%20The%20Watermill%20with%20the%20Great%20Red%20Roof%20-%201894.1031%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-4758` | Stoke-by-Nayland | 1922.4453 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:John%20Constable%20-%20Stoke-by-Nayland%20-%201922.4453%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-4796` | Fishing Boats with Hucksters Bargaining for Fish | 1922.4472 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Joseph%20Mallord%20William%20Turner%20-%20Fishing%20Boats%20with%20Hucksters%20Bargaining%20for%20Fish%20-%201922.4472%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-8991` | Improvisation No. 30 (Cannons) | 1931.511 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Vasily%20Kandinsky%20-%20Improvisation%20No.%2030%20(Cannons)%20-%201931.511%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-11312` | Woman Mending | 1959.636 | Commons（作品ページで所蔵番号照合） | [出典画像](https://commons.wikimedia.org/wiki/File:Kvinde_der_lapper.jpg) |
| `aic-11723` | Woman at Her Toilette | 1924.127 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Berthe_Morisot_-_Woman_at_Her_Toilette_-_1924.127_-_Art_Institute_of_Chicago.jpg) |
| `aic-14591` | Woman Reading | 1933.435 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:%C3%89douard%20Manet%20-%20Woman%20Reading%20-%201933.435%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-14598` | The Beach at Sainte-Adresse | 1933.439 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Beach_at_Sainte-Adresse_-_1933.439_-_Art_Institute_of_Chicago.jpg) |
| `aic-14620` | Cliff Walk at Pourville | 1933.443 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Cliff_Walk_at_Pourville_-_Google_Art_Project.jpg) |
| `aic-14624` | Stacks of Wheat (End of Day, Autumn) | 1933.444 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude%20Monet%20-%20Stacks%20of%20Wheat%20(End%20of%20Day%2C%20Autumn)%20-%201933.444%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-14655` | Two Sisters (On the Terrace) | 1933.455 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Two_Sisters_(On_the_Terrace)_-_Google_Art_Project.jpg) |
| `aic-16327` | The Annunciation | 1933.1062 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Jean%20Hey%2C%20(the%20Master%20of%20Moulins)%20-%20The%20Annunciation%20-%201933.1062%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-16549` | Apples and Grapes | 1933.1152 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Apples_and_Grapes_-_1933.1152_-_Art_Institute_of_Chicago.jpg) |
| `aic-16551` | Beata Beatrix | 1925.722 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Dante%20Gabriel%20Rossetti%20-%20Beata%20Beatrix%20-%201925.722%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-16554` | The Artist's House at Argenteuil | 1933.1153 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Artist's_House_at_Argenteuil_-_1933.1153_-_Art_Institute_of_Chicago.jpg) |
| `aic-16568` | Water Lilies | 1933.1157 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Water_Lilies_-_1933.1157_-_Art_Institute_of_Chicago.jpg) |
| `aic-16571` | Arrival of the Normandy Train, Gare Saint-Lazare | 1933.1158 | Commons（作品ページで所蔵番号照合） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Arrival_of_the_Normandy_Train%2C_Gare_Saint-Lazare_-_Google_Art_Project.jpg) |
| `aic-16622` | Madame Léon Clapisson | 1933.1174 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Madame_L%C3%A9on_Clapisson_-_1933.1174_-_Art_Institute_of_Chicago.jpg) |
| `aic-19339` | Arlésiennes (Mistral) | 1934.391 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Paul_Gauguin_-_Arl%C3%A9siennes_(Mistral)_-_1934.391_-_Art_Institute_of_Chicago.jpg) |
| `aic-20684` | Paris Street; Rainy Day | 1964.336 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Gustave_Caillebotte_-_Paris_Street,_Rainy_Day_-_1964.336_-_Art_Institute_of_Chicago.jpg) |
| `aic-20692` | El Maragato Threatens Friar Pedro de Zaldivia with His Gun | 1933.1071 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Francisco%20Jos%C3%A9%20de%20Goya%20y%20Lucientes%20-%20El%20Maragato%20Threatens%20Friar%20Pedro%20de%20Zaldivia%20with%20His%20Gun%20-%201933.1071%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-25825` | Woman at the Piano | 1937.1025 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Pierre-Auguste_Renoir_-_Woman_at_the_Piano_-_1937.1025_-_Art_Institute_of_Chicago.jpg) |
| `aic-25865` | The Herring Net | 1937.1039 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Winslow_Homer_-_The_Herring_Net_-_Google_Art_Project.jpg) |
| `aic-27943` | Mahana no atua (Day of the God) | 1926.198 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Paul%20Gauguin%20-%20Mahana%20no%20atua%20(Day%20of%20the%20God)%20-%201926.198%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-27949` | Madame Roulin Rocking the Cradle (La berceuse) | 1926.200 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Madame_Roulin_Rocking_the_Cradle_(La_berceuse)_-_1926.200_-_Art_Institute_of_Chicago.jpg) |
| `aic-27992` | A Sunday on La Grande Jatte — 1884 | 1926.224 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Georges_Seurat_-_A_Sunday_on_La_Grande_Jatte_--_1884_-_Google_Art_Project.jpg) |
| `aic-28560` | The Bedroom | 1926.417 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_The_Bedroom_-_1926.417_-_Art_Institute_of_Chicago.jpg) |
| `aic-30901` | The Denial of Saint Peter | 1969.3 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Hendrick_Terbrugghen_-_The_Denial_of_Saint_Peter_-_1969.3_-_Art_Institute_of_Chicago.jpg) |
| `aic-35195` | The Lamentation | 1970.1013 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Andrea_Vaccaro_-_The_Lamentation_-_1970.1013_-_Art_Institute_of_Chicago.jpg) |
| `aic-56905` | Nocturne: Blue and Gold—Southampton Water | 1900.52 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:James%20McNeill%20Whistler%20-%20Nocturne%2C%20Blue%20and%20Gold%E2%80%94Southampton%20Water%20-%201900.52%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-57148` | The Death of Procris | 1900.445 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Benjamin_West_-_The_Death_of_Procris_-_1900.445_-_Art_Institute_of_Chicago.jpg) |
| `aic-61128` | At the Moulin Rouge | 1928.610 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Henri_de_Toulouse-Lautrec_-_At_the_Moulin_Rouge_-_1928.610_-_Art_Institute_of_Chicago.jpg) |
| `aic-64729` | Early Morning, Tarpon Springs | 1911.32 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:George%20Inness%20-%20Early%20Morning%2C%20Tarpon%20Springs%20-%201911.32%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-79349` | The Drinkers | 1953.178 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Vincent%20van%20Gogh%20-%20The%20Drinkers%20-%201953.178%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-80607` | Self-Portrait | 1954.326 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Self-Portrait_-_1954.326_-_Art_Institute_of_Chicago.jpg) |
| `aic-81539` | On the Bank of the Seine, Bennecourt | 1922.427 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_On_the_Bank_of_the_Seine%2C_Bennecourt_-_1922.427_-_Art_Institute_of_Chicago.jpg) |
| `aic-81545` | Stacks of Wheat (Sunset, Snow Effect) | 1922.431 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Claude%20Monet%20-%20Stacks%20of%20Wheat%20(Sunset%2C%20Snow%20Effect)%20-%201922.431%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-81548` | Young Peasant Having Her Coffee | 1922.433 | Commons（作品ページで所蔵番号照合） | [出典画像](https://commons.wikimedia.org/wiki/File:Young_Peasant_Having_Her_Coffee.jpg) |
| `aic-81551` | The Place du Havre, Paris | 1922.434 | Commons（作品ページで所蔵番号照合） | [出典画像](https://commons.wikimedia.org/wiki/File:Camille_Pissarro_-_Place_du_Havre%2C_Paris_-_Art_Institute_of_Chicago.jpg) |
| `aic-81552` | Woman and Child at the Well | 1922.436 | Commons（作品ページで所蔵番号照合） | [出典画像](https://commons.wikimedia.org/wiki/File:Young-woman-and-child-at-the-well-1882.jpg) |
| `aic-81558` | Acrobats at the Cirque Fernando (Francisca and Angelina Wartenberg) | 1922.440 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Pierre-Auguste%20Renoir%20-%20Acrobats%20at%20the%20Cirque%20Fernando%20(Francisca%20and%20Angelina%20Wartenberg)%20-%201922.440%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-87479` | The Assumption of the Virgin | 1906.99 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Domenico%20Theotok%C3%B3poulos%2C%20called%20El%20Greco%20-%20The%20Assumption%20of%20the%20Virgin%20-%201906.99%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-90048` | Distant View of Niagara Falls | 1946.396 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Distant_View_of_Niagara_Falls_1830_Thomas_Cole.jpg) |
| `aic-93450` | Winter Scene | 1990.558 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Francisco%20Jos%C3%A9%20de%20Goya%20y%20Lucientes%20-%20Winter%20Scene%20-%201990.558%20-%20Art%20Institute%20of%20Chicago.jpg) |
| `aic-93782` | The Death of Orpheus | 1977.4 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Henri_Leopold_L%C3%A9vy_-_The_Death_of_Orpheus_-_1977.4_-_Art_Institute_of_Chicago.jpg) |
| `aic-94841` | The Song of the Lark | 1894.1033 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Jules_Breton,_le_chant_de_l%27alouette.1884.jpg) |
| `aic-95998` | Old Man with a Gold Chain | 1922.4467 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmenszoon_van_Rijn_-_Old_Man_with_a_Gold_Chain_-_1922.4467_-_Art_Institute_of_Chicago.jpg) |
| `aic-102227` | The Expulsion of Adam and Eve from Paradise | 1984.175 | Commons（ファイル名に所蔵番号） | [出典画像](https://commons.wikimedia.org/wiki/File:Benjamin_West_-_The_Expulsion_of_Adam_and_Eve_from_Paradise_-_1984.175_-_Art_Institute_of_Chicago.jpg) |
| `aic-111436` | The Basket of Apples | 1926.252 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Paul_C%C3%A9zanne_-_The_Basket_of_Apples_-_1926.252_-_Art_Institute_of_Chicago.jpg) |
| `aic-111442` | The Child's Bath | 1910.2 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Mary_Cassatt_-_The_Child%27s_Bath_-_1910.2_-_Art_Institute_of_Chicago.jpg) |
| `aic-154235` | The Girl by the Window | 2000.50 | ミラー画像（取得・SHA256一致、目視） | [出典画像](https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_The_Girl_by_the_Window_-_2000.50_-_Art_Institute_of_Chicago.jpg) |

## 既存の参考資料

- [画像台帳・登録済み配信の記録](../data/image-sources.json)
- [シカゴ51件の過去のJPEG再取得監査](aic-image-live-audit.json)（サムネイル50件一致・1件SHA変化。後者は別資料で再調査済み）
- [シカゴaic-81539追加調査](aic-81539-thumbnail-recheck.json)
- [データベース検証方針](review-guide.md)
- [シカゴ美術館の非ブラウザ画像アクセスの制約](https://github.com/art-institute-of-chicago/api-data/issues/9)

**編集範囲**：本監査レポートの追加のみ。`data/artworks.json`、`data/image-sources.json`および選定・解説関連の既存文書・実装は変更しない。
