# 2026-11-10 新規登録3作品の共通検査メモ

- 対象: met-871866 池田蕉園《手習い》、met-827660 クララ・ペーテルス《花束》、met-436875 マリー・ヴィクトワール・ルモワーヌ《女性画家のアトリエ》
- 既存301作品の内容は変更せず、新規3作品を個別の v2 監査・独自日本語本文・画像台帳とともに追加する。
- Met公式Object APIのID・作者・所蔵番号・作品本体Public Domainと、Met Open Access画像CC0を分けて確認。2026-11-10の画像確認はGitHub Actions [run 42750863200](https://github.com/matumaruex/kaiga-data/actions/runs/42750863200)。
- original/web-large JPEGの全量SHA256・寸法と縮小画の一致を検証。原図の主題はMet公開図版と視覚照合。各作品の細かな根拠と同一AI別工程検証の限界は個別JSON監査に保存。
- 登録は `scripts/add_artwork.py preview → save → check` を1作品ごとに実行し、302→303→304を確認。別モデル・人間専門家の独立検証を実施したとは記載しない。
- プログラムの本番適用は、このPRの「Check artwork data」と「Check visitor explanation drafts」両系統CI成功と、`main` 統合後に確定。美術館アプリへの表示・配信は未確認。
