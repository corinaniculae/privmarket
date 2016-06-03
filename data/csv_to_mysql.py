#!/usr/bin/python

import csv
import os
import sys

import datalib

files = ['daily_2016_05_01.csv', 'daily_2016_05_02.csv', 'daily_2016_05_03.csv',
         'daily_2016_05_04.csv', 'daily_2016_05_05.csv', 'daily_2016_05_06.csv',
         'daily_2016_05_07.csv', 'daily_2016_05_08.csv', 'daily_2016_05_09.csv',
         'daily_2016_05_10.csv', 'daily_2016_05_11.csv', 'daily_2016_05_12.csv',
         'daily_2016_05_13.csv']


def main():
    logger = datalib.get_new_logger('quick_fix', 'quick_fix.log')
    counter = 1
    for fl in files:
        source_path = os.path.join(datalib.CSV_FOLDER_GENERATED, fl)
        result_path = os.path.join(datalib.CSV_FOLDER_GENERATED,
                                   'mysql_' + str(counter) + '.sql')
        source_file = file(source_path, 'rb')
        result_file = file(result_path, 'wb')
        reader = csv.reader(source_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(result_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            new_row = datalib.MYSQL_INSERT_VALUES % ('generated',
                                                     row[0],
                                                     row[1],
                                                     row[2],
                                                     row[3])
            writer.writerow((new_row))
            logger.info('Wrote row: %s' % new_row)

        source_file.close()
        result_file.close()
        counter += 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)
