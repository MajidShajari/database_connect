#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
from psycopg2.extensions import parse_dsn
import pymongo


class DatabaseConfig:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def _get_params(self, section: str) -> dict:
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)
        db_params = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db_params[param[0]] = param[1]
        else:
            raise Exception(
                f'Section {section} not found in the {self.filename} file')
        return db_params

    def _check_connect_mongodb(self, url: str):
        """Replace the uri string with your MongoDB deployment's connection string."""

        client = None
        try:
            # get a handle to the database
            print('Connecting to the MongoDB database...')
            # set a 5-second connection timeout
            client = pymongo.MongoClient(
                url, serverSelectionTimeoutMS=5000)
            print("MongoDB version:")
            print(client.server_info()['version'])
            print("MongoDB Connection closed.")
            client.close()
            return True
        except Exception:
            print("Unable to connect to the MongoDB server.")

    def _check_connect_postgresql(self, url: str):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = parse_dsn(url)
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
            conn.close()
            print('PostgreSQL connection closed.')
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @property
    def mongodb_url(self):
        params = self._get_params(section='mongodb')
        conn_url = "mongodb://" +\
            f"{params['username']}:{params['password']}" + \
            f"@{params['host']}:{params['port']}" +\
            "/?authMechanism=DEFAULT"
        return conn_url

    @property
    def postgresql_url(self):
        params = self._get_params(section='postgresql')
        conn_url = "postgresql://" +\
            f"{params['user']}:{params['password']}" +\
            f"@{params['host']}: {params['port']}" +\
            f"/{params['dbname']}"
        if self._check_connect_postgresql(conn_url):
            return conn_url
        return None


if __name__ == "__main__":
    db_config = DatabaseConfig('database.ini')
    db_config.postgresql_url
    db_config.mongodb_url
