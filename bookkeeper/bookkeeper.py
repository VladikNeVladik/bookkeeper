from datetime import datetime

from bookkeeper.view.view import AbstractView

from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.category import Category
from bookkeeper.models.expense  import Expense
from bookkeeper.models.budget   import Budget

class Bookkeeper:
    def __init__(self,
                 view: AbstractView,
                 repository_type: type):

        # Abstract out of the view details:
        self.view = view

        #########################
        ## Category repository ##
        #########################

        self.category_repo = repository_type[Category](
            db_file="database/bookkeeper.db",
            cls=Category)

        self.categories = self.category_repo.get_all()

        # Configure view:
        self.view.set_categories(self.categories)

        self.view.set_category_add_handler   (self.add_category)
        self.view.set_category_delete_handler(self.delete_category)
        self.view.set_category_checker       (self.cat_checker)

        #######################
        ## Budget repository ##
        #######################

        self.budget_repo = repository_type[Budget](
            db_file="database/bookkeeper.db",
            cls=Budget)

        # Configure view handlers:
        self.view.set_budget_modify_handler(self.modify_budget)

        ########################
        ## Expense repository ##
        ########################

        self.expense_repo = repository_type[Expense](
            db_file="database/bookkeeper.db",
            cls=Expense)

        self.update_expenses()
        self.view.set_expense_add_handler   (self.add_expense)
        self.view.set_expense_delete_handler(self.delete_expenses)
        self.view.set_expense_modify_handler(self.modify_expense)

    def start_app(self):
        self.view.show_main_window()

    #########################
    ## Category operations ##
    #########################

    def cat_checker(self, cat_name: str):
        if cat_name not in [c.name for c in self.categories]:
            raise ValueError(f'Категории "{cat_name}" не существует')

    def add_category(self, name: str, parent: str | None = None):
        # Category existent:
        if name in [c.name for c in self.categories]:
            raise ValueError(f'Категория "{name}" уже существует')

        # No parent category:
        if parent is not None:
            if parent not in [c.name for c in self.categories]:
                raise ValueError(f'Категории "{parent}" не существует')
            parent_pk = self.category_rep.get_all(where={'name':parent})[0].pk
        else:
            parent_pk = None

        # Create category:
        cat = Category(name, parent_pk)

        # Update:
        # - Internal state
        # - Repository
        # - View
        self.categories.append(cat)
        self.category_repo.add(cat)
        self.view.set_categories(self.categories)

    def delete_category(self, cat_name: str):
        # No categories to delete:
        cat = self.category_rep.get_all(where={"name":cat_name})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]

        # Repo operation:
        self.category_repo.delete(cat.pk)

        # Update parent category for all children ("your papa is gone :("):
        for child in self.category_rep.get_all(where={'parent':cat.pk}):
            child.parent = cat.parent
            self.category_repo.update(child)

        # Update internal state:
        self.categories = self.category_rep.get_all()

        # Update view:
        self.view.set_categories(self.categories)

        # Update expense repo:
        for exp in self.expense_rep.get_all(where={'category':cat.pk}):
            exp.category = None
            self.expense_repo.update(exp)

        # Uodate expenses:
        self.update_expenses()

    ########################
    ## Expense operations ##
    ########################

    def update_expenses(self):
        self.expenses = self.expense_repo.get_all()
        self.view.set_expenses(self.expenses)

        # Update budgets as they have expanses inside:
        self.update_budgets()

    def add_expense(self, amount: str, cat_name: str, comment: str=""):
        # Parse user input:
        try:
            amount = int(amount)
        except:
            raise ValueError('Введите сумму целым числом.')

        # Handle negative or zero amounts:
        if amount <= 0:
            raise ValueError(f'Введите положительную величину покупки.')

        # Get expense category (to link to it's id):
        cat = self.category_repo.get_all(where={"name":cat_name.lower()})
        if len(cat) == 0:
            raise ValueError(f'Категории "{cat_name}" не существует')
        else:
            cat = cat[0]

        # Create the expense:
        new_exp = Expense(amount, cat.pk, comment=comment)

        self.expense_repo.add(new_exp)
        self.update_expenses()
        if len([b for b in self.budgets if b.spent > b.limitation]):
            self.view.not_on_budget_message()

    def modify_expense(self, pk: int, attr: str, new_val: str):
        # Get expense to be modified:
        exp = self.expense_repo.get(pk)

        # Modify category:
        if attr == "category":
            # Parse string:
            new_val = new_val.lower()

            if new_val not in [c.name for c in self.categories]:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Категории "{new_val}" не существует')

            new_val = self.category_rep.get_all(where={'name':new_val})[0].pk

        # Modify amount:
        if attr == "amount":
            # Parse integer:
            try:
                new_val = int(new_val)
            except:
                raise ValueError('Чем это Вы расплачивались?\n'
                                    + 'Введите сумму целым числом.')

            # Check for negative amount:
            if new_val <= 0:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Удачная покупка! Записывать не буду.')

        # Modify expense_date:
        if attr == "expense_date":
            # Parse datetime:
            try:
                new_val = datetime.fromisoformat(new_val).isoformat(
                                            sep='\t', timespec='minutes')
            except ValueError:
                self.view.set_expenses(self.expenses)
                raise ValueError(f'Неправильный формат даты.')

        # Update the expense:
        setattr(exp, attr, new_val)
        self.expense_repo.update(exp)

        # Update view and expenses in the budget:
        self.update_expenses()

    def delete_expenses(self, exp_pks: list[int]):
        for pk in exp_pks:
            self.expense_repo.delete(pk)
        self.update_expenses()

    #######################
    ## Budget operations ##
    #######################

    def update_budgets(self):
        # Update budget integrity:
        for budget in self.budget_repo.get_all():
            budget.update_spent(self.expense_repo)
            self.budget_repo.update(budget)

        # Update internal representation and view:
        self.budgets = self.budget_repo.get_all()
        self.view.set_budgets(self.budgets)

    def modify_budget(self, pk: int | None, new_limit: str, period: Period):
        # Remove budget if no spendings limit is set:
        if new_limit == "":
            if pk is not None:
                self.budget_repo.delete(pk)
            self.update_budgets()
            return

        # Parse limit as integer:
        try:
            new_limit = int(new_limit)
        except ValueError:
            self.update_budgets()
            raise ValueError('Неправильный формат.\n'
                                + 'Введите сумму целым числом.')

        # Handler nagative limit:
        if new_limit < 0:
            self.update_budgets()
            raise ValueError('За этот период придется заработать.')

        # Handle nonexistent primary key:
        if pk is None:
            budget = Budget(limitation=new_limit, period=period)
            self.budget_rep.add(budget)
        else:
            budget = self.budget_rep.get(pk)
            budget.limitation = new_limit
            self.budget_rep.update(budget)

        # Final update:
        self.update_budgets()
