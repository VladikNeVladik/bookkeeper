from PySide6        import QtWidgets
from PySide6.QtCore import Qt

class ExpenseTableWidget(QtWidgets.QTableWidget):
    """
    Виджет для расхода.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Table configuration:
        self.setColumnCount(4)
        self.setRowCount(20)

        headers = "Дата Сумма Категория Комментарий".split()
        self.setHorizontalHeaderLabels(headers)

        # Configure table header:
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        # Disable vertical header:
        self.verticalHeader().hide()

        # Enter edit mode on double-click:
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)

    def add_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(item.capitalize())
                )

class LabeledExpenseTable(QtWidgets.QGroupBox):
    """
    Виджет для расхода с подписью.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label:
        self.label = QtWidgets.QLabel("<b>Последние траты</b>")
        self.label.setAlignment(Qt.AlignCenter)

        # Expenses table:
        self.table = ExpenseTableWidget()

        # Vertical layout:
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.table)

        self.setLayout(self.vbox)

    def add_data(self, data: list[list[str]]):
        self.table.add_data(data)
