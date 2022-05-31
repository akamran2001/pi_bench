import timeit
import sys

def calc_pi(n):
    pi_4 = 1.0
    denom = 3.0
    op = -1.0
    for _ in range(n):
        pi_4 += op * (1.0/denom)
        op *= -1.0
        denom += 2.0
    return pi_4 * 4


if(len(sys.argv)==2):
    n = int(sys.argv[1])
    start = timeit.default_timer()
    pi = calc_pi(n)
    py_time = timeit.default_timer() - start
    print(F"Pi using {n} additions is {pi} and took {py_time} seconds in Python")
else:
    print("ERROR")