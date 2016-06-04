#!/usr/bin/python

# Script to generated users' weekday paths to be simulated.


import logging
import os
import sys


import datalib
from tfl_manager import TFLManager


def weekday_paths(weekday_file_counter):
    """ Generates today's path points and inserts them into the MySQL table. """

    logger = datalib.get_new_logger('weekday_paths', 'logs/weekday_paths.log')
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    weekday_file = 'weekday_' + str(weekday_file_counter) + '.csv'

    logger.info('Start creating ' + weekday_file + '... ')
    tfl_manager = TFLManager(weekday_paths_file=weekday_file)

    # Generate the file of used stop points.
    if not os.path.isfile(datalib.CSV_FOLDER + datalib.STOP_POINTS_FILE):
        tfl_manager.print_tube_stops_to_file()
        logger.info('Generated the stop points file.')

    # Generate user paths.
    tfl_manager.generate_and_print_weekday_patterns()
    logger.info('Created file ' + weekday_file + '.')


def main():
    for n in range(10, datalib.TOTAL_WEEKDAY_FILES):
        weekday_paths(n)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
