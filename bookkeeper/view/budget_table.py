from PySide6        import QtWidgets
from PySide6.QtCore import Qt

class BudgetTableWidget(QtWidgets.QTableWidget):
    """
    Виджет для бюджета.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Table configuration:
        self.setColumnCount(3)
        self.setRowCount(3)

        hheaders = "Бюджет Потрачено Остаток".split()
        self.setHorizontalHeaderLabels(hheaders)

        vheaders = "День Неделя Месяц".split()
        self.setVerticalHeaderLabels(vheaders)

        # Strech on resize:
        for h in [self.horizontalHeader(), self.verticalHeader()]:
            h.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Enter edit mode on double-click:
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)

    def add_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

class LabeledBudgetTable(QtWidgets.QGroupBox):
    """
    Виджет для бюджета с подписью.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label:
        self.label = QtWidgets.QLabel("<b>Бюджет</b>")
        self.label.setAlignment(Qt.AlignCenter)

        # Budget table:
        self.table = BudgetTableWidget()

        # Vertical layout:
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.table)

        self.setLayout(self.vbox)

    def add_data(self, data: list[list[str]]):
        self.table.add_data(data)
