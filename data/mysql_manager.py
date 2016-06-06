#!/usr/bin/python

# Script for handling all MySQL queries.


import argparse
import sys

import MySQLdb

import datalib


class MySQLManager:
    """Handler for MySQL queries."""

    """ Initiates a TFLManager object.

    Arguments:
        database: String of the name of the database to be used.
        table: String of the table to be used.
    """
    def __init__(self, database, table, daily=True):
        self._logger = datalib.get_new_logger('MySQLManager',
                                              'logs/mysql_manager.log')
        self._database = database
        self._table = table
        self._daily = daily
        self._db, self._cursor = self._open_new_database_connection()

    """ Opens a new MySQL connection and returns the associated db cursor.

    Returns:
        A Cursor object to execute the following MySQL queries.
    """
    def _open_new_database_connection(self):
        try:
            db = MySQLdb.connect(host=datalib.MYSQL_HOST,       # host name
                                 user=datalib.MYSQL_USER,       # username
                                 passwd=datalib.MYSQL_PASSWORD, # password
                                 local_infile=datalib.MYSQL_LOCAL_INFILE)
            cursor = self._db.cursor()  # Cursor object for following queries.
            self._logger.info('Connected to MySQL.')

            # Create the needed database and/or table.
            create_db_query = (datalib.MYSQL_CREATE_DB % self._db)
            use_db_query = (datalib.MYSQL_USE_DB % self._db)
            if self._daily:
                create_table_query = (
                    datalib.MYSQL_CREATE_GEN_TABLE % self._table)
            else:
                create_table_query = (
                    datalib.MYSQL_CREATE_PATHS_TABLE % self._table)
            cursor.execute(create_db_query)
            cursor.execute(use_db_query)
            cursor.execute(create_table_query)
            self._logger.info('Created/Fetched the database and the table.')

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        return db, cursor

    """ Close MySQL connection. """
    def close_db_manager(self):
        self._db.close()

    """ Inserts the given CSV file into the MySQLManager table.

    Arguments:
        csv_file_path: Full path of the CSV file to be loaded.

    Returns:
        Returns 1 if an unexpected error occured; 0 otherwise.
    """
    def insert_csv_file(self, csv_file_path):
        try:
            if self._daily:
                add_csv_query = (datalib.MYSQL_LOAD_GEN_FILE % (csv_file_path,
                                                                self._table))
            else:
                add_csv_query = (datalib.MYSQL_LOAD_PATH_FILE % (csv_file_path,
                                                                 self._table))

            self._cursor.execute(add_csv_query)
            self._db.commit()
            self._logger.info('Inserted CSV file: %s' % csv_file_path)

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))


class MySQLError(Exception):
    """Error class for handling MySQL related errors or warnings."""

    """ Initiates a MySQL error instance. """
    def __init__(self, value):
        self.value = value

    """ Gives the string representation of the error. """
    @property
    def __str__(self):
        return repr(self.value)
