#!/bin/bash
set -euxC

# .envファイルから環境変数を読み込む
if [ -f .env ]; then
    # set -a で自動的にすべての変数をエクスポート
    set -a
    source .env
    set +a
    echo ".envファイルから環境変数を読み込みました"
else
    echo "警告: .envファイルが見つかりません"
fi

# 環境変数を確実にエクスポート（snowコマンドが読み込めるように）
export SNOWFLAKE_ACCOUNT="$SF_ACCOUNT_IDENTIFIER"
export SNOWFLAKE_USER="$SF_USER"
export SNOWFLAKE_PASSWORD="$SF_PASSWORD"

# Streamlitアプリをデプロイ
# --temporary-connection フラグを使用して、設定ファイルなしで環境変数から直接接続
# --replace フラグで既存のアプリを置き換え
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd "${SCRIPT_DIR}/streamlit"

snow streamlit deploy --temporary-connection --replace \
    --database "${SF_DATABASE:-employees}" \
    --schema "${SF_SCHEMA:-public}" \
    --warehouse "${SF_WAREHOUSE:-COMPUTE_WH}"

set +x
echo "Streamlit Deploy completed"

