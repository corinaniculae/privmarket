""" Common utilities and constants library.

    Constant list includes:
        - CSV Files;
        - CSV Folders;
        - CSV Misc.;
        - Map's Topology Related;
        - TFL API Auth.;
        - TFL API Misc.;
        - TFL API Requests;
        - TFL API Response Entities;
        - MySQL/CryptDB Auth.;
        - MySQL/CryptDB Queries;
        - Logging Misc.;
"""

import calendar
import datetime
import logging
import random
import time


# CSV Files.
WEEKDAY_PATHS_CSV = 'weekday_%d.csv'     # Generic name for weekday paths file.
WEEKEND_PATHS_CSV = 'weekend_%d_%s.csv'  # Generic name for weekend paths file.
STOP_POINTS_FILE = 'stop_points.csv'     # List of all used map network stops.

# CSV Folder.
CSV_FOLDER = 'src/csv_files/'                      # Main CSV folder.
CSV_GENERATED_FOLDER = 'src/csv_files/generated/'  # Daily CSV data folder.
CSV_PATH_FOLDER = 'src/csv_files/paths'            # Path CSV data folder.

# CSV Miscellaneous.
DURATION = 3                    # Minimum time spent travelling in a cycle, pp.
JOURNEY_TIMES = range(6, 23)    # General commuting times to be simulated.
MORNING_TIMES = range(6, 12)    # Morning commuting times to be simulated.
EVENING_TIMES = range(4, 22)    # Evening commuting times to be simulated.
WEEKEND_TIMES = range(7, 23)    # Weekend travelling times to be simulated.
TOTAL_WEEKDAY_FILES = 1000      # No. of rows in a path data CSV file.
# Column names in the path CSV files.
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

# Map's Topology Related.
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
                  'dlr']        # Used lines for queries.

# TFL API Authentication.
APP_ID = 'ec039efe'                           # App ID for TFL API requests.
APP_KEY = 'fb265b0c73f86b5835afcde5d3585c18'  # App Key for TFL API requests.
# APP_ID_SPARE = 'ce6bfcc9'                              # Spare App ID.
# APP_KEY_SPARE = '9b365537a90d6e5427240840cb1bfee8'     # Spare App Key.

# TFL API Miscellaneous.
API_LIMIT = 420                 # Limit of requests per minute.
SLEEP_API = 60                  # Sleeping time when API LIMIT is achieved.
TIME_GET_DAILY_PATHS = '5:00'   # Time to query the TFL API for daily data.

# TFL API Requests.
REQUEST_AUTH_VARS = 'app_id=%s&app_key=%s' % (APP_ID, APP_KEY)
REQUEST_STOP_POINTS_BY_LINE = ('https://api.tfl.gov.uk/Line/%s/StopPoints?' +
                               REQUEST_AUTH_VARS)
REQUEST_JOURNEY = ('https://api.tfl.gov.uk/Journey/JourneyResults/%s/to/%s?' +
                   'nationalSearch=False&date=%s&time=%s&timeIs=Departing&' +
                   'journeyPreference=LeastTime&walkingSpeed=Average&' +
                   'cyclePreference=None&alternativeCycle=False&' +
                   'alternativeWalking=True&' +
                   'applyHtmlMarkup=False&useMultiModalCall=False&' +
                   'walkingOptimization=False&' +
                   REQUEST_AUTH_VARS)
REQUEST_TIMETABLE = ('https://api.tfl.gov.uk/Line/%s/Timetable/%s/to/%s?' +
                     REQUEST_AUTH_VARS)

# TFL API Response Entities.
TFL_REQUEST_ERROR = 'Tfl.Api.Presentation.Entities.ApiError'
TFL_FROM_DISAMBIGUATION = 'fromLocationDisambiguation'
TFL_TO_DISAMBIGUATION = 'toLocationDisambiguation'
TFL_VIA_DISAMBIGUATION = 'viaLocationDisambiguation'

# MYSQL/CryptDB Authentication.
CRYPTDB_DB = 'priv_coll'            # Database name in CryptDB.
CRYPTDB_TABLE = 'generated'         # Table name in CryptDB.
CRYPTDB_HOST = '146.169.46.236'          # Host name in CryptDB.
CRYPTDB_USER = 'root'               # Root user name in CryptDB.
CRYPTDB_PASSWORD = 'letmein'        # Root user password in CryptDB.
CRYPTDB_PORT = 3307                 # Proxy connection port for CryptDB.
MYSQL_DB = 'priv_proxy'             # Database name in MySQL.
MYSQL_GEN_TABLE = 'generated'       # Table name in MySQL.
MYSQL_HOST = 'localhost'            # Host name in MySQL.
MYSQL_USER = 'root'                 # Root user name in MySQL.
MYSQL_PASSWORD = 'letmein'          # Root user password in MySQL.
MYSQL_LOCAL_INFILE = 1              # Param. for running LOAD queries in MySQL.

