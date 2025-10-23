from langgraph.graph import StateGraph, END
from typing import TypedDict
from ai_logic.estimation_nodes import ai_estimation_node  # 👈 ここでAIノードを読み込む

# LangGraphで扱う状態（State）
class EstimationState(TypedDict):
    method: str
    result: dict
    user_input: dict  # Streamlitから渡ってくる入力データ

# ===== LangGraphの構成 =====
app_graph = StateGraph(state_schema=EstimationState)

# ノード追加（AI見積もりノード）
app_graph.add_node("ai_estimation", ai_estimation_node)

# 開始ノード設定
app_graph.set_entry_point("ai_estimation")

# 終了ノード設定
app_graph.add_edge("ai_estimation", END)

# Graphをコンパイル
app_graph = app_graph.compile()

# テスト実行（単体確認用）
if __name__ == "__main__":
    dummy_input = {
        "fp": 100,
        "loc": 2000,
        "functions": 10,
        "screens": 8,
        "tables": 5,
        "hardware": "Windows Server",
        "os": "Windows 11",
        "tools": "Python, Streamlit",
        "environment": "VSCode",
        "application_type": "業務システム",
        "complexity": "中",
        "lifecycle": "新規開発",
        "team_skill": "中級",
        "work_hours": 160
    }

    result = app_graph.invoke({"method": "", "result": {}, "user_input": dummy_input})
    print(result)
