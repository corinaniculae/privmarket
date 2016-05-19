#!/usr/bin/python

""" Script for querying TFL API for stop points information
in order to create a synthetic weekday and weekend path for n users. """

import argparse
import csv
import json
import logging
import os
import random
import requests
import time

import datalib

parser = argparse.ArgumentParser(description='Sets up n user paths via TFL.')
parser.add_argument('--users',
                    dest='n',
                    type=int,
                    default=1000,
                    help='Number of users to simulate.')
args = parser.parse_args()


# Indices in a stop tuple - (stop_id, stop_name, latitude, longitude).
STOP_ID = 0
STOP_NAME = 1
STOP_LAT = 2
STOP_LON = 3

# Column names in the paths CSV files.
USER_ID = 0
FROM_ID = 1
FROM_NAME = 2
FROM_LAT = 3
FROM_LON = 4
TO_ID = 5
TO_NAME = 6
TO_LAT = 7
TO_LON = 8


class TFLManager:
    """Handler for any TFL API requests."""

    """ Initiates a TFLManager object.

    Arguments:
        stop_points_file: File name for storing the set of stop points that was
        used when generating the user's paths.
        weekday_paths_file: File name for storing the weekday commuting paths of
        the users.
        weekend_paths_file: Prefix file name for storing the weekend commuting
        paths; to be generated for each day of the weekend.
        no_users: Integer, specifying the number of users to be simulated.
    """
    def __init__(self,
                 stop_points_file=datalib.STOP_POINTS_FILE,
                 weekday_paths_file=datalib.WEEKDAY_PATHS_CSV,
                 weekend_paths_file=datalib.WEEKEND_PATHS_CSV,
                 no_users=args.n):
        self._logger = logging.getLogger('TFLLogger')
        self._stop_points_file = stop_points_file
        self._weekday_paths_file = weekday_paths_file
        self._weekend_paths_file = weekend_paths_file
        self._no_users = no_users
        self.__get_all_tube_stops()

    """ Gets a set of all tube stops.

    Returns:
        A set of tuples (station_id, station_common_name, latitude, longitude)
        of all corresponding stops of the lines defined in
        datalib.TUBE_LINES_IDS.

    Raises:
        TFLError: Any error given by the TFL API calls.
    """
    def __get_all_tube_stops(self):
        self._stops_set = set([])
        for line_id in datalib.TUBE_LINES_IDS:
            request = (datalib.REQUEST_LINE_STOP_POINTS % line_id)
            result = requests.get(request).json()
            if 'type' in result and datalib.TFL_REQUEST_ERROR in result['type']:
                self._logger.error(TFLError(result['httpStatusCode'] + ': ' +
                                            result['httpStatus']))
            self._logger.info('GET stop points for line: %s.' % line_id)
            for stop in result:
                if 'lat' in stop and 'lon' in stop:
                    lat, lon = stop['lat'], stop['lon']
                else:
                    lat, lon = 0, 0
                self._stops_set.add((stop['id'],
                                     stop['commonName'],
                                     lat,
                                     lon))
        self._logger.info('The stop points set has been generated.')

    """ Prints the current set of stop points to the specified file.

    Arguments:
        file_name: Name of the CSV file to which the list is written.
    """
    def print_tube_stops_to_file(self):
        paths_file = file(datalib.CSV_FOLDER + self._stop_points_file, 'wb')
        writer = csv.writer(paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for stop in self._stops_set:
            writer.writerow(stop)
        paths_file.close()
        self._logger.info('The stop points set has been printed to file.')

    """ Returns a pair of stops, representing a valid path.

    Each stop is a tuple (stop_id, stop_name, latitude, longitude), and
    a path is considered valid if a call to TFL API (GET journey between the
    two stops, will not return a disambiguation.
    """
    def __get_valid_path(self):
        # The choices are randomly independent.
        from_stop = random.sample(self._stops_set, 1)[0]
        to_stop = random.sample(self._stops_set, 1)[0]

        i = 0
        while i < len(self._stops_set):
            # Check if they have a valid path.
            from_stop_pos = (from_stop[STOP_LAT] + ',' + from_stop[STOP_LON])
            to_stop_pos = to_stop[STOP_LAT] + ',' + to_stop[STOP_LON]
            request = (datalib.REQUEST_JOURNEY % from_stop_pos, to_stop_pos)
            result = requests.get(request)
            i += 1
            try:
                result = json.loads(result)
                if 'type' in result and datalib.TFL_DISAM in result['type']:
                    from_stop = random.sample(self._stops_set, 1)[0]
                    to_stop = random.sample(self._stops_set, 1)[0]
                    continue
            except ValueError:
                from_stop = random.sample(self._stops_set, 1)[0]
                to_stop = random.sample(self._stops_set, 1)[0]
                continue

        if i == len(self._stops_set):
            self._logger.error('No valid path found.')
            return None, None

        return from_stop, to_stop

    """ Generates and prints in file a weekday path for each user. """
    def generate_and_print_weekday_paths(self):
        weekday_paths_file_path = datalib.CSV_FOLDER + self._weekday_paths_file
        weekday_paths_file = file(weekday_paths_file_path, 'wb')
        writer = csv.writer(weekday_paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for user_id in range(0, args.n):
            (start_point, weekday_point) = self.__get_valid_path()
            writer.writerow({user_id,
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekday_point[STOP_ID],
                             weekday_point[STOP_NAME],
                             weekday_point[STOP_LAT],
                             weekday_point[STOP_LON]})
        weekday_paths_file.close()
        self._logger('The weekday paths file has been generated.')

    """ Get the full name of the current"""
    def get_today_paths_file_name(self):
        if datalib.is_weekend():
            return self._weekend_paths_file % str(time.strftime("%Y_%m_%d"))
        return self._weekday_paths_file

    """ Generates and prints in file a weekend day path for each user. """
    def generate_and_print_weekend_paths(self):
        # Get current date to name the file accordingly.
        file_name = (self._weekend_paths_file % str(time.strftime("%Y_%m_%d")))

        weekend_paths_file_path = datalib.CSV_FOLDER + file_name
        weekend_paths_file = file(weekend_paths_file_path, 'wb')
        writer = csv.writer(weekend_paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for user_id in range(0, args.n):
            (start_point, weekend_point) = self.__get_valid_path()
            writer.writerow({user_id,
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekend_point[STOP_ID],
                             weekend_point[STOP_NAME],
                             weekend_point[STOP_LAT],
                             weekend_point[STOP_LON]})
        self._logger('The weekend paths file has been generated.')

    """ Generate the needed path file to be used today. """
    def __generate_and_print_path_file(self):
        if datalib.is_weekend():
            self.generate_and_print_weekend_paths()
        else:
            self.generate_and_print_weekday_paths()

    """ Generates and prints in file the daily commute of the users.

    The data represent tuples (user_id, latitude, longitude, timestamp),
    emulating their daily path, whether it's weekend or weekday.

    """
    def generate_and_print_daily_paths(self):
        # Get current day, and the corresponding CSV path file.
        path_file = datalib.CSV_FOLDER + self.get_today_paths_file_name()
        if not os.path.isfile(path_file):
            self.__generate_and_print_path_file()
        path_file = file(path_file, 'r')
        reader = csv.reader(path_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        # Create the corresponding daily path file.
        daily_file_name = ('daily_%s.csv' % str(time.strftime("%Y_%m_%d")))
        daily_file = file(datalib.CSV_FOLDER + daily_file_name, 'wb')
        writer = csv.writer(daily_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        # Generate and write the paths.
        for record in reader:
            from_stop_pos = (record[FROM_LAT] + ',' + record[FROM_LON])
            to_stop_pos = record[FROM_LAT] + ',' + record[TO_LON]
            # TODO(corinan): Add departure time to the request.
            request = (datalib.REQUEST_JOURNEY % from_stop_pos, to_stop_pos)
            result = requests.get(request)
            try:
                result = json.loads(result)
                if 'journeys' not in result or 'legs' in result['journey']:
                    raise ValueError('No "journey" param in the json response.')
            except ValueError:
                self._logger.error('No journey for user ' + record[USER_ID])
                continue
            # There are no ambiguities or errors in the JSON response.
            journey = result['journeys'][0]
            for leg in journey['legs']:
                # Get the journey points + time.
                if ('path' in leg and 'duration' in leg and
                                      'lineString' in leg['path']):
                    duration = leg['duration']
                    curr_time = leg['departureTime']
                    line_string = json.loads(leg['path']['lineString'])
                    total = len(line_string)
                    freq = (total / duration if total > duration else 1)
                    count = 0
                    i = 0
                    while count < duration and i < total:
                        lat_lon = line_string[i]
                        curr_time = datalib.get_next_time(curr_time, duration)
                        writer.writerow({record[USER_ID],
                                         lat_lon[0],
                                         lat_lon[1],
                                         curr_time})
                        count += 1
                        i += freq


class TFLError(Exception):
    """Error class for handling TFL HTTPS request errors or warnings."""

    """ Initiates a TFL error instance. """

    def __init__(self, value):
        self.value = value

    """ Gives the string representation of the error. """

    @property
    def __str__(self):
        return repr(self.value)

