import streamlit as st
from types import SimpleNamespace
from mymodules.wasm_utils import run_wasm_func, WASM_STRUCTS_PATH

def render():
    st.header("Complex Structs")
    
    st.subheader("Distance Calculator (Points)")
    # Function signature: distance: func(p1: point, p2: point) -> f64
    # Record point: {x: s32, y: s32}
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.caption("Point 1")
        p1_x = st.number_input("x1", value=0, key="p1_x")
        p1_y = st.number_input("y1", value=0, key="p1_y")
    with col_p2:
        st.caption("Point 2")
        p2_x = st.number_input("x2", value=10, key="p2_x")
        p2_y = st.number_input("y2", value=10, key="p2_y")
        
    if st.button("Calculate Distance"):
        try:
            # Construct objects mapping to WIT records (requires attributes, not dict keys)
            point1 = SimpleNamespace(x=int(p1_x), y=int(p1_y))
            point2 = SimpleNamespace(x=int(p2_x), y=int(p2_y))
            
            dist = run_wasm_func(WASM_STRUCTS_PATH, "distance", point1, point2)
            st.success(f"Distance: {dist}")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Add Points"):
        try:
            point1 = SimpleNamespace(x=int(p1_x), y=int(p1_y))
            point2 = SimpleNamespace(x=int(p2_x), y=int(p2_y))
            
            # Returns a Point record (object with x, y)
            result_point = run_wasm_func(WASM_STRUCTS_PATH, "add-points", point1, point2)
            st.success(f"Result Point: x={result_point.x}, y={result_point.y}")
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.markdown("---")
    st.subheader("Greeter (Person)")
    # Function signature: greet: func(p: person) -> string
    # Record person: {name: string, age: u8}
    
    name_input = st.text_input("Name", "Alice")
    age_input = st.number_input("Age", value=30, min_value=0, max_value=255)
    
    if st.button("Greet"):
        try:
            person = SimpleNamespace(name=name_input, age=int(age_input))
            greeting = run_wasm_func(WASM_STRUCTS_PATH, "greet", person)
            st.success(greeting)
        except Exception as e:
            st.error(f"Error: {e}")
