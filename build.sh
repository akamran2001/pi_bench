gcc -O3 C_pi/src/main.c -o C_pi/build/pi_bench
cargo build --release --manifest-path=Rust_pi/Cargo.toml
javac Java_pi/src/Main.java -d Java_pi/build
python Python_pi/main.py