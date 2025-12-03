#!/bin/bash
set -e

echo "Building Rust project..."
cd rust_algo
# We must use this target name for the compiler, but we will hide the output path below.
cargo build --target wasm32-unknown-unknown --release
cd ..

# Copy the artifact to a cleaner location
cp rust_algo/target/wasm32-unknown-unknown/release/rust_algo.wasm ./rust_algo.wasm

echo "Build complete!"
echo "WASM file is ready at: ./rust_algo.wasm"
