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
import sys
import time

import datalib

parser = argparse.ArgumentParser(description='Sets up n user paths via TFL.')
# The number of users has to be a multiplier of 100.
parser.add_argument('--users',
                    dest='n',
                    type=int,
                    default=1000,
                    help='Number of users to simulate.')
parser.add_argument('--morning',
                    dest='morning',
                    type=float,
                    default=0.5,
                    help='Percentage of morning commuters.')
parser.add_argument('--evening',
                    dest='night',
                    type=float,
                    default=0.2,
                    help='Percentage of evening commuters.')
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
OUTBOUND_TIME = 9
INBOUND_TIME = 10


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
                 no_users=args.n,
		 initial_shift=0):
        log_file_name = datalib.LOG_FILE_TFL % initial_shift
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
        self._logger = datalib.get_new_logger(datalib.LOG_NAME_TFL,
                                              log_file_name)
        self._stop_points_file = stop_points_file
        self._weekday_paths_file = weekday_paths_file
        self._weekend_paths_file = weekend_paths_file
	self._initial_shift = initial_shift

        self._no_users = no_users
        self._counter = 0
        self.__get_all_tube_stops()

    """ Makes a GET request to TFL API and fetches the result.

    Arguments:
        request: String representing the GET request.

    Returns:
        A Response object with TFL's reply to the given request.
    """
    def _fetch_tfl_result(self, request):
        if self._counter > datalib.API_LIMIT:
            self._counter = 0
            self._logger.info('Sleeping now...')
            time.sleep(datalib.SLEEP_API * 2)
        self._counter += 1
        return requests.get(request)

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
            result = self._fetch_tfl_result(request)
            try:
                result = result.json()
            except ValueError:
                message = 'Reguest: ' + request + '\n Response: ' + str(result)
                self._logger.error('No valid JSON response from TFL API: \n' +
                                   message)
                continue
            if 'type' in result and datalib.TFL_REQUEST_ERROR in result['type']:
                error_message = '%s:%s' % (result['httpStatusCode'],
                                           result['httpStatus'])
                self._logger.error('Error in JSON response.: \n' +
                                   str(TFLError(error_message)))
                continue
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
        file_path = os.path.join(datalib.CSV_FOLDER, self._stop_points_file)
        if os.path.isfile(file_path):
            self._logger.warning('The stop points were printed to file before.')
            return
        paths_file = file(file_path, 'wb')
        writer = csv.writer(paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for stop in self._stops_set:
            writer.writerow(stop)
        paths_file.close()
        self._logger.info('The stop points set has been printed to file.')

    """ Gets a tube stop by its specified id.

    The stop is guaranteed to be in the self._stops_set.

    Arguments:
        stop_id: String of the stop id to be searched.

    Returns:
        A stop tuple, (station_id, station_common_name, latitude, longitude)
        from the self._stops_set.
    """
    def _get_stop_by_id(self, stop_id):
        matched_stops = [stop for stop in self._stops_set if stop[0] == stop_id]
        return matched_stops[0]

    """ Generates a pair of stops, representing a valid path.

    Each stop is a tuple (stop_id, stop_name, latitude, longitude), and
    a path is considered valid if a call to TFL API (GET journey between the
    two stops, will not return a disambiguation.

    Arguments:
        from_id: If specified, id, of the outbound departure stop.

    Returns:
        A pair, (from_stop, to_stop), representing information on the departure
        and arrival tube stops to be used for the travel.
    """
    def __get_valid_path(self, from_id=None):
        # The choices are randomly independent.
        if from_id is None:
            from_stop = random.sample(self._stops_set, 1)[0]
        else:
            from_stop = self._get_stop_by_id(from_id)
        to_stop = random.sample(self._stops_set, 1)[0]
        travel_date = datalib.get_formatted_date()
        leave_time = '0900'
        # Check if they have a valid path.
        while True:
            request = (datalib.REQUEST_JOURNEY % (from_stop[STOP_NAME],
                                                  to_stop[STOP_NAME],
                                                  travel_date,
                                                  leave_time))
            result = self._fetch_tfl_result(request)
            try:
                result = result.json()
                if ((datalib.TFL_FROM_DISAM in result) or
                        (datalib.TFL_TO_DISAM in result) or
                        (datalib.TFL_VIA_DISAM in result)):
                    self._logger.error(result)
                    raise ValueError()
            except ValueError:
                message = (('Failed to generate path between ' +
                            '%s and %s. Retrying...') % (from_stop[STOP_NAME],
                                                         to_stop[STOP_NAME]))
                self._logger.warning(message)
                if from_id is None:
                    from_stop = random.sample(self._stops_set, 1)[0]
                to_stop = random.sample(self._stops_set, 1)[0]
                continue
            break
        return from_stop, to_stop

    """ Generates and prints in file the daytime commute users.

    Arguments:
        writer: CSV file writer object to write the paths in file.
        id_shift: Integer, representing the shift in the user id.

    Returns:
        The number of users that have this commute time pattern.
    """
    def __generate_day_time_users(self, writer, id_shift):
        if writer is None:
            message = 'No writer argument when generating daytime time users.'
            raise TFLError(message)
        morning_users = int(args.morning * args.n)
        for tmp_user_id in range(0, morning_users):
            user_id = tmp_user_id + id_shift + self._initial_shift
            self._logger.info('Generating pattern for user: %s' % user_id)
            outbound_time = random.sample(datalib.MORNING_TIMES, 1)[0]
            inbound_time = random.sample(datalib.EVENING_TIMES, 1)[0]
            (start_point, weekday_point) = self.__get_valid_path()
            writer.writerow([user_id,
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekday_point[STOP_ID],
                             weekday_point[STOP_NAME],
                             weekday_point[STOP_LAT],
                             weekday_point[STOP_LON],
                             outbound_time,
                             inbound_time])
        self._logger.info('Morning user paths for weekday have been generated.')
        return morning_users

    """ Generates and prints in file the night time commute users.

    Arguments:
        writer: CSV file writer object to write the paths in file.
        id_shift: Integer, representing the shift in the user id.

    Returns:
        The number of users that have this commute time pattern.
    """
    def __generate_night_time_users(self, writer, id_shift):
        if writer is None:
            message = 'No writer argument when generating night time users.'
            raise TFLError(message)
        night_users = int(args.night * args.n)
        for tmp_user_id in range(0, night_users):
            user_id = tmp_user_id + id_shift + self._initial_shift
            self._logger.info('Generating pattern for user: %s' % user_id)
            (start_point, weekday_point) = self.__get_valid_path()
            outbound_time = random.sample(datalib.EVENING_TIMES, 1)[0]
            inbound_time = random.sample(datalib.MORNING_TIMES, 1)[0]
            writer.writerow([user_id,
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekday_point[STOP_ID],
                             weekday_point[STOP_NAME],
                             weekday_point[STOP_LAT],
                             weekday_point[STOP_LON],
                             outbound_time,
                             inbound_time])
        self._logger.info('Night user paths for weekday have been generated.')
        return night_users

    """ Generates and prints in file the random time pattern commute users.

    Arguments:
        writer: CSV file writer object to write the paths in file.
        id_shift: Integer, representing the shift in the user id.

    Returns:
        The number of users that have this commute time pattern.
    """
    def __generate_random_users(self, writer, id_shift):
        if writer is None:
            message = 'No writer argument when generating random time users.'
            raise TFLError(message)
        random_users = int((1 - args.morning - args.night) * args.n)
        for tmp_user_id in range(0, random_users):
            user_id = tmp_user_id + id_shift + self._initial_shift
            self._logger.info('Generating pattern for user: %s' % user_id)
            (start_point, weekday_point) = self.__get_valid_path()
            (outbound_time,
             inbound_time) = datalib.generate_random_travel_interval()
            writer.writerow([user_id,
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekday_point[STOP_ID],
                             weekday_point[STOP_NAME],
                             weekday_point[STOP_LAT],
                             weekday_point[STOP_LON],
                             outbound_time,
                             inbound_time])
        self._logger.info('Random user paths for weekday have been generated.')
        return random_users

    """ Generates and prints in file a weekday path for each user. """
    def generate_and_print_weekday_patterns(self):
        file_path = os.path.join(datalib.CSV_FOLDER, self._weekday_paths_file)
        if os.path.isfile(file_path):
            self._logger.warning('The weekday paths were already generated.')
            return
        weekday_paths_file = file(file_path, 'wb')
        writer = csv.writer(weekday_paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        day_time_users = self.__generate_day_time_users(writer, 0)
        night_time_users = self.__generate_night_time_users(writer,
                                                            day_time_users)
        self.__generate_random_users(writer, day_time_users + night_time_users)
        self._logger.info('All weekday paths have been generated.')

    """ Get the full name of the path file to be used at the specified date.

    Arguments:
        paths_date: If present, datetime object of the date to be queried;
        otherwise, today's date will be used.

    Returns:
        A string representing the name of the file to be used.
    """
    def get_paths_file_name(self, paths_date=None):
        if datalib.is_weekend(paths_date):
            if paths_date is None:
                prefix_file = str(time.strftime("_%Y_%m_%d"))
            else:
                prefix_file = paths_date.strftime("_%Y_%m_%d")
            return self._weekend_paths_file % prefix_file
        return self._weekday_paths_file

    """ Generates and prints in file a weekend day path for each user.

    Arguments:
        paths_date: If present, datetime object of the date to be queried;
        otherwise, today's date will be used.
    """
    def __generate_and_print_weekend_patterns(self, paths_date=None):
        # Make sure the weekday paths have been generated.
        self.generate_and_print_weekday_patterns()
        # Get current date to name the file accordingly.
        # At this point, it is guaranteed that's a weekend.
        file_name = self.get_paths_file_name(paths_date)
        if file_name == self._weekday_paths_file:
            self._logger('Today is not a weekday paths day.')
            return
        if os.path.isfile(file_name):
            message = ('The weekend paths for date %s were already generated.' %
                       (paths_date.strftime('%d-%m-%Y')))
            self._logger.warning(message)
            return
        weekend_file_path = os.path.join(datalib.CSV_FOLDER, file_name)
        weekday_file_path = os.path.join(datalib.CSV_FOLDER,
                                         self._weekday_paths_file)
        weekend_paths_file = file(weekend_file_path, 'wb')
        weekday_paths_file = file(weekday_file_path, 'rb')
        writer = csv.writer(weekend_paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        reader = csv.reader(weekday_paths_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            (start_point, weekend_point) = self.__get_valid_path(row[FROM_ID])
            (outbound_time,
             inbound_time) = datalib.generate_random_travel_interval(True)
            writer.writerow([row[USER_ID],
                             start_point[STOP_ID],
                             start_point[STOP_NAME],
                             start_point[STOP_LAT],
                             start_point[STOP_LON],
                             weekend_point[STOP_ID],
                             weekend_point[STOP_NAME],
                             weekend_point[STOP_LAT],
                             weekend_point[STOP_LON],
                             outbound_time,
                             inbound_time])
        self._logger('The weekend paths file has been generated.')

    """ Generate the needed path file to be used today.

    Arguments:
        paths_date: If present, datetime object of the date to be queried;
        otherwise, today's date will be used.
    """
    def __generate_and_print_path_file(self, paths_date=None):
        if datalib.is_weekend(paths_date):
            self.__generate_and_print_weekend_patterns(paths_date)
        else:
            self.generate_and_print_weekday_patterns()

    """ Generates and prints in file the daily commute of the users.

    The data represent tuples (user_id, latitude, longitude, timestamp),
    emulating their daily path, whether it's weekend or weekday.

    Arguments:
        paths_date: If present, datetime object of the date to be queried;
        otherwise, today's date will be used.
    """
    def generate_and_print_daily_paths(self, paths_date=None):
        # Get current day, and the corresponding CSV path file.
        source_path_file = os.path.join(datalib.CSV_FOLDER,
                                        self.get_paths_file_name(paths_date))
        if not os.path.isfile(source_path_file):
            self.__generate_and_print_path_file(paths_date)

        # Check if today's travels were not generated.
        if paths_date is not None:
            suffix_file = str(paths_date.strftime("%Y_%m_%d"))
        else:
            suffix_file = str(time.strftime("%Y_%m_%d"))
        daily_file_name = 'daily_%d_%s.csv' % (self._initial_shift / 1000,
                                               suffix_file)
        daily_file_path = os.path.join(datalib.CSV_FOLDER_GENERATED,
                                       daily_file_name)
        if os.path.isfile(daily_file_path):
            return

        daily_file = file(daily_file_path, 'wb')
        path_file = file(source_path_file, 'r')
        reader = csv.reader(path_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        # Create the corresponding daily path file.
        writer = csv.writer(daily_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        # Generate and write the paths.
        for record in reader:
            from_stop_pos = ('%s,%s' % (record[FROM_LAT], record[FROM_LON]))
            to_stop_pos = ('%s,%s' % (record[FROM_LAT], record[TO_LON]))
            out_time = datalib.get_random_formatted_time(record[OUTBOUND_TIME])
            travel_date = datalib.get_formatted_date(paths_date)
            request = (datalib.REQUEST_JOURNEY % (from_stop_pos,
                                                  to_stop_pos,
                                                  travel_date,
                                                  out_time))
            result = self._fetch_tfl_result(request)
            try:
                result = result.json()
                if 'journeys' not in result or 'legs' in result['journeys']:
                    raise ValueError('No "journey" param in the json response.')
            except ValueError:
                message = 'Reguest: ' + request + '\n Response: ' + str(result)
                self._logger.error('No journey for user ' + record[USER_ID] +
                                   message)
                continue
            # There are no ambiguities or errors in the JSON response.
            journey = result['journeys'][0]
            for leg in journey['legs']:
                # Get the journey points + time.
                if ('path' in leg and 'duration' in leg and
                                      'lineString' in leg['path']):
                    duration = leg['duration']
                    ct = datalib.get_datetime_from_string(leg['departureTime'])
                    line_string = json.loads(leg['path']['lineString'])
                    total = len(line_string) if len(line_string) != 0 else 1
                    if total > duration > 0:
                        freq = total / duration
                    else:
                        freq = 1
                    for i in range(0, total, freq):
                        lat_lon = line_string[i]
                        ct = datalib.get_next_time(ct, 1)
                        writer.writerow([record[USER_ID],
                                         lat_lon[0],
                                         lat_lon[1],
                                         ct.strftime('%Y-%m-%dT%H:%M')])
            self._logger.info('Wrote daily for user %s.' % record[USER_ID])
        daily_file.close()
        path_file.close()
        return daily_file_path


class TFLError(Exception):
    """Error class for handling TFL HTTPS request errors or warnings."""

    """ Initiates a TFL error instance. """

    def __init__(self, value):
        self.value = value

    """ Gives the string representation of the error. """

    @property
    def __str__(self):
        return repr(self.value)

