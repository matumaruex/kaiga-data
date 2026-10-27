# PR #3 の100下書きを新運用に引き継ぐ手順

この手順は原本に対して **読み取り専用**。本番DB、従来の制作・監査結果、PR #3の作業用ブランチを直接書き換えない。

出発点：2026-10-28時点のPR #3 コミット 3802b6bff4e71ec109e652fe5e1c9d8f821b9019。

## 基本ルール

- 監査記録の内容は **作品IDとその時の本文SHA-256** によって対応づける。表題や状態の「名前」の変更では未確認扱いに戻さない。
- 過去の文章監査100件と権利の予備確認100件は履歴として維持する。権利の予備確認は「57件優先／43件その他」で、**どれも権利クリアを意味しない**。
- 旧版と現行版の本文が違う場合、記録を捨てるのではなく、変更段落と関連する出典を重点的に再確認する。管理メタデータだけの差なら本文のやり直しは不要。
- Gitの旧コミットを読めない環境では差分を推測して合格を出さず、「以前の本文との直接比較不可」と記録する。
- 現在作業中の57件について、**未保存の作業経過を自動で復元することはできない**。担当作業の結果を追加のJSONとして残してから移行する。
- 人間の本文承認は必須にしないが、独立AI監査や権利・画像・出典の未確認を勝手に完了にしない。

## 確認コマンド

PR #3から派生した、このスクリプトと100下書き・監査ファイルが揃ったブランチで実行する。

    python3 scripts/legacy_review_checkpoint.py
    python3 scripts/legacy_review_checkpoint.py --write artifacts/review-checkpoint-v2.json
    python3 scripts/legacy_review_checkpoint.py --verify artifacts/review-checkpoint-v2.json
    python3 -m unittest discover -s tests -p 'test_legacy_review_checkpoint.py' -v

出力に含まれる changes_since_original_review に、変更段落、出典・証拠・管理メタデータの変更、再確認の対象が入る。履歴照合の結果だけで完成状態へ自動昇格しない。保存済みチェックポイントが古くなった場合、verify は失敗する。

## 今後の57件の作業結果を保存する形式

1件ごとに、例えば以下を追加し、過去のレポートを上書きしない。

    docs/visitor-content-audit-2026-10-27/rights-followups-v2/met-11140-01.json

ファイルの内容例（SHA値は実際の現在の下書きから計算する）：

    {
      "id": "met-11140",
      "draft_sha256": "実際の64桁のsha256に置換",
      "result": "checked_for_similarity",
      "review_scope": "公式解説と日本語本文、補助出典で実際に確認した範囲",
      "observations": "該当箇所と比較の内容・修正内容を具体的に記載",
      "source_urls": ["https://www.metmuseum.org/art/collection/search/11140"]
    }

result は checked_for_similarity / needs_revision / needs_more_evidence のいずれか。checked_for_similarity は実際に類似性を確認したという意味で、著作権侵害の不存在や公開許諾を判定したものではない。作業後に本文が再編集されても、旧版の記録として保存し、現行版に適用できる部分を確認する。

## 旧システム撤去の条件

最新PR #3に保存されている結果を漏れなく移行する → 100件の実データ照合と回帰テストを通す → 新しい独立AI監査と登録ガードを実装 → 美術館アプリの取り込み確認 → 最後に旧承認ゲートを廃止。

**この引き継ぎスクリプトは履歴保全と差分検出だけ。作品の事実確認・法的な権利判定・本番登録はしない。**
