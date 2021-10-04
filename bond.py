import numpy as np


def zero(principal, comp, price):
    return np.log(principal/price)/comp


def bootstrap(principal, comp, coupon, price, previous):
    _sum = 0
    freq = comp/(len(previous)+1)
    time = freq
    for i in previous:
        _sum += coupon*np.exp(-time*i)
        time += freq
    return np.log((principal+coupon)/(price-_sum))/comp


def zeros(data):
    zero_rate = []
    for bond in data:
        if bond[1] == 0:
            zero_rate.append(zero(bond[0], bond[2], bond[3]))
        else:
            zero_rate.append(bootstrap(bond[0], bond[1], bond[2], bond[3], zero_rate))
    return zero_rate


def forward_rate(zero_rate, unit=1):
    fr = []
    i = 1
    comp = unit
    while i < len(zero_rate):
        comp += 1
        fr_value = (zero_rate[i]*comp-zero_rate[i-1]*(comp-1)) / unit
        fr.append(fr_value)
        i += 1
    return fr


def bond_price(par, c, y, m, unit):
    t = m / unit
    i = 1
    p = 0
    while i < t:
        p += c * np.exp(-y * unit * i)
        i += 1
    p += (par+c)*np.exp(-y*m)
    return p


def duration(par, c, y, m, unit):
    t = m / unit
    i = 1
    d = 0
    p = bond_price(par, c, y, m, unit)
    while i < t:
        d += unit * i * (c * np.exp(-y * unit * i) / p)
        i += 1
    d += m*((par+c)*np.exp(-y*m)/p)
    return d


def icm_price(p, d, icm_y):
    return -d*icm_y*p


if __name__ == "__main__":
    _data = [
        [100, 0.50, 0, 94.9],
        [100, 1.00, 0, 90.0],
        [100, 1.50, 4, 96.0],
        [100, 2.00, 6, 101.6]
    ]

    data23 = [
        [100, 0.50, 0, 94.00],
        [100, 1.00, 0, 89.00],
        [100, 1.50, 4, 94.84],
        [100, 2.00, 5, 97.12]
    ]

    data0 = [
        [100, 0.50, 0, 99.5],
        [100, 1.00, 0, 98.3],
        [100, 1.50, 0, 97.1]
    ]
    # print(zeros(data0))

    # 4.14 answer
    _zero_rate0 = [0.02, 0.03, 0.037, 0.042, 0.045]
    print("4.14: "+str(forward_rate(_zero_rate0)))
    print("----------------------------------------")

    # 4.22 answers
    B = bond_price(100, 100*0.08, 0.11, 5, 1.0)
    print("4.22-a: "+str(B))
    D = duration(100, 100*0.08, 0.11, 5, 1.0)
    print("4.22-b: "+str(D))
    icm_p = icm_price(B, D, -0.002)
    print("4.22-c: The increment is " + str(icm_p))
    print("4.22-c: The bond price becomes " + str(B+icm_p))
    change = bond_price(100, 100*0.08, 0.108, 5, 1.0)
    print("4.22-d: " + str(change))
    print("----------------------------------------")

    # 4.35 answers
    print("4.35")
    print("(a)")
    A_price = bond_price(2000, 0, 0.1, 1, 1) + bond_price(6000, 0, 0.1, 10, 1)
    print("The price of A: "+str(A_price))
    A_duration = (1*2000*np.exp(-0.1*1)+10*6000*np.exp(-0.1*10))/A_price
    print("portfolio A duration is " + str(A_duration))
    B_price = bond_price(5000, 0, 0.1, 5.95, 1)
    print("The price of B: "+str(B_price))
    B_duration = duration(5000, 0, 0.1, 5.95, 1)
    print("portfolio B duration is " + str(B_duration))

    print("(b)")
    icm_A = icm_price(A_price, A_duration, 0.001)
    print("change percentage of price A after 0.1% increase in yields: " + str((A_price+icm_A)/A_price-1))
    icm_B = icm_price(B_price, B_duration, 0.001)
    print("change percentage of price B after 0.1% increase in yields: " + str((B_price+icm_B)/B_price-1))

    print("(c)")
    icm_case_c = icm_price(B_price, B_duration, 0.05)
    answer = (B_price+icm_case_c)/B_price-1
    print(answer)
    icm_case_d = icm_price(A_price, A_duration, 0.05)
    compare = (A_price+icm_case_d)/A_price-1
    print(compare)
    print("----------------------------------------")
