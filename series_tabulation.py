"""
Лабораторна робота № 3.
Модуль розгалужених обчислень, чисельного табулювання та рекурентних рядів Тейлора.
Освітній компонент: Програмування на Python.
"""

import math
import sys
import time


def evaluate_piecewise_function(x: float) -> float:
    """
    Обчислює значення кусочно-неперервної функції f(x) за допомогою
    каскадної конструкції розгалуження if-elif-else.
    """
    if x < 0:
        # Перша аналітична гілка для x < 0
        y = x**3 - math.sin(x)
    elif 0 <= x <= 3:
        # Друга аналітична гілка для 0 <= x <= 3
        y = math.sqrt(2.0 * x + 1.0)
    else:
        # Третя аналітична гілка для x > 3
        y = math.cos(math.sqrt(x))
    return y


def tabulate_function(start_a: float, end_b: float, step_h: float) -> list:
    """
    Здійснює чисельне табулювання функції на проміжку [a, b] із кроком h
    за допомогою параметричного циклу for та генератора range().
    """
    if step_h <= 0.0:
        raise ValueError("Крок табулювання h повинен бути строго додатним числом.")
    if start_a > end_b:
        raise ValueError("Початкова межа інтервалу 'a' не може перевищувати кінцеву 'b'.")

    # Обчислення кількості вузлів сітки
    num_steps = int(math.floor((end_b - start_a) / step_h))
    tabulated_data = []

    for i in range(num_steps + 1):
        # Точне позиціонування координати вузла
        x_i = start_a + i * step_h

        # Корекція похибки представлення кінцевої точки
        if x_i > end_b and math.isclose(x_i, end_b, abs_tol=1e-9):
            x_i = end_b

        y_i = evaluate_piecewise_function(x_i)

        # Класифікація діапазону за допомогою тернарного оператора
        branch_tag = "Гілка 1" if x_i < 0 else ("Гілка 2" if x_i <= 3 else "Гілка 3")

        tabulated_data.append((x_i, y_i, branch_tag))

    return tabulated_data


def compute_taylor_sqrt(x: float, epsilon: float = 1e-7, max_iterations: int = 1000) -> tuple:
    """
    Обчислює значення 1 / sqrt(1+x) через розклад у ряд Тейлора
    за допомогою циклу while та рекурентного співвідношення.
    Повертає кортеж: (обчислена_сума, кількість_ітерацій, еталонне_значення, абсолютна_похибка).
    """
    if epsilon <= 0.0:
        raise ValueError("Параметр точності epsilon повинен бути строго більшим за нуль.")
    if 1.0 + x <= 0.0:
        raise ValueError("1 + x має бути > 0")

    k = 0
    a_k = 1.0
    series_sum = a_k

    # Ітераційне накопичення доданків за рекурентною формулою
    while math.fabs(a_k) >= epsilon and k < max_iterations:
        k += 1
        # Рекурентний коефіцієнт R(k, x) = x^2 / (2k * (2k - 1))
        recurrence_ratio = (x * x) / (2.0 * k * (2.0 * k - 1.0))
        a_k *= recurrence_ratio
        series_sum += a_k
    else:
        # Специфіка блоку else у циклах Python
        if k >= max_iterations:
            print(f"Попередження: Досягнуто ліміт ітерацій ({max_iterations}) для x = {x:.4f}!")

    reference_val = 1.0 / math.sqrt(1.0 + x)
    absolute_error = math.fabs(series_sum - reference_val)

    return series_sum, k, reference_val, absolute_error


def print_tabulation_table(data: list) -> None:
    """Виводить на екран відформатовану таблицю значень функції."""
    separator = "=" * 65
    sub_sep = "-" * 65

    print(separator)
    print(f"{'ТАБЛИЦЯ ТАБУЛЮВАННЯ КУСОЧНОЇ ФУНКЦІЇ f(x)':^65}")
    print(separator)
    print(f"| {'№':^4} | {'Вузол x':^14} | {'Значення y = f(x)':^20} | {'Сегмент':^14} |")
    print(sub_sep)

    for idx, (x_val, y_val, tag) in enumerate(data, start=1):
        print(f"| {idx:^4} | {x_val:^14.4f} | {y_val:^20.8f} | {tag:^14} |")

    print(separator)


def main() -> None:
    """Головна функція демонстрації розгалужених та циклічних обчислень."""
    print("\n" + "#" * 80)
    print(f"{'ДЕМОНСТРАЦІЯ РОЗГАЛУЖЕНЬ ТА ЦИКЛІЧНИХ ПРОЦЕСІВ (ЛБ №3)':^80}")
    print("#" * 80 + "\n")

    # 1. Виконання чисельного табулювання кусочної функції
    a_start = -2.0
    b_end = 6.0
    h_step = 0.4
    tab_results = tabulate_function(a_start, b_end, h_step)
    print_tabulation_table(tab_results)

    # 2. Обчислення нескінченного ряду Тейлора для 1 / sqrt(1+x) у контрольних точках
    print("\n" + "=" * 80)
    print(f"{'ОБЧИСЛЕННЯ РЯДУ ТЕЙЛОРА 1 / sqrt(1+x) ІЗ ТОЧНІСТЮ eps = 1e-7':^80}")
    print("=" * 80)
    print(f"| {'Аргумент x':^10} | {'Сума ряду S(x)':^18} | {'Еталон 1 / sqrt(1+x)':^18} | {'Ітерацій':^8} | {'Похибка':^14} |")
    print("-" * 80)
    test_points = [-0.5, -0.2, 0.0, 0.5, 1.0, 2.0, 3.0]
    target_eps = 1e-7
    for x_test in test_points:
        calc_s, steps, ref_s, err = compute_taylor_sqrt(x_test, target_eps)
        print(f"| {x_test:^10.2f} | {calc_s:^18.10f} | {ref_s:^18.10f} | {steps:^8} | {err:^14.4e} |")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    t_start = time.perf_counter()
    main()
    t_elapsed = time.perf_counter() - t_start
    print(f"Загальний час виконання розрахунків: {t_elapsed * 1000:.3f} мс\n")