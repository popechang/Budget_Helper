"""
expenses.py содержит:
1. Функцию add_expense() - добавление нового расхода в список и обновление суммы за день
2. Функцию remove_expense() - удаление расхода из списка и обновление суммы за день
3. Функцию get_max_expense_day() - линейный поиск дня с максимальной суммой расходов
"""
from data import Expense

def add_expense(expenses, daily_expenses, day, amount, category):
    """
    Добавление нового расхода в список расходов и
    обновляет сумму расходов за соответствующий день.
    """

    expense = Expense(day, amount, category)

    expenses.append(expense)
    daily_expenses[day - 1] += amount

    return expense


def remove_expense(expenses, daily_expenses, expense=None):
    """
    Удаляет расход из общего списка и обновляет сумму
    расходов за соответствующий день.
    """
    # если расход не передали, берем последний добавленный
    if expense is None:
        if len(expenses) == 0:
            return None
        expense = expenses[-1]

    try:
        index = expenses.index(expense)
        expenses.pop(index)
        daily_expenses[expense.day - 1] -= expense.amount
        return expense
    except ValueError:
        return None



def get_max_expense_day(daily_expenses):
    """
    Линейный поиск дня с наибольшим расходом.
    Расходы за каждый день сравниваются с текущим максимумом.
    """
    if len(daily_expenses) == 0:
        return None, 0

    max_day = 1
    max_sum = daily_expenses[0]

    # проходим по всем дням подряд и ищем самый большой расход
    for i in range(len(daily_expenses)):
        if daily_expenses[i] > max_sum:
            max_sum = daily_expenses[i]
            max_day = i + 1

    return max_day, max_sum
