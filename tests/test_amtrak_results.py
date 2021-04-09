"""
Test for amtrak results parser.
"""
import os
import json
import pathlib
import unittest
import attr
from amtrakomatic import amtrak_results

TEST_DATA_DIR = os.path.join(pathlib.Path(__file__).parent, 'test_data')

class TestAmtrakResults(unittest.TestCase):
    """
    Tests that amtrak results object can handle our pages.
    """

    maxDiff = None

    def test_amtrak_results(self):
        """
        Tests that amtrak results object can handle our pages.
        """

        def run_example(name):
            expected_result = json.load(open(os.path.join(TEST_DATA_DIR, '%s.json' % name)))
            result_html = os.path.join(TEST_DATA_DIR, '%s_result.html' % name)
            details_html = os.path.join(TEST_DATA_DIR, '%s_details.html' % name)
            result = amtrak_results.AmtrakResult.from_result_and_details(open(result_html),
                    open(details_html))
            self.assertEqual(attr.asdict(result), expected_result)
        run_example("galesburg_denver_06_21_2021_False_1_0")
        run_example("newyork_kansascity_06_21_2021_False_0_0")

    def test_pretty_print(self):
        """
        Tests that amtrak results pretty print can at least run.
        """

        def run_example(name):
            result_html = os.path.join(TEST_DATA_DIR, '%s_result.html' % name)
            details_html = os.path.join(TEST_DATA_DIR, '%s_details.html' % name)
            result = amtrak_results.AmtrakResult.from_result_and_details(open(result_html),
                    open(details_html))
            self.assertTrue(result.pretty_print())
        run_example("galesburg_denver_06_21_2021_False_1_0")

    def test_filter_by_train(self):
        """
        Tests that we can filter by a specific train.
        """

        def run_example(name, train_name, not_train_name):
            expected_result = json.load(open(os.path.join(TEST_DATA_DIR, '%s.json' % name)))
            result_html = os.path.join(TEST_DATA_DIR, '%s_result.html' % name)
            details_html = os.path.join(TEST_DATA_DIR, '%s_details.html' % name)
            result = amtrak_results.AmtrakResult.from_result_and_details(open(result_html),
                    open(details_html))
            results = amtrak_results.AmtrakResults([result])
            result_by_train_name = results.get_by_train_name(train_name)
            # Both my test examples only have one train
            self.assertIsNotNone(result_by_train_name)
            self.assertEqual(attr.asdict(result_by_train_name), expected_result)
            self.assertIsNone(results.get_by_train_name(not_train_name))
        run_example("galesburg_denver_06_21_2021_False_1_0",
                "5 California Zephyr", "9001 Caliphony Zapper")
        run_example("newyork_kansascity_06_21_2021_False_0_0",
                "43 Pennsylvanian", "43 Crazy Pennsylvanian")
        run_example("newyork_kansascity_06_21_2021_False_0_0",
                "29 Capitol Limited", "29 Capitol Unlimited")
        run_example("newyork_kansascity_06_21_2021_False_0_0",
                "3 Southwest Chief", "3 Southwest Champ")

if __name__ == '__main__':
    unittest.main()
