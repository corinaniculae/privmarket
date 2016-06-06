


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

    def __init__(self, type):
        self._type = type