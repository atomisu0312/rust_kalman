import streamlit as st
import streamlit.components.v1 as components

with open("components/sample.html", "r") as f:
  html = f.read()

  # コンポーネントをレンダリングするだけだだそうです。
  components.html(
    html,
    height=600,
  )
