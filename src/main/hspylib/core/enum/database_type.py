from enum import Enum


class DatabaseType(Enum):
    MYSQL = 'mysql'
    POSTGRESS_SQL = 'postgres'
    FILE_STORAGET = 'file-storage'
    MONGO_DB = 'mongo-db'
