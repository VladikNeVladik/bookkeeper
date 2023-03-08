from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from typing import Callable, Any

from bookkeeper.view.labeled import LabeledComboBoxInput, LabeledLineInput
from bookkeeper.models.category import Category

class NewExpense(QtWidgets.QGroupBox):
    def __init__(self,
        categories          : list[Category],
        edit_button_handler : Callable,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Categories:
        self.categories          = categories
        self.cat_names           = [c.name for c in categories]
        self.edit_button_handler = edit_button_handler

        # Label:
        self.label = QtWidgets.QLabel("<b>Новая трата</b>")
        self.label.setAlignment(Qt.AlignCenter)

        # Expense amount input line:
        self.amount_input = LabeledLineInput("Сумма", "0")

        # Expense category selection:
        self.category_input = LabeledComboBoxInput("Категория", self.cat_names)

        # Edit button:
        self.cats_edit_button = QtWidgets.QPushButton('Редактировать')
        self.cats_edit_button.clicked.connect(self.edit_button_handler)

        # Expense Submit
        self.submit_button = QtWidgets.QPushButton('Добавить')
        self.submit_button.clicked.connect(self.submit)

        # Grid layout:
        self.grid = QtWidgets.QGridLayout()

        # AddWidget parameter meaning -----------> Y  X  dY  dX
        self.grid.addWidget(self.label,            0, 0,  1,  3)
        self.grid.addWidget(self.amount_input,     1, 0,  1,  2)
        self.grid.addWidget(self.category_input,   2, 0,  1,  2)
        self.grid.addWidget(self.cats_edit_button, 2, 2,  1,  1)
        self.grid.addWidget(self.submit_button,    3, 0,  1,  2)

        self.setLayout(self.grid)

    def set_categories(self, categories: list[Category]):
        self.categories = categories
        self.cat_names  = [c.name for c in categories]
        self.category_input.set_items(self.cat_names)

    def submit(self):
        # FIXME: debug printout
        print(f"Новая трата в категории {self.category_input.text()} \
            на сумму {self.amount_input.text()} добавлена")

        self.amount_input.clear()
        self.category_input.clear()