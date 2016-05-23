#!/usr/bin/python

# Script for handling all MySQL queries.


import argparse
import logging
import MySQLdb
import os
import sys

import datalib
from create_synthetic_paths import TFLManager


parser = argparse.ArgumentParser(description='MySQL query handler.')
parser.add_argument('--db',
                    dest='db',
                    type=str,
                    default=datalib.MYSQL_DB,
                    help='The MySQL database to be used.')
parser.add_argument('--table',
                    dest='table',
                    type=str,
                    default=datalib.MYSQL_TABLE,
                    help='The MySQL table to be used.')
args = parser.parse_args()


class MySQLManager:
    """Handler for MySQL queries."""

    """ Initiates a TFLManager object.

    Arguments:
        database: String of the name of the database to be used.
        table: String of the table to be used.
    """
    def __init__(self, database=args.db. table=args.table):
        self._logger = logging.getLogger('MySQLLogger')
        self._database = database
        self._table = table

    """ Inserts the given CSV file into the MySQLManager table.

    Arguments:
        csv_file_path: Full path of the CSV file to be loaded.

    Returns:
        Returns 1 if an unexpected error occured; 0 otherwise.
    """
    def insert_CSV_file(self, csv_file_path):
        try:
            # Connect to the MySQL server.
            db = MySQLdb.connect(host=datalib.MYSQL_HOST,           # host name
                                 user=datalib.MYSQL_USER,           # username
                                 passwd=datalib.MYSQL_PASSWORD,     # password
                                 local_infile=datalib.MYSQL_LOCAL_INFILE)
            cur = db.cursor() # Cursor object for executing MySQL queries.

            self._logger.info('Connected to the MySQL server.')

            # Create the MySQL database.
            create_db_query = (datalib.MYSQL_CREATE_DB % self._database)
            use_db_query = (datalib.MYSQL_USE_DB % self._database)
            create_table_query = (datalib.MYSQL_CREATE_GEN_TABLE % self._table)
            cur.execute(create_db_query)
            cur.execute(use_db_query)
            cur.execute(create_table_query)

            self._logger.info('Created/Fetched the database and the table.')

            # Insert CSV file
            add_csv_query = (datalib.MYSQL_LOAD_GEN_FILE % (csv_file_path,
                                                            self._table))
            cur.execute(add_csv_query)
            db.commit()

            self._logger.info('Inserted CSV file: %s' % csv_file_path)

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))
            return 1

        finally:
            if db:
                self._logger.info('Table has been populated.\n')
                db.close()
        return 0


class MySQLError(Exception):
    """Error class for handling MySQL related errors or warnings."""

    """ Initiates a TFL error instance. """

    def __init__(self, value):
        self.value = value

    """ Gives the string representation of the error. """

    @property
    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
