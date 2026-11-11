# 再開メモの更新履歴

普段は [現在の再開地点](../resume-artwork-work.md) を参照する。このファイルには更新のたびに古い状態を退避する。2026-11-10以前の履歴は [旧再開メモ](resume-artwork-work-through-2026-11-10.md) に保存済み。

---

### 2026-11-10 08:26 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：313作品**。正式件数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：314作品目から候補を調査**。旧300作品を再登録しない。
- 新規追加は [追加手順](artwork-expansion-v2.md)、品質判定は [共通v2基準](artwork-completion-workflow-v2.md) に従う。
- 308〜310作品・311〜313作品は、登録後にMet公式解説と追加照合済み。主要事実の不一致は見つからず、原監査と作品DBは変更していない。記録は [308〜310](source-rechecks/2026-11-10-met-308-310-official-description.md)、[311〜313](source-rechecks/2026-11-10-met-311-313-official-description.md)。
- 新規登録監査の形式は `artwork-v2-new-registration-2`。詳細は追加手順を参照。旧作品の監査を遡って変更しない。

---

### 2026-11-10 08:39 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：316作品**。正式件数は最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：317作品目から候補調査**。過去の完成作品は再登録しない。
- 314〜316の3作品は met-453283、met-860959、met-853239。根拠は作品別監査JSONに保存。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [品質基準](artwork-completion-workflow-v2.md) に従う。
- 3作品の公式作品別解説は2026-11-10に直接読んで照合。Met公式画像の原寸と表示用JPEGは全量SHAと縮小画像比較をGitHub Actionsで確認。
- 過去313件の監査は変更せず、既存の補足公式解説照合は [source-rechecks](source-rechecks/) に保持。

---

### 2026-11-10 08:58 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：319作品**。正式件数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：320作品目から候補調査**。既存作品は再登録しない。
- 317〜319の新作品は `met-764094`（ペルー）、`met-635384`（メキシコ）、`met-16580`（米国）。新規作品の一次出典、画像検査、権利判断は各作品の監査JSONに記録。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [共通v2基準](artwork-completion-workflow-v2.md) に従う。
- 新規登録監査は `artwork-v2-new-registration-2`。2026-11-10に作品別公式Overviewと画像を目視照合、Met公式API提供の原寸・表示JPEGを実取得してSHA256と縮小画素を照合。追加のHTMLオンライン自動照合はMetの制限により保証しない。
- 過去316件の元監査・作品本文は変更していない。過去の再照合は `docs/source-rechecks/` に保存。

---

### 2026-11-10 10:58 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：322作品**。正式数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：323作品目から候補調査**。以前の完成作品を再登録しない。
- 320〜322の新作品は `met-319625`（エチオピア）、`met-454054`（インド）、`met-860960`（朝鮮）。各作品の出典本文、画像、権利と解説の照合結果は作品別v2監査JSONに保存。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [共通v2基準](artwork-completion-workflow-v2.md) を守る。新規監査形式は `artwork-v2-new-registration-2`。
- 3作品のMet公式ページOverviewを直接読み、公式IIIF画像を目視。Met API配信の大小JPEGについて完全SHA256・バイト数とリサイズ一致をGitHub Actionsで確認。HTMLのオンライン再照合はMetによるHTTP制限があり保証しない。
- 過去319件の作品・元監査は不変。過去の出典追加照合は `docs/source-rechecks/` を参照。

---

