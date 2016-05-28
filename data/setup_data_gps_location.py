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
    logger = datalib.get_new_logger('setup_gps_data', 'logs/setup_gps_data.log')

    # Increase the size of the csv's fields to be read.
    csv.field_size_limit(sys.maxsize)

    # Curate the CSV files.
    print 'Curating the CSV files...'
    count = 0
    for root, subdirs, files in os.walk('/Volumes/Part1/Data'):
        if 'indexdb' in root:
            continue
        logger.info('root is: ' + root[-40:])

        if root[-40:] < '0f894e0b6eb6b84ce84517399d04e17af8853564':
            logger.info('%s was explored before.' % root)
            continue
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith('.gz'):
                logger.info('Searching in file: %s' % file_path)
                count += 1
                file_content = gzip.open(file_path, 'rb')
                reader = csv.reader(file_content,
                                    delimiter=';',
                                    quotechar="'",
                                    quoting=csv.QUOTE_ALL)
                write_file_name = '/Volumes/Part2/GPSCurated/all_loc.csv'
                csv_file = open(write_file_name, 'a')
                writer = csv.writer(csv_file,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                try:
                    for r in reader:
                        filter_tag = str(r[3])
                        if filter_tag.startswith('location'):
                            logger.info('Found one in file: %s' % filename)
                            writer.writerow((r[1], r[2], r[3], r[4]))
                except Exception:
                    continue
                file_content.close()
                csv_file.close()
                time.sleep(60)
    logger.info('Total files curated: %d' % count)
    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
