import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from view.labeled import LabeledComboBoxInput

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Create window:
    window = QtWidgets.QWidget()
    window.setWindowTitle('Тестовый стенд')
    window.resize(350, 150)

    # Create layout for window:
    horizontal_layout = QtWidgets.QHBoxLayout()

    # Create checkboxes:
    line_input = LabeledComboBoxInput(
        "Какое животное вы кусаити?", ["собак", "капiбара", "андатра"])

    horizontal_layout.addWidget(line_input)

    # Render window:
    window.setLayout(horizontal_layout)
    window.show()

    sys.exit(app.exec())
