#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd $(dirname $0); pwd)
ZIP_FILE="${SCRIPT_DIR}/struct_demo.zip"

# 2_deploy_to_stage.shから設定を自動抽出してsnowflake.ymlを生成
echo "Generating snowflake.yml from 2_deploy_to_stage.sh..."

DB_NAME="employees"
SCHEMA_NAME="public"
STAGE_NAME="my_internal_stage"
APP_NAME="struct_demo_app"
WAREHOUSE="COMPUTE_WH"

if [ -f "${SCRIPT_DIR}/2_deploy_to_stage.sh" ]; then
    STAGE_FULL=$(grep -o '@[^ ]*\.my_internal_stage' "${SCRIPT_DIR}/2_deploy_to_stage.sh" | head -1 | sed 's/@//')
    if [ -n "$STAGE_FULL" ]; then
        DB_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f1)
        SCHEMA_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f2)
        STAGE_NAME=$(echo "$STAGE_FULL" | cut -d'.' -f3)
    fi
    
    APP_NAME_EXTRACTED=$(grep 'CREATE OR REPLACE STREAMLIT' "${SCRIPT_DIR}/2_deploy_to_stage.sh" | grep -o 'STREAMLIT [^ ]*' | awk '{print $2}' | head -1)
    [ -n "$APP_NAME_EXTRACTED" ] && APP_NAME="$APP_NAME_EXTRACTED"
    
    WAREHOUSE_EXTRACTED=$(grep -o "QUERY_WAREHOUSE = '[^']*'" "${SCRIPT_DIR}/2_deploy_to_stage.sh" | sed "s/QUERY_WAREHOUSE = '//;s/'//" | head -1)
    [ -n "$WAREHOUSE_EXTRACTED" ] && WAREHOUSE="$WAREHOUSE_EXTRACTED"
fi

# snowflake.ymlを生成
cat > "${SCRIPT_DIR}/streamlit/snowflake.yml" <<EOF
definition_version: 2
entities:
  ${APP_NAME}:
    type: streamlit
    identifier: ${APP_NAME}
    stage: ${DB_NAME}.${SCHEMA_NAME}.${STAGE_NAME}
    query_warehouse: ${WAREHOUSE}
    main_file: app.py
    artifacts:
      - environment.yml
EOF

# 既存のzipファイルを削除
rm -f "${ZIP_FILE}"

# Streamlit in Snowflakeはzipのルートにapp.pyがあることを期待する
# streamlit/ディレクトリの中身をzipのルートに配置する
cd "${SCRIPT_DIR}/streamlit"

# zipファイルを作成（ルートにapp.pyが来るように）
# findコマンドで除外パターンを適用してからzip化
find . -type f \
  ! -path "*/.git/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/.venv/*" \
  ! -name ".DS_Store" \
  ! -name ".gitignore" \
  ! -name "*.zip" \
  -print0 | xargs -0 zip -r "${ZIP_FILE}"

echo "Done! ${ZIP_FILE}"