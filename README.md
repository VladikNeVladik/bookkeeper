# Простая программа для управления личными финансами
Это учебный проект для [курса по практике программирования на Python](https://github.com/FrCln/bookkeeper).

В качестве менеджера зависимостей используется poetry. Установка всех пакетов происходит автоматически:

```commandline
poetry install
```

Для запуска тестов и статических анализаторов используйте следующие команды (убедитесь,
что вы находитесь в корневой папке проекта):
```commandline
poetry run pytest --cov
poetry run mypy --strict bookkeeper
poetry run pylint bookkeeper
poetry run flake8 bookkeeper
```

Авто-наполение базы данных:
```commandline
poetry run python3 create_db_table.py
```


Запуск приложения:
```commandline
poetry run python3 -m bookkeeper
```
