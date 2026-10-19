# 250作品・作品解釈と感情タグの内容監査（一次評価・2026-10-20）

## 結論と監査範囲

- 対象正本：`data/artworks.json` の登録250件（AIC 51 / Met 199）。作品・画像の技術的整合性と内容解釈の妥当性は別に評価した。
- 全250件について、登録された感情区分・作者本人の言葉の状態・出典フィールド・主題・検索プロフィールを横断的に点検。
- **31件の異なるMet公式作品ページの本文を個別に照合**（第19〜20群の重要例および先行登録の作者発言例）。ページの実表示から確認できた範囲を下記の参照URLで記録。全250作品を公式の長文研究カタログまで個別精査したわけではない。
- **全作品を美術史的に最終承認したとは扱わない。** `review.interpretation_human_approved=false` の250件はそのまま。画像の肉眼照合と人間2人による受け取り方の採否はこの監査で置き換えない。
- 今回は**調査報告と具体的変更案のみ**を新規文書に保存。作品・感情タグ・既存ルール・選定プログラムはいっさい変更しない。固定指示に従い、下記の作品データ修正は利用者承認があるまで未反映。

## 横断点検の結果（警告と誤りを区別する）

| 項目 | 集計と意味 |
| --- | --- |
| 作品登録 | 250件。画像の実ダウンロード・SHA256検証の成功は別途既存のGitHub Actionsで確認済み。 |
| 感情タグ0件 | **62/250件**。無理な分類はしていない。感情タグ索引だけの一次抽出には入らない。これは仕様通りであり、不良作品数を意味しない。 |
| 作者の当該作品への本人発言「直接」 | **15件**（データの `direct_for_this_work` 状態）。15件全部の一次資料を今回再検証したわけではない。 |
| 当該作品に限らない作者発言 | 関連モチーフ・連作6件、関連する芸術理念2件。個別作品への直筆発言と混ぜない。 |
| 作者本人の当該作品への発言が未確認 | **227件**（データ上の `not_verified_for_this_work`）。価値が低いことや、作者の意図が存在しないことを意味しない。 |
| `scholarly_interpretation.summary` と `source_context_note` の文面が完全一致 | **96/250件**。新規50件は**50/50件**が一致。出典本文の独立照合が不十分な可能性を優先精査すべき「構造上の警告」であり、96件が虚偽だと証明したわけではない。 |
| 最終解釈の人間承認 | **0/250件**。現行の暫定状態が適切。 |

上記96件では、専門家の独立した解釈と制作背景が同じ短文を共有するため、根拠の強さを区別しにくい。特に、公式ページに作品解説本文がなく作品メタデータしか載っていない場合、単純な題名説明を「美術館研究による解釈」と呼ばないよう再整理が必要。

## 重要度A：事実の帰属と歴史的主題の訂正案（所蔵館ページで確認）

1. **`met-57280`《Mother and Children in Summer Night》：作者帰属を訂正。** 現在 `facts.artist=`「Katsushika Hokusai」。Met公式作品ページは **「School of Katsushika Hokusai」** と表示。APIの簡略な作者名と、美術館ページの帰属の確実性を区別すべき。**修正案：`facts.artist` を「School of Katsushika Hokusai」に変更**し、概要にも「北斎派」であって北斎本人作と断定しない。出典：https://www.metmuseum.org/art/collection/search/57280
2. **`met-437412`《Old Woman Cutting Her Nails》：作者帰属を訂正。** 現在 `facts.artist=`「Rembrandt (Rembrandt van Rijn)」。Metの現行公式表記は **「Style of Rembrandt (Rembrandt van Rijn)」**。過去にはレンブラントの作品とされたが現在は帰属が未確定。**修正案：`facts.artist` を「Style of Rembrandt (Rembrandt van Rijn)」**に訂正。出典：https://www.metmuseum.org/art/collection/search/437412
3. **`met-437286`《The Death of Harmonia》：歴史画を神話画と誤記。** 現在の本文に「歴史・神話画」、`visual_clues` に「神話の死」がある。Met公式によれば、**紀元前2世紀の王位継承・殺人・道徳的な自己犠牲をめぐる古代史の逸話**であり、神話として説明していない。**修正案：宗教・神話の推定を削り、史実と伝承の区別をした「古代史を題材にした悲劇的歴史画」へ訂正。** この絵を機械的に喪失感へ分類する必要はない。出典：https://www.metmuseum.org/art/collection/search/437286

## 重要度B：作者の証言と作品の背景を正確に補う案

