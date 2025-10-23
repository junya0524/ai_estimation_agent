def make_decision_prompt(user_input):
    return f"""
あなたはシステム開発コスト見積もりの専門AIです。
以下の入力情報をもとに、どの手法（FP法、COCOMO法、LOC法）が最適かを判断してください。
出力フォーマットはJSON形式で、以下のように出してください。

{{
  "recommended_model": "FP" または "COCOMO" または "LOC",
  "reason": "なぜそのモデルを選んだか説明"
}}

入力情報:
{user_input}
"""
