# 通常チャット用：鑑賞者向け解説の下書き・再開手順

## 目的

既存の解説40件（2026-10-21時点）は変更せず、未作成分を追加する。以後は必ず最新のDBを数え直す。

通常チャットが1回の応答内で何件制作できるかは保証されない。**5件ごとにGitHubの作業ブランチへ別ファイルで保存**し、途中で止まっても次のチャットで「続き」から再開できるようにする。Codex・有料AI APIは不要。この補助プログラム自体はAIを呼び出さず、チャット終了後に自律的に解説を増やすものでもない。

## 作業順

1. 最新の `main` と編集中のPR/ブランチを確認する。既存の下書きブランチがあれば再利用。
2. `python3 scripts/visitor_draft_queue.py status`：DB登録済み、下書き、未作成を数える。
3. `python3 scripts/visitor_draft_queue.py next --size 5`：未作成・未下書きの5件を抽出。所蔵館、時代、主題と公式資料の十分さを見て採用・差し替える。出力した参考URLは**未照合**。
4. 通常チャットで**作品ごとに**所蔵館の公式説明や専門資料を直接参照。史実と作者の証言、研究者の解釈、絵の描写、未確認事項を区別。既存の検索用`meaning_basis`を引き延ばして代用しない。感情の誘導や決まりきった結語、文字数の固定をしない。
5. 各作品について`drafts/visitor-explanations/<作品ID>.json`を作業ブランチに追加。1件ごとに出典の該当箇所を根拠メモとして保存。未確認は未確認と記録。
6. 5件保存ごとに`python3 scripts/visitor_draft_queue.py check`相当の形式検査を行い、次の5件へ進む。可能な範囲でまとめて実行する。ChatGPT側の時間制約・ツール許可があれば途中で止まる場合がある。
7. 下書きPRで後からまとめて確認できる。本番`data/artworks.json`には**承認まで書き込まない**。現行`docs/visitor-explanation-guide.md`の10件ごとの報告・承認ルールは、正式な変更承認があるまで維持する。
8. 承認された対象のみ、ローカルで`python3 scripts/visitor_draft_queue.py promote --ids <id1> <id2> --approved`。差分と`scripts/validate_artworks.py`を検証した後にDBへPRをマージ。スクリプトにはGitHubへの自動push機能はない。

### 下書き形式（**データ構造の例であり、実作品の解説ではない**）

```json
{
  "id": "met-12345",
  "visitor_explanation": {
    "language": "ja",
    "text": "原資料を確認して作成した日本語の作品解説",
    "source_urls": ["https://www.metmuseum.org/"],
    "review": {
      "content_status": "pending",
      "source_status": "pending",
      "rights_status": "pending",
      "reviewed_on": "2026-10-21"
    }
  },
  "evidence": [
    {
      "claim": "本文中の根拠が必要な主張",
      "source_url": "https://www.metmuseum.org/",
      "source_location": "原資料の対応する段落や見出し。確認できないなら、その旨を記す",
      "checked_against_source": false
    }
  ]
}
```

形式検査の「OK」は史実の正しさ、出典に主張が存在すること、著作権条件を保証しない。作業中に資料不足が判明したら、その作品は数合わせせず保留する。本人の言葉と専門家の読みの取り違えに特に注意する。

## チャットを替えたときの指示

「美術館の解説の続き。GitHubの`matumaruex/kaiga-data`の下書きPRと最新の`data/artworks.json`を確認して、未作成だけを原資料と照合し、5件ごとに下書き保存して進めて」

保存済みの解説やステータスを、前の会話だけを根拠に再制作・更新しない。新しい作業ブランチを無断で増やさない。
