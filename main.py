# %%
import pandas as pd
from multiprocessing import Process, Queue
import re
import subprocess
import timeit
from Python_pi.main import calc_pi

config = {
    "C":{
        "build":["gcc","-O3","C_pi/src/main.c","-o","C_pi/build/pi_bench"],
        "bin": "./C_pi/build/pi_bench"
    },
    "Rust":{
        "build":["cargo", "build","--release", "--manifest-path=Rust_pi/Cargo.toml"],
        "bin":"./Rust_pi/target/release/pi_bench"
    }
}

def bench_py(n):
    start = timeit.default_timer()
    q = Queue()
    p = Process(target=lambda q,n: q.put(calc_pi(n)), args=(q,n))
    p.start()
    p.join()
    pi =  q.get()
    py_time = timeit.default_timer() - start
    return py_time

def bench_rust(n,binary):
    out_rust = subprocess.check_output(args=[F"{binary}", str(n)]).decode("utf-8")
    rust_time = float(re.search(pattern="([0-9].[0-9]*) seconds",string=out_rust)[1])
    return rust_time

def bench_c(n,binary):
    out_c = subprocess.check_output(args=[F"{binary}", str(n)]).decode("utf-8")
    c_time = float(re.search(pattern="([0-9].[0-9]*) seconds",string=out_c)[1])
    return c_time

def log_bench(min,max,skip):
    data = []
    
    for n in range(min,max,skip):
        py_time = bench_py(n)
        rust_time = bench_rust(n,binary=config["Rust"]["bin"])
        c_time = bench_c(n,binary=config["C"]["bin"])
        
        diff_py_rs = py_time - rust_time
        ratio_py_rs = py_time / rust_time

        diff_py_c = py_time - c_time
        ratio_py_c = py_time / c_time

        #print(F"{n} terms",F"Python - Rust - C",F"1x - {ratio_py_rs}x - {ratio_py_c}x",sep="\n")
        
        data.append([n, py_time, rust_time, c_time ,diff_py_rs, diff_py_c, ratio_py_rs, ratio_py_c])
    
    return data

def compile_bins():
    for lang in config:
        build = config[lang]["build"]
        bin = config[lang]["bin"]
        out = subprocess.run(args=build,capture_output=True)
        if out.returncode==0:
            print(F"{lang} => success => {bin}")
        else:
            print(F"{out.stderr.decode('utf-8')}")

def run_analysis():
    compile_bins();
    
    header = ['terms', 'python', 'rust', 'c', 'py-rs', 'py-c', 'py/rs', 'py/c']

    data = log_bench(min=100_000,max=1_000_000,skip=10_000)

    df = pd.DataFrame(columns=header, data=data)

    plot_config ={
            "kind":'line',
            "x":'terms',
            "figsize":(10,5), 
            "grid":True, 
            "xlim":(100_000,1_000_000),
            "xlabel":"Number of terms used in Leibniz formula for π",
    }

    df.plot(**plot_config,y=["c","python","rust"],logy=True, ylabel="Seconds taken log scale")
    max_cr = df[['c', 'rust']].max().max()
    df.plot(**plot_config,y=["c","rust"],ylim=(0,max_cr+(0.15*max_cr)), ylabel="Seconds taken")
    

run_analysis()





# %%
