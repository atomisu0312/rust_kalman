use clap::Parser;

fn gcd(mut n: u64, mut m: u64) -> u64 {
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            let t = m;
            m = n;
            n = t;
        }
        m = m % n;
    }
    n
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(14, 15), 1);

    assert_eq!(gcd(2 * 3 * 5 * 11 * 17, 3 * 7 * 11 * 13 * 19), 3 * 11);
}

#[derive(Parser, Debug)]
#[command(name = "gcd", about = "Find the greatest common divisor", long_about = None)]
struct Args {
    #[arg(short, long)]
    first: u64,
    #[arg(short, long, default_value_t = 1)]
    second: u64,
}

fn main() {
    let args = Args::parse();

    let mut d = args.first;
    d = gcd(d, args.second);

    println!("{}", d);
}
