# Commons画像の取得と作品同一性チェック（2026-10-18）

## 共有台帳と画像実取得の結果

- 画像共通台帳：`data/image-sources.json` に計24点。うち16点は既存美術館アプリ由来、8点は追加でWikimedia Commonsのファイルを確認したもの。
- **24点とも実際にJPEGを取得し、SHA256を計算して保存**。既存16点は元アプリが記録したSHA256とも一致。
- 検証ログ：[GitHub Actions](https://github.com/matumaruex/kaiga-data/actions/runs/39104302015)
- ファイル配信元はCommonsの画像APIと、Commonsを由来として固定コミットに保存された公開GitHubミラー。シカゴ美術館のIIIF（403）には依存しない。
- **作品名と所蔵番号を対応させた**。別版の絵を誤って使う危険を下げるため、次回以降のデータ整合性チェックにも入れた。
- 調査対象19点のうち旧アプリと重なるのは11点。旧アプリにだけ存在する5点は画像出典を先に確保しているが、まだ共通の感情分析は行っていない。

## 今回新たに画像を取得した8点

| ID | 作品 | シカゴ所蔵番号 | Commonsのファイル | 実取得サイズ | SHA256の先頭 |
|---|---|---|---|---:|---|
| aic-869 | The Watermill with the Great Red Roof | 1894.1031 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:Meindert%20Hobbema%20-%20The%20Watermill%20with%20the%20Great%20Red%20Roof%20-%201894.1031%20-%20Art%20Institute%20of%20Chicago.jpg) | 194,911 B | `965d92306503` |
| aic-4575 | Judith | 1956.1109 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:Jan%20Sanders%20van%20Hemessen%20-%20Judith%20-%201956.1109%20-%20Art%20Institute%20of%20Chicago.jpg) | 277,169 B | `72dd789a65e6` |
| aic-4758 | Stoke-by-Nayland | 1922.4453 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:John%20Constable%20-%20Stoke-by-Nayland%20-%201922.4453%20-%20Art%20Institute%20of%20Chicago.jpg) | 293,399 B | `e47ed2634ea2` |
| aic-4796 | Fishing Boats with Hucksters Bargaining for Fish | 1922.4472 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:Joseph%20Mallord%20William%20Turner%20-%20Fishing%20Boats%20with%20Hucksters%20Bargaining%20for%20Fish%20-%201922.4472%20-%20Art%20Institute%20of%20Chicago.jpg) | 188,836 B | `e912bf9ac13b` |
| aic-14591 | Woman Reading | 1933.435 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:%C3%89douard%20Manet%20-%20Woman%20Reading%20-%201933.435%20-%20Art%20Institute%20of%20Chicago.jpg) | 506,272 B | `6a32eac233c0` |
| aic-16327 | The Annunciation | 1933.1062 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:Jean%20Hey%2C%20(the%20Master%20of%20Moulins)%20-%20The%20Annunciation%20-%201933.1062%20-%20Art%20Institute%20of%20Chicago.jpg) | 426,885 B | `3407ddfd8cf1` |
| aic-16551 | Beata Beatrix | 1925.722 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:Dante%20Gabriel%20Rossetti%20-%20Beata%20Beatrix%20-%201925.722%20-%20Art%20Institute%20of%20Chicago.jpg) | 353,588 B | `eedc5cee61b8` |
| aic-64729 | Early Morning, Tarpon Springs | 1911.32 | [画像と利用条件](https://commons.wikimedia.org/wiki/File:George%20Inness%20-%20Early%20Morning%2C%20Tarpon%20Springs%20-%201911.32%20-%20Art%20Institute%20of%20Chicago.jpg) | 316,194 B | `42e627b1de8a` |

## まだ未完了の確認

1. 新しい8点について、**作品の画面内容そのものを人の目で再確認**（意図しないトリミングや誤った画像を避ける）。所蔵番号と作品タイトルの記載は照合済み。
2. Commonsの各ファイルページに記載された個別の再利用条件・クレジットを、実際の配布形態で最終確認。
3. 第2群15候補の感情・背景・代替解釈は追加レビューを実施し、**14件を試験用登録、1件を刺激の強い描写のため保留**。[個別レビュー](review-report-batch-002-final.md)。人間による最終承認は未了。
4. 次の10〜20作品群は、人間による画像の最終視認・作品選定テストの基準が整理できてから進める。シカゴ所蔵という理由だけで画像を除外せず、**公式作品情報＋適切な公開画像源**を基本とする。

## 成功したこと／主張していないこと

成功したのは、画像のHTTP取得、JPEG形式、ハッシュ再照合、所蔵番号ベースの作品同定。
AI選定の品質、個別ファイルの日本法を含めた権利確認、すべての画像の鑑賞視認までは自動テストでは担保しない。
