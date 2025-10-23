import streamlit as st
from estimation.fp_model import estimate_fp
from estimation.cocomo_model import estimate_cocomo
from estimation.loc_model import estimate_loc
from ai_logic.decision_graph import app_graph  # LangGraphを利用

st.set_page_config(page_title="AI Estimation Agent", layout="wide")
st.title("💡 AI Estimation Agent")
st.write("3つの手法（FP法 / COCOMO法 / LOC法）とLangGraphによるAI自動選択見積もりを行います。")

# --- タブを4つに拡張 ---
tab1, tab2, tab3, tab4 = st.tabs(["FP法", "COCOMO法", "LOC法", "AI自動見積もり"])

# ---------------- FP法 ----------------
with tab1:
    st.header("📊 FP法による見積もり")
    ei = st.number_input("外部入力 (EI)", min_value=0)
    eo = st.number_input("外部出力 (EO)", min_value=0)
    eq = st.number_input("外部照会 (EQ)", min_value=0)
    ilf = st.number_input("内部論理ファイル (ILF)", min_value=0)
    eif = st.number_input("外部インターフェースファイル (EIF)", min_value=0)

    if st.button("FP法で見積もり計算"):
        result = estimate_fp(ei, eo, eq, ilf, eif)
        st.json(result)

# ---------------- COCOMO法 ----------------
with tab2:
    st.header("📈 COCOMO法による見積もり")
    size_kloc = st.number_input("開発規模 (KLOC単位)", min_value=1)
    mode = st.selectbox("開発モード", ["organic", "semi_detached", "embedded"])

    if st.button("COCOMO法で見積もり計算"):
        result = estimate_cocomo(size_kloc, mode)
        st.json(result)

# ---------------- LOC法 ----------------
with tab3:
    st.header("💻 LOC法による見積もり")
    loc_count = st.number_input("コード行数 (LOC)", min_value=100)

    if st.button("LOC法で見積もり計算"):
        result = estimate_loc(loc_count)
        st.json(result)

# ---------------- AI自動モード（LangGraph連携） ----------------
with tab4:
    st.header("🤖 LangGraphによるAI自動選択モード")
    st.write("プロジェクト内容を入力すると、LangGraphが最適な手法（FP/COCOMO/LOC）を選び、見積もりを実行します。")

    project_desc = st.text_area("プロジェクト概要を入力してください", height=150)

    if st.button("LangGraphで自動見積もり実行"):
        with st.spinner("LangGraphが思考中です..."):
            graph = app_graph()
            result = graph.invoke({"method": "FP法", "result": {}})

        st.success("LangGraphが見積もりを実行しました！")
        st.subheader("🧠 AIの判断結果")
        st.json({"method": result["method"]})
        st.subheader("📈 見積もり結果")
        st.json(result["result"])
