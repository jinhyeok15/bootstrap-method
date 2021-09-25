import numpy as np


def zero(principal, comp, price):
    return np.log(principal/price)/comp


def bootstrap(principal, coupon, comp, price, previous):
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
        if bond[2] == 0:
            zero_rate.append(zero(bond[0], bond[1], bond[3]))
        else:
            zero_rate.append(bootstrap(bond[0], bond[2], bond[1], bond[3], zero_rate))
    return zero_rate


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
    print(zeros(data23))