# MYSQL/CryptDB queries.
MYSQL_CREATE_DB = 'CREATE DATABASE IF NOT EXISTS %s ;'
MYSQL_USE_DB = 'USE %s;'
MYSQL_CREATE_GEN_TABLE = """CREATE TABLE IF NOT EXISTS %s (
                                RecordId VARCHAR(60) NOT NULL,
                                Latitude VARCHAR(60) NOT NULL,
                                Longitude VARCHAR(60) NOT NULL,
                                Timestamp VARCHAR(60) NOT NULL
                                );"""
MYSQL_CREATE_PATHS_TABLE = """CREATE TABLE IF NOT EXISTS %s (
                                    RecordId VARCHAR(60) NOT NULL, \
                                    FromStopId varchar(60) not null, \
                                    FromStopName varchar(120) not null, \
                                    FromLat varchar(60) not null, \
                                    FromLon varchar(60) not null, \
                                    ToStopId varchar(60) not null, \
                                    ToStopName varchar(120) not null, \
                                    ToLat varchar(60) not null, \
                                    ToLon varchar(60) not null, \
                                    FromHour int(16) not null, \
                                    ToHour int(16) not null
                                    );"""
MYSQL_LOAD_GEN_FILE = """LOAD DATA LOCAL INFILE '%s' into table %s
                                fields terminated by ';'
                                lines terminated by '\n'
                                (RecordId, Latitude, Longitude, Timestamp); """
MYSQL_LOAD_PATH_FILE = """LOAD DATA LOCAL INFILE '%s' into table %s
                                fields terminated by ';'
                                lines terminated by '\n'
                                (RecordId,
                                 FromStopId,
                                 FromStopName,
                                 FromLat,
                                 FromLon,
                                 ToStopId,
                                 ToStopName,
                                 ToLat,
                                 ToLon,
                                 FromHour,
                                 ToHour);"""
MYSQL_INSERT_GEN_VALUES = """INSERT INTO %s VALUES ('%s', '%s', '%s', '%s');"""

# Logging Miscellaneous.
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_CRYPTDB = 'logs/cryptdb_manager.log'
LOG_FILE_GEN_TODAY = 'logs/today_daily.log'
LOF_FILE_MYSQL = 'logs/MySQLManager.log'
LOG_FILE_TFL = 'logs/TFLManager_%s.log'
LOG_NAME_CRYPTDB = 'CryptDBManager'
LOG_NAME_GEN_TODAY = 'today_daily'
LOG_NAME_MYSQL = 'MySQLManager'
LOG_NAME_TFL = 'TFLManager'


def is_weekend(path_date=None):
    """Returns true if it's a weekend day; false otherwise.

    Arguments:
        path_date: If present, datetime object of the date to be queried;
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


def date_range(str_start_date, str_end_date):
    """ Generate a date range between the specified dates.

    Arguments:
        str_start_date: String DD-MM-YYYY, representing the start date of
        the time range.
        str_end_date: String DD-MM-YYYY, representing the end date of the range.

    Returns:
        An iterator for the specified date range.
    """
    start_tokens = str_start_date.split('-')
    end_tokens = str_end_date.split('-')
    start_date = datetime.date(int(start_tokens[2]),
                               int(start_tokens[1]),
                               int(start_tokens[0]))
    end_date = datetime.date(int(end_tokens[2]),
                             int(end_tokens[1]),
                             int(end_tokens[0]))
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


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
                             int(time_tokens[1]))    # Minute


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


def get_timestamp_from_request_string(str_time):
    """ Parses a timestamp from TFL and returns a datetime.datetime object.

    Attributes:
        str_time: String YYYY/MM/DD HH:MM (AM|PM) from TFL's API response.

    Returns:
        The equivalent datetime.datetime object of the given string.
    """
    tokens = str_time.split(' ')
    type = tokens[2]
    date_tokens = tokens[0].split('/')
    time_tokens = tokens[1].split(':')
    year = int(date_tokens[2])
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    hour = int(time_tokens[0])
    if type is 'PM':
        hour += 12
    minute = int(time_tokens[1])
    dt = datetime.datetime(year, month, day, hour, minute)
    return int(time.mktime(dt.timetuple()))


def prepare_coordinate(coord_str):
    # Reformat e-notation numbers. (Such as -7.721184e-05)
    if 'e' in coord_str:
        print 'got: ' + coord_str
        tokens = coord_str.split('.')
        negative = '-' in tokens[0]
        initial_decimals = tokens[1].split('e')
        first = tokens[0][1:] if negative else tokens[0]
        second = initial_decimals[0]
        shift = int(initial_decimals[1][1:])
        decimals = str(first + second)  # All decimals of the number.
        coord_str = '0.' + decimals.rjust(len(decimals) + shift, '0')
        if negative:
            coord_str = '-' + coord_str
        print 'transformed into: ' + coord_str + '\n'

    # Remove the digits before the point.
    tokens = coord_str.split('.')
    decimals = tokens[1].ljust(18, '0')
    coord1 = 1000000000 - int(decimals[:9])
    coord2 = 1000000000 - int(decimals[9:18])
    return coord1, coord2