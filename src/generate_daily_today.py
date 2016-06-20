#!/usr/bin/python

# Script to be run in background for querying TFL data on a daily basis.

import sys

from tfl_manager import TFLManager
from mysql_manager import MySQLManager


def main():

    tfl_manager = TFLManager()
    mysql_manager = MySQLManager()

    tfl_manager.print_tube_stops_to_file()

    # Generate today's daily path file.
    daily_file_path = tfl_manager.generate_and_print_daily_paths()

    # Write the records into the database.
    return mysql_manager.insert_CSV_file(daily_file_path)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
