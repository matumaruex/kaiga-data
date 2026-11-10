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
