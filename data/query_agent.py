
import tfl_manager


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

    def __init__(self):
        self._tfl_manager = tfl_manager.

    def get_syntactic_count_one_area(self):
        return

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