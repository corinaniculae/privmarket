#!/usr/bin/python

# Script for handling all MySQL queries.


import csv
import os
import sys
import time

import MySQLdb

import datalib


class CryptDBManager:
    """Handler for CryptDB queries."""

    """ Initiates a CryptDB handler.

    Arguments:
        database: String of the name of the database to be used.
        table: String of the table to be used.
    """
    def __init__(self,
                 database=datalib.CRYPTDB_DB,
                 table=datalib.CRYPTDB_TABLE):
        self._logger = datalib.get_new_logger('CryptDBManager')
        self._database = database
        self._table = table
        self._db, self._cursor = self._open_new_database_connection()

    """ Close the CryptDB connection. """
    def close_db_manager(self):
        self._db.close()

    """ Opens a new CryptDB connection and returns the associated db cursor.

    Returns:
        A Cursor object to execute the following MySQL queries on CryptDB.
    """
    def _open_new_database_connection(self):
        try:
            db = MySQLdb.connect(host=datalib.CRYPTDB_HOST,  # host name
                                 user=datalib.CRYPTDB_USER,  # username
                                 passwd=datalib.CRYPTDB_PASSWORD,  # password
                                 port=datalib.CRYPTDB_PORT)         # port no.
            cursor = db.cursor()  # Cursor object for following queries.
            self._logger.info('Connected to CryptDB.')

            # Create the needed database and/or table.
            create_db_query = (datalib.MYSQL_CREATE_DB % self._database)
            use_db_query = (datalib.MYSQL_USE_DB % self._database)
            create_table_query = (datalib.MYSQL_CREATE_GEN_TABLE % self._table)
            cursor.execute(create_db_query)
            cursor.execute(use_db_query)
            cursor.execute(create_table_query)
            self._logger.info('Created/Fetched the database and the table.')

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        return db, cursor

    def execute_void_query(self, sql_query):
        try:
            self._cursor.execute(sql_query)
            self._db.commit()
        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))

    """ Executes the given count query over CryptDB.

    Arguments:
        sql_query: MySQL query having a count aggregate in projection.

    Returns:
        An integer, representing the result of the aggregate.
        In case of an error, -1 is returned.
    """
    def execute_count_query(self, sql_query):
        try:
            self._cursor.execute(sql_query)
            self._db.commit()
            return self._cursor.fetchone()[0]
        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))
            return -1

    def insert_daily(self, csv_file_path):
        try:
            csv_file = file(csv_file_path, 'rb')
            reader = csv.reader(csv_file,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if int(row[0]) > 500:
                    break
                self._logger.info('Now row: %s' % row)
                insert_csv_query = (
                    datalib.MYSQL_INSERT_GEN_VALUES % (self._table,
                                                       row[0],
                                                       row[1],
                                                       row[2],
                                                       row[3]))
                self._cursor.execute(insert_csv_query)
            self._db.commit()
            self._logger.info('Inserted CSV file: %s' % csv_file_path)

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))

        finally:
            csv_file.close()
        lat1, lat2 = datalib.prepare_coordinate(a1)
        lat3, lat4 = datalib.prepare_coordinate(a2)
        lng1, lng2 = datalib.prepare_coordinate(b1)
        lng3, lng4 = datalib.prepare_coordinate(b2)
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
    """ Inserts the given CSV file into CryptDB.

    Arguments:
        csv_file_path: Full path of the CSV file to be loaded.

    Returns:
        Returns 1 if an unexpected error occured; 0 otherwise.
    """
    def insert_csv_file(self, csv_file_path):
        try:
            csv_file = file(csv_file_path, 'rb')
            reader = csv.reader(csv_file,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if int(row[0]) > 500:
                    break
                self._logger.info('Now row: %s' % row)
                insert_csv_query = (
                    datalib.MYSQL_INSERT_GEN_VALUES % (self._table,
                                                       row[0],
                                                       row[1],
                                                       row[2],
                                                       row[3]))
                self._cursor.execute(insert_csv_query)
            self._db.commit()
            self._logger.info('Inserted CSV file: %s' % csv_file_path)

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))

        finally:
            csv_file.close()

    def load_mysql_files(self):
        start_time = time.time()
        for day in range(2, 3):
            for counter in range(1, 3):
                if day < 10:
                    file_name = 'mysql_daily_%s_2016_05_0%s.sql' % (counter, day)
                else:
                    file_name = 'mysql_daily_%s_2016_05_%s.sql' % (counter, day)
                print 'now will source file: ' + file_name
                file_path = os.path.join('src/csv_files/generated', file_name)
                sql_file = file(file_path, 'rb')
                reader = csv.reader(sql_file,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    self._cursor.execute(str(row[0]) + ';')
                self._db.commit()
                sql_file.close()
        elapsed_time = time.time() - start_time
        print 'and it took: ' + str(elapsed_time)


class MySQLError(Exception):
    """Error class for handling MySQL related errors or warnings."""

    """ Initiates a TFL error instance. """

    def __init__(self, value):
        self.value = value

    """ Gives the string representation of the error. """

    @property
    def __str__(self):
        return repr(self.value)

