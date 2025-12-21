#!/bin/bash
set -e

echo "Building Struct Demo project..."
cargo build --release --target wasm32-unknown-unknown

echo "Creating WASM Component..."
wasm-tools component new target/wasm32-unknown-unknown/release/struct_demo.wasm -o structs-comp.wasm

echo "Copying artifacts to streamlit directory..."
cp structs-comp.wasm ../../streamlit/

echo "Done!"
