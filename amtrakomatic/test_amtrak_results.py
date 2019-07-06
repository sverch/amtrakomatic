"""
Test for amtrak results parser.
"""
import os
import json
import pathlib
import unittest
import attr
import amtrak_results

TEST_DATA_DIR = os.path.join(pathlib.Path(__file__).parent, 'test_data')
PAGE1 = os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_1.html')
PAGE2 = os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_2.html')
PAGE3 = os.path.join(TEST_DATA_DIR, 'Boston_vermont_08_18_2019_False_0.html')
PAGE4 = os.path.join(TEST_DATA_DIR, 'elpaso_houston_12_01_2019_False_0.html')
PAGE5 = os.path.join(TEST_DATA_DIR, 'seattle_chicago_08_24_2019_False_0.html')


PAGE1_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_1.json')))
PAGE2_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_2.json')))
PAGE3_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'Boston_vermont_08_18_2019_False_0.json')))
PAGE4_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'elpaso_houston_12_01_2019_False_0.json')))
PAGE5_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'seattle_chicago_08_24_2019_False_0.json')))


class TestAmtrakResults(unittest.TestCase):
    """
    Tests that amtrak results object can handle our pages.
    """

    maxDiff = None

    def test_amtrak_results(self):
        """
        Tests that amtrak results object can handle our pages.
        """

        def run_example(html_page, expected_results):
            results = amtrak_results.AmtrakResults.from_html(open(html_page))
            dict_results = []
            for result in results.results[1:]:
                dict_results.append(attr.asdict(result))
            self.assertEqual(dict_results, expected_results)
        run_example(PAGE1, PAGE1_EXPECTED)
        run_example(PAGE2, PAGE2_EXPECTED)
        run_example(PAGE3, PAGE3_EXPECTED)
        run_example(PAGE4, PAGE4_EXPECTED)

if __name__ == '__main__':
    unittest.main()
