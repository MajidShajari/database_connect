from custom_decorator import timeit
from database_config import DatabaseConfig


@timeit
def main():
    db_config = DatabaseConfig("database.ini")
    print(db_config.postgresql_url)
    print(db_config.mongodb_url)


if __name__ == "__main__":
    main()
