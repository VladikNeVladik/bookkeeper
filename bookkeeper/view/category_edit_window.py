from PySide6        import QtWidgets
from PySide6.QtCore import Qt

from typing import Callable

from bookkeeper.models.category import Category
from bookkeeper.view.labeled    import LabeledComboBoxInput, LabeledLineInput

class CategoriesEditWindow(QtWidgets.QWidget):
    """
    Окно для добавления/редактирования/удаления категорий
    """

    # Class static variables:
    NO_PARENT_CATEGORY: str = "- Без родительской категории -"

    def __init__(self,
        cats               : list[Category],
        cat_add_handler    : Callable,
        cat_delete_handler : Callable,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.cat_add_handler    : Callable = cat_add_handler
        self.cat_delete_handler : Callable = cat_delete_handler

        #===============#
        # Category tree #
        #===============#
        # Label:
        label_cats = QtWidgets.QLabel("<b>Список категорий</b>")
        label_cats.setAlignment(Qt.AlignCenter)

        # Category tree:
        self.cat_tree = QtWidgets.QTreeWidget()
        self.cat_tree.setHeaderLabel("")

        #===================#
        # Category deletion #
        #===================#
        # Label:
        label_del = QtWidgets.QLabel("<b>Удаление категории</b>")
        label_del.setAlignment(Qt.AlignCenter)

        # Category to be deleted:
        self.cat_del = LabeledComboBoxInput("Категория", [])

        # Delete button:
        self.cat_del_button = QtWidgets.QPushButton('Удалить')
        self.cat_del_button.clicked.connect(self.delete_category)

        #===================#
        # Category addition #
        #===================#
        # Label:
        label_add = QtWidgets.QLabel("<b>Добавление категории</b>")
        label_add.setAlignment(Qt.AlignCenter)

        # Added category parent:
        self.cat_add_parent = LabeledComboBoxInput("Родитель", [])

        # Added category name:
        self.cat_add_name = LabeledLineInput("Название", "Новая категория")

        # Add button:
        self.cat_add_button = QtWidgets.QPushButton('Добавить')
        self.cat_add_button.clicked.connect(self.add_category)

        # Grid layout:
        self.grid = QtWidgets.QGridLayout()

        # AddWidget parameter meaning ---------> Y  X  dY  dX
        self.grid.addWidget(label_cats,          0, 0,  1,  2)
        self.grid.addWidget(self.cat_tree,       1, 0,  1,  2)
        self.grid.addWidget(label_del,           2, 0,  1,  2)
        self.grid.addWidget(self.cat_del,        3, 0,  1,  1)
        self.grid.addWidget(self.cat_del_button, 3, 1,  1,  1)
        self.grid.addWidget(label_add,           4, 0,  1,  2)
        self.grid.addWidget(self.cat_add_parent, 5, 0,  1,  1)
        self.grid.addWidget(self.cat_add_name,   6, 0,  1,  1)
        self.grid.addWidget(self.cat_add_button, 6, 1,  1,  1)

        self.setLayout(self.grid)

        # Set categories when the class is all set up:
        self.set_categories(cats)
        self.update_categories()

    def update_categories(self):
        """
        Рекурсивный обход списка категорий с построением их иерархии.
        """

        self.cat_names = [c.name for c in self.categories]

        # Recursively traverse categories adding subcategories into the tree:
        cat_hierarchy = self.find_children()

        self.cat_tree.clear()
        self.cat_tree.insertTopLevelItems(0, cat_hierarchy)

        self.cat_del.set_items(self.cat_names)
        self.cat_add_parent.set_items([CategoriesEditWindow.NO_PARENT_CATEGORY]
                                                        + self.cat_names)

    def set_categories(self, cats: list[Category]):
        self.categories = cats

    def delete_category(self):
        # Category to be deleted:
        del_cat_name = self.cat_del.text()

        self.cat_delete_handler(self, del_cat_name)
        self.cat_del.clear()

        # Assume that cat_delete_handler() has called set_categories():
        self.update_categories()

    def set_cat_checker(self, checker):
        self.cat_checker = checker

    def add_category(self):
        parent_cat_name = self.cat_add_parent.text()

        if parent_name == CategoriesEditWindow.NO_PARENT_CATEGORY:
            self.cat_add_handler(self, self.cat_add_name.text(), None)
        else:
            # FIXME: normal code would change added category
            #        for circular dependencies
            #        as they would hang the program
            #
            # Often only the presence of parent is checked:
            self.cat_checker(parent_name)

            self.cat_add_handler(self, self.cat_add_name.text(), self.cat_add_parent.text())

        self.cat_add_name.clear()
        self.cat_add_parent.clear()

        # Assume that cat_add_handler() has called set_categories():
        self.update_categories()


    def find_children(self, parent_pk=None):
        """
        Обход списка категорий с построением их иерархии.
        """

        items = []
        children = [c for c in self.categories if c.parent == parent_pk]
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])

            # FIXME: cycle in a category hierarchy
            #        will recurse this code out!
            item.addChildren(self.find_children(parent_pk=child.pk))

            items.append(item)

        return items
