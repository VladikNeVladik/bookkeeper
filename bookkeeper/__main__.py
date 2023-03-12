from bookkeeper.bookkeeper                   import Bookkeeper
from bookkeeper.view.view                    import View
from bookkeeper.repository.sqlite_repository import SQLiteRepository

###################
## Main finction ##
###################

view = View()
bookkeeper_app = Bookkeeper(view, SQLiteRepository)

# Execute it!
bookkeeper_app.start_app()
