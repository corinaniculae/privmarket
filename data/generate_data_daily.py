#!/usr/bin/python

# Script to be run in background for querying TFL data on a daily basis.

import argparse
import logging
import MySQLdb
import os
import schedule
import sys
import time

import datalib
from create_synthetic_paths import TFLManager


def daily_paths():

    tfl_manager = TFLManager()
    mysql_manager = MySQLManager()

    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    logger = logging.getLogger('daily_paths')

    # Generate the file of used stop points.
    if not os.path.isfile(datalib.CSV_FOLDER + datalib.STOP_POINTS_FILE):
        tfl_manager.print_tube_stops_to_file()

    # Generate today's daily path file.
    if not os.path.isfile(tfl_manager.get_today_paths_file_name()):
        tfl_manager.generate_and_print_daily_paths()

    # Write the records into the database.
    today_source = os.path.join(datalib.CSV_FOLDER_GENERATED,
                                tfl_manager.get_today_paths_file_name)
    mysql_manager.insert_CSV_file(today_source)


def main():
    while True:
        schedule.every().day.at(datalib.TIME_GET_DAILY_PATHS).do(daily_paths)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
