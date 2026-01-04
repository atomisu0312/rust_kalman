import streamlit as st
from util import validate_kalman_parameters, get_matrix_from_session, get_vector_from_session
from common.constant import (
    SESSION_STATE_KEY_A,
    SESSION_STATE_KEY_C,
    SESSION_STATE_KEY_QW,
    SESSION_STATE_KEY_QV,
    SESSION_STATE_KEY_X0,
    SESSION_STATE_KEY_P0,
)


def render_confirmation_tab(dimension, obs_dimension):
    """パラメータ確認タブをレンダリング
    
    Args:
        dimension: 状態次元数
        obs_dimension: 観測次元数
    """
    st.header("パラメータ確認")
    
    # 行列を取得
    A = get_matrix_from_session(SESSION_STATE_KEY_A, dimension, dimension)
    C = get_matrix_from_session(SESSION_STATE_KEY_C, obs_dimension, dimension)
    Qw = get_matrix_from_session(SESSION_STATE_KEY_QW, obs_dimension, obs_dimension)
    Qv = get_matrix_from_session(SESSION_STATE_KEY_QV, dimension, dimension)
    x0 = get_vector_from_session(SESSION_STATE_KEY_X0, dimension)
    P0 = get_matrix_from_session(SESSION_STATE_KEY_P0, dimension, dimension)
    
    # パラメータの表示
    st.subheader("入力パラメータの確認")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**状態遷移行列 A**")
        st.write(A)
        
        st.write("**観測行列 C**")
        st.write(C)
        
        st.write("**初期状態ベクトル x₀**")
        st.write(x0)
    
    with col2:
        st.write("**システムノイズ共分散行列 Q_v**")
        st.write(Qv)

        st.write("**観測ノイズ共分散行列 Q_w**")
        st.write(Qw)
        
        st.write("**初期共分散行列 P₀**")
        st.write(P0)
    
    # パラメータの検証
    st.divider()
    st.subheader("パラメータ検証")
    validation_errors = validate_kalman_parameters(Qw, Qv, P0)
    
    if validation_errors:
        for error in validation_errors:
            st.error(error)
    else:
        st.success("✅ すべてのパラメータが有効です")

