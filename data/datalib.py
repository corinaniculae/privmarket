

import calendar
import datetime
import logging
import random


# Data Files.
WEEKDAY_PATHS_CSV = 'weekday_1.csv'
WEEKEND_PATHS_CSV = 'weekend_paths_%s.csv'
CSV_FOLDER = 'data/csv_files/'
CSV_FOLDER_GENERATED = 'data/csv_files/generated/'
STOP_POINTS_FILE = 'stop_points.csv'


# TFL API Related Misc.
#APP_ID = 'ce6bfcc9'
#APP_KEY = '9b365537a90d6e5427240840cb1bfee8'
APP_ID = 'ec039efe'
APP_KEY = 'fb265b0c73f86b5835afcde5d3585c18'
API_LIMIT = 420
SLEEP_API = 60


# TFL API Requests.
REQUEST_AUTHENTICATION_VARS = 'app_id=' + APP_ID + '&app_key=' + APP_KEY
REQUEST_LINE_STOP_POINTS = ('https://api.tfl.gov.uk/Line/%s' +
                            '/StopPoints?' +
                            REQUEST_AUTHENTICATION_VARS)
REQUEST_JOURNEY = ('https://api.tfl.gov.uk/Journey/JourneyResults/%s/to/%s?' +
                   'nationalSearch=False&date=%s&time=%s&timeIs=Departing&' +
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
TFL_FROM_DISAM = 'fromLocationDisambiguation'
TFL_TO_DISAM = 'toLocationDisambiguation'
TFL_VIA_DISAM = 'viaLocationDisambiguation'

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
MYSQL_GEN_TABLE = 'generated'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'letmein'
MYSQL_PORT = 3307
MYSQL_LOCAL_INFILE = 1


# MYSQL queries.
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
MYSQL_INSERT_VALUES = """INSERT INTO %s VALUES (%s, %s, %s, %s);"""


# Daily path generation related.
TIME_GET_DAILY_PATHS = '5:00'
DURATION = 3
JOURNEY_TIMES = range(6, 23)
MORNING_TIMES = range(6, 12)
EVENING_TIMES = range(4, 22)
WEEKEND_TIMES = range(7, 23)
TOTAL_WEEKDAY_FILES = 1000


# Logging related.
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_GEN_TODAY = 'logs/today_daily_paths.log'
LOF_FILE_MYSQL = 'logs/MySQLManager.log'
LOG_FILE_TFL = 'logs/TFLManager_%d.log'
LOG_GEN_TODAY = 'today_daily_paths'
LOG_NAME_MYSQL = 'MySQLManager'
LOG_NAME_TFL = 'TFLManager'


def is_weekend(path_date=None):
    """Returns true if it's a weekend day; false otherwise.

    Arguments:
        paths_date: If present, datetime object of the date to be queried;
        otherwise, today's date will be used.
    """
    date_today = path_date if path_date else datetime.date.today()
    return calendar.day_name[date_today.weekday()] in ['Saturday, Sunday']


def generate_random_travel_interval(weekend=False):
    """ Generates a random time interval.

    There will be a minim time difference of datalib.DURATION between
    the outbound journey and the inbound journey.

    Arguments:
        weekend: Boolean check for a weekend travel; if false, it signifies
        a weekday random journey travel time.

    Returns:
        A pair (outbound_time, inbound_time), of integers, representing
        random travel times.
    """
    time_set = WEEKEND_TIMES if weekend else JOURNEY_TIMES
    x = random.sample(time_set, 1)[0]
    y = random.sample(time_set, 1)[0]
    while abs(x - y) < DURATION:
        x = random.sample(time_set, 1)[0]
        y = random.sample(time_set, 1)[0]
    outbound_time = min(x, y)
    inbound_time = max(x, y)
    return outbound_time, inbound_time


def get_random_formatted_time(hour):
    """ Returns a time in the specified [hour; hour+1) time range.

    Arguments:
        hour: Integer, 0 <= hour < 24, representing the hour time.

    Returns:
        String HHMM, representing a random time in the mention time range.
    """
    minute = random.randrange(0, 60)
    travel_time = datetime.time(int(hour), minute)
    return travel_time.strftime('%H%M')


def get_formatted_date(travel_date=None):
    """ Formats the date for a TFL request.

    Arguments:
        travel_date: If specified, a date object, representing the needed date;
        otherwise, today's date will be used.

    Returns:
        String YYYYMMDD, representing the formatted specified date.
    """
    if travel_date is None:
        return datetime.date.today().strftime('%Y%m%d')
    return travel_date.strftime('%Y%m%d')


def get_datetime_from_string(str_time):
    """ Parses a timestamp from TFL and returns a datetime.datetime object.

    Attributes:
        str_time: String YYYY-MM-DDTHH:MM from TFL's API response.

    Returns:
        The equivalent datetime.datetime object of the given string.
    """
    tokens = str_time.split('T')
    date_tokens = tokens[0].split('-')
    time_tokens = tokens[1].split(':')
    return datetime.datetime(int(date_tokens[0]),    # Year
                             int(date_tokens[1]),    # Month
                             int(date_tokens[2]),    # Day
                             int(time_tokens[0]),    # Hour
                             int(time_tokens[1]),    # Minute
                             int(time_tokens[2]))    # Second


def get_next_time(curr_time, duration):
    """ Returns the timestamp, elapsed after the specified duration.

        Arguments:
            curr_time: Datetime object representing the current time.
            duration: Integer of the number of minutes that need to pass.

        Returns:
            Datetime object with the specified delta time added.
    """
    return curr_time + datetime.timedelta(minutes=duration)


def get_new_logger(logger_name, file_name=None):
    """Returns a new logger, as requested, with all setup done.

        Arguments:
            logger_name: String of the name of the logger.
            file_name: If present, file name to record all the logs.
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Create console handler.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
