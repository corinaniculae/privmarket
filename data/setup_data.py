#!/usr/bin/python

# Script for setting up a proxy database that simulates the user data
# collection, by using the Ubicomp CSV collection.


import csv
import gzip
import os
import sys
import time

import datalib


def main():
    logger = datalib.get_new_logger('setup_data', 'logs/setup_data.log')

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
                logger.info('Searching in file: %s' % file_path)
                dest_file = '/Volumes/Part2/Curated/%s.csv' % root[-40:]
                if os.path.isfile(dest_file):
                    logger.info('File %s was curated before.' % filename)
                    continue
                count += 1
                file_content = gzip.open(file_path, 'rb')
                reader = csv.reader(file_content,
                                    delimiter=';',
                                    quotechar="'",
                                    quoting=csv.QUOTE_ALL)
                csv_file = open(dest_file, 'wb')
                writer = csv.writer(csv_file,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for r in reader:
                    filter_tag = str(r[3]) 
                    if (filter_tag.startswith('phone|celllocation') or
                            filter_tag.startswith('location')):
                        writer.writerow(r[1],r[2],r[3], r[4])
                        
                file_content.close()
                csv_file.close()
                time.sleep(60)
    logger.info('Total files curated: %d' % count)
    return 0
   

if __name__ == '__main__':
    status = main()
    sys.exit(status)
