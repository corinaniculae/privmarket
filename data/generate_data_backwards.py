#!/usr/bin/python

""" Script to be run in background for querying TFL data backwards.

The script will query for the specified day interval TFL in order to get the
daily paths + timestamps for each passed day.

"""

import argparse
import datetime
import logging
import os
import sys

import datalib
from mysql_manager import MySQLManager
from tfl_manager import TFLManager


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
                    default='01.05.2016',
                    help='Start date as DD.MM.YYYY.')
parser.add_argument('--end',
                    dest='end_date',
                    type=str,
                    default='25.05.2016',
                    help='End date as DD.MM.YYYY.')
args = parser.parse_args()


def daily_paths(query_date):
    """ Generates today's path points and inserts them into the MySQL table.

    Arguments:
        query_date: Datetime object, representing the date to be queried.
    """
    tfl_manager = TFLManager()
    mysql_manager = MySQLManager()

    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    logger = logging.getLogger('backwards_paths')

    # Generate the file of used stop points.
    if not os.path.isfile(datalib.CSV_FOLDER + datalib.STOP_POINTS_FILE):
        tfl_manager.print_tube_stops_to_file()
        logger.info('Generated the stop points file.')

    # Generate today's daily path file.
    today_paths_file_name = tfl_manager.get_paths_file_name(query_date)
    if not os.path.isfile(today_paths_file_name):
        tfl_manager.generate_and_print_daily_paths()
        logger.info('Generated the daily paths: ' + today_paths_file_name)

    # Write the records into the database.
    today_source = os.path.join(datalib.CSV_FOLDER_GENERATED,
                                tfl_manager.get_paths_file_name(query_date))
    mysql_manager.insert_CSV_file(today_source)
    logging.info('Inserted the corresponding CSV file into the database.')


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
    start_date = datetime.date(start_tokens[2],
                               start_tokens[1],
                               start_tokens[0])
    end_date = datetime.date(end_tokens[2],
                             end_tokens[1],
                             end_tokens[0])
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def main():
    for single_date in date_range(args.start_date, args.end_date):
        daily_paths(single_date)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
