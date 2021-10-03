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


def forward_rate(data, delta):
    fr = []
    i = 0
    for bond in data:
        if i == 0:
            fr.append(zero(bond[0], bond[1], bond[3]))
        else:
            pre_price = data[i-1][3]
            fr.append(np.log(pre_price/bond[3])/delta)
        i += 1
    return fr


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
    print(zeros(data0))
    print(forward_rate(data0, 0.5))
