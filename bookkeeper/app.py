import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from view.expense_table import LabeledExpenseTable

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Create window:
    window = QtWidgets.QWidget()
    window.setWindowTitle('Тестовый стенд')
    window.resize(350, 150)

    # Data to be rendered:
    data = [["2023-02-26 14:30:00", str( 100), "кофе",   ""],
            ["2023-02-26 14:00:00", str(1000), "одежда", ""],
            ["2023-02-25 18:30:00", str( 500), "мясо",   ""],
            ["2023-02-20 19:46:00", str(  33), "вода",   ""],]

    # Create expenses table:
    expenses = LabeledExpenseTable()
    expenses.add_data(data)

    # Create layout for window:
    horizontal_layout = QtWidgets.QHBoxLayout()

    horizontal_layout.addWidget(expenses)

    window.setLayout(horizontal_layout)

    # Render window:
    window.show()

    sys.exit(app.exec())
