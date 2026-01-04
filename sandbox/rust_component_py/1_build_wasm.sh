#!/bin/bash
set -e
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}/rust/sampladder
echo "Building Rust project..."
cargo build --release --target wasm32-unknown-unknown

echo "Creating WASM Component..."
wasm-tools component new target/wasm32-unknown-unknown/release/sampladder.wasm -o sampladder-comp.wasm

echo "Copying artifacts to streamlit directory..."
cp sampladder-comp.wasm ${SCRIPT_DIR}/streamlit/

cd ${SCRIPT_DIR}/rust/struct_demo
echo "Building Rust project..."
cargo build --release --target wasm32-unknown-unknown

echo "Creating WASM Component..."
wasm-tools component new target/wasm32-unknown-unknown/release/struct_demo.wasm -o structs-comp.wasm

echo "Copying artifacts to streamlit directory..."
cp structs-comp.wasm ${SCRIPT_DIR}/streamlit/

echo "Done!"
