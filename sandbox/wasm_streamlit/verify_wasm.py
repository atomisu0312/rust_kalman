from wasmtime import Store, Module, Instance

WASM_PATH = "rust_algo.wasm"

def verify():
    print(f"Loading {WASM_PATH}...")
    store = Store()
    module = Module.from_file(store.engine, WASM_PATH)
    instance = Instance(store, module, [])
    
    run_demo = instance.exports(store)["run_demo"]
    get_output_ptr = instance.exports(store)["get_output_ptr"]
    memory = instance.exports(store)["memory"]
    
    print("Running demo function...")
    length = run_demo(store)
    print(f"Output length: {length}")
    
    ptr = get_output_ptr(store)
    print(f"Output pointer: {ptr}")
    
    output_bytes = memory.read(store, ptr, ptr + length)
    output_str = output_bytes.decode('utf-8')
    
    print("-" * 20)
    print(output_str)
    print("-" * 20)
    
    # Assertions
    assert "Original Matrix" in output_str
    assert "Slice" in output_str
    assert "Inverse" in output_str
    assert "3, 2, 1" in output_str or "3, 2, 1" in output_str.replace(".0","") # Check content roughly
    
    print("Verification SUCCESS!")

if __name__ == "__main__":
    verify()
