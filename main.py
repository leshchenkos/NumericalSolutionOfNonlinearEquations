import numpy as np
import matplotlib.pyplot as plt


def get_fun(function_num):
    if function_num == '1':
        return np.linspace(-3, 3, 200), \
               lambda x: x ** 3 - x + 4
    elif function_num == '2':
        return np.linspace(-3, 3, 200), \
               lambda x: x ** 3 - 3 * (x ** 2) + 2 * x + 1
    elif function_num == '3':
        return np.linspace(-10, 10, 200), \
               lambda x: np.sin(x)
    else:
        return None


def file_input():
    with open("input.txt", 'rt') as file:
        try:
            fun_info = get_fun(file.readline())
            if fun_info is None:
                raise ValueError
            x, fun = fun_info
            ax = plt.gca()
            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            plt.plot(x, fun(x))
            plt.show()
            data = {'fun': fun}
            method = file.readline()
            if method != '1' and method != '2':
                raise ValueError
            data["method"] = method
            if method == '1':
                a, b = map(float, file.readline().strip().split())
                if fun(a) * fun(b) > 0:
                    raise ArithmeticError
                data['a'] = a
                data['b'] = b
            elif method == '2':
                x0 = float(file.readline())
                data['x0'] = x0
            err = float(file.readline())
            if err < 0:
                raise ArithmeticError
            data['err'] = err
            return data
        except (ValueError, ArithmeticError):
            return None


def keyboard_input():
    print("Выберите функцию: ")
    print("1 - x^3 - x + 4")
    print("2 - x^3 - 3x^2 + 2x + 1")
    print("3 - sin(x)")
    fun_info = get_fun(input())
    while fun_info is None:
        print("Ошибка, повторите попытку ввода")
        fun_info = get_fun(input())
    x, fun = fun_info
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.plot(x, fun(x))
    plt.show()
    hashMap = {'fun': fun}
    print("Выберите метод решения: ")
    print("1 - Метод секущих")
    print("2 - Метод простой итерации")
    method = input()
    while method != '1' and method != '2':
        print("Ошибка повторите попытку ввода")
        method = input()
    hashMap['method'] = method
    if method == '1':
        print("Введите границы интервала через пробел")
        while True:
            try:
                a, b = map(float, input().split())
                if fun(a) * fun(b) > 0:
                    raise ArithmeticError
                break
            except ArithmeticError:
                print("Ошибка, некорректный интервал")
        hashMap['a'] = a
        hashMap['b'] = b
    elif method == '2':
        print("Введите начальное приближение.")
        while True:
            try:
                x0 = float(input(""))
                break
            except ValueError:
                print("Ошибка ввода")
        hashMap['x0'] = x0
    print("Введите погрешность вычисления: ")
    while True:
        try:
            err = float(input())
            if err <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Ошибка, некорректные данные")
    hashMap['err'] = err
    return hashMap


def diff(n, x, f):
    h = 0.00000001
    if n <= 0:
        return None
    elif n == 1:
        return (f(x + h) - f(x)) / h
    return (diff(n - 1, x + h, f) - diff(n - 1, x, f)) / h


def secant_method(a, b, f, e):
    if f(a) * diff(2, a, f) > 0:
        x0 = a
    elif f(b) * diff(2, a, f) > 0:
        x0 = b
    else:
        return None
    x1 = x0 + e
    x = x1 + 2 * e
    iteration = 0
    while abs(x - x1) > e:
        x1, x, x0 = x1 - (x1 - x0) / (f(x1) - f(x0)) * f(x1), x1, x
        iteration = iteration + 1

    return x1, f(x1), iteration


def iteration_method(x0, f, e):
    def phi(x):
        return x + (-1 / diff(1, x, f)) * f(x)
    x = phi(x0)
    iteration = 0
    while abs(x - x0) > e:
        if diff(1, x, phi) >= 1:
            return None
        x0, x = x, phi(x)
        iteration = iteration + 1
    return x, f(x), iteration


def main():
    print("Лабораторная работа №2")
    print("Численное решение нелинейных уравнений и систем")
    print("Вариант 11")
    print("Автор: Лещенко Сергей")
    print()
    print("Для чтения с клавиатуры нажмите 1, для чтения из файла 2")
    choice = input()
    while choice != '1' and choice != '2':
        print("Ошибка, повторите попытку")
        choice = input()
    if choice == '1':
        data = keyboard_input()
    else:
        data = file_input()
        if data is None:
            print("Ошибка, неверно составлен файл")
            return None
    try:
        result = []
        if data['method'] == '1':
            result = secant_method(data['a'], data['b'], data['fun'], data['err'])
            if result is None:
                print("Знаки функций и вторых производных не равны ни в 'a', ни в 'b'.")
                raise ValueError
        elif data['method'] == '2':
            result = iteration_method(data['x0'], data['fun'], data['err'])
            if result is None:
                print("Не выполнено условие сходимости")
                raise ValueError

        print(f"Корень уравнения: {result[0]}")
        print(f"Значение функции в корне: {result[1]}")
        print(f"Число итераций: {result[2]}")
    except ValueError:
        pass


main()
