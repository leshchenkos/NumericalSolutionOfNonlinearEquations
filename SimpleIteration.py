import numpy as np


def get_phi1(x1, x2):
    return 0.3 - 0.1 * x1 * x1 - 0.2 * x2 * x2


def get_phi2(x1, x2):
    return 0.7 - 0.2 * x1 * x1 - 0.1 * x1 * x2


def checkDiffConv_phi1(x1, x2):
    return abs(-0.2 * x1) + abs(-0.4 * x2)


def checkDiffConv_phi2(x1, x2):
    return abs(-0.4 * x1 + 0.1 * x2) + abs(0.1 * x1)


def alg(eps):
    arr = np.linspace(0, 1, 100, endpoint=False)
    for i in arr:
        for j in arr:
            if checkDiffConv_phi1(i, j) >= 1 or checkDiffConv_phi2(i, j) >= 1:
                print("Ошибка, нарушено условие сходимости")
                return None
    iterations = 0
    x1_err = []
    x2_err = []
    x1_0 = 1
    x2_0 = 1
    x1 = get_phi1(x1_0, x2_0)
    x2 = get_phi2(x1_0, x2_0)
    while max(abs(x1 - x1_0), abs(x2 - x2_0)) > eps:
        x1_0 = x1
        x2_0 = x2
        x1 = get_phi1(x1_0, x2_0)
        x2 = get_phi2(x1_0, x2_0)
        x1_err.append(abs(x1 - x1_0))
        x2_err.append(abs(x2 - x2_0))
        iterations = iterations + 1
    print()
    print("Вектор неизвестных: ")
    print(x1)
    print(x2)
    print()
    print("Вектор погрешностей для x1: ")
    for i in x1_err:
        print(i)
    print()
    print("Вектор погрешностей для x2: ")
    for i in x2_err:
        print(i)
    print("Количество итераций: ")
    print()
    print(iterations)


alg(0.01)
