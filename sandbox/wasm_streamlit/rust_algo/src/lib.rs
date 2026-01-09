use ndarray::{array, s};
use ndarray_inverse::Inverse;
use std::cell::RefCell;

// Thread-local storage for the output string to pass to JS/Python
thread_local! {
    static OUTPUT_BUFFER: RefCell<String> = RefCell::new(String::new());
}

#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
pub extern "C" fn sub(a: i32, b: i32) -> i32 {
    a - b
}

#[no_mangle]
pub extern "C" fn run_demo() -> i32 {
    // 1. Create from data
    let arr = array![[3.0, 2.0, 1.0], [2.0, 3.0, 2.0], [1.0, 2.0, 3.0]];

    let mut output = String::new();
    output.push_str("Original Matrix (A):\n");
    output.push_str(&format!("{}\n\n", arr));

    // 2. Slicing
    let slice = arr.slice(s![0..2, 1..3]);
    output.push_str("Slice (rows 0..2, cols 1..3):\n");
    output.push_str(&format!("{}\n\n", slice));

    // 3. Element-wise operations (要素ごとの積)
    // * 演算子は要素ごとの掛け算になります
    let elem_wise = &arr * 2.0;
    output.push_str("Element-wise (* 2.0):\n");
    output.push_str(&format!("{}\n\n", elem_wise));

    // ==========================================
    // 4. Matrix Multiplication (行列の積)
    // .dot() メソッドを使用します
    // ==========================================
    let arr2 = array![
        [1.0, 2.0, 0.0],
        [0.0, 1.0, 0.0],
        [3.0, 0.0, 1.0]
    ]; 
    
    // 行列 A と 行列 B の積を計算 (A . B)
    let dot_product = arr.dot(&arr2);

    output.push_str("Matrix Multiplication (A . dot(B)):\n");
    output.push_str("Matrix B:\n");
    output.push_str(&format!("{}\n", arr2));
    output.push_str("Result:\n");
    output.push_str(&format!("{}\n\n", dot_product));


    // 5. Compute norm / Inverse
    output.push_str("Inverse of A:\n");
    match arr.inv() {
        Some(inv) => output.push_str(&format!("{}", inv)),
        None => output.push_str("Matrix is singular (not invertible)"),
    }

    OUTPUT_BUFFER.with(|b| {
        *b.borrow_mut() = output;
        b.borrow().len() as i32
    })
}

#[no_mangle]
pub extern "C" fn get_output_ptr() -> *const u8 {
    OUTPUT_BUFFER.with(|b| b.borrow().as_ptr())
}
