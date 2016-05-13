#!/usr/bin/python

# Script for querying TFL API for tube (live) information
# in order to create a synthetic path for n users.

import argparse
import csv
import json
import random
import requests
import sys
import urllib2


APP_ID = 'ec039efe'
APP_KEY = 'fb265b0c73f86b5835afcde5d3585c18'
TUBE_LINES_IDS = ['bakerloo', 'central', 'circle', 'district',
				  'hammersmith-city', 'jubilee', 'metropolitan',
				  'piccadilly', 'victoria', 'waterloo-city', 'london-overground', 'dlr']
REQUEST_ALL_TUBE_LINES = 'https://api.tfl.gov.uk/Line/Mode/tube/Route?app_id=' + APP_ID + '&app_key=' + APP_KEY
REQUEST_LINE_STOPPOINTS = 'https://api.tfl.gov.uk/Line/'


parser = argparse.ArgumentParser(description='Sets up n user paths via TFL.')
parser.add_argument('--users', dest='n', metavar='n', type=int, default=1000,
                    help='Number of users to simulate.')
args = parser.parse_args()


def main():
	print 'Creating daily commute paths for ' + str(args.n) + ' users...'

	# Get all possible stops.
	stops_list = []
	for line_id in TUBE_LINES_IDS:
		request = REQUEST_LINE_STOPPOINTS + line_id + '/StopPoints?app_id=' + APP_ID + '&app_key=' + APP_KEY
		result = requests.get(request).json()
		for stop in result:
			stops_list.append(stop['commonName'])
	stops_set = set(stops_list)
	
	# Write daily paths in an intermediate CSV file.
	with open('daily_paths.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)                   	    
		for user_id in range(0, args.n):
			start_point = random.sample(stops_set, 1)[0]
			end_point = random.sample(stops_set, 1)[0]
			writer.writerow([user_id, start_point, end_point])


if __name__ == '__main__':
    status = main()
    sys.exit(status)