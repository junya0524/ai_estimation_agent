import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv  # ← これが大事！

# ===== 環境変数読み込み（OpenAI APIキー対応） =====
load_dotenv()

# ===== モジュールインポート =====
from estimation.fp_model import estimate_fp
from estimation.cocomo_model import estimate_cocomo
from estimation.loc_model import estimate_loc
from ai_logic.decision_graph import app_graph  # LangGraphを利用

# ===== Streamlit設定 =====
st.set_page_config(page_title="AI Estimation Agent", layout="wide")
st.title("💡 AI Estimation Agent")
st.write("3つの手法（FP法 / COCOMO法 / LOC法）＋ LangGraph＋AI自動見積もりを行います。")

tab1, tab2, tab3, tab4 = st.tabs(["FP法", "COCOMO法", "LOC法", "AI自動見積もり"])

# -------------------------------------------------
# 📊 FP法
# -------------------------------------------------
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

# -------------------------------------------------
# 📈 COCOMO法
# -------------------------------------------------
with tab2:
    st.header("📈 COCOMO法による見積もり")
    size_kloc = st.number_input("開発規模 (KLOC単位)", min_value=1)
    mode = st.selectbox("開発モード", ["organic", "semi_detached", "embedded"])

    if st.button("COCOMO法で見積もり計算"):
        result = estimate_cocomo(size_kloc, mode)
        st.json(result)

# -------------------------------------------------
# 💻 LOC法
# -------------------------------------------------
with tab3:
    st.header("💻 LOC法による見積もり")
    loc_count = st.number_input("コード行数 (LOC)", min_value=100)

    if st.button("LOC法で見積もり計算"):
        result = estimate_loc(loc_count)
        st.json(result)

# -------------------------------------------------
# 🤖 LangGraph + AI自動選択
# -------------------------------------------------
with tab4:
    st.header("🤖 LangGraphによるAI自動選択モード")
    st.write("IPA見積もり要素を入力すると、LangGraphとAIが最適な見積もり方法を選定し、推定を実行します。")

    # === IPA入力フォーム ===
    st.subheader("📏 規模情報")
    fp = st.number_input("ファンクションポイント（FP）", min_value=0.0, step=1.0)
    loc = st.number_input("コード行数（LOC）", min_value=0)
    functions = st.number_input("機能数", min_value=0)
    screens = st.number_input("画面数", min_value=0)
    tables = st.number_input("テーブル数", min_value=0)

    st.subheader("🖥️ プラットフォーム / 環境")
    hardware = st.text_input("ハードウェア")
    os = st.text_input("オペレーティングシステム")
    tools = st.text_input("言語・ツール・ユーティリティ")
    environment = st.text_input("開発環境")

    st.subheader("📦 プロダクト特性")
    application_type = st.text_input("アプリケーション種別（例：業務システム、Web、モバイルなど）")
    complexity = st.selectbox("複雑度", ["低", "中", "高"])
    lifecycle = st.selectbox("ライフサイクル", ["新規開発", "改修", "保守"])

    st.subheader("👥 人材情報")
    team_skill = st.selectbox("チームの能力・経験", ["初級", "中級", "上級"])
    work_hours = st.number_input("総労働時間（時間）", min_value=0)

    # ===== LangGraph実行 =====
    if st.button("LangGraphでAI自動見積もりを実行"):
        with st.spinner("LangGraphが思考中です..."):
            user_input = {
                "fp": fp,
                "loc": loc,
                "functions": functions,
                "screens": screens,
                "tables": tables,
                "hardware": hardware,
                "os": os,
                "tools": tools,
                "environment": environment,
                "application_type": application_type,
                "complexity": complexity,
                "lifecycle": lifecycle,
                "team_skill": team_skill,
                "work_hours": work_hours,
            }

            # LangGraph経由でAI見積もりノード実行
            result = app_graph.invoke({"method": "", "result": {}, "user_input": user_input})

        st.success("✅ LangGraphがAI見積もりを完了しました！")

        # --- AI選定結果 ---
        st.subheader("🧠 AIの選定結果")
        if isinstance(result["method"], dict):
            method = result["method"].get("recommended_model", "不明")
            reason = result["method"].get("reason", "理由不明")
        else:
            method = result["method"]
            reason = "AI理由は未取得またはフォーマット外出力でした。"

        st.markdown(f"**選定手法：** {method}")
        st.markdown(f"**理由：** {reason}")

        # --- AI見積もり（類推法・開発規模提案・重み付け評価） ---
        st.subheader("🧩 AI見積もりの内訳（3要素）")
        st.markdown("""
        ① **類推法**：過去類似プロジェクトの規模・工数から推定  
        ② **開発規模提案**：規模バランスに基づき、機能拡張 or 縮小をAIが提案  
        ③ **重み付け評価**：選定根拠・要因の重み付けをAIが出力
        """)

        if "ai_analysis" in result:
            st.json(result["ai_analysis"])

        # --- 表形式で結果表示 ---
        st.subheader("📈 見積もり結果")
        df = pd.DataFrame(result["result"].items(), columns=["項目", "値"])
        st.table(df)

        # --- 📉 各手法比較グラフ ---
        st.subheader("📉 各手法の比較（工数・期間・コスト）")

        methods = ["FP法", "COCOMO法", "LOC法"]
        effort = [result["result"].get("工数(人月)", 0), 8, 6]
        duration = [3, 4, 5]
        cost = [result["result"].get("コスト(万円)", 0), 800, 650]

        df_compare = pd.DataFrame({
            "手法": methods,
            "工数(人月)": effort,
            "期間(月)": duration,
            "コスト(万円)": cost
        })

        st.markdown("#### 📊 工数・コスト比較（棒グラフ）")
        st.bar_chart(df_compare.set_index("手法")[["工数(人月)", "コスト(万円)"]])

        st.markdown("#### 🕒 開発期間比較（折れ線グラフ）")
        st.line_chart(df_compare.set_index("手法")[["期間(月)"]])
