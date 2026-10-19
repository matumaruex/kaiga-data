# 第11群：100 → 110作品、10点試験登録（2026-10-19）

## 調査結果と区別
Metの公式作品ページを読み、現行Object APIの作品ID・題名・帰属・作品種別・作品番号・PD状態、公式primary JPEG実取得とJPEG形式、SHA256、バイト数を照合。**10/10のAPI・画像実取得が成功し、10点を試験登録した**。確認詳細は[API・JPEG検証原票](batch011-online-result.json)、候補と分類は[候補履歴](../data/candidates-batch-011.json)。画像情報は共通台帳に同期。

人間による画像の最終目視、個別の解釈承認、公開時の権利審査は未了。顔が見える・色が正しいという人間の判断はHTTP/JPEG確認では証明できない。

## 作品別の根拠（作者の心理とは区別）

| 作品 | 主タグ／補助タグ | 作品を選ぶ根拠・注意 |
|---|---|---|
| [ダヴィッド《ソクラテスの死》](https://www.metmuseum.org/art/collection/search/436105) | 喪失感・希望／— | 哲学者の信念と弟子の悲嘆が交差。死そのものを肯定する推薦にはしない。 |
| [ホーマー《ガルフ・ストリーム》](https://www.metmuseum.org/art/collection/search/11122) | 不安／希望 | サメと暴風雨、帝国史と奴隷制の歴史。人物の内面は未確定。 |
| [バスティアン＝ルパージュ《ジャンヌ・ダルク》](https://www.metmuseum.org/art/collection/search/435621) | 希望／不安 | Metが作者の手紙を引用し、故郷を発つ決意を描いたと紹介する。原手紙の単独照合は未了。 |
| [サージェント《マダムX》](https://www.metmuseum.org/art/collection/search/12127) | 好奇心／不安 | 当初の右肩紐、1884年の酷評、修正と後年の作者の自負を分離。モデルの心情は推定しない。 |
| [フラゴナール《恋文》](https://www.metmuseum.org/art/collection/search/436322) | 好奇心／期待 | 花束と手紙が絵の外の物語を暗示。文字や結末を創作しない。 |
| [ブリューゲル《穀物の収穫》](https://www.metmuseum.org/art/collection/search/435809) | 安心／喜び | 仕事・食事・休息の景観。裕福な依頼主に合わせた理想化も重要。 |
| [曽我蕭白《天台山石橋図》](https://www.metmuseum.org/art/collection/search/53410) | 不安／好奇心 | 子獅子を試す伝承と仏教・道教的背景。生物学的な事実ではない。 |
| [作者不詳《山神と虎と従者》](https://www.metmuseum.org/art/collection/search/676034) | 好奇心／安心 | 朝鮮の山神信仰、仏教と土着宗教の融合。虎の図像を軽視しない。 |
| [八大山人《二鷹図》](https://www.metmuseum.org/art/collection/search/39540) | 怒り／希望 | 清への抵抗と明への忠誠というMetの読解。怒りは本人の直接証言ではない。 |
| [馬遠《高士観瀑図》](https://www.metmuseum.org/art/collection/search/40086) | 安心／好奇心 | 滝や樹木の動きと静かな文人の対照。心の治癒の作者意図は未確認。 |

## 機械的な確認と例外
- 公式Object APIと主画像JPEG：**10 / 10成功**、画像はSHA256・バイト数・取得先URLを記録。
- 《ガルフ・ストリーム》《マダムX》はAPIのclassificationが空欄。公式の`objectName: Painting`、`medium: Oil on canvas`、個別の館ページによって絵画と同定（元の空欄も調査原票に保存）。
- 記述の根拠は原則として個々のMet作品ページ。作品本人に関する発言と、所蔵館の解釈は`meaning_basis`内で区別。
- 感情タグは鑑賞者の入力との索引で、観客がどんな反応をするかの予言ではない。

試験登録100→110、画像台帳101→111。第10群の旧検証プログラムにある「ちょうど100点」の固定値は、過去群の検証条件を維持して最低100点の条件に変更。
