# 第7群：感情・地域・時代の偏りを減らす研究と登録結果（2026-10-18）

## 最終結果：51 → 60作品

- The Metropolitan Museum of Artの**11候補すべて**を現行公式Open Access Object APIで再照合。作品ID・作品名（空白の差は正規化）・所蔵番号・画家／作者未詳・Public Domain・Painting分類（サージェントの1件は分類欄が空のため公式ページの「Oil on canvas」を確認）を11/11確認。
- **公式APIのprimaryImageSmall URLのJPEGを実際に11/11取得**。HTTP、JPEGシグネチャ、バイト長、SHA256を[検証レポート](../docs/batch007-online-result.json)に記録。再現可能な検証コード：[scripts/research_batch007.py](../scripts/research_batch007.py)。
- **9作品を試験用登録、2作品を保留**。データベースの試験登録は**60作品／100目標（残り40）**。画像台帳は登録60作品＋旧保留『Judith』1件で**61件**。
- The Metの[Open Access / CC0方針](https://www.metmuseum.org/hubs/open-access)と、各作品のPublic Domain表示を確認。画像の直接表示は個別所蔵品番号に紐づく公式APIから検出。
- **最終的な人間の画像視認や展示での組版・公開承認は未実施**。画像の実取得・チェックサムは画題や感情の美術史的解釈まで保証しない。

## 今回登録した9作品

| 作品（公式ページ） | 地域・時代 | 主タグ | 感情と作品がつながる根拠／注意 |
|---|---|---|---|
| [小林清親『頼豪阿闍梨図』](https://www.metmuseum.org/art/collection/search/749407) | 日本、1900年頃 | 怒り | 破られた約束への頼豪の激怒。儀礼の秩序が崩れる構図が見える。**画家自身の怒りではない**。 |
| [顧洛『空房對月圖』](https://www.metmuseum.org/art/collection/search/737735) | 中国、1829年 | 喪失感 | **画家の画賛が哀悼の詩を参照**。作者が身近な人と死別したかは不明。 |
| [作者未詳『風流踊図屏風』](https://www.metmuseum.org/art/collection/search/816203) | 日本、1660年頃 | 喜び | 武家屋敷の庭で踊る文化的な楽しさ。**四曲屏風**で鑑賞の方向は右→左、主画像だけで細部をすべて捉えたとはいえない。 |
| [賢江祥啓『山水図』](https://www.metmuseum.org/art/collection/search/42346) | 日本、1478–80 | 安心 | 世俗を離れた静けさの画賛。ただし**詩を書いた桃源瑞仙は画家とは別人**。孤独の苦しみとは扱わない。 |
| [童鈺『浸月圖』](https://www.metmuseum.org/art/collection/search/73161) | 中国、18世紀 | 安心 | **作者本人の詩**が雪後の静けさと梅を語る。根拠のない『懐かしさ』補助タグは削除。 |
| [作者未詳『恋人のもとを去る女性』](https://www.metmuseum.org/art/collection/search/74692) | インド、1790–1820年頃 | 未練 | 美術館の別離の苦しみという説明を主な接点とする。ただし再会希望・後悔の明言はなく、**主タグは暫定的な検索索引**。 |
| [デヴィダサ『口論で仲違いした恋人たち』](https://www.metmuseum.org/art/collection/search/37941) | インド、1694–95 | 不安 | 半開きの戸と暗い門で関係の亀裂を表す。**怒りは数合わせで付けない**。 |
| [サージェント『隠者』](https://www.metmuseum.org/art/collection/search/12110) | 米国、1908 | 安心 | 本人が館長宛に宗教的連想より**静けさ・汎神論**を望んだと明言。Met APIの`classification`は空値だが公式ページの`Oil on canvas`でPainting作品と判断。 |
| [サモジェ『湖畔の亭』](https://www.metmuseum.org/art/collection/search/40429) | 韓国、18世紀後期 | 安心 | 朝鮮の文人画に由来する落ち着いた構成。作者個人が安らぎを感じていたという意味ではない。 |

## 保留した2作品

1. [尾形光琳『八橋図屏風』](https://www.metmuseum.org/art/collection/search/39664)：**二隻一対の六曲屏風**。Metの主画像1件のHTTP/JPEG/SHA256までは成功したが、左右両方の画像と並びを特定して統合するまで試験登録しない。文学の人物の郷愁を画家本人の未練とは扱わない。
2. [作者未詳『官僚たちの集い』](https://www.metmuseum.org/art/collection/search/851420)：Metの画像・作品情報は合格。ただし官僚の会合を記録する性格が強く、既存分類の「安心」「喜び」に十分直接結びつくとまでは判断しにくい。無理にタグを振って収録しない。

## 主タグの前後比較

| 主感情 | 第6群終了 | 第7群終了 | 差分 |
|---|---:|---:|---:|
| 好奇心 | 24 | 24 | 0 |
| 怒り | 0 | **1** | +1 |
| 喜び | 1 | **2** | +1 |
| 喪失感 | 5 | **6** | +1 |
| 未練 | 2 | **3** | +1 |
| 不安 | 7 | **8** | +1 |
| 安心 | 8 | **12** | +4 |
| 寂しさ | 0 | **0** | 0 |
| 期待 | 1 | **1** | 0 |
| その他：懐かしさ／孤独／希望 | 2／2／4 | 2／2／4 | 0 |

「好奇心」主タグの割合は24/51（47%）→24/60（40%）に減少。ただし「安心」の増加もあるため完全なバランスではない。地域も新しく東アジア・インドに広げられたが、ほかの地域と時代は引き続き不足。

## 技術メモ

- 登録済データ：[data/artworks.json](../data/artworks.json)。
- The Metの画像出典・SHA：[data/image-sources.json](../data/image-sources.json)。
- 検証詳細（11件分）：[docs/batch007-online-result.json](batch007-online-result.json)。
- 候補履歴（9登録・2保留）：[data/candidates-batch-007.json](../data/candidates-batch-007.json)。
- 画像ID形式を`aic-{ID}`（シカゴUUID）と`met-{ID}`（Met primary画像）で分け、各館のIDを混ぜない。既存51件のデータ内容・SHAは変更していない。
- The Metの`isPublicDomain=true`と作品のPainting判定は、現在のAPIを根拠とする。第7群は`image.visual_checked=false`、`interpretation_human_approved=false`の試験登録。正式公開には画像を鑑賞して個々の作品の主題・表示・権利を確認する。

## 次の優先事項

- 像を見た人の怒りが明確な非宗教画、生活に由来する寂しさ、達成の喜び、期待を作者の言葉や美術館の研究から探す。神話の暴力から怒りと決めつけない。
- 作品が多い19世紀フランスとモネへの偏りをさらに減らし、現代・異なる地域や文化圏・女性作家などの公開可能な作品を調べる。
- 展示体験・本番のAI選定は約100作品になるまで行わない。
