# 第17・18群：200作品の公式情報と画像検証（2026-10-20）

- **共有作品数200点（追加36点）**。元の164点に変更・削除なし。
- 第17群から18点：既存の公式Object API・PD・画像JPEG SHA256検証結果と登録データが一致。出典：docs/batch017-online-result.json。
- 第18群から18点：GitHub Actionsの読み取り専用再検証で公式Met Object APIと対応するprimaryImageSmall JPEGを**18/18件実取得しJPEG署名・末尾・MIME・バイト数・SHA256照合成功**。出典：docs/batch018-online-result.json。
- 個別の機械判定例外2件：met-436947（Édouard ManetのアクセントはMet APIでEdouard Manet）とmet-11417（Met API classification空欄。ただしobjectName=Painting、medium=Oil on canvas）。絵画として妥当で、記録にも残した。再検証コードはアクセント差・class空欄と他フィールドの確認を区別。
- 200点のデータ構造・検索タグ・画像台帳とSHA256の参照整合をチェック。GitHubの既存全体自動テストと全画像の現時点再取得は別。
- **作者の個別制作意図・専門的解釈・感情との関連は別々に扱う。** 関連づけは暫定判断で、人間による作品画面と内容の最終確認・権利の公開判定は未了。展示体験の試験は今回実施しない。
- 200点の画像を毎回ライブで読み込んだという主張はしない。既存作品の画像SHAの記録と新規18点の取得実測を区別。

公式Met APIの作品ごとのタイトル・作者・制作年・館蔵番号・分類・画像URL・SHA256は新しい検証結果に追従して更新。

## 追加の内容検証

- met-38056『Panchama Ragini』：Met公式作品解説は関連詩に「満ち足りた幸福と愛情」を明記。タグ0から『喜び』主3へ根拠付きで改訂。作者本人の感情と混同しない。作品の人間審査は未了。出典：https://www.metmuseum.org/art/collection/search/38056
- 第18群の再実行は全18点の公式メタデータ・公式主画像JPEG照合に合格。証拠：https://github.com/matumaruex/kaiga-data/actions/runs/39287755344
