"""
Test for amtrak results parser.
"""
import os
import json
import pathlib
import unittest
import amtrak_results
import format_output

TEST_DATA_DIR = os.path.join(pathlib.Path(__file__).parent, 'test_data')
PAGE1 = os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_1.html')
PAGE2 = os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_2.html')
PAGE3 = os.path.join(TEST_DATA_DIR, 'seattle_chicago_08_24_2019_False_0.html')

PAGE1_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_1.json')))
PAGE2_EXPECTED = json.load(open(
    os.path.join(TEST_DATA_DIR, 'boston_newyork_08_24_2019_False_2.json')))
PAGE3_EXPECTED = json.load(open(
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

        def run_example(html_page):
            format_result = format_output.print_results(amtrak_results.AmtrakResults.from_html(
                open(html_page)).results)
            self.assertTrue(format_result)
        run_example(PAGE3)
        run_example(PAGE1)
        run_example(PAGE2)

if __name__ == '__main__':
    unittest.main()
