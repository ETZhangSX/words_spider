from orator import Model, DatabaseManager

from config.database import DATABASES

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)
