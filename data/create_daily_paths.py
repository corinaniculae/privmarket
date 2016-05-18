#!/usr/bin/python

# Script for daily querying TFL for travel times.

import csv
import json
import os
import requests
import sys

import datalib

SOURCE_CSV = os.getcwd()
MYSQL_TABLE = 'generated_info'
MYSQL_DATABASE = 'priv_proxy'

def get_next_time(curr_time, duration):
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


def main(argv=None):
    with open(datalib.WEEKDAY_PATHS_CSV, 'rb') as f:
        daily_final_csv = file('daily_final.csv', 'wb')
        writer = csv.writer(daily_final_csv,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL) 
        reader = csv.reader(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for record in reader:
            request = (datalib.REQUEST_JOURNEY +
                       record[datalib.FROM_LAT] + ',' +
                       record[datalib.FROM_LON] + '/to/' +
                       record[datalib.TO_LAT] + ',' +
                       record[datalib.TO_LON] + datalib.REQUEST_JOURNEY_VAR)
            result = requests.get(request).json()
            if 'journeys' in result:
                # There are no ambiguations or errors.
                journey = result['journeys'][0]
                if 'legs' in journey:
                    for leg in journey['legs']:
                        # Get start location + time
                        if 'departurePoint' in leg and 'departureTime' in leg:
                            start_coord = (leg['departurePoint']['lat'],
                                           leg['departurePoint']['lon'])
                            print (record[datalib.USER_ID] + ';' +
                                   str(start_coord[0]) + ';' +
                                   str(start_coord[1]) + ';' +
                                   leg['departureTime'])
                        # Get intermediate points.
                        if 'path' in leg and 'lineString' in leg['path'] and 'duration' in leg:
                            duration = leg['duration']
                            curr_time = leg['departureTime']
                            line_string = json.loads(leg['path']['lineString'])
                            total = len(line_string)
                            freq = total / duration if total > duration else 1
                            count = 0
                            i = 0
                            while count < duration and i < total:
                                lat_lon = line_string[i]
                                curr_time = get_next_time(curr_time, duration)
                                weekend_writer.writerow([record[datalib.USER_ID],
                                                         str(lat_lon[0]),
                                                         str(lat_lon[1]),
                                                         curr_time])
                                count = count + 1
                                i = i + freq
            # Put the entire path + time in a CSV.
            try:
            # Connect to the MySQL server.
            print 'Connect to the MySQL server...'
            db = MySQLdb.connect(host="localhost",    # host name
                                 user="root",         # username
                                 passwd="letmein",    # password
                                 local_infile = 1)
                                
            cur = db.cursor() # Cursor object for executing MySQL queries.

            # Create the MySQL database.
            print 'Creating/Fetching the database and the table...'
            create_db_query = "CREATE DATABASE IF NOT EXISTS " + MYSQL_DATABASE + ";"
            use_db_query = "USE " + MYSQL_DATABASE + ";"
            create_table_query = "CREATE TABLE IF NOT EXISTS " + MYSQL_TABLE + "( \
                                    ID int(11) AUTO_INCREMENT, \
                                    RecordId VARCHAR(60) NOT NULL, \
                                    Timestamp VARCHAR(60) NOT NULL, \
                                    Location VARCHAR(60) NOT NULL, \
                                    PRIMARY KEY (ID));" 
            cur.execute(create_db_query)
            cur.execute(use_db_query)
            cur.execute(create_table_query)

            # Insert CSV files into the database.
            source = SOURCE_CSV + 'daily_final.csv'
                    add_csv_query = "LOAD DATA LOCAL INFILE \'" + source + "\' into table " + MYSQL_TABLE + " fields terminated by ';' \
                                     lines terminated by '\n' \
                                     (RecordId, Timestamp, Location);"
                    cur.execute(add_csv_query)
        db.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        
        finally:    
            if db:
                print 'Table has been populated.'
                db.close()



if __name__ == '__main__':
    status = main()
    sys.exit(status)