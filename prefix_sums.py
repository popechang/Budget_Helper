"""
prefix_sums.py содержит:
1. Функцию build_prefix_sums() - построение массива префиксных сумм
2. Функцию get_interval_sum() - получение суммы расходов за период
"""


def build_prefix_sums(daily_expenses):
    """
    Построение массива префиксных сумм.
    prefix[i] хранит сумму расходов с 1 дня до i дня.
    """
    prefix = [0] * (len(daily_expenses) + 1)

    for i in range(len(daily_expenses)):
        prefix[i + 1] = prefix[i] + daily_expenses[i]

    return prefix


def get_interval_sum(prefix, start_day, end_day):
    """
    Получение суммы расходов за период за O(1).
    Берем сумму до end_day и вычитаем сумму до дня перед start_day.
    """
    return prefix[end_day] - prefix[start_day - 1]
