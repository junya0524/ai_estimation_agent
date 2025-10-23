def make_decision_prompt(user_input):
    """
    システム開発コスト見積り手法（FP法／COCOMO法／LOC法）の選択をAIに判断させるためのプロンプトを生成する関数。
    user_inputは辞書型を想定。
    """

    prompt = f"""
あなたはIPAが定めるシステム開発見積りガイドラインを熟知した専門AIです。
以下の入力情報をもとに、どの見積り手法（FP法、COCOMO法、LOC法）が最適かを判断してください。

【判断基準（参考）】
- FP法：機能数・画面数・テーブル数など、論理的機能単位が明確な場合
- COCOMO法：開発規模（LOCやFP）が概算で分かり、工数見積りの補正式が必要な場合
- LOC法：コード行数ベースで単純な規模見積りをしたい場合

出力は **JSON形式** で返してください。以下の形式に厳密に従ってください。

{{
  "recommended_model": "FP" または "COCOMO" または "LOC",
  "reason": "なぜそのモデルを選んだかを100文字程度で説明"
}}

---

【入力情報】
- ファンクションポイント（FP）: {user_input.get('fp')}
- コード行数（LOC）: {user_input.get('loc')}
- 機能数: {user_input.get('functions')}
- 画面数: {user_input.get('screens')}
- テーブル数: {user_input.get('tables')}
- アプリケーション種別: {user_input.get('application_type')}
- 複雑度: {user_input.get('complexity')}
- チーム経験: {user_input.get('team_skill')}
- 総労働時間: {user_input.get('work_hours')}

判断の根拠には、入力項目のどれが影響したかも触れてください。
"""

    return prompt
