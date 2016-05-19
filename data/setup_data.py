#!/usr/bin/python

# Script for setting up a proxy database that simulates the user data
# collection, by using the Ubicomp CSV collection.


import csv
import os
import MySQLdb
import urllib2
import sys

# TODO(corina): Change this.s
CSV_FILES_URL = 'https://dl.dropboxusercontent.com/u/954872/UbicompSample.zip?dl=1'
CSV_FILES_DOWNLOAD = 'UbicompSample.zip'
CSV_FILES_SOURCE = os.getcwd() + '/UbicompSample/' # Script must run from main dir.
# TODO(corina): Change this.
CSV_FILTER = 'phone|celllocation|cid' 
MYSQL_DATABASE = 'priv_proxy'
MYSQL_TABLE = 'collected_info'


# Sanitize the CSV collection.
def sanitize_CSV_files():
    # PRE: The CSV files are downloaded from CSV_FILES_URL.
    
    for source in os.listdir(CSV_FILES_SOURCE):
    if source.endswith(".csv"):
            print source
             with open(CSV_FILES_SOURCE + source, 'rb') as f:
             reader = csv.reader(f, delimiter=';', quotechar="'", quoting=csv.QUOTE_ALL)
                 with open(CSV_FILES_SOURCE + source[:-4] + "_result.csv","wb") as result:
                     wtr = csv.writer(result, delimiter=';', quotechar="'", quoting=csv.QUOTE_ALL)
                     for r in reader:
                         if (r[3] == CSV_FILTER):
                             wtr.writerow((r[1],r[2],r[4]))


def main(argv=None):
    # Saintize the CSV files.
    print 'Sanitize the CSV files...'
    sanitize_CSV_files()

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
        print 'Populating the table...'
        for source in os.listdir(CSV_FILES_SOURCE):
            if source.endswith("_result.csv"):
        source = CSV_FILES_SOURCE + source
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
