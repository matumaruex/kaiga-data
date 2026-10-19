# 第19群：200→220作品の登録と検証（2026-10-20）

- 公式Met Object APIで作品ID・原題・作者・制作年・所蔵番号・Paintings分類・Public Domainフラグを20/20照合。
- Met公式 primaryImageSmall JPEGを20/20実際にダウンロードし、Content-Type、JPEG先頭・末尾、byte length、SHA-256を記録。
- 出典：https://github.com/matumaruex/kaiga-data/actions/runs/39299875231
- 既存の200作品に変更・削除なし。重複IDを拒否し、画像出典台帳も同時に追加。
- 第19群20作品は作品説明と選定タグの仮分類を登録。作者本人の制作意図は確認できない限り `null` を保ち、個別の美術館説明と区別。
- `curation.emotion_categories` は主0～2・補助0～2を維持。タグ0作品は無理に分類しない。
- 全20点の最終目視・美術史的精査・公開時の権利の最終承認は実施していない。展示体験は対象外。
