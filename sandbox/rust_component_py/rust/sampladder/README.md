# Sampladder (WASM Component)

This project contains a Rust library compiled to a WASM Component using `wit-bindgen`.

## Build Instructions

### Prerequisites
- Rust toolchain
- `wasm32-unknown-unknown` target: `rustup target add wasm32-unknown-unknown`
- `wasm-tools`: `cargo install wasm-tools`

### Compilation
To compile the project and create a WASM component:

1. Build the WASM module:
```bash
cargo build --release --target wasm32-unknown-unknown
```

2. Convert the module to a component:
```bash
wasm-tools component new target/wasm32-unknown-unknown/release/sampladder.wasm -o sampladder-comp.wasm
```

### Streamlit Integration
The generated `sampladder-comp.wasm` should be placed in the `streamlit` directory for the Python app to use.
```bash
cp sampladder-comp.wasm ../../streamlit/
```
