# 作業別ガイド

AI共通の入口は [AGENTS.md](../AGENTS.md)。通常の作業先は `main` を基準にした作業ブランチ。資料を読むだけで登録・検査・外部通信を自動実行しない。

| 作業 | 現行文書 | 実装・検査 |
| --- | --- | --- |
| 新規作品登録の再開 | [再開地点](resume-artwork-work.md) → [追加手順](artwork-expansion-v2.md) → [品質基準](artwork-completion-workflow-v2.md) | [add_artwork.py](../scripts/add_artwork.py) · [登録テスト](../tests/test_artwork_addition.py) |
| 既存作品の完成証拠 | [品質基準](artwork-completion-workflow-v2.md) · [旧登録経路の案内](artwork-registration-v2.md) | [complete_artwork.py](../scripts/complete_artwork.py) · [完成テスト](../tests/test_artwork_completion.py) |
| 出典本文・日本語解説 | [解説ガイド](visitor-explanation-guide.md) · [品質基準](artwork-completion-workflow-v2.md) | [verify_official_source_text.py](../scripts/verify_official_source_text.py) · [出典照合テスト](../tests/test_official_source_text.py) |
| 画像・作品同定 | [品質基準](artwork-completion-workflow-v2.md) · [追加手順](artwork-expansion-v2.md) | [verify_target_image_live.py](../scripts/verify_target_image_live.py) · [check_image_sources.py](../scripts/check_image_sources.py) |
| 感情タグ・データ形式 | [基本方針](data-policy.md) · [制作意図・タグの設計根拠](intent-first-curation.md) | [感情語彙](../data/emotions.json) · [validate_artworks.py](../scripts/validate_artworks.py) · [audit_coverage.py](../scripts/audit_coverage.py) |
| DB全体・既存作品の保護 | [基本方針](data-policy.md) · [品質基準](artwork-completion-workflow-v2.md) | [validate_artworks.py](../scripts/validate_artworks.py) · [check_catalog_snapshot.py](../scripts/check_catalog_snapshot.py) |
| 再開メモ更新 | [追加手順](artwork-expansion-v2.md) · [再開地点](resume-artwork-work.md) | [rotate_resume.py](../scripts/rotate_resume.py) · [再開メモテスト](../tests/test_resume_rotation.py) |
| 旧下書きの互換検査 | [旧方式の案内](visitor-draft-workflow.md) | [visitor_draft_queue.py](../scripts/visitor_draft_queue.py) · [互換テスト](../tests/test_visitor_draft_promotion.py) |

作品ごとの完成条件は品質基準が正本。データ・監査の正本は最新mainの実物。文書や過去のログだけで完成数を決めない。

## 検証

通常の構造・登録検査のコマンドは [Check artwork data](../.github/workflows/check-artworks.yml) が正本。Python 3.12を使い、リポジトリのルートから必要な検査を実行する。

- 新規作品は追加手順の preview → save → check と既存のCIを守る。作品内容・権利・出典本文・実画像の別工程審査は別に必要。
- `python3 -m unittest discover -s tests -p 'test_*.py'` は登録ガード等の自動テスト。
- 画像の対象別オンライン検査は `python3 scripts/verify_target_image_live.py --id <作品ID>`。出典本文のオンライン検査は追加手順に従う。ネットワーク接続が必要で、取得できない場合は成功扱いにしない。
- CIは変更パスと実行条件に依存する。MDだけの変更では通常のデータCIが起動しない場合がある。CI未実行と失敗を区別し、構造検査の成功を作品の内容・画像同定・公開権利の保証としない。

## 履歴・個別証拠

[履歴資料の目次](history/README.md) に分類している。過去の数値・承認・計画を現行ルールにしない。作品別監査や調査記録は証拠として必要な場合のみ読む。全履歴・全DBを一括で読み込まず、対象IDと必要な項目から調べる。