### 2026-11-10 11:20 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：323作品**。正式数は最新 `main` の `data/artworks.json` とREADMEを確認する。
- **次：324作品目から候補調査**。既存の完成作品を再登録しない。
- 323番目は `met-435991`（Camille Corot, *A Woman Reading*, 1869 and 1870）。Metの作品別Overviewと公式画像を照合し、独自日本語解説・v2監査に登録。
- Met APIの原寸／表示JPEGを完全SHA256・サイズ・縮小RMSで照合（[GitHub Actionsの検証](https://github.com/matumaruex/kaiga-data/actions/runs/42802438308)）。同AIの別工程審査であり人間の外部審査ではない。
- 既存322件と各監査は不変。323件目は登録プログラムと全体検査に合格。一時検証ワークフローは撤去済み。次は [追加ガイド](artwork-expansion-v2.md) と [共通基準](artwork-completion-workflow-v2.md) に従う。

---

### 2026-11-10 22:27 UTC

#### 保存前の状態（2026-11-10時点）

- **完成登録：326作品**。正式件数は最新 `main` の `data/artworks.json` で確認。
- **次：327作品目から候補調査**。重複IDと同作別画像を調べ、品質未満は保留。
- 324〜326作品：`met-764090` ペルー《楽園のアダムとエバ》、`met-77180` 日本《花魁図》、`met-701989` アメリカ《エマ・ヴァン・ネーム》。独自日本語解説・作品別v2出典監査を保存。
- 3件の公式作品解説と公式IIIF画像を確認。Met公式APIで原寸・表示用JPEG計6ファイルのSHA256、バイト数、寸法、縮小RMSを完全照合（[検証記録](https://github.com/matumaruex/kaiga-data/actions/runs/42805639776)）。同じAIによる別工程審査であり、外部の人間の鑑定ではない。
- 既存323作品と旧監査は変更せず、[新規登録ガイド](artwork-expansion-v2.md) と [v2完成条件](artwork-completion-workflow-v2.md) に準拠。GitHubの標準検査後にmainへ統合。

---

### 2026-11-10 22:47 UTC

#### 保存前の状態（2026-11-11時点）

- **完成登録：329作品**。正式数は統合後の最新 `main` とREADMEを確認。
- **次：330作品目から候補調査**。既存作品の重複と画面・出典・画像権利を照合。
- 327〜329作品：`met-49471` 中国《洞窟での瞑想》、`met-747199` メキシコ《カルメンの聖母と煉獄の魂》、`met-456966` インド《馬上のナワーブ・ムザッファル・アリー・ハーン》。個別のv2出典監査と独自日本語解説を保存。
- 公式作品別Overviewと実画像を照合し、Met公式APIの原寸・表示JPEG計6点をSHA256・サイズ・寸法・縮小RMSで検証（[実画像の証拠](https://github.com/matumaruex/kaiga-data/actions/runs/42914013617)）。同一AIによる別工程の審査で、外部の人間の鑑定ではない。
- 既存326作品と監査は変更していない。[新規追加ガイド](artwork-expansion-v2.md) および [v2基準](artwork-completion-workflow-v2.md) を引き継ぐ。

---

### 2026-11-11 00:01 UTC

#### 保存前の状態（2026-11-11時点）

- **完成登録：332作品**。正式数は最新mainとREADMEを確認。
- **次：333作品目から候補調査**。重複・出典本文・作品本体と公式画像の権利・表示を照合。
- 今回330〜332：`met-37817` チベットのンゴル寺第8代住職肖像、`met-437102` ピーテル・デ・モライン《小屋のある風景》、`met-451256` イラン《瓶と杯を持つ人物》。
- 3作品の独自日本語解説、作品別Overviewの短い2箇所と説明文の対応、公式APIによる原寸/表示JPEG完全SHA256・バイト数・寸法・縮小RMS、Met Open Access CC0画像権利とPD表示を個別に照合（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42916204559)）。同一AIによる別工程の監査で、外部の人間による審査ではない。
- 既存329作品と画像台帳の過去部分は変更なし。品質と手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を参照。

---

### 2026-11-11 00:13 UTC

#### 保存前の状態（2026-11-11時点）

- **完成登録：335作品**。正式な数は最新mainとREADMEを確認。
- **次：336作品目から候補調査**。作品ID・題材重複、所蔵館の作品別出典、作品・画像・現代解説の権利、公式JPEGの対象画面を検証する。
- 333〜335：`met-816194` 日本・相阿弥（伝）《山水図》、`met-929265` 韓国・張承業《鳥・動物・静物図屏風》、`met-11287` アメリカ・テオドール・カウフマン《自由への道》。
- 各作品に独自日本語解説・公式概要と短い2箇所の引用照合・v2監査。PDと公式Open Access CC0画像の権利を分け、元画像と表示JPEGのSHA256・寸法・縮小画像を照合（[画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42927377170)）。同一AIの別パスによる確認で外部専門家の審査ではない。
- 過去332作品のレコードと画像台帳の既存部分は変更していない。手順は [新規登録ガイド](artwork-expansion-v2.md) と [共通品質基準](artwork-completion-workflow-v2.md) を継続。
