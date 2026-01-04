#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd $(dirname $0); pwd)

# 2_deploy_to_stage.shから設定を抽出
DEPLOY_SCRIPT="${SCRIPT_DIR}/2_deploy_to_stage.sh"

# デフォルト値
DB_NAME="employees"
SCHEMA_NAME="public"
STAGE_NAME="my_internal_stage"
APP_NAME="struct_demo_app"
WAREHOUSE="COMPUTE_WH"

# スクリプトから設定を抽出
if [ -f "$DEPLOY_SCRIPT" ]; then
    # ステージ名を抽出
    STAGE_FULL=$(grep -o '@[^ ]*\.my_internal_stage' "$DEPLOY_SCRIPT" | head -1 | sed 's/@//')
    if [ -n "$STAGE_FULL" ]; then
        DB_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f1)
        SCHEMA_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f2)
        STAGE_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f3)
    fi
    
    # アプリ名を抽出
    APP_NAME_EXTRACTED=$(grep -o 'CREATE OR REPLACE STREAMLIT [^ ]*' "$DEPLOY_SCRIPT" | awk '{print $4}' | head -1)
    if [ -n "$APP_NAME_EXTRACTED" ]; then
        APP_NAME="$APP_NAME_EXTRACTED"
    fi
    
    # ウェアハウス名を抽出
    WAREHOUSE_EXTRACTED=$(grep -o "QUERY_WAREHOUSE = '[^']*'" "$DEPLOY_SCRIPT" | sed "s/QUERY_WAREHOUSE = '//;s/'//" | head -1)
    if [ -n "$WAREHOUSE_EXTRACTED" ]; then
        WAREHOUSE="$WAREHOUSE_EXTRACTED"
    fi
fi

# .envファイルからウェアハウス名を取得（あれば）
if [ -f "${SCRIPT_DIR}/.env" ]; then
    if grep -q "SF_WAREHOUSE" "${SCRIPT_DIR}/.env"; then
        WAREHOUSE=$(grep "SF_WAREHOUSE" "${SCRIPT_DIR}/.env" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    fi
fi

# snowflake.ymlを生成
cat > "${SCRIPT_DIR}/streamlit/snowflake.yml" <<EOF
definition_version: 1
streamlit:
  - name: ${APP_NAME}
    main_file: app.py
    root_location: '@${DB_NAME}.${SCHEMA_NAME}.${STAGE_NAME}'
    query_warehouse: ${WAREHOUSE}
EOF

echo "Generated snowflake.yml:"
echo "  App name: ${APP_NAME}"
echo "  Root location: @${DB_NAME}.${SCHEMA_NAME}.${STAGE_NAME}"
echo "  Warehouse: ${WAREHOUSE}"

