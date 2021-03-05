from hspylib.core.enum.enumeration import Enumeration


class DatabaseType(Enumeration):
    FILE_STORAGE = 'file-storage'
    MYSQL = 'mysql'
    POSTGRES_SQL = 'postgres'
    MONGO_DB = 'mongo-db'
