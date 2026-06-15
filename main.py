"""
main.py содержит:
1. Функцию rebuild_tree() - пересборка дерева расходов после удаления
2. Функцию show_daily_chart() - отображение вертикальной
гистограммы расходов по дням через matplotlib
3. Функцию show_category_chart() - отображение гистограммы
расходов по категориям через matplotlib
4. Функцию main() - основная функция программы с меню и обработкой
ввода пользователя
"""

from expenses import add_expense, remove_expense, get_max_expense_day
from prefix_sums import build_prefix_sums, get_interval_sum
from sorting import insertion_sort_categories
from undo_stack import push, pop
from data import insert, inorder
import matplotlib.pyplot as plt


def rebuild_tree(expenses):
    """
    Пересборка дерева заново после удаления расхода.
    Это нужно для правильной работы отмены последнего добавления.
    """
    root = None

    for expense in expenses:
        root = insert(root, expense)

    return root


def show_daily_chart(expenses_by_day):
    """
    Отображение вертикальной гистограммы расходов по дням.
    График выводится отдельной картинкой через matplotlib.
    """
    max_expense = max(expenses_by_day)

    # если расходов нет, то делить на 0 нельзя
    if max_expense == 0:
        print("Расходов пока нет.")
        return

    days = list(range(1, len(expenses_by_day) + 1))

    plt.figure(figsize=(12, 6))
    plt.bar(days, expenses_by_day)
    plt.xlabel("День")
    plt.ylabel("Расходы, ₽")
    plt.title("Вертикальная гистограмма расходов по дням")
    plt.xticks(days)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    for day, amount in zip(days, expenses_by_day):
        if amount > 0:
            plt.text(day, amount, f"{amount:.2f}₽", ha="center", va="bottom")

    plt.tight_layout()
    plt.show()


def show_category_chart(expenses):
    """
    Отображение гистограммы расходов по категориям.
    График выводится отдельной картинкой через matplotlib.
    """
    sorted_categories = insertion_sort_categories(expenses)

    if len(sorted_categories) == 0:
        print("Категорий пока нет.")
        return

    categories = []
    amounts = []

    # переносим категории и суммы в отдельные списки для графика
    for category, amount in sorted_categories:
        categories.append(category)
        amounts.append(amount)

    figure_width = max(10, len(categories))

    plt.figure(figsize=(figure_width, 6))
    plt.bar(categories, amounts)
    plt.xlabel("Категория")
    plt.ylabel("Расходы, ₽")
    plt.title("Расходы по категориям")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.xticks(rotation=0, ha="center")

    for category, amount in zip(categories, amounts):
        plt.text(category, amount, f"{amount:.2f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.show()


def main():
    """
    Основная функция программы.
    В ней находится меню и обработка выбора пользователя.
    """
    expenses = []
    daily_expenses = [0] * 31
    undo_stack = []
    root = None

    while True:
        print("\n======== Бюджетный помощник ========")
        print("1. Добавить расход")
        print("2. Показать дерево расходов")
        print("3. Сумма расходов за период")
        print("4. День с максимальным расходом")
        print("5. Сортировка категорий по сумме трат")
        print("6. Отменить последний добавленный расход")
        print("7. Вертикальная гистограмма расходов по дням")
        print("8. Гистограмма расходов по категориям")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            # проверка на правильность ввода
            while True:
                try:
                    day = int(input("День: "))
                    if day < 1 or day > 31:
                        print("Ошибка: день должен быть от 1 до 31")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите целое число")

            while True:
                try:
                    amount = float(input("Сумма: "))
                    if amount <= 0:
                        print("Ошибка: сумма должна быть положительной")
                        continue
                    if amount > 1000000:
                        print("Ошибка: сумма не может превышать 1,000,000")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите число")

            category = input("Категория: ")
            if not category:
                category = "Без категории"
                print("Категория не указана, установлено 'Без категории'")

            # добавляем расход во все нужные структуры
            expense = add_expense(
                expenses,
                daily_expenses,
                day,
                amount,
                category
            )
            push(undo_stack, expense)
            root = insert(root, expense)

            print("Расход добавлен.")

        elif choice == "2":
            if root is None:
                print("Расходов нет.")
            else:
                inorder(root)

        elif choice == "3":
            # Проверки ввода
            if len(expenses) == 0:
                print("Расходов пока нет. Сумма за период: 0")
                continue

            while True:
                try:
                    start_day = int(input("Начальный день: "))
                    if start_day < 1 or start_day > 31:
                        print("Ошибка: день должен быть от 1 до 31")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите целое число")

            while True:
                try:
                    end_day = int(input("Конечный день: "))
                    if end_day < 1 or end_day > 31:
                        print("Ошибка: день должен быть от 1 до 31")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите целое число")

            if start_day > end_day:
                print("Ошибка: начальный день не может быть больше конечного")
                continue
            # строим префиксные суммы и быстро считаем сумму за период
            prefix = build_prefix_sums(daily_expenses)
            total = get_interval_sum(prefix, start_day, end_day)

            print(f"Сумма расходов с {start_day} по {end_day}: {total}")

        elif choice == "4":
            max_day, max_sum = get_max_expense_day(daily_expenses)
            if max_day is None or max_sum == 0:
                print("Пока расходов нет")
            else:
                print(f"Максимальный расход был в день {max_day}: {max_sum}")

        elif choice == "5":
            sorted_categories = insertion_sort_categories(expenses)

            if len(sorted_categories) == 0:
                print("Категорий пока нет.")
            else:
                print("Категории по сумме трат:")
                for category, amount in sorted_categories:
                    print(f"{category}: {amount}")

        elif choice == "6":
            last_expense = pop(undo_stack)

            if last_expense is None:
                print("Отменять нечего.")
            else:
                # удаляем расход и пересобираем дерево
                remove_expense(expenses, daily_expenses, last_expense)
                root = rebuild_tree(expenses)
                print("Последний расход отменён.")

        elif choice == "7":
            show_daily_chart(daily_expenses)

        elif choice == "8":
            show_category_chart(expenses)

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
