use ndarray::array;
use ndarray::s;
use ndarray_linalg::Inverse;

fn main() {
    // Create a 3x3 matrix
    //let matrix = Array2::<f64>::zeros((3, 3));

    // Create from data
    let arr = array![
        [3.0f32, 2.0f32, 1.0f32],
        [2.0f32, 3.0f32, 2.0f32],
        [1.0f32, 2.0f32, 3.0f32]
    ];

    // Slicing
    let slice = &arr.slice(s![0..2, 1..3]);
    println!("{}", slice);

    // Element-wise operations
    let result = &arr * 2.0;
    println!("{}", result);

    // Compute norm
    let inv = arr.inv();
    println!("{}", inv.unwrap());
}
