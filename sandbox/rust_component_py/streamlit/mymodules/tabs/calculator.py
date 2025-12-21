import streamlit as st
from mymodules.wasm_utils import run_wasm_func, WASM_ADDER_PATH

def render():
    st.header("Adder & Multiplier")
    
    col1, col2 = st.columns(2)
    with col1:
        val_a = st.number_input("Enter first number", value=0, step=1, key="val_a")
    with col2:
        val_b = st.number_input("Enter second number", value=0, step=1, key="val_b")

    if st.button("Calculate Sum"):
        try:
            result = run_wasm_func(WASM_ADDER_PATH, "add", int(val_a), int(val_b))
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Multiplication")

    col3, col4 = st.columns(2)
    with col3:
        mul_a = st.number_input("Enter first number for Mul", value=0, step=1, key="mul_a")
    with col4:
        mul_b = st.number_input("Enter second number for Mul", value=0, step=1, key="mul_b")

    if st.button("Calculate Product"):
        try:
            result = run_wasm_func(WASM_ADDER_PATH, "multiply", int(mul_a), int(mul_b))
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
