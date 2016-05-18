#!/usr/bin/python

""" Script for querying TFL API for stop points information
in order to create a synthetic weekday and weekend path for n users. """

import argparse
import csv
import json
import random
import requests
import sets
import sys
import urllib2

import datalib
from data_errors import TFLError

parser = argparse.ArgumentParser(description='Sets up n user paths via TFL.')
parser.add_argument('--users', dest='n', metavar='n', type=int, default=1000,
                    help='Number of users to simulate.')
args = parser.parse_args()


""" Gets a set of all tube stops.

Returns:
    A set of pairs (station_id, station_common_name) of all corresponding stops
    of the lines defined in datalib.TUBE_LINES_IDS.

Raises:
    TFLError: Any error given by the TFL API calls.
"""
def get_all_tube_stops():
    stops_set = sets.Set([])
    for line_id in datalib.TUBE_LINES_IDS:
        request = (datalib.REQUEST_LINE_STOPPOINTS +
                   line_id +
                   '/StopPoints?app_id=' +
                   datalib.APP_ID +
                   '&app_key=' +
                   datalib.APP_KEY)
        result = requests.get(request).json()
        if ('type' in result and
            datalib.TFL_ENTITY_REQUEST_ERROR in result['type']):
            raise TFLError(result['httpStatusCode'] + ': ' +
                           result['httpStatus'])
        for stop in result:
            if 'lat' in stop and 'lon' in stop:
                lat, lon = stop['lat'], stop['lon']
            else:
                lat, lon = 0, 0
            stops_set.add((stop['id'],
                           stop['commonName'],
                           lat,
                           lon))
    return stops_set


""" Get three random elements from the specified set.

Arguments:
    stops_set: A set of possible stop points of the TFL network.

Returns:
    A triple (a, b, c) of three independently random variables from the set. """
def get_triple_pts(stops_set):
    a = random.sample(stops_set, 1)[0]
    b = random.sample(stops_set, 1)[0]
    c = random.sample(stops_set, 1)[0]
    return a, b, c


""" Writes n possible user paths in the given CSV files.

Writes a number n of commuting paths specified by the --users flag, with the
following semantics:
x - departure point (user's home stop)
y - arrival point (user's work stop)
z - alternative arrival point (user's stop in the weekend)
The path x-y will be the weekday path and written in the WEEKDAY_PATH_CSV file,
while x-z will be the weekend path, that has a probability of happening, in 
which case will be written in the WEEKEND_PATH_CSV file. If the journey is
supposingly not happening, x-x will be filled.

Args:
    stop_set: A list of pairs (station_id, station_common_name) corresponding to
    the possible stops on the TFL map.

Returns:
    A set of pairs (station_id, station_common_name) of all corresponding stops
    of the lines defined in datalib.TUBE_LINES_IDS.

Raises:
    TFLError: Any error given by the TFL API calls.
"""
def write_to_csv_files(stops_set):

    weekday_csv = file(datalib.WEEKDAY_PATHS_CSV, 'wb')
    weekend_csv = file(datalib.WEEKEND_PATHS_CSV, 'wb')

    weekday_writer = csv.writer(weekday_csv,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
    weekend_writer = csv.writer(weekend_csv,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL) 

    for user_id in range(0, args.n):
        (start_point, weekday_point, weekend_point) = get_triple_pts(stops_set)
        weekday_writer.writerow([user_id,
                                 start_point[0],
                                 start_point[1],
                                 start_point[2],
                                 start_point[3],
                                 weekday_point[0],
                                 weekday_point[1],
                                 weekday_point[2],
                                 weekday_point[3]])
        if random.uniform(0, 1):
            weekend_point = start_point
        weekend_writer.writerow([user_id,
                                 start_point[0],
                                 start_point[1],
                                 start_point[2],
                                 start_point[3],
                                 weekday_point[0],
                                 weekday_point[1],
                                 weekday_point[2],
                                 weekday_point[3]])


def main():
    print 'Creating daily commute paths for ' + str(args.n) + ' users...'

    try:
        # Get all possible stops.
        stops_set = get_all_tube_stops()
    except TFLError, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    # Write the paths in the CSV files.
    write_to_csv_files(stops_set)

    print str(args.n) + ' have been created.'


if __name__ == '__main__':
    status = main()
    sys.exit(status)