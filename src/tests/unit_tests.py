"""
This module contains 10 unit tests for testing our compute_metrics and analysis modules
"""
import compute_metrics
import unittest
import os.path as osp
import pandas

names = {
            "Twilight Sparkle": "twilight",
            "Applejack": "applejack",
            "Rarity": "rarity",
            "Pinkie Pie": "pinkie",
            "Rainbow Dash": "rainbow",
            "Fluttershy": "fluttershy",
        }
src_file = osp.join(osp.dirname(osp.dirname(osp.dirname(__file__))), "clean_dialog.csv")
#full file
df = pandas.read_csv(src_file)
#first 100 rows
df_100 = pandas.read_csv(src_file, nrows=100)


class MetricsTestCase(unittest.TestCase):
    def test_mentions_sum_to_1(self):
        returned_dict = compute_metrics.calculate_mentions(df, names)
        for pony, other_ponies in returned_dict.items():
            sum = 0
            for fraction in other_ponies.values():
                sum += fraction
            self.assertTrue(0.99 <= sum <= 1.0)

    def test_follow_on_sum_to_1(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df, names)
        for pony, other_ponies in returned_dict.items():
            sum = 0
            for fraction in other_ponies.values():
                sum += fraction
            self.assertTrue(0.99 <= sum <= 1.0)

    def test_verbosity_first_100_rows(self):
        returned_dict = compute_metrics.calculate_verbosity(df_100, names)
        correct_output = {
                    "twilight": float(41)/57,
                    "applejack": float(7)/57,
                    "rarity": float(1)/57,
                    "pinkie": 0,
                    "rainbow": float(8)/57,
                    "fluttershy": 0
                }
        self.assertDictEqual(returned_dict, correct_output)

    def test_mentions_first_100_rows(self):
        returned_dict = compute_metrics.calculate_mentions(df_100, names)
        correct_output = {
                    "twilight": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 1.0,
                            "fluttershy": 0,
                        },
                     "applejack": {
                            "twilight": 1.0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                        },
                     "rarity": {
                            "applejack": 0,
                            "twilight": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                        },
                     "pinkie": {
                            "applejack": 0,
                            "rarity": 0,
                            "twilight": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                        },
                     "rainbow": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "twilight": 1.0,
                            "fluttershy": 0,
                        },
                     "fluttershy": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "twilight": 0,
                        }
                }
        self.assertDictEqual(returned_dict, correct_output)

    def test_follow_on_first_100_rows(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df_100, names)
        correct_output = {
                    "twilight": {
                            "applejack": float(6)/41,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": float(8)/41,
                            "fluttershy": 0,
                            "other": float(27)/41
                        },
                     "applejack": {
                            "twilight": float(5)/7,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": float(2)/7
                        },
                     "rarity": {
                            "applejack": 0,
                            "twilight": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 1.0
                        },
                     "pinkie": {
                            "applejack": 0,
                            "rarity": 0,
                            "twilight": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 0
                        },
                     "rainbow": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "twilight": 1.0,
                            "fluttershy": 0,
                            "other": 0
                        },
                     "fluttershy": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "twilight": 0,
                            "other": 0.
                        }
                }
        self.assertDictEqual(returned_dict, correct_output)
