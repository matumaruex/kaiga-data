# 絵画DB 250作品追加登録・検証結果（2026-10-20）

## 対象
- 登録済みの作品数：**250**（以前200＋第19群20＋第20群30）。
- Art Institute of Chicago 51点、Metropolitan Museum of Art 199点。
- 作品IDは250点すべて重複なし。画像台帳251件のうち250件は本登録作品、残り1件（aic-4575）は過去の保留候補。
- 登録250作品の画像URL、JPEGバイト数、SHA-256を画像台帳に保存・整合性検査済み。
- 感情15種類の主0～2、補助0～2と互換索引を維持。感情タグ0点の作品は62点。件数合わせに感情を付けていない。

## 新規追加50点の公式資料検証
- **第19群20/20**：Met Object APIで作品ID・原題・作者・絵画分類・PDの表示を確認。Met公式の主JPEGを完全ダウンロードしMIME、JPEG先頭・末尾、SHA-256で検証。参照：[実測GitHub Actions](https://github.com/matumaruex/kaiga-data/actions/runs/39299875231)、[結果JSON](batch019-online-result.json)。
- **第20群30/30**：同じ手順で30点すべて通過。参照：[実測GitHub Actions](https://github.com/matumaruex/kaiga-data/actions/runs/39301700290)、[結果JSON](batch020-online-result.json)。
- 画像の完全取得と所蔵館の公式作品IDを照合したことは、描写・美術史の人間による最終承認を意味しない。

## 古い保留候補を再評価した記録
- `met-438130`《The Departure of the Gondola》は第10群では「喜び・期待」の感情根拠不足で保留。
- 現在はタグ0件でも作品収録できるため、第20群で主0・補助0の**無タグ作品**として再評価。公式API・PD・画像SHAの独立した検証に合格した。
- 第10群の歴史的な保留情報は変更せず、`scripts/validate_batch010.py`に独立の証拠が揃う場合だけ認める対象限定のチェックを追加。

## 現行構造・分類の検証
- [250作品のデータ形式・旧候補との整合テスト](https://github.com/matumaruex/kaiga-data/actions/runs/39302574947) の `validate-format` は成功。
- [251件の画像再取得とSHA照合を含む同テスト](https://github.com/matumaruex/kaiga-data/actions/runs/39302574947) は別ジョブで実行する。実際の成功件数と結論はそのジョブの結果を優先する。

## 制限と継続課題
- 今回追加の作品情報・解釈・感情タグは暫定キュレーション分類。作者本人の意図・所蔵館の解説・鑑賞の感情との結び付きを混同せず保存。
- 250点すべての人間による作品画像目視や美術史的内容確認・公開時の画像権利の最終承認は未了。承認済みとの記録は付けない。
- 展示選定アルゴリズムや展示体験のテストは一切行っていない。
