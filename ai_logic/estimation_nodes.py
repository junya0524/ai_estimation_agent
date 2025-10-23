import os
from openai import OpenAI
from dotenv import load_dotenv
from estimation.fp_model import estimate_fp
from estimation.cocomo_model import estimate_cocomo
from estimation.loc_model import estimate_loc

# ==== 環境変数のロード ====
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==== LangGraph用ノード ====
def ai_estimation_node(state):
    """
    LangGraphのメインAI見積もりノード。
    入力されたIPA要素を基に、AIが推定・提案・評価を行う。
    """
    user_input = state.get("user_input", {})

    # --- モデル選択プロンプト ---
    decision_prompt = f"""
あなたはシステム開発コスト見積もりの専門AIです。
以下の情報をもとに、どの手法（FP法 / COCOMO法 / LOC法）が最も適切かを判断してください。
出力形式はJSONで：
{{
  "recommended_model": "FP" または "COCOMO" または "LOC",
  "reason": "選択理由（100文字程度）"
}}

入力情報:
{user_input}
"""

    decision = client.responses.create(
        model="gpt-4o-mini",
        input=decision_prompt,
        temperature=0.3,
    )

    # JSON部分の抽出
    model_choice = decision.output_text.strip()

    # --- 実際の見積もり実行 ---
    model = "FP"
    if "COCOMO" in model_choice:
        model = "COCOMO"
    elif "LOC" in model_choice:
        model = "LOC"

    if model == "FP":
        result = estimate_fp(3, 2, 1, 4, 2)
    elif model == "COCOMO":
        result = estimate_cocomo(10, "organic")
    else:
        result = estimate_loc(2000)

    # --- AIによる3つの評価 ---
    analysis_prompt = f"""
あなたは見積もりAIの分析担当です。
以下の開発条件に基づき、3つの観点から分析を行ってください：

1. 類推法（過去類似プロジェクトや業界平均を踏まえた推定コメント）
2. 開発規模提案（機能過多・不足に関する提案）
3. 重み付け評価（主要因と重みをJSON形式で）

出力フォーマット：
{{
  "類推法": "〜〜〜",
  "開発規模提案": "〜〜〜",
  "重み付け評価": {{
    "複雑度": 数値,
    "チーム経験": 数値,
    "FP/LOC規模": 数値,
    "その他": 数値
  }}
}}

入力情報：
{user_input}
選定手法：{model}
見積もり結果：{result}
"""

    analysis = client.responses.create(
        model="gpt-4o-mini",
        input=analysis_prompt,
        temperature=0.5,
    )

    ai_analysis = analysis.output_text.strip()

    return {
        "method": {
            "recommended_model": model,
            "reason": model_choice,
        },
        "result": result,
        "ai_analysis": ai_analysis,
    }

