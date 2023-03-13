"""
Модель бюджета.
"""
from dataclasses import dataclass
from enum        import Enum
from datetime    import datetime, timedelta

from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense                 import Expense


@dataclass
class Budget:
    """
    Бюджет, хранит название периода в атрибуте period,
    допустимую сумму трат за период в атрибуте limitation,
    потраченную за период сумму в атрибуте spent
    """
    limitation : int      # Maximum allowed sum of spendings
    period     : str      # The period to be budgeted
    spent      : int = 0  # The amount of money spent in the period
    pk         : int = 0  # Primary key

    def __init__(
        self,
        limitation : int,
        period     : str,
        spent      : int = 0,
        pk         : int = 0
    ):
        # Parse the period:
        if period not in ["day", "week", "month"]:
            raise ValueError(f"unknown period \"{period}\" for budget\n"
                             "should be \"day\", \"week\" or \"month\"")

        # Set other parameters:
        self.limitation = limitation
        self.period     = period
        self.spent      = spent
        self.pk         = pk

    def update_spent(self, expense_repo: AbstractRepository[Expense]) -> None:
        # Generate timestamp for operation:
        date = datetime.now().isoformat()[:10]  # YYYY-MM-DD format

        if self.period == "day":
            mask   = f"{date}"
            period_exps = expense_repo.get_all_by_pattern({"expense_date": mask})

        elif self.period == "week":
            weekday_now    = datetime.now().weekday()
            day_now        = datetime.fromisoformat(date)
            first_week_day = day_now - timedelta(days=weekday_now)

            period_exps = []
            for i in range(7):
                weekday   = first_week_day + timedelta(days=i)
                mask = f"{weekday.isoformat()[:10]}"

                period_exps += expense_repo.get_all_by_pattern({"expense_date": mask})

        elif self.period == "month":
            mask = f"{date[:7]}-"

            period_exps = expense_repo.get_all_by_pattern({"expense_date": mask})

        # Update money spent:
        # pylint: disable=consider-using-generator
        self.spent = sum([int(exp.amount) for exp in period_exps])
