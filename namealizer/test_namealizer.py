"""unittest based tests for namealizer"""
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
    first = namealizer.main(seed=seed_to_use, **kwargs)
    second = namealizer.main(seed=seed_to_use, **kwargs)
    return first == second


class TestWordGenerator(unittest.TestCase):
    """Test the WordGenerator class for expected operation"""
    def test_default_initialization(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        self.assertEqual(wg.wordstyle, "lowercase")
        self.assertEqual(wg.separator, " ")
        self.assertIsInstance(wg.seed, int)

    def test_valid_wordstyles(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        # test that these calls work, actual formatting is tested elsewhere
        wg.wordstyle = "lowercase"
        wg[3]

        wg.wordstyle = "uppercase"
        wg[3]

        wg.wordstyle = "mixedcase"
        wg[3]

        wg.wordstyle = "capitalize"
        wg[3]

    def test_invalid_wordstyle(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        wg.wordstyle = "cookies"
        with self.assertRaises(namealizer.InvalidWordStyleError):
            wg[3]

    def test_valid_separators(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        wg.separator = "-"
        returned = wg[3]
        self.assertEqual(len(returned.split(wg.separator)), 3)

    def test_string_access_method(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        returned = wg["abc"].split()
        self.assertEqual(returned[0][0], "a")
        self.assertEqual(returned[1][0], "b")
        self.assertEqual(returned[2][0], "c")

    def test_count_access_method(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        returned = wg[3].split()
        self.assertEqual(len(returned), 3)

    def test_invalid_access_method(self):
        wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")
        with self.assertRaises(TypeError):
            wg[None]


class TestDictionaryImport(unittest.TestCase):
    """
    Test the ability of the tool to import dictionaries. This tests
    also serves as the specification for how dictionaries should be
    formatted. This specification is also documented here.

    Dictionary format (on-disk):
    Dictionaries have a fairly simple format, each word is on it's own
    line. That's it.

    Dictionary format (in memory):
    Within the script dictionaries should be stored as a Python
    dictionary where each key is mapped to a unique first character of
    the word and the value of each of these keys is a Python list of all
    the words that have that first character.
    """
    well_formatted_all = "well-formatted-all.dict"
    words_all = ["able", "boson", "cannon", "dog",
                 "exxon", "foggy", "grand", "housing",
                 "interpreted", "joking", "king",
                 "lemon", "michael", "nixon", "opening",
                 "pricing", "queen", "respected",
                 "stuffing", "travis", "unopened", "very",
                 "washington", "xylo", "yocto", "zebra"]

    well_formatted_sparse = "well-formatted-sparse.dict"
    words_sparse = ["able", "exxon", "washington", "xylophone"]

    def setUp(self):
        # create and import the well formatted full dictionary
        write_dictionary(self.well_formatted_all, self.words_all)
        with open(self.well_formatted_all, "r") as dictionary_file:
            imported = namealizer.import_dictionary(dictionary_file)
            self.well_formatted_all = imported

        # create and import the well formatted sparse dictionary
        write_dictionary(self.well_formatted_sparse, self.words_sparse)
        with open(self.well_formatted_sparse, "r") as dictionary_file:
            imported = namealizer.import_dictionary(dictionary_file)
            self.well_formatted_sparse = imported

    def test_import_well_formatted_all_letters(self):
        # first just make sure it is a dictionary
        self.assertIsInstance(self.well_formatted_all, dict)

        # make sure all of the keys are lists
        for value in self.well_formatted_all.values():
            self.assertIsInstance(value, list)

        # verify that this dictionary has all 26 letters specified
        self.assertEqual(len(self.words_all), len(self.well_formatted_all))

        # check that the first word in a `letter group` got imported in whole
        # this is a test for issue #17
        self.assertEqual(self.words_all[0], self.well_formatted_all["a"][0])

    def test_import_well_formatted_sparse(self):
        # first just make sure it is a dictionary
        self.assertIsInstance(self.well_formatted_all, dict)

        # make sure all of the keys are lists
        for value in self.well_formatted_all.values():
            self.assertIsInstance(value, list)

        # verify that this dictionary has all the letters specified
        len_all = len(self.words_sparse)
        len_sparse = len(self.well_formatted_sparse)
        self.assertEqual(len_all, len_sparse)

        # check that the first word in a `letter group` got imported in whole
        # this is a test for issue #17
        self.assertEqual(self.words_all[0], self.well_formatted_all["a"][0])

    def test_sparse_dict_access_unavailable_letter(self):
        """Tests condition of dict not containing the desired letter"""
        with self.assertRaises(namealizer.NoWordForLetter):
            func = namealizer.get_random_word
            dictionary = self.well_formatted_sparse
            func(dictionary, starting_letter='c')

    def tearDown(self):
        # remove the dictionaries
        for dict_file in glob.glob("*.dict"):
            os.remove(dict_file)


class TestStringFormatter(unittest.TestCase):
    """Verifies string formatting functionality

    This function is the final thing that processes strings before they
    are printed so it takes strings of the format "hello this is a
    string" and turns them into things like "HelloThisIsAString"
    """
    # test all the base wordstyles
    test_string = "all the world"
    separators = ["", "_", "-", "*", "$", "@#$", "monkey"]
    expected_lowercase = ["alltheworld", "all_the_world",
                          "all-the-world", "all*the*world", "all$the$world",
                          "all@#$the@#$world", "allmonkeythemonkeyworld"]
    expected_uppercase = ["ALLTHEWORLD", "ALL_THE_WORLD", "ALL-THE-WORLD",
                          "ALL*THE*WORLD", "ALL$THE$WORLD",
                          "ALL@#$THE@#$WORLD", "ALLmonkeyTHEmonkeyWORLD"]
    expected_capitalize = ["AllTheWorld", "All_The_World",
                           "All-The-World", "All*The*World", "All$The$World",
                           "All@#$The@#$World", "AllmonkeyThemonkeyWorld"]
    expected_mixedcase = ["allTheWorld", "all_The_World",
                          "all-The-World", "all*The*World", "all$The$World",
                          "all@#$The@#$World", "allmonkeyThemonkeyWorld"]

    def test_lowercase(self):
        standard = self.test_string.lower()
        test = namealizer.format_string(self.test_string, "lowercase")
        self.assertEqual(standard, test)

    def test_uppercase(self):
        standard = self.test_string.upper()
        test = namealizer.format_string(self.test_string, "uppercase")
        self.assertEqual(standard, test)

    def test_capitalize(self):
        standard = "All The World"
        test = namealizer.format_string(self.test_string, "capitalize")
        self.assertEqual(standard, test)

    def test_mixedcase(self):
        standard = "all The World"
        test = namealizer.format_string(self.test_string, "mixedcase")
        self.assertEqual(standard, test)

    # test some separators
    def test_separators_lowercase(self):
        for index, separator in enumerate(self.separators):
            standard = self.expected_lowercase[index]
            test = namealizer.format_string(self.test_string,
                                            "lowercase",
                                            separator)
            self.assertEqual(standard, test)

    def test_separators_uppercase(self):
        for index, separator in enumerate(self.separators):
            standard = self.expected_uppercase[index]
            test = namealizer.format_string(self.test_string,
                                            "uppercase",
                                            separator)
            self.assertEqual(standard, test)

    def test_separators_capitalize(self):
        for index, separator in enumerate(self.separators):
            standard = self.expected_capitalize[index]
            test = namealizer.format_string(self.test_string,
                                            "capitalize",
                                            separator)
            self.assertEqual(standard, test)

    def test_separators_mixedcase(self):
        for index, separator in enumerate(self.separators):

            standard = self.expected_mixedcase[index]
            test = namealizer.format_string(self.test_string,
                                            "mixedcase",
                                            separator)
            self.assertEqual(standard, test)

    def test_invalid_wordstyle(self):
        with self.assertRaises(namealizer.InvalidWordStyleError):
            namealizer.format_string("My big pizza", "copy")


class TestCommandLineParameters(unittest.TestCase):
    """Verifies command line parameters are handled correctly
    """

    def test_create_parser(self):
        import argparse
        return_value = namealizer.create_parser()
        self.assertIsInstance(return_value, argparse.Namespace)
        num_args = 6
        self.assertEqual(len(return_value.__dict__), num_args)


class TestActualUsage(unittest.TestCase):
    """Test expected program usage
    """

    def test_no_arguments(self):
        # this test should return a two letter lowercase set
        self.assertEqual(2, len(namealizer.main().split(" ")))

    def test_with_various_count_arguments(self):
        # verify that we can return up to a certain number of words
        for test in range(6):
            result = namealizer.main(count=test)
            if test == 0:
                # this test has to be special cased because splitting
                # on spaces means that even an empty string will have a
                # length of 1.
                self.assertEqual("", result)
            else:
                self.assertEqual(test, len(result.split(" ")))

    def test_with_various_initials(self):
        # check the case where initials is passed in as an empty string
        self.assertEqual("", namealizer.main(initials=""))

        max_number_of_initials = 24
        for test in range(6):
            num_initials = random.randint(1, max_number_of_initials)
            initials = ""
            # pull this many random letters from the alphabet
            for _ in range(num_initials):
                initials += random.choice(string.ascii_letters)

            result = namealizer.main(initials=initials).split(" ")
            self.assertEqual(num_initials, len(result))

    def test_seed_option(self):
        # perform a couple of tests and ensure that given everything
        # else being constant, the same seed produces # the same results

        # test for 0 seed
        self.assertTrue(are_two_seed_runs_equal(0))

        # test for sys.maxsize seed
        self.assertTrue(are_two_seed_runs_equal(sys.maxsize))

        # test for 10 random seeds
        for _ in range(10):
            seed = random.randint(1, sys.maxsize)
            self.assertTrue(are_two_seed_runs_equal(seed))

    def test_count_and_initials_both_defined(self):
        """If count and initials are passed to main, initials are used"""
        initials_to_use = "MHL"
        count_to_use = 4
        result = namealizer.main(count=count_to_use, initials=initials_to_use)
        self.assertTrue(len(result), len(initials_to_use))

    def test_dictionary_not_found(self):
        with self.assertRaises(namealizer.DictionaryNotFoundError):
            namealizer.main(dictionary="your_mom.dict")

if __name__ == '__main__':
    random.seed()
    unittest.main()
