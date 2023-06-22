import connect_mongodb
import connect_postgresql
from custom_decorator import timeit


@timeit
def main():
    connect_postgresql.connect()
    connect_mongodb.connect()


if __name__ == "__main__":
    main()
