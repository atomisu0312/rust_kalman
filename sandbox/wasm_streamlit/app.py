import streamlit as st
from wasmtime import Store, Module, Instance, Func, FuncType, ValType
import os

st.title("Rust WASM Calculator")

# Path to the compiled WASM file (now in the root directory)
WASM_PATH = "rust_algo.wasm"

def load_wasm():
    if not os.path.exists(WASM_PATH):
        st.error(f"WASM file not found at {WASM_PATH}. Please run './build.sh' first.")
        return None
    
    store = Store()
    module = Module.from_file(store.engine, WASM_PATH)
    instance = Instance(store, module, [])
    return instance, store

st.write("This app uses a Rust-compiled WASM module to perform additions.")

col1, col2 = st.columns(2)

with col1:
    add_a = st.number_input("Enter first number", value=0, step=1, key="add_a")

with col2:
    add_b = st.number_input("Enter second number", value=0, step=1, key="add_b")

if st.button("Calculate Sum"):
    try:
        instance, store = load_wasm()
        if instance:
            add_func = instance.exports(store)["add"]
            result = add_func(store, int(add_a), int(add_b))
            st.success(f"Result from Rust WASM: {result}")
    except Exception as e:
        st.error(f"Error executing WASM: {e}")

col21, col22 = st.columns(2)

with col21:
    sub_a = st.number_input("Enter first number", value=0, step=1, key="sub_a")

with col22:
    sub_b = st.number_input("Enter second number", value=0, step=1, key="sub_b")

if st.button("Calculate Sub"):
    try:
        instance, store = load_wasm()
        if instance:
            sub_func = instance.exports(store)["sub"]
            result = sub_func(store, int(sub_a), int(sub_b))
            st.success(f"Result from Rust WASM: {result}")
    except Exception as e:
        st.error(f"Error executing WASM: {e}")


st.markdown('''
---
### How it works

1. Rust code is compiled to WASM
2. Python uses `wasmtime` to load the WASM module
3. Streamlit inputs are passed to the WASM function
4. Result is returned and displayed

''')
