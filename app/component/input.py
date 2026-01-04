import streamlit as st
import numpy as np
from component import create_matrix_input, create_vector_input
from common.constant import (
    SESSION_STATE_KEY_A,
    SESSION_STATE_KEY_C,
    SESSION_STATE_KEY_QW,
    SESSION_STATE_KEY_QV,
    SESSION_STATE_KEY_X0,
    SESSION_STATE_KEY_P0,
)


def render_input_tab(dimension, obs_dimension):
    """パラメータ入力タブをレンダリング
    
    Args:
        dimension: 状態次元数
        obs_dimension: 観測次元数
    """
    st.header("パラメータ入力")
    
    # 状態遷移行列 F (dimension x dimension)
    st.subheader("1. 状態遷移行列 A")
    st.caption(f"サイズ: {dimension} × {dimension}")
    A = create_matrix_input(dimension, dimension, key_prefix=SESSION_STATE_KEY_A)
    
    # 観測行列 H (obs_dimension x dimension)
    st.subheader("2. 観測行列 C")
    st.caption(f"サイズ: {obs_dimension} × {dimension}")
    C = create_matrix_input(obs_dimension, dimension, key_prefix=SESSION_STATE_KEY_C)
    
    # システムノイズ共分散行列 Q_w (dimension x dimension)
    st.subheader("3. システムノイズ共分散行列 Q_w")
    st.caption(f"サイズ: {dimension} × {dimension} (対称行列)")
    Q_w = create_matrix_input(dimension, dimension, key_prefix=SESSION_STATE_KEY_QW)
    
    # 観測ノイズ共分散行列 Q_v (obs_dimension x obs_dimension)
    st.subheader("4. 観測ノイズ共分散行列 Q_v")
    st.caption(f"サイズ: {obs_dimension} × {obs_dimension} (対称行列)")
    Q_v = create_matrix_input(obs_dimension, obs_dimension, key_prefix=SESSION_STATE_KEY_QV)
    
    # 初期状態 x0 (dimension x 1)
    st.subheader("5. 初期状態ベクトル x₀")
    st.caption(f"サイズ: {dimension} × 1")
    
    x0 = create_vector_input(dimension, key_prefix=SESSION_STATE_KEY_X0)
    
    # 初期共分散行列 P0 (dimension x dimension)
    st.subheader("6. 初期共分散行列 P₀")
    st.caption(f"サイズ: {dimension} × {dimension} (対称行列)")
    P0 = create_matrix_input(dimension, dimension, key_prefix=SESSION_STATE_KEY_P0)

