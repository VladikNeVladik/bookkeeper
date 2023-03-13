from bookkeeper.bookkeeper import Bookkeeper

from bookkeeper.view.view import View

from bookkeeper.repository.abstract_repository import repository_factory
from bookkeeper.repository.sqlite_repository   import SQLiteRepository

###################
## Main finction ##
###################

# Repo factory
repo_gen = repository_factory(SQLiteRepository, db_file="database/bookkeeper.db")

view = View()
bookkeeper_app = Bookkeeper(view, repo_gen)

# Execute it!
bookkeeper_app.start_app()
