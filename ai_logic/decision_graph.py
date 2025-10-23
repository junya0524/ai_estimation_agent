from langgraph.graph import StateGraph, END
from typing import TypedDict
import os, sys

# パス設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from estimation.fp_model import estimate_fp


# LangGraphで扱う状態
class EstimationState(TypedDict):
    method: str
    result: dict


# FP法での見積もりノード
def start_node(state: EstimationState):
    print("📘 開始：FP法を使用して見積もりを計算します")
    result = estimate_fp(3, 2, 1, 4, 2)
    return {"method": "FP法", "result": result}


# ✅ LangGraph用のグラフをここで定義（←ここが重要）
app_graph = StateGraph(state_schema=EstimationState)

app_graph.add_node("start", start_node)
app_graph.set_entry_point("start")
app_graph.add_edge("start", END)

# LangGraphが読み取れるようにcompileしておく
app_graph = app_graph.compile()

if __name__ == "__main__":
    result = app_graph.invoke({"method": "", "result": {}})
    print(result)

