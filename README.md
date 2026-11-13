# 絵画データベース

実在する絵画の資料・画像情報・鑑賞者向け日本語解説を管理するデータリポジトリ。展示アプリ本体は別リポジトリ。

## 登録状況

<!-- EXPANSION_COUNT_START -->
**v2完成登録：419作品**
<!-- EXPANSION_COUNT_END -->

登録数は最新 `main` の `data/artworks.json` を正本とする。DBへの登録と公開サイトへの反映は別。

## 作業を再開するとき

1. [現在の再開地点](docs/resume-artwork-work.md) — 完成数・次の着手・未解決事項
2. [新規作品の追加手順](docs/artwork-expansion-v2.md) — 候補調査、制作、登録
3. [作品の共通品質基準](docs/artwork-completion-workflow-v2.md) — 作品ごとの完成条件

作品データは `data/artworks.json`、画像台帳は `data/image-sources.json`、作品別の監査記録は `docs/artwork-completion-audits/`。登録・形式確認は `scripts/` と GitHub Actions で行う。

## 過去の記録

初期300作品の制作過程・日付別状況・当時の手順は以下に保管。現在の作業手順や登録数とは分けて参照する。

- [以前のREADME全体](docs/history/README-through-2026-11-10.md)
- [旧・完成運用ガイド](docs/history/artwork-completion-workflow-v2-through-2026-11-10.md)
- [以前の詳細な再開履歴](docs/history/resume-artwork-work-through-2026-11-10.md)
