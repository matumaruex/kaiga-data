# 200作品のデータ検証記録（2026-10-20）

## 対象と結論
- `data/artworks.json` に200件の作品を登録。ID重複なし、AIC 51件、Met 149件。
- `data/image-sources.json` は合計201件。200作品に加えて、作品DBに昇格していない `aic-4575` の保留候補1件を保持。
- 正本200作品の画像レコードは全てSHA256、バイト数、HTTPS URLが記録され、画像台帳と一致。
- 主0〜2・補助0〜2の感情タグ、15語彙、強度、制作意図と専門家の説明の区別、出典の必須項目について自動検証成功。
- 無タグ作品は33点。無理なタグを付けず収録を続ける方針に従う。
- **全201画像の実際のJPEG取得・SHA256一致は201/201成功。** 200作品以外の保留1画像も含む。
- 実際の展示、鑑賞者による感想、作品内容の人間の目視と解釈の公開承認は今回行っていない。

## 証拠
1. [201/201全画像HTTP取得とSHA256チェックの成功ログ](https://github.com/matumaruex/kaiga-data/actions/runs/39287755296) （2026-10-20 JST）。`verify-image-sources` が成功。JPEG群と JSON 検証結果の一時アーティファクトあり。
2. [18/18第18群のMet Object API・Primary JPEG検証](https://github.com/matumaruex/kaiga-data/actions/runs/39287755344) 。作者・原題・アクセッション番号・PD・絵画種別の確認に合格。公式の主画像のダウンロードとSHA256検証にも全件成功。`docs/batch018-online-result.json` に結果を保存。
3. [最新mainの形式・タグ・画像台帳を含む自動検査成功](https://github.com/matumaruex/kaiga-data/actions/runs/39288626038)。
4. [第17群の既存候補の先行調査](batch017-online-result.json) と [第18群再検証](batch018-online-result.json)。

## 修正点
- 第18群18点の暫定Met画像URLを、Object APIから取得した真の `primaryImageSmall` 公式JPEG URLに訂正。SHA256・バイト数・館蔵番号・制作年代・確認日を作品DBと画像台帳に反映。
- 第18群2点は厳密な文字列照合に差があった。 `met-436947` はÉdouard/Edouardというアクセント差。 `met-11417` はMet Object APIのclassificationが空欄だが、`objectName=Painting`, `medium=Oil on canvas` から絵画と確認。照合プログラムも根拠を確認する形に修正。
- `met-38056`『Panchama Ragini』：Met解説が関連する詩に満ち足りた幸福と愛情を明記しているため、根拠不足の暫定タグ0から『喜び』主3へ改訂（[所蔵館の作品解説](https://www.metmuseum.org/art/collection/search/38056)）。作品の心理と作者の感情、鑑賞者の反応を混同しない。

## 検証範囲と残る制約
- プログラム検証は、画像が取得でき、公式画像URLと作品の識別情報が結び付いていて、同じJPEGのSHA256が一致することを確認する。すべての絵画を人間が見て作品の取り違えや撮影状態を確認したという意味ではない。
- 最新のMet Object APIとの詳細再照合は今回追加の18作品で実施した。既存作品には先行のAPI検証記録があるが、全200点のメタデータを今回一斉に再調査したわけではない。
- 感情タグや作者の意図・制作背景の細部は資料に基づく暫定キュレーション判断。全作品を人間の美術史研究として最終承認したことを示さない。
- 作品のパブリックドメイン確認と、画像の公開利用条件の最終判断は区別する。
- 展示体験の試験と展示選定プログラムの実装は、この検証の対象外。
