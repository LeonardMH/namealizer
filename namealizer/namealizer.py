"""Create and format random collections of words"""
from pkg_resources import resource_filename
import argparse
import sys
import random
import os
import logging


class DictionaryNotFoundError(Exception):
    """
    Exception to be raised when the script fails at importing a dictionary
    """
    pass


class InvalidWordStyleError(Exception):
    """
    Exception to raise when the user passes in an invalid wordstyle
    """
    pass


class NoWordForLetter(Exception):
    """
    Raised when dictionary has no word beginning with requested letter
    """
    pass


class WordGenerator(object):
    """Main word generation class"""
    def __init__(self,
                 dictionary="dictionaries/all_en_US.dict",
                 wordstyle="lowercase", separator=" ",
                 seed=None):
        """Initializer for WordGenerator

        :param dictionary Any valid .dict formatted dictionary
        :param wordstyle Any allowed `wordstyle` format specification
        :param separator What character (or word) to separate words with
        :param seed Seed to use for the PRNG

        :raises DictionaryNotFoundError if the `dictionary` parameter can't
                be found on disk
        :raises InvalidWordStyleError if user attempts to retrieve a word
                when `self.wordstyle` is set to an invalid value
        :raises NoWordForLetter when the user attempts to reteive a word
                where the starting letter given does not exist in the
                dictionary
        """
        if dictionary == "dictionaries/all_en_US.dict":
            try:
                dictionary = resource_filename('namealizer', dictionary)
            except ImportError:
                pass

        self.dictionary = import_dictionary(dictionary)
        self.wordstyle = wordstyle
        self.separator = separator
        self.seed = generate_seed(seed)

    def __getitem__(self, key):
        if isinstance(key, str):
            return format_string(string_for_initials(self.dictionary, key),
                                 wordstyle=self.wordstyle,
                                 separator=self.separator)
        elif isinstance(key, int):
            return format_string(string_for_count(self.dictionary, key),
                                 wordstyle=self.wordstyle,
                                 separator=self.separator)
        else:
            raise TypeError


def format_word_list_lowercase(word_list):
    """
    Given a list of words, this function returns a new list where all of
    the words are lowercase

    :param word_list: list, a list of words
    :return: list, a list of words formatted in lowercase
    """
    return [word.lower() for word in word_list]


def format_word_list_uppercase(word_list):
    """
    Given a list of words, this function returns a new list where all of
    the words are uppercase

    :param word_list: list, a list of words
    :return: list, a list of words formatted in uppercase
    """
    return [word.upper() for word in word_list]


def format_word_list_capitalize(word_list):
    """
    Given a list of words, this function returns a new list where all of
    the words are capitalized

    :param word_list: list, a list of words
    :return: list, a list of words where each word is capitalized
    """
    return [word.capitalize() for word in word_list]


def format_word_list_mixedcase(word_list):
    """
    Given a list of words, this function returns a new list where the
    words follow mixed case convention.

    As a reminder this is mixedCase.

    :param word_list: list, a list of words
    :return: list, a list of words where the words are mixed case
    """
    to_return, first_word = list(), True
    for word in word_list:
        if first_word:
            to_return.append(word.lower())
            first_word = False
        else:
            to_return.append(word.capitalize())
    return to_return


def format_string(string_to_format, wordstyle="lowercase", separator=" "):
    """
    Takes an un-formatted string and returns it in the desired format
    Acceptable formats are defined in the function_map dictionary.
    """
    # first split the string up into its constituent words
    words = string_to_format.split(" ")

    # format the individual words
    function_map = {
        "lowercase": format_word_list_lowercase,
        "uppercase": format_word_list_uppercase,
        "capitalize": format_word_list_capitalize,
        "mixedcase": format_word_list_mixedcase
    }

    try:
        words = function_map[wordstyle](words)
    except KeyError:
        msg = "Passed in an invalid wordstyle, allowed styles are {}"
        raise InvalidWordStyleError(msg.format(function_map.keys()))

    # now add in the separator and return
    return str(separator).join(words)


