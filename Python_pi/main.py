def calc_pi(n):
    pi_4 = 1.0
    denom = 3.0
    op = -1.0
    for _ in range(n):
        pi_4 += op * (1.0/denom)
        op *= -1.0
        denom += 2.0
    return pi_4 * 4