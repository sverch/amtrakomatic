"""
Test for fuzzy matcher library.
"""
import unittest
import collections
import fuzzy_match

class TestStationMatch(unittest.TestCase):
    """
    Tests that our fuzzy matcher gets the right stations.
    """

    def test_station_match(self):
        """
        Tests that our fuzzy matcher gets the right stations.
        """

        TestExample = collections.namedtuple('TestExample', 'input expected_result')

        test_examples = [
            TestExample("New York", ('New York (Penn Station), New York', 'NYP')),
            TestExample("Boston", ('Boston (South Station), Massachusetts', 'BOS')),
            TestExample("Vermont", ('Essex Junction, Vermont', 'ESX')),
            TestExample("Harrisburg", ('Harrisburg, Pennsylvania', 'HAR')),
            TestExample("Kansas City", ('Kansas City, Missouri', 'KCY')),
            TestExample("Denver", ('Denver, Colorado', 'DEN')),
            TestExample("Salt Lake City", ('Salt Lake City, Utah', 'SLC')),
            TestExample("Sacramento", ('Sacramento, California', 'SAC')),
            TestExample("Seattle", ('Seattle (Amtrak), Washington', 'SEA')),
            TestExample("Chico", ('Chico, California', 'CIC')),
            TestExample("San Jose", ('San Jose, California', 'SJC')),
            TestExample("Los Angeles", ('Los Angeles, California', 'LAX')),
            TestExample("New Mexico", ('Albuquerque, New Mexico', 'ABQ')),
            TestExample("Houston", ('Houston, Texas', 'HOS')),
            TestExample("Washington DC", ('Washington, District of Columbia', 'WAS')),
            TestExample("New York", ('New York (Penn Station), New York', 'NYP')),
                ]
        for test_example in test_examples:
            print("\"%s\", %s" % (test_example.input, fuzzy_match.station(test_example.input)))
            self.assertEqual(fuzzy_match.station(test_example.input), test_example.expected_result)

if __name__ == '__main__':
    unittest.main()
