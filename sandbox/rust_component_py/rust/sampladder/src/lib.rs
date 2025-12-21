wit_bindgen::generate!("adder");

struct Component;

impl Guest for Component {
    // エクスポートする関数の実装
    fn add(x: i32, y: i32) -> i32 {
        x + y
    }

    fn multiply(x: i32, y: i32) -> i32 {
        x * y
    }
}

export!(Component);
