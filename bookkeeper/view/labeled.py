from PySide6        import QtWidgets
from PySide6.QtCore import Qt

from typing import Callable, Any

class LabeledCheckBox(QtWidgets.QWidget):
    """
    Чекбокс с подписью.
    """

    def __init__(
        self,
        label_text       : str,
        checkbox_handler : Callable = None,
        init_state       : Any      = Qt.Unchecked,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Checkbox:
        self.check_box = QtWidgets.QCheckBox()

        self.check_box.setCheckState(init_state)
        if checkbox_handler is not None:
            self.check_box.stateChanged.connect(checkbox_handler)

        # It's label:
        self.label = QtWidgets.QLabel(label_text)

        # Horizontal layout:
        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.check_box, stretch=1)
        self.layout.addWidget(self.label, stretch=1)

        self.setLayout(self.layout)

class LabeledLineInput(QtWidgets.QWidget):
    """
    Поле ввода с подписью.
    """

    def __init__(self, label_text: str, placeholder: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder

        # Label:
        self.label = QtWidgets.QLabel(label_text)

        # Line-edit:
        self.input = QtWidgets.QLineEdit(self.placeholder)

        # Horizontal layout:
        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.input, stretch=5)

        self.setLayout(self.layout)

    def clear(self):
        self.input.setText(self.placeholder)

    def text(self):
        return self.input.text()

    def set_text(self, text: str) -> None:
        self.input.setText(text)

class LabeledComboBoxInput(QtWidgets.QWidget):
    """
    Поле выбора из нескольких вариантов.
    """

    def __init__(self, text: str, items: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label:
        self.label = QtWidgets.QLabel(text)

        # Combo box:
        self.combo_box = QtWidgets.QComboBox()

        self.combo_box.setEditable(True)
        self.combo_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combo_box.setMaxVisibleItems(16)

        self.set_items(items)

        # Horizontal layout:
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.combo_box, stretch=5)

        self.setLayout(self.layout)

    def clear(self):
        self.combo_box.setCurrentText(self.combo_box.placeholderText())

    def text(self):
        return self.combo_box.currentText()

    def set_text(self, text: str) -> None:
        self.combo_box.setCurrentText(text)

    def set_items(self, items: list[str]):
        self.items = items

        self.combo_box.clear()
        self.combo_box.addItems(items)

        if len(items) != 0:
            self.combo_box.setPlaceholderText(items[0])
        else:
            self.combo_box.setPlaceholderText("...")

        self.clear()
