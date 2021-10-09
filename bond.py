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


def forward_price(asset_price, zero_rate, maturity):
    return asset_price*np.exp(zero_rate*maturity)


if __name__ == "__main__":
    _data = [
        [100, 0.50, 0, 94.9],
        [100, 1.00, 0, 90.0],
        [100, 1.50, 4, 96.0],
        [100, 2.00, 6, 101.6]
    ]

    print(forward_price(1.05, 0.01, 2/12))
    pv = lambda x, y, z: x*np.exp(-y*z)
    storage_cost = forward_price(sum([25, pv(0.06, 0.05, 3/12), pv(0.06, 0.05, 6/12), pv(0.06, 0.05, 9/12)]),
                                 0.05, 9/12)
    print(storage_cost)
