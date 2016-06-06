#!/usr/bin/python

import csv
import os
import sys

import datalib
import mysql_manager

PATHS_FOLDER = 'data/csv_files/paths'
MYSQL_PATH_DB = 'priv_coll'
MYSQL_PATH_TABLE = 'paths'


def main():
    logger = datalib.get_new_logger('paths_to_mysql', 'paths_to_mysql.log')
    try:
        mm = mysql_manager.MySQLManager(MYSQL_PATH_DB, MYSQL_PATH_TABLE, False)
        for fl in PATHS_FOLDER:
            logger.info('Preparing to insert file: %s' % fl)
            source_path = os.path.join(PATHS_FOLDER, fl)
            mm.insert_csv_file(source_path)
            logger.info('Inserted file: %s' % source_path)
        mm.close_db_manager()
        return 0
    except Exception, e:
        logger.error('%s: %s' % (e.args[0], e.args[1]))


if __name__ == '__main__':
    status = main()
    sys.exit(status)
