fn main() {
    let dst = cmake::build("../../");

    println!("cargo:rustc-link-search=native={}/build", dst.display());
    println!("cargo:rustc-link-lib=static=kernels_cpu");

    // Link OpenMP if on Linux
    if std::env::consts::OS == "linux" {
        println!("cargo:rustc-link-lib=dylib=gomp");
    }
}
