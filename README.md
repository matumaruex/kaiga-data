# 絵画データベース

実在する絵画の資料・画像情報・鑑賞者向け日本語解説を管理するデータリポジトリ。展示アプリ本体は [お前の美術館](https://github.com/matumaruex/omaenobizyutu/tree/codex/museum-preview)（別リポジトリ）。

## 登録状況

<!-- EXPANSION_COUNT_START -->
**v2完成登録：482作品**
<!-- EXPANSION_COUNT_END -->

登録数は最新 `main` の `data/artworks.json` を正本とする。DBへの登録と公開サイトへの反映は別。

## 作業を再開するとき

AI向けの共通作業指示は [AGENTS.md](AGENTS.md) にあります。進捗・登録手順・品質基準は以下の文書が正本です。

1. [現在の再開地点](docs/resume-artwork-work.md) — 完成数・次の着手・未解決事項
2. [新規作品の追加手順](docs/artwork-expansion-v2.md) — 候補調査、制作、登録
3. [作品の共通品質基準](docs/artwork-completion-workflow-v2.md) — 作品ごとの完成条件

作品データは `data/artworks.json`、画像台帳は `data/image-sources.json`、作品別の監査記録は `docs/artwork-completion-audits/`。登録・形式確認は `scripts/` と GitHub Actions で行う。

その他の作業（画像・出典の再検証、既存作品の監査、検査コードなど）は [作業別ガイド](docs/README.md) へ。

## 過去の記録

[履歴資料の目次](docs/history/README.md) から必要な資料を探す。過去の件数・承認方式・計画は現行の作業指示ではない。
