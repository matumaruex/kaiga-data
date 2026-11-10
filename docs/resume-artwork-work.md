# 美術館データの再開地点

## 現在の状態（2026-11-10時点）

- **完成登録：323作品**。正式数は最新 `main` の `data/artworks.json` とREADMEを確認する。
- **次：324作品目から候補調査**。既存の完成作品を再登録しない。
- 323番目は `met-435991`（Camille Corot, *A Woman Reading*, 1869 and 1870）。Metの作品別Overviewと公式画像を照合し、独自日本語解説・v2監査に登録。
- Met APIの原寸／表示JPEGを完全SHA256・サイズ・縮小RMSで照合（[GitHub Actionsの検証](https://github.com/matumaruex/kaiga-data/actions/runs/42802438308)）。同AIの別工程審査であり人間の外部審査ではない。
- 既存322件と各監査は不変。323件目は登録プログラムと全体検査に合格。一時検証ワークフローは撤去済み。次は [追加ガイド](artwork-expansion-v2.md) と [共通基準](artwork-completion-workflow-v2.md) に従う。

## 過去の作業履歴

日付別の進捗・作品別の問題・PR・出典は [旧再開メモの全文](history/resume-artwork-work-through-2026-11-10.md) と [その後の更新履歴](history/resume-updates.md) に保管する。過去の「最新」「現行」は当時の状態を示す。
