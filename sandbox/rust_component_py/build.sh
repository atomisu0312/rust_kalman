#!/bin/bash
set -e

cd ./rust/sampladder
echo "Building Rust project..."
cargo build --release --target wasm32-unknown-unknown

echo "Creating WASM Component..."
wasm-tools component new target/wasm32-unknown-unknown/release/sampladder.wasm -o sampladder-comp.wasm

echo "Copying artifacts to streamlit directory..."
cp sampladder-comp.wasm ../../streamlit/

echo "Done!"
