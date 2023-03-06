from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest

@pytest.fixture
def custom_class():
    class Custom():
        pk = 0

    return Custom

@pytest.fixture
def repo():
    return SQLiteRepository()
