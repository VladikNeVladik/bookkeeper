from PySide6        import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui  import QAction

from bookkeeper.view.labelef     import LabeledCheckBox
from bookkeeper.view.budget      import BudgetTableGroup
from bookkeeper.view.expenses    import ExpensesTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup

from bookkeeper.models.category import Category

class MainWindow(QtWidgets.QWidget):
    """
    Главное окно программы.
    """

    def __init__(self,
        budget_table  : BudgetTableGroup,
        new_expense   : NewExpenseGroup,
        expense_table : ExpensesTableGroup,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Window options:
        self.setWindowTitle("Bookkeeper")

        # Window internal widgets:
        self.budget_table   = budget_table
        self.new_expense    = new_expense
        self.expenses_table = expenses_table

        # Vertical layout:
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.budget_table,   stretch=3)
        self.vbox.addWidget(self.new_expense,    stretch=1)
        self.vbox.addWidget(self.expenses_table, stretch=6)

        self.setLayout(self.vbox)

    def closeEvent(self, event):
        # Spawn a messagebox:
        reply = QtWidgets.QMessageBox.question(self,
            "Закрыть приложение",
            "Вы уверены?\nВсе несохраненные данные будут потеряны.")

        # Parse Yes/No reply:
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            app = QtWidgets.QApplication.instance()
            app.closeAllWindows()
        else:
            event.ignore()
