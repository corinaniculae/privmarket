#!/usr/bin/python

# Script for setting up a proxy database that simulates the user data
# collection, by using the Ubicomp CSV collection.


import csv
import gzip
import os
#import MySQLdb
import urllib2
import shutil
import sys

# TODO(corina): Change this.s
CSV_FILES_URL = 'https://dl.dropboxusercontent.com/u/954872/UbicompSample.zip?dl=1'
CSV_FILES_DOWNLOAD = 'UbicompSample.zip'
# TODO(corina): Change this.
CSV_FILTER = 'phone|celllocation|cid' 
MYSQL_DATABASE = 'priv_proxy'
MYSQL_TABLE = 'test'
                

def main():
    """
    db = None
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
    """
    # Insert CSV files into the database.
    print 'Populating the table...'
    stop = False
    ind = 0
    count = 0
    for root, subdirs, files in os.walk('/Volumes/Part1/Data'):
        print root
        if 'indexdb' in root:
            continue
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith('.gz'):
                count += 1
                file_content = gzip.open(file_path, 'rb')
                reader = csv.reader(file_content, delimiter=';', quotechar="'", quoting=csv.QUOTE_ALL)
                if '\\' not in root[-40:]:
                    new_file_name = root[-40:]
                    print new_file_name
                    ind +=1
                else:
                    print "This is an error."
                continue
                write_file_name = '/Volumes/Part2/Curated/csv_' + root[-20:]+ '.csv'
                csv_file = open(write_file_name, 'wb')
                writer = csv.writer(csv_file,
                            delimiter=';',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
                for r in reader:
                    if (r[3] == CSV_FILTER):
                        writer.writerow((r[1],r[2],r[4]))
                file_content.close()
                csv_file.close()

                source = './csv_file.csv'
                #add_csv_query = "LOAD DATA LOCAL INFILE \'" + source + "\' into table " + MYSQL_TABLE + " fields terminated by ';' \
                #                            lines terminated by '\n' \
                #                            (RecordId, Timestamp, Location);"
                #cur.execute(add_csv_query)
                #db.commit()
                if count == 10:
                    stop = True
                    break
        if stop:
            break
    print 'total: ' + str(ind)
    """
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
        if db:
            print 'Table has been populated.'
            db.close()
    """

if __name__ == '__main__':
    status = main()
    sys.exit(status)
