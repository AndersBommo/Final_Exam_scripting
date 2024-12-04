from geopy.distance import geodesic

class DistanceCalculator:
    def calculate_distance(self, loc1, loc2):
        """
        Calculate the distance between two points using geodesic distance.
        :param loc1: Tuple (latitude, longitude)
        :param loc2: Tuple (latitude, longitude)
        :return: Distance in km
        """
        return geodesic(loc1, loc2).km
