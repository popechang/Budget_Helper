"""
data.py содержит:
1. Класс Expense, содержащий информацию об одном конкретном расходе
2. Класс TreeNode, хранящий узел дерева расходов по дням
3. Функции inorder() (симметричный обход) и insert() (вставить расход)
для работы с деревом
"""

class Expense:
    """
    Класс одного расхода: сохраняет день, сумму и категорию расхода.
    """
    def __init__(self, day, amount, category):
        self.day = day
        self.amount = amount
        self.category = category

    def __str__(self):
        # Для вывода расхода
        return f"День: {self.day}, Сумма: {self.amount}, Категория: {self.category}"


class TreeNode:
    """
    Класс для узлов дерева, в которых хранятся расходы.
    Хранит расход и "детей".
    """
    def __init__(self, expense):
        self.expense = expense
        self.left = None
        self.right = None


def insert(tree, expense):
    """
    Добавление расхода в дерево по дням.
    Если день расхода меньше существующего узла -
    влево, если больше - вправо.
    """
    if tree is None:
        return TreeNode(expense)

    if expense.day < tree.expense.day:
        tree.left = insert(tree.left, expense)
    else:
        tree.right = insert(tree.right, expense)

    return tree


def inorder(tree):
    """
    Симметричный обход дерева и вывод: левая ветвь - корень - правая ветвь.
    """
    result = []

    if tree:
        result += inorder(tree.left)
        print(tree.expense)
        result.append(tree.expense)
        result += inorder(tree.right)

    return result
