"""
Это модуль с убер-функциями
"""


def add(a_arg: int, b_arg: int):
    """
    Функция для сложения a и b
    """
    return a_arg + b_arg


def sub(a_arg: int, b_arg: int):
    """
    Функция для вычитания a и b
    """
    return a_arg - b_arg


def mult(a_arg: int, b_arg: int):
    """
    Функция для умножения a и b
    """
    return a_arg * b_arg


def round_div(a_arg: int, b_arg: int):
    """
    Функция для целочисленного деления a и b
    """
    return a_arg // b_arg


if __name__ == "__main__":
    a, b = [int(x) for x in input().split()]
    result = add(a, b) * mult(a, b) - sub(a, b) * round_div(a, b)
    print(result)
