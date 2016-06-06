#!/usr/bin/python

# Script to generated users' weekday paths to be simulated.


import logging
import os
import sys

import datalib
from tfl_manager import TFLManager


def main():
    """ Generates today's path points and inserts them into the MySQL table. """
    for weekday_file_counter in range(18, datalib.TOTAL_WEEKDAY_FILES):
        logger = datalib.get_new_logger('weekday_paths',
                                        'logs/weekday_paths.log')
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
        weekday_file = 'paths/weekday_%d.csv' % weekday_file_counter

        logger.info('Start creating ' + weekday_file + '... ')
        initial_shift = weekday_file_counter * 1000
        tfl_manager = TFLManager(weekday_paths_file=weekday_file,
                                 initial_shift=initial_shift)

        # Generate the file of used stop points.
        if not os.path.isfile(datalib.CSV_FOLDER + datalib.STOP_POINTS_FILE):
            tfl_manager.print_tube_stops_to_file()
            logger.info('Generated the stop points file.')

        # Generate user paths.
        tfl_manager.generate_and_print_weekday_patterns()
        logger.info('Created file ' + weekday_file + '.')
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
