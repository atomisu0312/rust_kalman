import streamlit as st
from mymodules.tabs import calculator, struct_demo

st.title("Rust WASM Component Calculator")
st.write("This app demonstrates Rust-compiled WASM Components.")
st.info("Component Model enabled. Using `wit-bindgen` generated components.")

tab1, tab2 = st.tabs(["Calculator", "Struct Demo"])

with tab1:
    calculator.render()

with tab2:
    struct_demo.render()
