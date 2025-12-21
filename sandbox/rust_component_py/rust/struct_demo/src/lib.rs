wit_bindgen::generate!("structs");

struct Component;

impl Guest for Component {
    fn distance(p1: Point, p2: Point) -> f64 {
        let dx = (p1.x - p2.x) as f64;
        let dy = (p1.y - p2.y) as f64;
        (dx * dx + dy * dy).sqrt()
    }

    fn add_points(p1: Point, p2: Point) -> Point {
        Point {
            x: p1.x + p2.x,
            y: p1.y + p2.y,
        }
    }

    fn greet(p: Person) -> String {
        format!("Hello, {}! You are {} years old.", p.name, p.age)
    }
}

export!(Component);
