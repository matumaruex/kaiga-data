# 絵画データベース

実在する絵画の作品情報と、気持ちに合わせた展示のための**試験的な解釈データ**を管理する、2人で共有するデータリポジトリです。美術館アプリ本体のデザインや3D空間はここに置きません。

## 初回登録（2026-10-18）
- **4作品**を `data/artworks.json` に登録（pilot-001）
- **出典**：Art Institute of Chicago（シカゴ美術館）の作品API
- 4作品とも公式APIで `is_public_domain: true`、作品種別 `Painting`、`image_id` を確認した
- 画像URLは美術館のIIIF公式仕様で組み立てた。**ブラウザでの実表示・HTTP到達性は未検証**
- 作品の感情との結び付けは**キュレーション上の仮説**であり、作者の意図を確定したものではない
- 日本語作品名は便宜的な訳で、公式名称とは限らない
- 感情タグの**人間による承認はまだ行っていない**。レビュー後に拡大する

## ファイル
- `data/artworks.json`：作品ごとの出典・事実・画像・解釈・レビュー状態
- `data/emotions.json`：感情（emotions）／空気感（tones）／主題（themes）の分類
- `scripts/validate_artworks.py`：重複・ID・タグ・必須項目などをローカル検証
- `docs/review-guide.md`：追加の前に確認するレビュー手順

## 検証
```bash
python3 scripts/validate_artworks.py
```
※この検証は形式チェック。画像の疎通確認や美術解釈の良し悪しまで保証しません。

## 出典と画像
作品ごとに `source.api_url` と `source.artwork_url` を記録しています。作品画像はGitHubに大量保存せず、Art Institute of ChicagoのIIIF画像配信サービスを参照します。

- [Art Institute of Chicago API](https://api.artic.edu/docs/)
- [利用規約](https://www.artic.edu/terms)
- 作品の元データは出典APIの条件に従い、説明文の転載ではなく独自の短い日本語分析を書いています。

公開条件は**作品と画像を区別**して確認してください。将来、他館の画像を追加する場合は各館の条件を再確認します。

## 段階的に増やす方針
1. pilot-001（4作品）：形式とレビュー方法を確認
2. レビューで課題を修正
3. 次の10〜20作品で感情の幅を増やす
4. 実際の入力文による選定テストを実施
5. 合格した品質基準に従い50→100作品と拡張する

**大量追加の前に、利用者の許可を取る。**
