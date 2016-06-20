#!/usr/bin/python

""" Formats the daily CSV files to be inserted in CryptDB.


"""

import csv
import datetime
import logging
import os
import sys
import time
import datalib


INSERT_GEN_1 = """INSERT INTO generated_2 VALUES (%d, %d, %d, %d, %d, %d);"""


def get_formatted_row(row):
    lat1, lat2 = datalib.prepare_coordinate(str(row[1]))
    lng1, lng2 = datalib.prepare_coordinate(str(row[2]))
    dt = datalib.get_datetime_from_string(str(row[3]))
    timestamp = int(time.mktime(dt.timetuple()))
    return INSERT_GEN_1 % (int(row[0]), lat1, lat2, lng1, lng2, timestamp)


def daily_paths(day):
    """ Generates today's path points and inserts them into the MySQL table.

    Arguments:
        query_date: Datetime object, representing the date to be queried.
    """
    for counter in range(1, 2):
        logging.info('Generating daily for %s, day %s' % (counter, day))
        file_source_name = 'daily_%s_2016_05_0%s.csv' % (counter, day)
        file_dest_name ='mysql_daily_%s_2016_05_0%s.sql' % (counter, day)
        file_source_path = os.path.join(datalib.CSV_GENERATED_FOLDER,
                                        file_source_name)
        file_dest_path = os.path.join(datalib.CSV_GENERATED_FOLDER,
                                      file_dest_name)
        source_file = file(file_source_path, 'rb')
        dest_file = file(file_dest_path, 'wb')
        reader = csv.reader(source_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        count = 0
        for row in reader:
            if count == 10:
                break
            count += 1
            insert_query = get_formatted_row(row)
            dest_file.write(insert_query + '\n')

        source_file.close()
        dest_file.close()


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    for day in range(1, 2):
        daily_paths(day)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
