"""
Модель бюджета.
"""
from dataclasses import dataclass
from enum        import Enum
from datetime    import datetime, timedelta

from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense                 import Expense

class Period(Enum):
    """
    Enum для задания кванта планирования бюджета.
    """
    DAY   = 0
    WEEK  = 1
    MONTH = 2

@dataclass
class Budget:
    """
    Бюджет, хранит название периода в атрибуте period,
    допустимую сумму трат за период в атрибуте limitation,
    потраченную за период сумму в атрибуте spent
    """
    limitation : int      # Maximum allowed sum of spendings
    period     : Period   # The period to be budgeted
    spent      : str = 0  # The amount of money spent in the period
    pk         : str = 0  # Primary key

    def __init__(self, limitation: int, period: str,
                       spent: str = 0, pk: str = 0):
        # Parse the period:
        if period == "day":
            self.period = Period.DAY
        if period == "week":
            self.period = Period.WEEK
        if period == "month":
            self.period = Period.MONTH
        else:
            raise ValueError(f'unknown period "{period}" for budget'
                             + 'should be "day", "week" or "month"')

        # Set other parameters:
        self.limitation = limitation
        self.spent      = spent
        self.pk         = pk

    def update_spent(self, expense_repo: AbstractRepository[Expense]) -> None:
        # Generate timestamp for operation:
        date = datetime.now().isoformat()[:10] # YYYY-MM-DD format

        if self.period == Period.DAY:
            date_mask   = f"{date}"
            period_exps = exp_repo.get_all_like(like={"expense_date":date_mask})

        elif self.period == Period.WEEK:
            weekday_now    = datetime.now().weekday()
            day_now        = datetime.fromisoformat(date)
            first_week_day = day_now - timedelta(days=weekday_now)

            period_exps = []
            for i in range(7):
                weekday   = first_week_day + timedelta(days=i)
                date_mask = f"{weekday.isoformat()[:10]}"

                period_exps += exp_repo.get_all_like(like={"expense_date":date_mask})

        elif self.period.lower() == Period.MONTH:
            date_mask = f"{date[:7]}-"

            period_exps = exp_repo.get_all_like(like={"expense_date":date_mask})

        # Update money spent:
        self.spent = sum([int(exp.amount) for exp in period_exps])
