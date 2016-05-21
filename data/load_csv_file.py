#!/usr/bin/python

# Script for daily querying TFL for travel times.


import argparse
import logging
import MySQLdb
import os
import sys

import datalib
from create_synthetic_paths import TFLManager


parser = argparse.ArgumentParser(description='Puts CSV files into MySQL table.')
parser.add_argument('--file',
                    dest='file_name',
                    type=str,
                    default='daily_2016_05_20.csv',
                    help='The CSV file to be loaded into the table.')
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


def main():

    tfl_manager = TFLManager()
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    logger = logging.getLogger('load_csv_file')

    # Write the records into the database.
    try:
        # Connect to the MySQL server.
        db = MySQLdb.connect(host='localhost',    # host name
                             user='root',         # username
                             passwd='letmein',    # password
                             local_infile = 1)
        cur = db.cursor() # Cursor object for executing MySQL queries.

        logger.info('Connected to the MySQL server.')

        # Create the MySQL database.
        create_db_query = (datalib.MYSQL_CREATE_DB % args.db)
        use_db_query = (datalib.MYSQL_USE_DB % args.db)
        create_table_query = (datalib.MYSQL_CREATE_GENERATED_TABLE % args.table)
        cur.execute(create_db_query)
        cur.execute(use_db_query)
        cur.execute(create_table_query)

        logging.info('Created/Fetched the database and the table.')

        print 'database: ' + args.db + '; table: ' + args.table + '; file: ' + args.file_name
        # Insert CSV file
        source = (os.getcwd() +
                  '/' +
                  datalib.CSV_FOLDER_GENERATED +
                  args.file_name)
        add_csv_query = (datalib.MYSQL_LOAD_GENERATED_FILE % (source, args.table))
        print add_csv_query 
        cur.execute(add_csv_query)
        db.commit()

        logger.info('Populated the table with CSV file: ' + args.file_name)

    except MySQLdb.Error, e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
        return 1
    
    finally:    
        if db:
            logger.info('Table has been populated.')
            db.close()
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