def get_random_word(dictionary, starting_letter=None):
    """
    Takes the dictionary to read from and returns a random word
    optionally accepts a starting letter
    """
    if starting_letter is None:
        starting_letter = random.choice(list(dictionary.keys()))

    try:
        to_return = random.choice(dictionary[starting_letter])
    except KeyError:
        msg = "Dictionary does not contain a word starting with '{}'"
        raise NoWordForLetter(msg.format(starting_letter))

    return to_return


def import_dictionary(dictionary):
    """
    Function used to import the dictionary file into memory
    opened_file should be an already opened dictionary file

    :raises DictionaryNotFoundError if dictionary can't be loaded
    """
    def load_into_dictionary(dictionary_file):
        """create the dictionary to hold the words"""
        to_return = dict()
        for line in dictionary_file:
            try:
                to_return[line[0].lower()].append(line.strip().lower())
            except KeyError:
                to_return[line[0].lower()] = [line.strip().lower()]

        return to_return

    try:
        with open(dictionary) as dictionary_file:
            to_return = load_into_dictionary(dictionary_file)

    except TypeError:
        to_return = load_into_dictionary(dictionary)

    except IOError:
        message = "Could not find the dictionary at {}".format(dictionary)
        raise DictionaryNotFoundError(message)

    return to_return


def string_for_initials(dictionary, initials):
    """Create a random string of words of len(initials)"""
    string_to_print = ""
    for letter in initials:
        word = get_random_word(dictionary, letter.lower())
        string_to_print += "{} ".format(word)

    return string_to_print.strip()


def string_for_count(dictionary, count):
    """Create a random string of N=`count` words"""
    string_to_print = ""
    if count is not None:
        if count == 0:
            return ""
        ranger = count
    else:
        ranger = 2
    for index in range(ranger):
        string_to_print += "{} ".format(get_random_word(dictionary))

    return string_to_print.strip()


def generate_seed(seed):
    """Generate seed for random number generator"""
    if seed is None:
        random.seed()
        seed = random.randint(0, sys.maxsize)
    random.seed(a=seed)

    return seed


def main(dictionary='dictionaries/all_en_US.dict', count=None, initials=None,
         seed=None, wordstyle='lowercase', separator=' '):
    """Main processing function for namealizer"""
    generate_seed(seed)

    # attempt to read in the given dictionary
    dictionary = import_dictionary(dictionary)

    # if count and initials are both set, let the user know what's up
    if count and initials:
        msg = "--count and --initials are mutually exclusive, using initials"
        logging.info(msg)

    if initials is not None:
        string_to_print = string_for_initials(dictionary, initials)
    else:
        string_to_print = string_for_count(dictionary, count)

    return format_string(string_to_print, wordstyle, separator)


def create_parser():
    """Creates the Namespace object to be used by the rest of the tool"""
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-d', '--dictionary',
                        nargs='?',
                        default='dictionaries/all_en_US.dict',
                        help='Specify a non-default word dictionary to use.')
    parser.add_argument('-c', '--count',
                        help='Specify the number of words to return.',
                        type=int)
    parser.add_argument('-i', '--initials',
                        type=str,
                        help='String of letters used to form the word list')
    parser.add_argument('-s', '--seed',
                        help='Specify the seed to use for the random number '
                        'generator. Using the same seed without changing '
                        'other settings will give repeatable results.',
                        type=int)
    parser.add_argument('-ws', '--wordstyle',
                        nargs='?',
                        default='lowercase',
                        type=str,
                        help='Specify how to style the individual words. '
                        'Default is lowercase.')
    parser.add_argument('-sep', '--separator',
                        nargs='?',
                        default=' ',
                        type=str,
                        help='How to separate words. Default is space.')

    return parser.parse_args()
