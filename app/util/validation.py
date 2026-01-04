import numpy as np


def validate_kalman_parameters(Q_w, Q_v, P_0):
    """カルマンフィルタのパラメータを検証
    
    Args:
        Q_w: システムノイズ共分散行列
        Q_v: 観測ノイズ共分散行列
        P_0: 初期共分散行列
    
    Returns:
        list: 検証エラーメッセージのリスト（エラーがない場合は空リスト）
    """
    validation_errors = []
    
    # 対称性チェック
    if not np.allclose(Q_w, Q_w.T):
        validation_errors.append("⚠️ システムノイズ共分散行列 Q_w は対称行列である必要があります")
        
    if not np.allclose(Q_v, Q_v.T):
        validation_errors.append("⚠️ 観測ノイズ共分散行列 Q_v は対称行列である必要があります")
    if not np.allclose(P_0, P_0.T):
        validation_errors.append("⚠️ 初期共分散行列 P_0 は対称行列である必要があります")
    
    # 正定値性チェック（簡易版）
    try:
        if np.any(np.linalg.eigvals(Q_w) <= 0):
            validation_errors.append("⚠️ システムノイズ共分散行列 Q_w は正定値である必要があります")
    except (np.linalg.LinAlgError, ValueError):
        pass
    
    try:
        if np.any(np.linalg.eigvals(Q_v) <= 0):
            validation_errors.append("⚠️ 観測ノイズ共分散行列 R は正定値である必要があります")
    except (np.linalg.LinAlgError, ValueError):
        pass
    
    try:
        if np.any(np.linalg.eigvals(P_0) <= 0):
            validation_errors.append("⚠️ 初期共分散行列 P₀ は正定値である必要があります")
    except (np.linalg.LinAlgError, ValueError):
        pass
    
    return validation_errors

