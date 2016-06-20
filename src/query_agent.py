

import cryptdb_manager
import datalib
import mysql_manager


TYPE_1 = """SELECT count(DISTINCT RecordId) FROM generated_1 WHERE
                          Lat1 BETWEEN %d AND %d AND
                          Lat2 BETWEEN %d AND %d AND
                          Lng1 BETWEEN %d AND %d AND
                          Lng2 BETWEEN %d AND %d AND
                          Timestamp BETWEEN %d AND %d;
         """
CREATE_GENERATED_1 = """CREATE TABLE IF NOT EXISTS generated_1 (
                                RecordId INT(10) NOT NULL,
                                Lat1 INT(10) NOT NULL,
                                Lat2 INT(10) NOT NULL,
                                Lng1 INT(10) NOT NULL,
                                Lng2 INT(10) NOT NULL,
                                Timestamp INT(10) NOT NULL
                                );"""
TYPE_2 = """ SELECT count(DISTINCT L.RecordId) FROM generated_1 L
                      INNER JOIN generated_1 R
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
TYPE_3 = """SELECT count(DISTINCT RecordId) FROM generated_1 WHERE
                          StopID LIKE '%s' AND
                          Timestamp BETWEEN %d AND %d;
         """
TYPE_4 = """ SELECT count(DISTINCT L.RecordId) FROM generated_1 L
              INNER JOIN generated_1 R
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
        self._cryptdb = cryptdb_manager.CryptDBManager()
        self._cryptdb.execute_void_query(CREATE_GENERATED_1)
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
        lat1, lat2 = datalib.prepare_coordinate(b1)
        lat3, lat4 = datalib.prepare_coordinate(b2)
        lng1, lng2 = datalib.prepare_coordinate(a1)
        lng3, lng4 = datalib.prepare_coordinate(a2)
        from_timestamp = datalib.get_timestamp_from_request_string(from_time)
        to_timestamp = datalib.get_timestamp_from_request_string(to_time)
        query = TYPE_1 % (min(lat1, lat3), max(lat1, lat3),
                          min(lat2, lat4), max(lat2, lat4),
                          min(lng1, lng3), max(lng1, lng3),
                          min(lng2, lng4), max(lng2, lng4),
                          from_timestamp, to_timestamp)
        count = self._cryptdb.execute_count_query(query)
        return query + '<br> and result is: ' + str(count)

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
        #return self._cryptdb.execute_count_query(query)

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