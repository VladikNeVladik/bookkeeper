from PySide6        import QtWidgets
from PySide6.QtCore import Signal, Qt

from typing import Callable, Any

from bookkeeper.models.budget import Budget, Period

class BudgetTableWidget(QtWidgets.QTableWidget):
    """
    Виджет для бюджета.
    """

    cellDoubleClicked : Signal  # Double click handler with attachable pre-handler
    cellChanged       : Signal  # Cell edit handler with attachable pre-handler

    def __init__(self,
        budget_modify_handler : Callable[[int, str, str], None],
        *args                 : Any,
        **kwargs              : Any
    ):
        super().__init__(*args, **kwargs)

        self.budget_modify_handler = budget_modify_handler

        self.row_to_period = {0:"day",
                              1:"week",
                              2:"month"}

        # Table configuration:
        self.setColumnCount(3)
        self.setRowCount(3)

        hheaders = "Бюджет Потрачено Остаток".split()
        self.setHorizontalHeaderLabels(hheaders)

        vheaders = "День Неделя Месяц".split()
        self.setVerticalHeaderLabels(vheaders)

        # Strech on resize:
        for h in [self.horizontalHeader(), self.verticalHeader()]:
            h.setSectionResizeMode(QtWidgets.QHeaderView.Stretch) # type: ignore

        # Enter edit mode on double-click:
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked) # type: ignore

        # On double click set "cell edited" handler
        self.cellDoubleClicked.connect(self.double_click)

    def double_click(self, row: int, columns: int) -> None:
        self.cellChanged.connect(self.cell_changed)

    def cell_changed(self, row: int, column: int) -> None:
        # Disconnect this handler:
        self.cellChanged.disconnect(self.cell_changed)

        # Perform the database request:
        pk        = int(self.data[row][-1])
        new_limit = self.item(row, column).text()
        self.budget_modify_handler(pk, new_limit, self.row_to_period[row])


    def add_data(self, data: list[list[str]]) -> None:
        self.data = data

        # Fill the table with data:
        for i, row in enumerate(data):
            for j, x in enumerate(row[:-1]):
                self.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x.capitalize())
                )

                # Set the alignment:
                self.item(i, j).setTextAlignment(Qt.AlignCenter)  # type: ignore

                # Select the upper row for edit:
                if j == 0:
                    self.item(i, j).setFlags(Qt.ItemIsEditable       # type: ignore
                                             | Qt.ItemIsEnabled      # type: ignore
                                             | Qt.ItemIsSelectable)  # type: ignore
                else:
                    self.item(i, j).setFlags(Qt.ItemIsEnabled)  # type: ignore


class LabeledBudgetTable(QtWidgets.QGroupBox):
    """
    Виджет для бюджета с подписью.
    """

    def __init__(
        self,
        budget_modify_handler : Callable[[int, str, str], None],
        *args                 : Any,
        **kwargs              : Any
    ):
        super().__init__(*args, **kwargs)

        # Label:
        self.label = QtWidgets.QLabel("<b>Бюджет</b>")
        self.label.setAlignment(Qt.AlignCenter)  # type: ignore

        # Budget table:
        self.table = BudgetTableWidget(budget_modify_handler)

        # Vertical layout:
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.table)

        self.setLayout(self.vbox)

    def set_budgets(self, budgets: list[Budget]) -> None:
        self.budgets = budgets
        self.data    = self.budgets_to_data(self.budgets)

        self.table.clearContents()
        self.table.add_data(self.data)

    def budgets_to_data(self, budgets: list[Budget]) -> list[list[str]]:
        data = []

        # Iterate over subtables:
        for period in [Period.DAY, Period.WEEK, Period.MONTH]:
            bdg = [b for b in budgets if b.period == period]
            if len(bdg) == 0:
                data.append(["- Не установлен -", "", "", ""])
            else:
                b = bdg[0]
                data.append([str(b.limitation),
                             str(b.spent),
                             str(b.limitation - b.spent),
                             str(b.pk)])
        return data
