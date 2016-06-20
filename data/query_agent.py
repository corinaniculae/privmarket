

import cryptdb_manager
import datalib
import mysql_manager


TYPE_1 = """SELECT count(DISTINCT RecordId) FROM generated WHERE
                          Latitude BETWEEN %f AND %f AND
                          Longitude BETWEEN %f AND %f AND
                          Timestamp BETWEEN %d AND %d;
         """
TYPE_2 = """ SELECT count(DISTINCT L.RecordId) FROM generated L
                      INNER JOIN generated R
                      ON L.RecordId = R.RecordId AND L.Timestamp < R.Timestamp
                      WHERE L.Latitude BETWEEN %d AND %d AND
                            L.Longitude BETWEEN %d AND %d AND
                            L.Timestamp BETWEEN %d AND %d AND
                            R.Latitude BETWEEN %d AND %d AND
                            R.Longitude BETWEEN %d AND %d AND
                            R.Timestamp BETWEEN %d AND %d;
        """

class QueryAgent:

    """ Initiates a QueryAgent object.

    Arguments:
        stop_set: A set of tuples (station_id, station_common_name, latitude,
        longitude) to issue queries on.
        cryptdb: A CryptDB manager to execute the queries.
    """
    def __init__(self, stop_set):
        self._stop_set = stop_set
        #self._cryptdb = cryptdb_manager.CryptDBManager()
        #self._mysqldb = mysql_manager.MySQLManager()

    """ Counts the number of travelers in a given rectangle area

    Arguments:
        stop: String ID of the desired tube stop.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_syntactic_count_one_area(self, a1, a2, b1, b2, from_time, to_time):
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_1 % (b1, b2, a1, a2, from_timestamp, to_timestamp)
        return query

    def get_syntactic_count_two_areas(self):
        return

    """ Counts the number of travelers in a given tube stop.

    Arguments:
        stop: String ID of the desired tube stop.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_semantic_count_one_stop(self, stop, from_time, to_time):
        return

    """ Counts the number of travelers between 2 given tube stops.

    Arguments:
        from_stop: String ID of the departure tube stop.
        to_stop: String ID of the arrival tube stop.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_semantic_count_two_stops(
            self, from_stop, to_stop, from_time, to_time):
        return