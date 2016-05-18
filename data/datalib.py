
## Data Files.
WEEKDAY_PATHS_CSV = 'weekday_paths.csv'
WEEKEND_PATHS_CSV = 'weekend_paths.csv'
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


## TFL API Related.
APP_ID = 'ec039efe'
APP_KEY = 'fb265b0c73f86b5835afcde5d3585c18'
# TFL API Requests.
REQUEST_ALL_TUBE_LINES = 'https://api.tfl.gov.uk/Line/Mode/tube/Route?app_id=' + APP_ID + '&app_key=' + APP_KEY
REQUEST_JOURNEY = 'https://api.tfl.gov.uk/Journey/JourneyResults/'
REQUEST_JOURNEY_VAR ='?nationalSearch=False&timeIs=Departing&journeyPreference=LeastTime&walkingSpeed=Average&cyclePreference=None&alternativeCycle=False&alternativeWalking=True&applyHtmlMarkup=False&useMultiModalCall=False&walkingOptimization=False&app_id=ec039efe&app_key=fb265b0c73f86b5835afcde5d3585c18'
REQUEST_LINE_STOPPOINTS = 'https://api.tfl.gov.uk/Line/'
REQUEST_TIMETABLE = 'https://api.tfl.gov.uk/Line/'
TFL_ENTITY_REQUEST_ERROR = 'Tfl.Api.Presentation.Entities.ApiError'


## TFL Network.
TUBE_LINES_IDS = ['bakerloo', 'central', 'circle', 'district',
				  'hammersmith-city', 'jubilee', 'metropolitan',
				  'piccadilly', 'victoria', 'waterloo-city', 'london-overground', 'dlr']

