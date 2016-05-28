#!/usr/bin/python

# Script for setting up a proxy database that simulates the user data
# collection, by using the Ubicomp CSV collection.


import csv
import gzip
import os
import sys

import datalib


START_DIR_POINT = '0'


def main():
    logger = datalib.get_new_logger('setup_data', 'logs/setup_data.log')

    # Curating for the location related records.
    print 'Curating the CSV files...'
    count = 0
    for root, subdirs, files in os.walk('/Volumes/Part1/Data'):
        print root
        if 'indexdb' in root:
            continue
        if root[-40:] < START_DIR_POINT:
            logger.info('%s was explored before.' % root)
            continue
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith('.gz'):
                logger.info('Searching in file: %s' % root)
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
                try:
                    for r in reader:
                        filter_tag = str(r[3])
                        if filter_tag.startswith('phone|celllocation'):
                            writer.writerow((r[0], r[1], r[2], r[3], r[4]))
                except Exception, e:
                    logger.error(str(e))
                    continue
                file_content.close()
                csv_file.close()
    logger.info('Total files curated: %d' % count)
    return 0
   

if __name__ == '__main__':
    status = main()
    sys.exit(status)
