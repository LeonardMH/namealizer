import sys
import os
import unittest
import glob
import random
import string
import namealizer


def write_dictionary(file_name, words_to_write):
    with open(file_name, "w") as dictionary_file:
        dictionary_file.write("\n".join(words_to_write))


def are_two_seed_runs_equal(seed_to_use, **kwargs):
    return namealizer.main(seed=seed_to_use, **kwargs) == namealizer.main(seed=seed_to_use, **kwargs)


class TestDictionaryImport(unittest.TestCase):
    """
    Test the ability of the tool to import dictionaries. This tests also serves as the specification for
    how dictionaries should be formatted. This specification is also documented here.

    Dictionary format (on-disk):
    Dictionaries have a fairly simple format, each word is on it's own line. That's it.

    Dictionary format (in memory):
    Within the script dictionaries should be stored as a Python dictionary where each key is mapped to a unique first
    character of the word and the value of each of these keys is a Python list of all the words that have that first
    character.
    """
    well_formatted_all = "well-formatted-all.dict"
    words_for_well_formatted_all = ["able", "boson", "cannon", "dog", "exxon", "foggy", "grand", "housing",
                                    "interpreted", "joking", "king", "lemon", "michael", "nixon", "opening",
                                    "pricing", "queen", "respected", "stuffing", "travis", "unopened", "very",
                                    "washington", "xylophone", "yocto", "zebra"]

    well_formatted_sparse = "well-formatted-sparse.dict"
    words_for_well_formatted_sparse = ["able", "exxon", "washington", "xylophone"]

    def setUp(self):
        # create and import the well formatted full dictionary
        write_dictionary(self.well_formatted_all, self.words_for_well_formatted_all)
        with open(self.well_formatted_all, "r") as dictionary_file:
            self.well_formatted_all = namealizer.import_dictionary(dictionary_file)

        # create and import the well formatted sparse dictionary
        write_dictionary(self.well_formatted_sparse, self.words_for_well_formatted_sparse)
        with open(self.well_formatted_sparse, "r") as dictionary_file:
            self.well_formatted_sparse = namealizer.import_dictionary(dictionary_file)

    def test_import_well_formatted_all_letters(self):
        # first just make sure it is a dictionary
        self.assertIsInstance(self.well_formatted_all, dict)

        # make sure all of the keys are lists
        for value in self.well_formatted_all.values():
            self.assertIsInstance(value, list)

        # verify that this dictionary has all 26 letters specified
        self.assertEqual(len(self.words_for_well_formatted_all), len(self.well_formatted_all))

    def test_import_well_formatted_sparse(self):
        # first just make sure it is a dictionary
        self.assertIsInstance(self.well_formatted_all, dict)

        # make sure all of the keys are lists
        for value in self.well_formatted_all.values():
            self.assertIsInstance(value, list)

        # verify that this dictionary has all the letters specified
        self.assertEqual(len(self.words_for_well_formatted_sparse), len(self.well_formatted_sparse))

    def tearDown(self):
        # remove the dictionaries
        for dict_file in glob.glob("*.dict"):
            os.remove(dict_file)


class TestStringFormatter(unittest.TestCase):
    """
    Verifies that the string formatting functionality works as expected.
    This function is the final thing that processes strings before they are printed so it takes
    strings of the format "hello this is a string" and turns them into things like
    "HelloThisIsAString"
    """
    # test all the base wordstyles
    test_string = "all the world"
    separators = ["", "_", "-", "*", "$", "@#$", "monkey"]
    expected_lowercase = ["alltheworld", "all_the_world", "all-the-world", "all*the*world", "all$the$world",
                          "all@#$the@#$world", "allmonkeythemonkeyworld"]
    expected_uppercase = ["ALLTHEWORLD", "ALL_THE_WORLD", "ALL-THE-WORLD", "ALL*THE*WORLD", "ALL$THE$WORLD",
                          "ALL@#$THE@#$WORLD", "ALLmonkeyTHEmonkeyWORLD"]
    expected_capitalize = ["AllTheWorld", "All_The_World", "All-The-World", "All*The*World", "All$The$World",
                           "All@#$The@#$World", "AllmonkeyThemonkeyWorld"]
    expected_mixedcase = ["allTheWorld", "all_The_World", "all-The-World", "all*The*World", "all$The$World",
                          "all@#$The@#$World", "allmonkeyThemonkeyWorld"]

    def test_lowercase(self):
        self.assertEqual(self.test_string.lower(), namealizer.format_string(self.test_string, "lowercase"))

    def test_uppercase(self):
        self.assertEqual(self.test_string.upper(), namealizer.format_string(self.test_string, "uppercase"))

    def test_capitalize(self):
        self.assertEqual("All The World", namealizer.format_string(self.test_string, "capitalize"))

    def test_mixedcase(self):
        self.assertEqual("all The World", namealizer.format_string(self.test_string, "mixedcase"))

    # test some separators
    def test_separators_lowercase(self):
        for index, separator in enumerate(self.separators):
            self.assertEqual(self.expected_lowercase[index],
                             namealizer.format_string(self.test_string, "lowercase", separator))

    def test_separators_uppercase(self):
        for index, separator in enumerate(self.separators):
            self.assertEqual(self.expected_uppercase[index],
                             namealizer.format_string(self.test_string, "uppercase", separator))

    def test_separators_capitalize(self):
        for index, separator in enumerate(self.separators):
            self.assertEqual(self.expected_capitalize[index],
                             namealizer.format_string(self.test_string, "capitalize", separator))

    def test_separators_mixedcase(self):
        for index, separator in enumerate(self.separators):
            self.assertEqual(self.expected_mixedcase[index],
                             namealizer.format_string(self.test_string, "mixedcase", separator))


class TestRandomWordGrabber(unittest.TestCase):
    """
    Checks the behavior of the function that grabs random words out of the dictionary
    """
    pass


class TestCommandLineParameters(unittest.TestCase):
    """
    Verifies that the script responds to the appropriate command line parameters and responds as expected.
    """
    pass


class TestActualUsage(unittest.TestCase):
    """
    Performs a few tests that use the program as it is actually expected to be used
    """

    def test_no_arguments(self):
        # this test should return a two letter lowercase set
        self.assertEqual(2, len(namealizer.main().split(" ")))

    def test_with_various_count_arguments(self):
        # verify that we can return up to a certain number of words
        for test in range(40):
            if test == 0:
                # this test has to be special cased because splitting on spaces means that even an empty string
                # will have a length of 1.
                self.assertEqual("", namealizer.main(count=test))
            else:
                self.assertEqual(test, len(namealizer.main(count=test).split(" ")))

    def test_with_various_initials(self):
        # check the case where initials is passed in as an empty string
        self.assertEqual("", namealizer.main(initials=""))

        max_number_of_initials = 50
        for test in range(40):
            num_initials = random.randint(1, max_number_of_initials)
            initials = ""
            # pull this many random letters from the alphabet
            for _ in range(num_initials):
                initials += random.choice(string.ascii_letters)

            self.assertEqual(num_initials, len(namealizer.main(initials=initials).split(" ")))

    def test_seed_option(self):
        # perform a couple of tests and ensure that given everything else being constant, the same seed produces
        # the same results

        # test for 0 seed
        self.assertTrue(are_two_seed_runs_equal(0))

        # test for sys.maxsize seed
        self.assertTrue(are_two_seed_runs_equal(sys.maxsize))

        # test for 10 random seeds
        for _ in range(10):
            self.assertTrue(are_two_seed_runs_equal(random.randint(1, sys.maxsize)))

if __name__ == '__main__':
    random.seed()
    unittest.main()
