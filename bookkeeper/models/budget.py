"""
Модель бюджета.
"""

from dataclasses import dataclass
from enum import Enum


class Period(Enum):
    """
    Enum для задания кванта планирования бюджета
    """
    DAY   = 0
    WEEK  = 1
    MONTH = 2


@dataclass(
    slots=True
)
class Budget:
    """
    Модель бюджета
    """

    amount      : int      # The budget to be spend
    category_id : int      # Budget category id
    period      : Period   # The granularity of the budget
    pk          : int = 0  # Primary key
