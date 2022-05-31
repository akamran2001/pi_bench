use std::env;
use std::time::Instant;

fn calc_pi(n: u32) -> f64 {
    let mut pi_4 = 1.0;
    let mut denom = 3.0;
    let mut op = -1.0;
    for _i in 0..n {
        pi_4 += op * (1.0 / denom);
        op *= -1.0;
        denom += 2.0;
    }
    return pi_4 * 4.0;
}
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 {
        let n: u32 = args[1].parse().expect("Use a number");
        let start = Instant::now();
        let pi = calc_pi(n);
        let duration = start.elapsed().as_secs_f64();
        print!(
            "Pi using {} additions is {} and took {} seconds in Rust",
            n, pi, duration,
        );
    } else {
        println!("Please supply arguments");
    }
}
