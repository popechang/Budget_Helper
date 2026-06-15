"""
sorting.py содержит:
1. Функцию insertion_sort_categories() - сортировка категорий
по общей сумме расходов методом вставок
"""


def insertion_sort_categories(expenses):
    """
    Сортировка категорий по сумме трат методом вставок.
    Категории сортируются от большей суммы к меньшей.
    """
    categories_sum = {}

    # сначала считаем общую сумму по каждой категории
    for expense in expenses:
        if expense.category in categories_sum:
            categories_sum[expense.category] += expense.amount
        else:
            categories_sum[expense.category] = expense.amount

    # переводим словарь в список пар: категория и сумма
    category_list = []
    for category in categories_sum:
        category_list.append((category, categories_sum[category]))

    # сортировка вставками по сумме, от большей к меньшей
    for i in range(1, len(category_list)):
        key = category_list[i]
        j = i - 1

        while j >= 0 and category_list[j][1] < key[1]:
            category_list[j + 1] = category_list[j]
            j -= 1

        category_list[j + 1] = key

    return category_list
