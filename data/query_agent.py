

import cryptdb_manager
import datalib
import mysql_manager


TYPE_1 = """SELECT count(DISTINCT RecordId) FROM generated WHERE
                          Lat1 BETWEEN %d AND %d AND
                          Lat2 BETWEEN %d AND %d AND
                          Lng1 BETWEEN %d AND %d AND
                          Lng2 BETWEEN %d AND %d AND
                          Timestamp BETWEEN %d AND %d;
         """
TYPE_2 = """ SELECT count(DISTINCT L.RecordId) FROM generated L
                      INNER JOIN generated R
                      ON L.RecordId = R.RecordId AND L.Timestamp < R.Timestamp
                      WHERE L.Lat1 BETWEEN %d AND %d AND
                            L.Lat2 BETWEEN %d AND %d AND
                            L.Lng1 BETWEEN %d AND %d AND
                            L.Lng2 BETWEEN %d AND %d AND
                            L.Timestamp BETWEEN %d AND %d AND
                            R.Lat1 BETWEEN %d AND %d AND
                            R.Lat2 BETWEEN %d AND %d AND
                            R.Lng1 BETWEEN %d AND %d AND
                            R.Lng2 BETWEEN %d AND %d AND
                            R.Timestamp BETWEEN %d AND %d;
         """
TYPE_3 = """SELECT count(DISTINCT RecordId) FROM generated WHERE
                          StopID LIKE '%s' AND
                          Timestamp BETWEEN %d AND %d;
         """
TYPE_4 = """ SELECT count(DISTINCT L.RecordId) FROM generated L
              INNER JOIN generated R
              ON L.RecordId = R.RecordId AND L.Timestamp < R.Timestamp
              WHERE L.StopID LIKE '%s' AND
                    L.Timestamp BETWEEN %d AND %d AND
                    R.StopID LIKE '%s' AND
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
        a1: String of the lower longitude.
        a2: String of the upper longitude.
        b1: String of the lower latitude.
        b2: String of the upper latitude.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_syntactic_count_one_area(self, a1, a2, b1, b2, from_time, to_time):
        lat1, lat2 = datalib.prepare_coordinate(a1)
        lat3, lat4 = datalib.prepare_coordinate(a2)
        lng1, lng2 = datalib.prepare_coordinate(b1)
        lng3, lng4 = datalib.prepare_coordinate(b2)
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_1 % (lat1, lat2, lat3, lat4, lng1, lng2, lng3, lng4, from_timestamp, to_timestamp)
        return query

    def get_syntactic_count_two_areas(self, coord_arr, from_time, to_time):
        pairs = []
        for coord in coord_arr:
            coord_1, coord_2 = datalib.prepare_coordinate(coord)
            pairs.append((coord_1, coord_2))
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_2 % (pairs[0][0], pairs[0][1],
                          pairs[1][0], pairs[1][1],
                          pairs[2][0], pairs[2][1],
                          pairs[3][0], pairs[3][1],
                          from_timestamp, to_timestamp,
                          pairs[4][0], pairs[4][1],
                          pairs[5][0], pairs[5][1],
                          pairs[6][0], pairs[6][1],
                          pairs[7][0], pairs[7][1],
                          from_timestamp, to_timestamp)
        return query

    """ Counts the number of travelers in a given tube stop.

    Arguments:
        stop: String ID of the desired tube stop.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_semantic_count_one_stop(self, stop_id, from_time, to_time):
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_3 % (stop_id, from_timestamp, to_timestamp)
        return query

    """ Counts the number of travelers between 2 given tube stops.

    Arguments:
        from_stop: String ID of the departure tube stop.
        to_stop: String ID of the arrival tube stop.
        from_time: Timestamp of lower bound of the given time interval.
        to_time: Timestamp of upper bound of the given time interval.
    """
    def get_semantic_count_two_stops(self, from_stop_id, to_stop_id, from_time, to_time):
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_4 % (from_stop_id, from_timestamp, to_timestamp, to_stop_id, from_timestamp, to_timestamp)
        return query