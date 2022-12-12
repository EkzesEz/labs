"""
Finding errors for 2 wires mode and for 4 wires mode (R +/- delta, P)
Finding average, STD for resistors and capacitors,
check if it obey the normal law.
Check if it belong to E48 and E24 raws.
Export all data in excel file. (name it output1.xlsx)
"""


import pandas as pd
import math
from typing import NamedTuple


class Errors(NamedTuple):
    x_avg: float
    delta: float
    P: float = 0.95


def _get_theta(reading: float, range: int) -> float: # works only for range <= 200 Ohm
    if range <= 200:
        return (0.03*reading + 0.005 * range)/100
    raise ValueError


def _find_error(data: pd.Series) -> Errors:
    # finding Theta
    n = data.count()
    t = 2.093 if n == 20 else 2.009
    k = 1.0976
    range = 200
    mean = float(data.mean())
    std = data.std()
    sigma_theta = _get_theta(mean, range) / math.sqrt(3)
    Theta = k * sigma_theta
    sigma_x = std / math.sqrt(n)
    eps = t*sigma_x
    sigma_sum = math.sqrt(sigma_theta ** 2 + sigma_x ** 2)
    K = (eps + Theta) / (sigma_x + sigma_theta)
    delta = K * sigma_sum
    return Errors(x_avg = mean, delta = delta)


def _get_d(data: pd.Series) -> float:
    n = int(data.count())
    sigma_sm = data.std(ddof=0)
    l = [abs(data[i] - data.mean()) for i in range(1, n+1)]
    #print(n, sigma_sm, l)
    d = float(sum(l) / (n*sigma_sm))
    return d


def _count_m(data: pd.Series) -> int:
    counter = 0
    z = 2.58
    mean = data.mean()
    std = data.std()
    i = 1
    for i in range(1, data.count() + 1):
        if abs(data[i] - mean) > z*std:
            counter += 1
    return counter


def _is_normal_law(data: pd.Series) -> bool:
    d_max = 0.9001
    d_min = 0.695
    m_max = 1
    d = _get_d(data)
    m = _count_m(data)
    flag1 = d > d_min and d < d_max
    flag2 = m < m_max
    return flag1 and flag2


def main():
    filename = "СМ5-31Б_ЛР1_Поседкин_НМ_Паламарчук_АД.xlsx"

    try:
        data = pd.read_excel(filename, index_col=0, header=1)
    except:
        print("file not found")
        exit(0)
    for i in data:
        if 'WR' in i:
           print(i, "{}±{}, {}".format(*_find_error(data[i])), sep='\n')
        else:
            print(f'for {i} mean={data[i].mean()}, std={data[i].std()}')
            print(f"d = {_get_d(data[i])}")
            print(f"m = {_count_m(data[i])}")
            print(i, ("" if _is_normal_law(data[i]) else "not"), 'obey the normal law')


if __name__ == '__main__':
    main()
