import streamlit as st
import os
from wasmtime import Config, Engine, Store
from wasmtime.component import Component, Linker

WASM_ADDER_PATH = "sampladder-comp.wasm"
WASM_STRUCTS_PATH = "structs-comp.wasm"

@st.cache_resource
def get_engine_component(wasm_path):
    if not os.path.exists(wasm_path):
        st.error(f"WASM file not found at {wasm_path}.")
        return None, None

    config = Config()
    config.wasm_component_model = True
    
    engine = Engine(config)
    
    try:
        component = Component.from_file(engine, wasm_path)
        return engine, component
    except Exception as e:
        st.error(f"Failed to load WASM component: {e}")
        return None, None

def run_wasm_func(wasm_path, func_name, *args):
    engine, component = get_engine_component(wasm_path)
    if not engine or not component:
        return None

    store = Store(engine)
    linker = Linker(engine)
    
    try:
        instance = linker.instantiate(store, component)
        func = instance.get_func(store, func_name)
        
        if func:
            return func(store, *args)
        else:
            raise Exception(f"Function '{func_name}' not found")
            
    except Exception as e:
        raise e
