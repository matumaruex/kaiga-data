# 美術館データの再開地点

## 現在の状態（2026-11-10時点）

- **完成登録：322作品**。正式数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：323作品目から候補調査**。以前の完成作品を再登録しない。
- 320〜322の新作品は `met-319625`（エチオピア）、`met-454054`（インド）、`met-860960`（朝鮮）。各作品の出典本文、画像、権利と解説の照合結果は作品別v2監査JSONに保存。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [共通v2基準](artwork-completion-workflow-v2.md) を守る。新規監査形式は `artwork-v2-new-registration-2`。
- 3作品のMet公式ページOverviewを直接読み、公式IIIF画像を目視。Met API配信の大小JPEGについて完全SHA256・バイト数とリサイズ一致をGitHub Actionsで確認。HTMLのオンライン再照合はMetによるHTTP制限があり保証しない。
- 過去319件の作品・元監査は不変。過去の出典追加照合は `docs/source-rechecks/` を参照。

## 過去の作業履歴

日付別の進捗・作品別の問題・PR・出典は [旧再開メモの全文](history/resume-artwork-work-through-2026-11-10.md) と [その後の更新履歴](history/resume-updates.md) に保管する。過去の「最新」「現行」は当時の状態を示す。
