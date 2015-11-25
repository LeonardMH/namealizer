"""
This module is used for creating random collections of words.
"""
import argparse
import sys
import random
import os
import logging


class DictionaryNotFoundError(Exception):
    """
    Exception to be raised when the script fails at importing a dictionary.
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

def format_word_list_lowercase(word_list):
    """
    Given a list of words, this function returns a new list where all of the words are lowercase
    :param word_list: list, a list of words
    :return: list, a list of words formatted in lowercase
    """
    return [word.lower() for word in word_list]


def format_word_list_uppercase(word_list):
    """
    Given a list of words, this function returns a new list where all of the words are uppercase
    :param word_list: list, a list of words
    :return: list, a list of words formatted in uppercase
    """
    return [word.upper() for word in word_list]


def format_word_list_capitalize(word_list):
    """
    Given a list of words, this function returns a new list where all of the words are capitalized
    :param word_list: list, a list of words
    :return: list, a list of words where each word is capitalized
    """
    return [word.capitalize() for word in word_list]


def format_word_list_mixedcase(word_list):
    """
    Given a list of words, this function returns a new list where the words follow mixed case convention.
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


def import_dictionary(opened_file):
    """
    Function used to import the dictionary file into memory
    opened_file should be an already opened dictionary file
    """
    # create the dictionary to hold the words
    dictionary = dict()
    for line in opened_file:
        try:
            dictionary[line[0].lower()].append(line.strip().lower())
        except KeyError:
            dictionary[line[0].lower()] = list(line.strip().lower())

    return dictionary


def main(dictionary='dictionaries/all_en_US.dict', count=None, initials=None,
         seed=None, wordstyle='lowercase', separator=' '):
    # Generate seed for random number generator
    if seed is None:
        random.seed()
        seed = random.randint(0, sys.maxsize)
    random.seed(a=seed)

    # attempt to read in the given dictionary
    try:
        with open(dictionary) as dictionary_file:
            dictionary = import_dictionary(dictionary_file)
    except IOError:
        message = "Could not find the dictionary at {}".format(dictionary)
        raise DictionaryNotFoundError(message)

    # If count and initials are set at the same time let the user know that's a no-no
    if count is not None and initials is not None:
        msg = "--count and --initials are mutually exclusive, using initials"
        logging.info(msg)

    string_to_print = ""
    if initials is not None:
        for letter in initials:
            string_to_print += "{} ".format(get_random_word(dictionary, letter.lower()))

    else:
        if count is not None:
            if count == 0:
                return ""
            ranger = count
        else:
            ranger = 2
        for index in range(ranger):
            string_to_print += "{} ".format(get_random_word(dictionary))

    return format_string(string_to_print.strip(), wordstyle, separator)

def create_parser():
    """Creates the Namespace object to be used by the rest of the tool"""
    program_description = 'Takes user inputs and returns a random collection of words.'
    parser = argparse.ArgumentParser(description=program_description)

    parser.add_argument('-d', '--dictionary',
                        nargs='?',
                        default='dictionaries/all_en_US.dict',
                        help='Specify a non-default word dictionary to use.')
    parser.add_argument('-c', '--count',
                        help='Specify the number of words to return.',
                        type=int)
    parser.add_argument('-i', '--initials',
                        type=str,
                        help='Give a string of letters to form the word list from')
    parser.add_argument('-s', '--seed',
                        help='Specify the seed to use for the random number generator. '
                        'Using the same seed without changing other settings will give '
                        'repeatable results.',
                        type=int)
    parser.add_argument('-ws', '--wordstyle',
                        nargs='?',
                        default='lowercase',
                        type=str,
                        help='Specify how to style the individual words. Default is lowercase.')
    parser.add_argument('-sep', '--separator',
                        nargs='?',
                        default=' ',
                        type=str,
                        help='What to use to separate words. Default is space.')

    return parser.parse_args()

if __name__ == '__main__':
    # Parse the input arguments
    args = create_parser()
    print(main(dictionary=args.dictionary,
               count=args.count,
               initials=args.initials,
               seed=args.seed,
               wordstyle=args.wordstyle,
               separator=args.separator))