4. **`met-670896`《Plum Blossoms》：作品に書かれた作者の言葉の取りこぼし。** 現在 `author_intent.status=not_verified_for_this_work`。Met解説は**没倫紹等自身の画賛**に、牡丹やジャスミンより梅が春の表現にふさわしい、という主張が記されていると説明。墨の円環は空と形の仏教的意味を表す可能性にも触れる。**修正案：画賛を「当該作品への本人の言葉」として出典付きで記録**する。作者本人の「喜び・希望」の心理だとは断定せず、感情タグ0件は維持する。出典：https://www.metmuseum.org/art/collection/search/670896
5. **`met-438130`《The Departure of the Gondola》：題名以上の社会的・季節的文脈が不足。** Metは白い仮面と黒い覆いから**カーニバル季節**を特定し、青白い制服の二人が当時ヴェネツィアの**奴隷にされた人々と自由身分の有色人種の労働史**に関連すると明記する。現DBは「ゴンドラが出発する18世紀の油彩」としか記録していない。**修正案：この史的文脈を専門的解釈・制作背景・選定上の注意に追加。** 無タグは維持してよい。出典：https://www.metmuseum.org/art/collection/search/438130
6. **`met-857030`《The avatar Narasimha》：制作・流通の実際の文脈が抜けている。** Metは19世紀カルカッタの**カーリーガート絵画**、寺院の巡礼者向けの低価格な宗教画という制作・販売背景を詳述。DBには「ヴィシュヌ神の人獅子の化身」しかない。**修正案：巡礼土産としての歴史的機能を`creation_context`と専門的解釈に追加。** 「畏敬」を自動削除する必要はない。出典：https://www.metmuseum.org/art/collection/search/857030
7. **`met-437479`《The Return of the Cattle》：牧畜主題の説明に偏っている。** Metの力点は**下描きのような未完成感を意図的な美学として採ったこと、ディドロの批評、ブーシェの人物図像の転用**にもある。**修正案：絵画技法と同時代の批評を追加**。無タグはそのまま。出典：https://www.metmuseum.org/art/collection/search/437479
8. **`met-437439`《A Young Girl with Daisies》：関連した作者発言が既に解説にある。** Metは1888年にルノワールが画商へ送った「柔らかく軽い画風への回帰」に関する発言を紹介。DB本文はそれに触れている一方、`author_intent`は`not_verified_for_this_work`。**修正案：個別作品そのものへの直接発言とはせず`related_artistic_program`として記録**。出典：https://www.metmuseum.org/art/collection/search/437439

## 重要度C：感情タグの強度と根拠を再判定する候補

9. **`met-436801`《The Marriage Feast at Cana》主「希望」強度2**：Metは婚礼での奇跡を説明するが、DBの「救い」という心理的解釈は出典から自明ではない。関連が絶対に不適切とは言えないので、**「なぜ希望への入口として自然か」を作品固有に説明する**か、根拠が薄ければタグなしへ移す候補として検討。出典：https://www.metmuseum.org/art/collection/search/436801
10. **`met-437638`《The Marriage of Cupid and Psyche》補助「期待」強度1**：Metは神々を伴う婚礼を説明するが、「結婚したから期待」というだけでは現在の基準には弱い可能性がある。**補助「期待」の根拠を描写・主題から追加できなければ削除する案。** 主「喜び」は婚礼という具体的な場面との関連を保留不要。出典：https://www.metmuseum.org/art/collection/search/437638
11. **`met-57280`《Mother and Children in Summer Night》主「慈しみ」強度2**：現Met作品ページは作者・題名・材質のみで**詳しい作品解説本文がない**。現DBの`visual_clues`も「母親と子どもたちの様子」という一般記述にとどまる。親子が並ぶだけで保護・いたわりの表現と決めない。**実画像の細部を確認して維持／補助格下げ／削除を選ぶ**。根拠がないと断定する段階ではない。出典：https://www.metmuseum.org/art/collection/search/57280

## 現状維持が妥当と判断できる根拠付きの例

- **`met-45805`《Mother and Children at the New Year》：主「喜び」補助「慈しみ」**。Metが正月の遊びと子どもの身振りを具体的に解説。色や「家族」という言葉からの短絡ではない。 https://www.metmuseum.org/art/collection/search/45805
- **`met-74996` ジャイナ教絵画：主「慈しみ」補助「不安」**。動物の叫びが主人公の憐れみと出家の決断を導くことがMetに明記されており、具体的な接点がある。 https://www.metmuseum.org/art/collection/search/74996
- **`met-436678`《The Visit》主「好奇心」**。牡蠣・天蓋付き寝台が一見普通の室内を別の意味に変える根拠をMetが示す。好奇心は単なる「作者の研究心」ではなく画面固有の手掛かりに接続。 https://www.metmuseum.org/art/collection/search/436678
- **`met-906843`《Kannon by a Lotus Pond》の白隠本人の画賛**はMetが実際に翻刻し、1754年ごろの書簡とその社会的意味も説明している。出典のレベル区別は現在のまま維持できる。 https://www.metmuseum.org/art/collection/search/906843
- **`met-49001`《Cherry Blossoms at Yoshino》の頼山陽本人と母の画賛の区別**はMet作品ページに根拠がある。 https://www.metmuseum.org/art/collection/search/49001

## まとめと次の編集のための承認事項

優先順位は**Aの帰属・歴史画説明3点の誤り訂正 → Bの作品固有の意味・本人発言5点の補強 → Cのタグ3件を人間の判断で検討**。

この文書では修正案を具体化したが、`data/artworks.json`、既存のタグや方針文書は変更していない。GitHub固定指示にある「変更案を先に提示・承認を得てから修正」を守る。承認された案のみ後続コミットに反映する。展示体験・選定ロジックのテストは今回の対象外。
