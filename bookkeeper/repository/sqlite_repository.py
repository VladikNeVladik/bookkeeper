from inspect import get_annotations
import sqlite3

###############################
## Database helper functions ##
###############################

def generate_objects(fields: dict[str, type], pk, values: list[type]):
	obj = {'pk': pk}
	for i, field in enumerate(fields):
		setattr(obj, field, values[i])

	return obj


###################################
## SQL repository implementation ##
###################################

class SQLiteRepository(AbstractRepository[T]):
	"""
	Репозиторий, основанный на БД SQLite. Работает поверх файловой системы.
	"""
	def __init__(self, db_file: str, cls: type) -> None:
		# Type annotations:
		self._db_file    : str
		self._table_name : str
		self._fields     : dict[str, type]

		self._db_file    = db_file
		self._table_name = cls.__name__.lower()
		self._fields     = get_annotations(cls, eval_str=True)
		self._fields.pop('pk')

	def add(self, obj: T) -> int:
		# Check for input values:
		if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'Trying to add object {obj} with filled `pk` attribute')

        # Generate the query:
		names  = ", ".join(self._fields.keys())
		p      = ", ".join("?" * len(self._fields))
		values = [getattr(obj, x) for x in self._fields]

		with sqlite3.connect(self._db_file) as con:
			cur = con.cursor()
			cur.execute("PRAGMA foreign_keys = ON")
			cur.execute(
				f"INSERT INTO {self._table_name} ({names}) VALUES ({p})",
				values
			)
			obj.pk = cur.lastrowid

		con.close()
		return obj.pk

	def get(self, pk: int) -> T | None:
		# Generate the query:
		with sqlite3.connect(self._db_file) as con:
			cur = con.cursor()
			res = cur.execute(f"SELECT * FROM {self._table_name} WHERE pk={pk}")

			rows       = res.fetchall()
			num_rows = len(values)

			# Check result:
			if num_rows == 0:
				raise ValueError(f'No entry found with pk={pk}')
			if num_rows > 1:
				raise ValueError(f'Several entries found with pk={pk}')

		con.close()

		# Generate the resulting object:
		return generate_object(self._fields, pk, rows[0])

	def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
		with sqlite3.connect(self.db_file) as con:
			cur = con.cursor()
			if where is None:
				res  = cur.execute(f"SELECT * FROM {self._table_name}")
				rows = res.fetchall()

				for row in rows
        	else:












	def get_all(self, where: dict[str, Any] | None = None) -> list[T]:

	def update(self, obj: T) -> None:

	def delete(self, pk: int) -> None:
