# Streamlit + Rust WASM Example

This project demonstrates how to call a Rust-compiled WASM function from a Streamlit app.

## Prerequisites

- Rust (with `wasm32-unknown-unknown` target)
- `uv` (for Python dependency management)

## Setup & Run

1.  **Build the Project**:
    Run the build script to compile the Rust code and place the `.wasm` file in the project root.
    ```bash
    ./build.sh
    ```

2.  **Run the App**:
    ```bash
    uv run streamlit run app.py
    ```

## Notes

- The build script handles the compilation target details (`wasm32-unknown-unknown`) internally and outputs a clean `rust_algo.wasm` file.
