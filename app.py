from PySide6 import QtWidgets
from PySide6.QtCore import Qt

import sys

from bookkeeper.view.expense_table import LabeledExpenseTable
from bookkeeper.view.new_expense   import NewExpense
from bookkeeper.models.category import Category

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Create window:
    window = QtWidgets.QWidget()
    window.setWindowTitle('Тестовый стенд')
    window.resize(350, 150)

    # Create expenses table:
    expenses = LabeledExpenseTable()

    expense_data = [["2023-02-26 14:30:00", str( 100), "кофе",   ""],
                    ["2023-02-26 14:00:00", str(1000), "одежда", ""],
                    ["2023-02-25 18:30:00", str( 500), "мясо",   ""],
                    ["2023-02-20 19:46:00", str(  33), "вода",   ""],]

    expenses.add_data(expense_data)

    # Create new expense:
    categories = [Category(f"Категория {2*i}") for i in range(11)]
    new_expense = NewExpense(categories, None)

    # Create layout for window:
    vertical_layout = QtWidgets.QVBoxLayout()

    vertical_layout.addWidget(expenses)
    vertical_layout.addWidget(new_expense)

    window.setLayout(vertical_layout)

    # Render window:
    window.show()

    sys.exit(app.exec())
