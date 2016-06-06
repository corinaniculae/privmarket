#!/usr/bin/python

import csv
import os
import sys

import cryptdb_manager
import datalib

files = ['daily_0_2016_05_01.csv', 'daily_0_2016_05_02.csv',
         'daily_0_2016_05_03.csv', 'daily_0_2016_05_04.csv',
         'daily_0_2016_05_05.csv', 'daily_0_2016_05_06.csv',
         'daily_0_2016_05_07.csv', 'daily_0_2016_05_08.csv',
         'daily_0_2016_05_09.csv', 'daily_0_2016_05_10.csv',
         'daily_0_2016_05_11.csv', 'daily_0_2016_05_12.csv',
         'daily_0_2016_05_13.csv']


def main():
    cryptdb = cryptdb_manager.CryptDBManager()
    logger = datalib.get_new_logger('quick_fix', 'quick_fix.log')
    for fl in files:
        logger.info('Preparing to insert file: %s' % fl)
        source_path = os.path.join(datalib.CSV_GENERATED_FOLDER, fl)
        cryptdb.insert_csv_file(source_path)
        logger.info('Inserted file: %s' % source_path)
        break
    cryptdb.close_db_manager()
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
