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

# Snowflake CLIでSQLを実行
# --temporary-connection フラグを使用して、設定ファイルなしで環境変数から直接接続
# 環境変数（SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD）が設定されている必要がある

# ステージにzipファイルをアップロード
SCRIPT_DIR=$(cd $(dirname $0); pwd)
snow stage copy "${SCRIPT_DIR}/struct_demo.zip" @employees.public.my_internal_stage --temporary-connection

# Streamlitアプリを作成（既に存在する場合は置き換え）
# データベースとスキーマを指定（qualified nameを使用）
snow sql -q "USE DATABASE employees; USE SCHEMA public; CREATE OR REPLACE STREAMLIT struct_demo_app ROOT_LOCATION = '@employees.public.my_internal_stage' MAIN_FILE = 'app.py' QUERY_WAREHOUSE = 'COMPUTE_WH'" --temporary-connection