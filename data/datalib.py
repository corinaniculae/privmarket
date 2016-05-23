

import calendar
import datetime


# Data Files.
WEEKDAY_PATHS_CSV = 'weekday_paths.csv'
WEEKEND_PATHS_CSV = 'weekend_paths_%s.csv'
CSV_FOLDER = 'data/csv_files/'
CSV_FOLDER_GENERATED = 'data/csv_files/generated/'
STOP_POINTS_FILE = 'stop_points.csv'


# TFL API Related Misc.
APP_ID = 'ec039efe'
APP_KEY = 'fb265b0c73f86b5835afcde5d3585c18'
API_LIMIT = 450
SLEEP_API = 60


# TFL API Requests.
REQUEST_AUTHENTICATION_VARS = 'app_id=' + APP_ID + '&app_key=' + APP_KEY
REQUEST_LINE_STOP_POINTS = ('https://api.tfl.gov.uk/Line/%s' +
                            '/StopPoints?' +
                            REQUEST_AUTHENTICATION_VARS)
REQUEST_JOURNEY = ('https://api.tfl.gov.uk/Journey/JourneyResults/%s/to/%s?' +
                   'nationalSearch=False&timeIs=Departing&' +
                   'journeyPreference=LeastTime&walkingSpeed=Average&' +
                   'cyclePreference=None&alternativeCycle=False&' +
                   'alternativeWalking=True&' +
                   'applyHtmlMarkup=False&useMultiModalCall=False&' +
                   'walkingOptimization=False&' +
                   REQUEST_AUTHENTICATION_VARS)
REQUEST_TIMETABLE = ('https://api.tfl.gov.uk/Line/%s/Timetable/%s/to/%s?' +
                     REQUEST_AUTHENTICATION_VARS)


# TFL API Response Entities.
TFL_REQUEST_ERROR = 'Tfl.Api.Presentation.Entities.ApiError'
TFL_DISAM = 'Tfl.Api.Presentation.Entities.JourneyPlanner.DisambiguationResult'


# TFL Network.
TUBE_LINES_IDS = ['bakerloo',
                  'central',
                  'circle',
                  'district',
                  'hammersmith-city',
                  'jubilee',
                  'metropolitan',
                  'piccadilly',
                  'victoria',
                  'waterloo-city',
                  'london-overground',
                  'dlr']


# MYSQL variables.
MYSQL_DB = 'priv_proxy'
MYSQL_TABLE = 'generated'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'letmein'
MYSQL_LOCAL_INFILE = 1


#MYSQL queries.
MYSQL_CREATE_DB = 'CREATE DATABASE IF NOT EXISTS %s ;'
MYSQL_USE_DB = 'USE %s;'
MYSQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS %s (
                                RecordId VARCHAR(60) NOT NULL,
                                Timestamp VARCHAR(60) NOT NULL,
                                Location VARCHAR(60) NOT NULL
                                );"""
MYSQL_CREATE_GEN_TABLE = """CREATE TABLE IF NOT EXISTS %s (
                                RecordId VARCHAR(60) NOT NULL,
                                Latitude VARCHAR(60) NOT NULL,
                                Longitude VARCHAR(60) NOT NULL,
                                Timestamp VARCHAR(60) NOT NULL
                                );"""
MYSQL_LOAD_FILE = """LOAD DATA LOCAL INFILE '%s' into table %s
                                fields terminated by ';'
                                lines terminated by '\n'
                                (RecordId, Timestamp, Location); """
MYSQL_LOAD_GEN_FILE = """LOAD DATA LOCAL INFILE '%s' into table %s
                                fields terminated by ';'
                                lines terminated by '\n'
                                (RecordId, Latitude, Longitude, Timestamp); """


#Daily path generation related.
TIME_GET_DAILY_PATHS = '5:00'


def is_weekend():
    """Returns true if it's a weekend day; false otherwise."""
    date_today = datetime.date.today()
    return calendar.day_name[date_today.weekday()] in ['Saturday, Sunday']


def get_next_time(curr_time, duration):
    """ Returns the timestamp, elapsed after the specified duration.

        Arguments:
            curr_time: String of the form YYYY-MM-DDTHH:MM:SS.
            duration: Integer specifying the number of minutes that need to pass.

        Returns:
            String of the form YYYY-MM-DDTHH:MM:SS, with the new timestamp.
    """
    # TODO(corinan): Fix this.
    tokens = curr_time.split('T')
    time_tokens = str(tokens[1]).split(':')
    new_min = int(time_tokens[1]) + duration
    if new_min < 60:
        tokens[1] = time_tokens[0] + ':' + str(new_min) + ':' + time_tokens[2]
    else:
        new_hour = (int(time_tokens[0]) + 1) % 24
        new_min = int(new_min) % 60
        tokens[1] = str(new_hour) + ':' + str(new_min) + ':' + time_tokens[2]
    return tokens[0] + 'T' + tokens[1]
