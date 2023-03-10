from PySide6        import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui  import QAction

from bookkeeper.view.labeled       import LabeledCheckBox
from bookkeeper.view.budget_table  import LabeledBudgetTable
from bookkeeper.view.expense_table import LabeledExpenseTable
from bookkeeper.view.new_expense   import NewExpense

from bookkeeper.models.category import Category

class MainWindow(QtWidgets.QWidget):
    """
    Главное окно программы.
    """

    def __init__(self,
        budget_table  : LabeledBudgetTable,
        new_expense   : NewExpense,
        expense_table : LabeledExpenseTable,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Window options:
        self.setWindowTitle("Bookkeeper")

        # Window internal widgets:
        self.budget_table  = budget_table
        self.new_expense   = new_expense
        self.expense_table = expense_table

        # Vertical layout:
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.budget_table,  stretch=3)
        self.vbox.addWidget(self.new_expense,   stretch=1)
        self.vbox.addWidget(self.expense_table, stretch=6)

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
