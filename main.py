# %%
import pandas as pd
from multiprocessing import Process, Queue
import re
import subprocess
import matplotlib.pyplot as plt

LOW = 100_000
HIGH = 1_000_000
OUT_REGEX = "([0-9].[0-9]*) seconds"
CONFIG = {
    "C":{
        "build":["gcc","-O3","C_pi/src/main.c","-o","C_pi/build/pi_bench"],
        "run": "./C_pi/build/pi_bench"
    },
    "Rust":{
        "build":["cargo", "build","--release", "--manifest-path=Rust_pi/Cargo.toml"],
        "run":"./Rust_pi/target/release/pi_bench"
    },
    "Java":{
        "build":["javac", "Java_pi/src/Main.java", "-d", "Java_pi/build"],
        "run": ["java", "-cp", "Java_pi/build", "Main"]
    },
    "Python": {
        "build":["python","Python_pi/main.py"],
        "run":["python","Python_pi/main.py"]
    }
}

def bench_py(n,binary):
    args = binary+[str(n)]
    out_py = subprocess.check_output(args=args).decode("utf-8")
    py_time = float(re.search(pattern=OUT_REGEX,string=out_py)[1])
    return py_time

def bench_rust(n,binary):
    out_rust = subprocess.check_output(args=[F"{binary}", str(n)]).decode("utf-8")
    rust_time = float(re.search(pattern=OUT_REGEX,string=out_rust)[1])
    return rust_time

def bench_c(n,binary):
    out_c = subprocess.check_output(args=[F"{binary}", str(n)]).decode("utf-8")
    c_time = float(re.search(pattern=OUT_REGEX,string=out_c)[1])
    return c_time

def bench_java(n,binary):
    args = binary+[str(n)]
    out_java = subprocess.check_output(args=args).decode("utf-8")
    java_time = float(re.search(pattern=OUT_REGEX,string=out_java)[1])
    return java_time


def log_bench(min,max,skip):
    data = []
    
    for n in range(min,max,skip):
        py_time = bench_py(n, binary=CONFIG["Python"]["run"])
        rust_time = bench_rust(n,binary=CONFIG["Rust"]["run"])
        c_time = bench_c(n,binary=CONFIG["C"]["run"])
        java_time = bench_java(n,binary=CONFIG["Java"]["run"])
        
        diff_py_rs = py_time - rust_time
        ratio_py_rs = py_time / rust_time

        diff_py_c = py_time - c_time
        ratio_py_c = py_time / c_time

        diff_py_java = py_time - java_time
        ratio_py_java = py_time / java_time

        data.append({
            'terms': n, 
            'python':py_time,
            'rust':rust_time,
            'c':c_time,
            'java':java_time,
            'py-rs':diff_py_rs, 
            'py-c':diff_py_c,
            'py-j':diff_py_java,
            'py/rs':ratio_py_rs,
            'py/c':ratio_py_c,
            'py/j':ratio_py_java
        })
    
    return data

def create_builds():
    for lang in CONFIG:
        build = CONFIG[lang]["build"]
        build = CONFIG[lang]["run"]
        out = subprocess.run(args=build,capture_output=True)
        if out.returncode==0:
            print(F"{lang} => success => {build}")
        else:
            print(F"{out.stderr.decode('utf-8')}")

if(__name__== "__main__"):
    data = log_bench(min=LOW,max=HIGH,skip=HIGH//100)
    df = pd.DataFrame(data=data)
    plot_config ={
            "kind":'line',
            "x":'terms',
            "figsize":(10,5), 
            "grid":True, 
            "xlim":(LOW,HIGH),
            "xlabel":"Number of terms used in Leibniz formula for π",
    }

    df.plot(**plot_config,y=["c","python","rust","java"],logy=True, ylabel="Seconds taken log scale")
    plt.show()
    
    
    df.plot(**plot_config,y=["c","python","rust"],logy=True, ylabel="Seconds taken log scale")
    plt.show()

    
    max_cr = df[['c', 'rust']].max().max()
    df.plot(**plot_config,y=["c","rust"],ylim=(0,max_cr+(0.15*max_cr)), ylabel="Seconds taken")
    plt.show()

    
    df.plot(**plot_config,y=["python","java"],logy=True, ylabel="Seconds taken log scale")
    plt.show()


# %%
