# AI選定データの重複・旧形式3項目・summary_for_aiの必要性調査（2026-10-20）

> **後日の実施確定（2026-10-20）**：本書の「削除禁止」「比較してから廃止」は、調査実施時点の判断を残した**履歴**。その後、利用者の決定により旧形式の解釈3項目と `summary_for_ai` を**全300作品から削除済み**。現行プレビューと家族試験の両ブランチ、DBの検証スクリプト、初期カタログ・テストも更新済み。最新の運用規則は [データ基本方針](data-policy.md) と [レビュー手順](review-guide.md) を参照。必要な独自情報を全件再検証して正本へ移す作業は行っていない。削除前の全文はGit履歴から復元できる。

## 結論（静的コード監査で確認した範囲）

| フィールド | 現行 `bijutsukan` プレビューのAI選定/表示 | DB側の必須チェック | 判断 |
|---|---|---|---|
| `curation.meaning_basis` | **使用中**：選定AIへ作品ごとの根拠として送信、作品画面にも表示 | 有 | **正本として維持** |
| 感情タグと強度 | **使用中**：一次候補抽出 | 有 | **維持** |
| `search_profile.fitting_situations` / `selection_cautions` | **使用中**：候補AIに送信 | 有 | **維持、ただし冗長な文は整理可能** |
| `curation.interpretation` / `source_context_note` / `alternate_reading`（旧形式3項目） | **現行プレビュー版の正規化・選定・作品表示の実行経路で未使用** | **有：`scripts/validate_artworks.py` が必須** | **段階的統廃合候補。現在は削除禁止** |
| `search_profile.summary_for_ai` | **使用中**：候補24件それぞれの `summary` としてAIへ送信 | **有**、アプリのZodスキーマでも必須 | **必要性の比較試験後に簡素化/廃止判断。現在は削除禁止** |

### 確認した実装（`matumaruex/bijutsukan` の `codex/museum-preview`）

- [`src/lib/ai/candidates.ts`](https://github.com/matumaruex/bijutsukan/blob/codex/museum-preview/src/lib/ai/candidates.ts)：`primary` / `secondary` のタグ・強度で、プログラムが24件まで候補を抽出する。旧形式の文章もAI要約も、**この一次候補抽出には参照しない**。
- [`src/lib/catalog/normalize.ts`](https://github.com/matumaruex/bijutsukan/blob/codex/museum-preview/src/lib/catalog/normalize.ts)：共有DBから `meaning_basis` → `meaning`、`summary_for_ai` → `summary`、適合状況・注意点を選定用に正規化。旧形式3項目はここで選定/表示用の値にしていない。Zodスキーマは `summary_for_ai` を必須とする。
- [`src/lib/ai/select.ts`](https://github.com/matumaruex/bijutsukan/blob/codex/museum-preview/src/lib/ai/select.ts)：候補に `summary`、`fitting`、`cautions`、`meaning.author_intent`、`meaning.scholarly_interpretation`、`meaning.creation_context`、`meaning.visual_clues`、`meaning.uncertainty_note` を**同時に送信**。同義の情報を重複送信する余地がある。長さの上限は各欄で個別に設定されている。
- [`src/components/ArtworkView.tsx`](https://github.com/matumaruex/bijutsukan/blob/codex/museum-preview/src/components/ArtworkView.tsx)：作品画面は `meaning` 由来の制作背景・専門家解釈・不確実性・作者発言を表示し、DBの旧形式3項目を直接読み出していない。
- [`scripts/validate_artworks.py`](https://github.com/matumaruex/kaiga-data/blob/main/scripts/validate_artworks.py)：旧形式3項目について、`curation` の必須文字列として現存確認する。なくしたら現行検証は失敗する。

**調査範囲の限界**：これは確認したGitHub上の現行プレビュー実装と共有DBの検証器から分かる事実。構想中の「2つ目のアプリ」や別ブランチ/外部クライアントの参照までは網羅していない。**どこでも使われないと断定しない**。AIに `summary_for_ai` を渡さない場合の作品選定品質も、API実験をしていないので未評価。

## 300作品の重複分析：固定スナップショット

- 参照した `data/artworks.json` の blob SHA：`4dee6db08d5cda6b24fb57efe1b2478612184862`
- **旧 `interpretation` と `meaning_basis.scholarly_interpretation.summary` が完全一致：176 / 300**
- **旧 `source_context_note` と `meaning_basis.creation_context` が完全一致：289 / 300**
- **旧 `alternate_reading` と `meaning_basis.uncertainty_note` が完全一致：159 / 300**
- **`summary_for_ai` と専門家解釈が完全一致：88 / 300**
- **`summary_for_ai` の中に専門家解釈の全文が含まれる：176 / 300**（上記88件も含む）
- `summary_for_ai` と旧 `interpretation` が完全一致：45 / 300
- これらは**文字列一致**の観測であり、意味的な重複や誤りの全数を計測したものではない。他のチャットが修正すると件数は変わる。

### 削除を急いではいけない理由

- 旧 `interpretation` には新しい専門家の解釈とは異なる**鑑賞の感情的接点**が書かれた作品がある（例：`aic-869` の旧欄は「平穏さに接続する」、新欄は画面と史料を区別）。
- 旧 `alternate_reading` には `uncertainty_note` とは言い回しも注意点も違う文章がある（例：`met-898196` の奴隷制・上塗り・差別的展示への注意）。優先して、正本の注意点や索引で落とさないか精査する。
- `source_context_note` と新しい制作背景が異なる11件のように、新しい欄が暫定記述になっていて、旧欄のほうに具体的な事実がある例もある（例：`met-435627`）。**旧欄を機械的に消すと内容が後退する場合がある**。
- `summary_for_ai` が別途どの程度判断に貢献しているかは、単純な文字列重複だけでは決められない。

## 正式な統廃合判断に必要な工程

1. **旧形式3項目**：新しい正本と全作品で差分比較する。差分にしかない確認済みの事実/選定時の重要な注意点を適切な正本・索引欄へ移す。
2. 別アプリ、DB作成・検証スクリプト、テスト、公開中の古いデプロイ、外部利用者を調べる。利用先がなければ新規登録時の旧欄必須を廃止し、プレビューとDB検証を更新してから削除する。**作品データだけ先に消さない**。
3. **`summary_for_ai`**：同じ鑑賞者入力・同じ候補群・同じモデル/出力条件で「送信する／送信しない」を比較する。比較項目は作品選定の妥当性、無関係な選出/見落とし、選定エラー率、入力トークン数、API料金。難しい感情混合・否定文も含める。十分な優位性がなければ送信を削るか、必要時に正本から派生させる。API実験の費用・無断実行にも注意する。
4. 本文が薄いからといって鑑賞者向けに説明を先回りして増やす必要はない。鑑賞者向けの文章は後から公式美術館や学術原資料を**直接参照**して独立制作する。人為的な感情誘導や多段階解説はしない。

**今行ったのはルールと調査報告の更新のみ。共有作品データも、アプリの実装も削除・変更していない。**
