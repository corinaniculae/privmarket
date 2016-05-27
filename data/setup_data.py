#!/usr/bin/python

# Script for setting up a proxy database that simulates the user data
# collection, by using the Ubicomp CSV collection.


import csv
import gzip
import os
import urllib2
import shutil
import sys
import time

MYSQL_DATABASE = 'priv_proxy'
MYSQL_TABLE = 'collected'
                

def main():
    # Curating for the location related records.
    print 'Curating the CSV files...'
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
                reader = csv.reader(file_content,
                                    delimiter=';',
                                    quotechar="'",
                                    quoting=csv.QUOTE_ALL)
                write_file_name = ('/Volumes/Part2/Curated2/' +
                                   root[-40:] +
                                   '.csv')
                csv_file = open(write_file_name, 'wb')
                writer = csv.writer(csv_file,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for r in reader:
                    filter_tag = str(r[3]) 
                    if (filter_tag.startswith('phone|celllocation') or
                            filter_tag.startswith('location')):
                        writer.writerow((r[1],r[2],r[3], r[4]))
                        
                file_content.close()
                csv_file.close()
                time.sleep(60 * 5)
    print 'total: ' + str(ind)
   

if __name__ == '__main__':
    status = main()
    sys.exit(status)
