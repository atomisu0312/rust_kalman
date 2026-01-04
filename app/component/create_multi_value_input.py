import streamlit as st
import numpy as np
from common.constant import SESSION_STATE_KEY_MATRICES


def create_matrix_input(rows, cols, key_prefix=""):
    """行列入力用のUIを生成
    
    Args:
        rows: 行列の行数
        cols: 行列の列数
        key_prefix: セッションステートのキープレフィックス
    
    Returns:
        numpy.ndarray: 入力された行列
    """
    
    # セッションステートから既存の行列を取得
    if key_prefix in st.session_state[SESSION_STATE_KEY_MATRICES]:
        existing_matrix = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
        # 既存の行列を新しい次元に合わせてリサイズ
        matrix = np.zeros((rows, cols))
        copy_rows = min(existing_matrix.shape[0], rows)
        copy_cols = min(existing_matrix.shape[1], cols)
        matrix[:copy_rows, :copy_cols] = existing_matrix[:copy_rows, :copy_cols]
    else:
        matrix = np.zeros((rows, cols))
    
    cols_list = st.columns(cols)
    
    for i in range(rows):
        for j in range(cols):
            with cols_list[j]:
                value = st.number_input(
                    f"({i+1},{j+1})",
                    value=float(matrix[i, j]),
                    key=f"{key_prefix}_{i}_{j}",
                    step=0.1,
                    format="%.3f"
                )
                matrix[i, j] = value
                
    # 行列全体を保存
    st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = matrix
    return matrix

def create_vector_input(length, key_prefix=""):
    """ベクトル入力用のUIを生成
    
    Args:
        length: ベクトルの長さ
        key_prefix: セッションステートのキープレフィックス
    
    Returns:
        numpy.ndarray: 入力されたベクトル
    """
    # セッションステートから既存の行列を取得
    if key_prefix in st.session_state[SESSION_STATE_KEY_MATRICES]:
        existing_matrix = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
        # 既存の行列を新しい次元に合わせてリサイズ
        matrix = np.zeros(length)
        copy_length = min(existing_matrix.shape[0], length)
        matrix[:copy_length] = existing_matrix[:copy_length]
    else:
        matrix = np.zeros(length)
    
    cols_list = st.columns(length)
    
    for i in range(length):
        with cols_list[i]:
            value = st.number_input(
                f"{key_prefix}[{i+1}]",
                value=float(matrix[i]),
                key=f"{key_prefix}_{i}",
                step=0.1,
                format="%.3f"
            )
            matrix[i] = value
    
    # ベクトル全体を保存
    st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = matrix
    return matrix