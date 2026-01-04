import streamlit as st
from tabs import render_input_tab, render_confirmation_tab
from util import handle_dimension_change

st.set_page_config(page_title="カルマンフィルタ パラメータ設定", layout="wide")

st.title("カルマンフィルタ 内部状態次元数設定")

# 次元の選択（1〜5）
dimension = st.selectbox(
    "状態次元数",
    options=[1, 2, 3, 4, 5],
    index=1,  # デフォルトは2次元
    help="カルマンフィルタの状態ベクトルの次元数を選択してください"
)

# 観測次元は1で固定
obs_dimension = 1

# 次元が変更された場合、古い値をクリア
handle_dimension_change(dimension, obs_dimension)

# タブで入力と確認を分ける
tab1, tab2 = st.tabs(["📝 パラメータ入力", "✅ パラメータ確認"])

with tab1:
    render_input_tab(dimension, obs_dimension)

with tab2:
    render_confirmation_tab(dimension, obs_dimension)
