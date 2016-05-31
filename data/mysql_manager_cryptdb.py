#!/usr/bin/python

# Script for handling all MySQL queries.


import argparse
import csv
import datetime
import MySQLdb
import os
import sys

import datalib


parser = argparse.ArgumentParser(
    description='Generate daily paths for the specified time interval.')
parser.add_argument('--users',
                    dest='n',
                    type=int,
                    default=1000,
                    help='Number of users to simulate.')
parser.add_argument('--start',
                    dest='start_date',
                    type=str,
                    default='01-05-2016',
                    help='Start date as DD-MM-YYYY.')
parser.add_argument('--end',
                    dest='end_date',
                    type=str,
                    default='14-05-2016',
                    help='End date as DD=MM-YYYY.')
parser.add_argument('--db',
                    dest='db',
                    type=str,
                    default=datalib.MYSQL_DB,
                    help='The MySQL database to be used.')
parser.add_argument('--table',
                    dest='table',
                    type=str,
                    default=datalib.MYSQL_GEN_TABLE,
                    help='The MySQL table to be used.')
args = parser.parse_args()


def date_range(str_start_date, str_end_date):
    """ Generate a date range between the specified dates.

    Arguments:
        str_start_date: String DD-MM-YYYY, representing the start date of
        the time range.
        str_end_date: String DD-MM-YYYY, representing the end date of the range.

    Returns:
        An iterator for the specified date range.
    """
    start_tokens = str_start_date.split('-')
    end_tokens = str_end_date.split('-')
    start_date = datetime.date(int(start_tokens[2]),
                               int(start_tokens[1]),
                               int(start_tokens[0]))
    end_date = datetime.date(int(end_tokens[2]),
                             int(end_tokens[1]),
                             int(end_tokens[0]))
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


class MySQLManagerCryptDB:
    """Handler for MySQL queries."""

    """ Initiates a TFLManager object.

    Arguments:
        database: String of the name of the database to be used.
        table: String of the table to be used.
    """
    def __init__(self, database=args.db, table=args.table):
        self._logger = datalib.get_new_logger('MySQLManager')
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
                                 port=datalib.MYSQL_PORT)           # port
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

            reader = csv.reader(csv_file_path,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            # Insert CSV file
            for row in reader:
                insert_csv_query = (datalib.MYSQL_INSERT_VALUES % (self._table,
                                                                   row[0],
                                                                   row[1],
                                                                   row[2],
                                                                   row[3]))
                cur.execute(insert_csv_query)
            db.commit()

            self._logger.info('Inserted CSV file: %s' % csv_file_path)

        except MySQLdb.Error, e:
            self._logger.error("Error %d: %s" % (e.args[0], e.args[1]))
            return 1

        finally:
            if db is not None:
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


def main():
    mysql_ins = MySQLManagerCryptDB()
    for single_date in date_range(args.start_date, args.end_date):
        suffix_file = str(single_date.strftime("%Y_%m_%d"))
        daily_file_name = 'daily_%s.csv' % suffix_file
        daily_file_path = os.path.join(datalib.CSV_FOLDER_GENERATED,
                                       daily_file_name)
        mysql_ins.insert_CSV_file(daily_file_path)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
