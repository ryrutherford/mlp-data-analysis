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
#first row
df_1 = pandas.read_csv(src_file, nrows=1)
#first 100 rows
df_100 = pandas.read_csv(src_file, nrows=100)
#first 200 rows
df_200 = pandas.read_csv(src_file, nrows=200)
#part that includes episode change (last pony from last episode != first pony from next episode)
df_skip_1 = pandas.read_csv(src_file, skiprows=2568, nrows=5, names=["title", "author", "pony", "dialog"])
#part that includes episode change (last pony from last episode == first pony from next episode)
df_skip_2 = pandas.read_csv(src_file, skiprows=1960, nrows=8, names=["title", "author", "pony", "dialog"])



class MetricsTestCase(unittest.TestCase):
    """
    this test is meant to check that the mentions function is working properly by testing whether the values of the dictionary sum to 1
    """
    def test_mentions_sum_to_1(self):
        returned_dict = compute_metrics.calculate_mentions(df, names)
        for pony, other_ponies in returned_dict.items():
            sum = 0
            for fraction in other_ponies.values():
                sum += fraction
            self.assertTrue(0.99 <= sum <= 1.01)

    """
    this test is meant to check that the follow on function is working properly by testing whether the values of the dictionary sum to 1
    """
    def test_follow_on_sum_to_1(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df, names)
        for pony, other_ponies in returned_dict.items():
            sum = 0
            for fraction in other_ponies.values():
                sum += fraction
            self.assertTrue(0.99 <= sum <= 1.01)


    """
    this test is meant to check if the verbosity function calculates the right output when we know what the output is supposed to be
    """
    def test_verbosity_first_100_rows(self):
        returned_dict = compute_metrics.calculate_verbosity(df_100, names)
        #there are 86 unique instances of dialog in the first 100 rows, 40 belong to twilight, 7 to aj, 1 to rarity, 8 to rainbow
        correct_output = {
                    "twilight": 40/86,
                    "applejack": 7/86,
                    "rarity": 1/86,
                    "pinkie": 0,
                    "rainbow": 8/86,
                    "fluttershy": 0
                }
        self.assertDictEqual(returned_dict, correct_output)

    """
    this test is meant to see if the mentions function calculates the right output
    when we know what the output is supposed to be
    it also helps us test how the function behaves when a pony isnt mentioned
    """
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

    """
    this test is meant to see if the follow on comments function is working when we
    know the correct output.
    this test also helps us see if values of 0 are entered when a pony has no follow on comments
    """
    def test_follow_on_first_100_rows(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df_100, names)
        correct_output = {
                    "twilight": {
                            "applejack": 6/40,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 8/40,
                            "fluttershy": 0,
                            "other": 26/40
                        },
                     "applejack": {
                            "twilight": 5/7,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 2/7
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

    """
    this will test the correct number of mentions for the first 200 rows
    this test is meant to compare the results computed for more input
    i hand counted the correct ouput to make sure the function was working
    """
    def test_mentions_first_200_rows(self):
        returned_dict = compute_metrics.calculate_mentions(df_200, names)
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
                            "twilight": 1.0,
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


    """
    this will test for the correct amount of follow on comments in the first 200 rows
    I wanted to test this to make sure it still worked with larger input and
    changing episodes.
    I hand counted the correct amounts
    """
    def test_follow_on_first_200_rows(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df_200, names)
        correct_output = {
                    "twilight": {
                            "applejack": 7/67,
                            "rarity": 7/67,
                            "pinkie": 4/67,
                            "rainbow": 8/67,
                            "fluttershy": 5/67,
                            "other": 36/67
                        },
                     "applejack": {
                            "twilight": 5/11,
                            "rarity": 0,
                            "pinkie": 1/11,
                            "rainbow": 2/11,
                            "fluttershy": 0,
                            "other": 3/11
                        },
                     "rarity": {
                            "applejack": 0,
                            "twilight": 5/8,
                            "pinkie": 1/8,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 2/8
                        },
                     "pinkie": {
                            "applejack": 1/9,
                            "rarity": 0,
                            "twilight": 3/9,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 5/9
                        },
                     "rainbow": {
                            "applejack": 1/11,
                            "rarity": 0,
                            "pinkie": 0,
                            "twilight": 9/11,
                            "fluttershy": 0,
                            "other": 1/11
                        },
                     "fluttershy": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "twilight": 5/11,
                            "other": 6/11
                        }
                }
        self.assertDictEqual(returned_dict, correct_output)


    """
    this test will make sure we are collecting the right non dict words
    it will also make sure that when a pony has less than 5 non dict words it will
    still display the non dict words it has if any
    """
    def test_non_dictionary_words_first_100_rows(self):
        returned_dict = compute_metrics.find_non_dict_words(df_100, names)
        correct_output = {
                    "twilight": ["Equestria", "ve", "Hmm", "Spi", "Nng"],
                    "applejack": ["makin", "Yeehaw", "everypony", "attem"],
                    "rarity": [],
                    "pinkie": [],
                    "rainbow": ["Lemme", "Wonderbolts", "Ponyville"],
                    "fluttershy": [],
                }
        self.assertDictEqual(returned_dict, correct_output)

    """
    this test is meant to check that when no ponies have any lines the values for all ponies 
    in the verbosity dict is 0
    """
    def test_verbosity_is_0(self):
        returned_dict = compute_metrics.calculate_verbosity(df_1, names)
        correct_output = {
                    "twilight": 0,
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 0,
                    "rainbow": 0,
                    "fluttershy": 0,
                }
        self.assertDictEqual(returned_dict, correct_output)

    """
    this test will make sure that when there is an episode change the last line from the previous episode
    doesn't affect the first line from the new episode
    """

    def test_episode_change_follow_on(self):
        returned_dict = compute_metrics.calculate_follow_on_comments(df_skip_1, names)
        correct_output = {
                    "twilight": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 0
                        },
                     "applejack": {
                            "twilight": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 0
                        },
                     "rarity": {
                            "applejack": 0,
                            "twilight": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "fluttershy": 0,
                            "other": 0
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
                            "applejack": 1.0,
                            "rarity": 0,
                            "pinkie": 0,
                            "twilight": 0,
                            "fluttershy": 0,
                            "other": 0
                        },
                     "fluttershy": {
                            "applejack": 0,
                            "rarity": 0,
                            "pinkie": 0,
                            "rainbow": 0,
                            "twilight": 0,
                            "other": 0
                        }
                }
        self.assertDictEqual(returned_dict, correct_output)

    """
    this test will ensure that the verbosity function isn't undercounting by not counting two dialog lines
    when a pony has the last line in the last episode and the first line in the next episode
    """
    def test_episode_change_verbosity(self):
        returned_dict = compute_metrics.calculate_verbosity(df_skip_2, names)
        correct_output = {
                    "twilight": 4/6,
                    "applejack": 0,
                    "rarity": 0,
                    "pinkie": 1/6,
                    "rainbow": 0,
                    "fluttershy": 0,
                }
        self.assertDictEqual(returned_dict, correct_output)


