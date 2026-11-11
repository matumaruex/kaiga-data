# 美術館データの再開地点

## 現在の状態（2026-11-11時点）

- **完成登録：380作品**。mainのDBとREADMEを正本とする。
- **次：381作品目から候補調査**。重複・個別の公式Overview本文・実画像と利用権利の照合を一点ずつ行う。
- 今回378〜380：`met-845805` 長澤蘆雪《月夜山水図》（日本1794〜95年）、`met-74661` 《走る象（表）・象の素描練習（裏）》（インド、コータ、18世紀半ば）、`met-45680` 蔣嵩（伝）《冬景山水図》（中国・明代）。
- 全件Met作品別OverviewをWebで直接確認し、二つずつの短い正確な英文を日本語鑑賞解説の主張と照合。Met API作品PD・Open Access CC0画像と美術館の現代解説文の権利を区別。原寸/表示JPEGの全SHA256・バイト数・画面サイズ・縮小RMS・画像目視も確認（[一次画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42976021314)、[別JPEGを再確認](https://github.com/matumaruex/kaiga-data/actions/runs/42976707754)、[長巻の画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42976227882)）。同じAIによる別工程の監査で外部専門家の査読ではない。
- `met-74661`は公式主画像が表側のみ、`met-45680`は7mの長巻の一部分のみであることを明記。`met-45680`の作者帰属は未確定。すでに登録済みの韓国作品と非PDのエチオピア作品は除外。
- 既存377作品と画像台帳の以前の部分は変更せず、[新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。

## 過去の作業履歴

日付別の進捗・作品別の問題・PR・出典は [旧再開メモの全文](history/resume-artwork-work-through-2026-11-10.md) と [その後の更新履歴](history/resume-updates.md) に保管する。過去の「最新」「現行」は当時の状態を示す。
