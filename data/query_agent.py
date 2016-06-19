
import cryptdb_manager
import mysql_manager


TYPE_A = """SELECT count(*) FROM generated WHERE Latitude > %d AND
                                                 Latitude < %d AND
                                                 Longitude > %d AND
                                                 Longitude < %d AND
                                                 Timestamp > %d AND
                                                 Timestamp < %d
         """
TYPE_B = """SELECT count(*) FROM generated WHERE Latitude IS %d AND
                                                 Longitude IS %d AND
                                                 Timestamp > %d AND
                                                 Timestamp < %d
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
    def get_syntactic_count_one_area(self, a1, a2, b1, b2):
        print 'we got: ' + a1 + ' and ' + a2 + ' and ' + b1 + ' aaand ' + b2

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