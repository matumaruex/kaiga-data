# 美術館データの再開地点

## 現在の状態（2026-11-10時点）

- **完成登録：326作品**。正式件数は最新 `main` の `data/artworks.json` で確認。
- **次：327作品目から候補調査**。重複IDと同作別画像を調べ、品質未満は保留。
- 324〜326作品：`met-764090` ペルー《楽園のアダムとエバ》、`met-77180` 日本《花魁図》、`met-701989` アメリカ《エマ・ヴァン・ネーム》。独自日本語解説・作品別v2出典監査を保存。
- 3件の公式作品解説と公式IIIF画像を確認。Met公式APIで原寸・表示用JPEG計6ファイルのSHA256、バイト数、寸法、縮小RMSを完全照合（[検証記録](https://github.com/matumaruex/kaiga-data/actions/runs/42805639776)）。同じAIによる別工程審査であり、外部の人間の鑑定ではない。
- 既存323作品と旧監査は変更せず、[新規登録ガイド](artwork-expansion-v2.md) と [v2完成条件](artwork-completion-workflow-v2.md) に準拠。GitHubの標準検査後にmainへ統合。

## 過去の作業履歴

日付別の進捗・作品別の問題・PR・出典は [旧再開メモの全文](history/resume-artwork-work-through-2026-11-10.md) と [その後の更新履歴](history/resume-updates.md) に保管する。過去の「最新」「現行」は当時の状態を示す。
