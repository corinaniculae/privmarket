#!/usr/bin/python

import csv
import os
import sys

from data import datalib


def main():
    logger = datalib.get_new_logger('quick_fix', 'quick_fix.log')
    source_path = os.path.join(datalib.CSV_FOLDER,
                               'weekday_paths_1.csv')
    result_path = os.path.join(datalib.CSV_FOLDER_GENERATED,
                               'result_formatted.csv')
    source_file = file(source_path, 'rb')
    result_file = file(result_path, 'wb')
    reader = csv.reader(source_file,
                        delimiter=';',
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(result_file,
                        delimiter=';',
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)

    for r in reader:
        writer.writerow((str(int(r[0]) + 5000),
                        r[1], r[2], r[3], r[4], r[5],
                        r[6], r[7], r[8], r[9], r[10]))
        msg = ('Changed ' + str(r[0]) + ' into ' + str(int(r[0]) + 5000))
        logger.info(msg)

    source_file.close()
    result_file.close()


if __name__ == '__main__':
    status = main()
    sys.exit(status)
