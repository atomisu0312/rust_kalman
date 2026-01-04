import streamlit as st
import numpy as np
from common.constant import (
    SESSION_STATE_KEY_MATRICES,
    SESSION_STATE_KEY_A,
    SESSION_STATE_KEY_C,
    SESSION_STATE_KEY_QW,
    SESSION_STATE_KEY_QV,
    SESSION_STATE_KEY_X0,
    SESSION_STATE_KEY_P0,
)


def clear_old_matrix_values(key_prefix, max_rows, max_cols, prev_rows=None, prev_cols=None):
    """次元変更に対応して行列の値をリサイズ
    既存の値を保持しつつ、次元が小さくなった場合は余分な次元を切り捨て、大きくなった場合は足りない次元を0埋め
    
    Args:
        key_prefix: セッションステートのキープレフィックス
        max_rows: 現在の最大行数
        max_cols: 現在の最大列数
        prev_rows: 前回の最大行数（Noneの場合は切り捨てのみ）
        prev_cols: 前回の最大列数（Noneの場合は切り捨てのみ）
    """
    if key_prefix not in st.session_state[SESSION_STATE_KEY_MATRICES]:
        # 行列が存在しない場合は、新しい次元で0埋めの行列を作成
        st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = np.zeros((max_rows, max_cols))
        return
    
    # 既存の行列を取得
    old_matrix = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
    
    # 新しい次元にリサイズ（既存の値は保持、新しい領域は0埋め）
    new_matrix = np.zeros((max_rows, max_cols))
    if prev_rows is not None and prev_cols is not None:
        # 既存の値をコピー（小さい方の次元まで）
        copy_rows = min(prev_rows, max_rows)
        copy_cols = min(prev_cols, max_cols)
        new_matrix[:copy_rows, :copy_cols] = old_matrix[:copy_rows, :copy_cols]
    else:
        # prev_rows/prev_colsがNoneの場合は、既存の行列の次元を使用
        copy_rows = min(old_matrix.shape[0], max_rows)
        copy_cols = min(old_matrix.shape[1], max_cols)
        new_matrix[:copy_rows, :copy_cols] = old_matrix[:copy_rows, :copy_cols]
    
    # リサイズした行列を保存
    st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = new_matrix


def clear_old_state_vector_values(key_prefix, max_length, prev_length=None):
    """ベクトルの値を更新
    次元が小さくなった場合は余分な次元を切り捨て、大きくなった場合は足りない次元を0埋め
    
    Args:
        key_prefix: セッションステートのキープレフィックス
        max_length: 現在の最大長
        prev_length: 前回の最大長（Noneの場合は切り捨てのみ）
    """
    if key_prefix not in st.session_state[SESSION_STATE_KEY_MATRICES]:
        # ベクトルが存在しない場合は、新しい次元で0埋めのベクトルを作成
        st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = np.zeros(max_length)
        return
    
    # 既存のベクトルを取得
    old_vector = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
    
    # 新しい次元にリサイズ（既存の値は保持、新しい領域は0埋め）
    new_vector = np.zeros(max_length)
    if prev_length is not None:
        copy_length = min(prev_length, max_length)
    else:
        # prev_lengthがNoneの場合は、既存のベクトルの長さを使用
        copy_length = min(len(old_vector), max_length)
    new_vector[:copy_length] = old_vector[:copy_length]
    
    # リサイズしたベクトルを保存
    st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix] = new_vector


def handle_dimension_change(dimension, obs_dimension):
    """次元が変更された場合、古い値をクリア
    
    Args:
        dimension: 現在の状態次元
        obs_dimension: 現在の観測次元
    """
    # セッションステートの初期化
    if SESSION_STATE_KEY_MATRICES not in st.session_state:
        st.session_state[SESSION_STATE_KEY_MATRICES] = {}
    if 'prev_dimension' not in st.session_state:
        st.session_state.prev_dimension = dimension
    if 'prev_obs_dimension' not in st.session_state:
        st.session_state.prev_obs_dimension = obs_dimension
    
    # 状態次元が変更された場合、値を更新
    if st.session_state.prev_dimension != dimension:
        clear_old_matrix_values(SESSION_STATE_KEY_A, dimension, dimension, st.session_state.prev_dimension, st.session_state.prev_dimension)
        clear_old_matrix_values(SESSION_STATE_KEY_QW, dimension, dimension, st.session_state.prev_dimension, st.session_state.prev_dimension)
        clear_old_matrix_values(SESSION_STATE_KEY_P0, dimension, dimension, st.session_state.prev_dimension, st.session_state.prev_dimension)
        clear_old_state_vector_values(SESSION_STATE_KEY_X0, dimension, st.session_state.prev_dimension)
        st.session_state.prev_dimension = dimension
    
    # 観測次元が変更された場合、値を更新
    if st.session_state.prev_obs_dimension != obs_dimension:
        clear_old_matrix_values(SESSION_STATE_KEY_C, obs_dimension, dimension, st.session_state.prev_obs_dimension, st.session_state.prev_dimension)
        clear_old_matrix_values(SESSION_STATE_KEY_QV, obs_dimension, obs_dimension, st.session_state.prev_obs_dimension, st.session_state.prev_obs_dimension)
        st.session_state.prev_obs_dimension = obs_dimension


def get_matrix_from_session(key_prefix, rows, cols):
    """セッションステートから行列を取得
    
    Args:
        key_prefix: キープレフィックス
        rows: 行数
        cols: 列数
    
    Returns:
        numpy.ndarray: 行列
    """
    # セッションステートの初期化
    if SESSION_STATE_KEY_MATRICES not in st.session_state:
        st.session_state[SESSION_STATE_KEY_MATRICES] = {}
    
    if key_prefix in st.session_state[SESSION_STATE_KEY_MATRICES]:
        existing_matrix = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
        # 既存の行列を新しい次元に合わせてリサイズ
        matrix = np.zeros((rows, cols))
        copy_rows = min(existing_matrix.shape[0], rows)
        copy_cols = min(existing_matrix.shape[1], cols)
        matrix[:copy_rows, :copy_cols] = existing_matrix[:copy_rows, :copy_cols]
        return matrix
    return np.zeros((rows, cols))


def get_vector_from_session(key_prefix, length):
    """セッションステートからベクトルを取得
    
    Args:
        key_prefix: キープレフィックス
        length: ベクトルの長さ
    
    Returns:
        numpy.ndarray: ベクトル
    """
    if key_prefix in st.session_state[SESSION_STATE_KEY_MATRICES]:
        existing_vector = st.session_state[SESSION_STATE_KEY_MATRICES][key_prefix]
        # 既存のベクトルを新しい次元に合わせてリサイズ
        vector = np.zeros(length)
        copy_length = min(len(existing_vector), length)
        vector[:copy_length] = existing_vector[:copy_length]
        return vector
    return np.zeros(length)

