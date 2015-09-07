"""
This module is used for creating random collections of words.
"""

import argparse
import sys
import random
import string
import os

# Define global constants
FORMATS = ['lowercase', 'uppercase', 'capitalize', 'mixedcase', 'camelcase',
           'hyphenate-lowercase',
           'hyphenate-uppercase',
           'hyphenate-capitalize',
           'hyphenate-mixedcase',
           'hyphenate-camelcase',
           'underscore-lowercase',
           'underscore-uppercase',
           'underscore-capitalize',
           'underscore-mixedcase',
           'underscore-camelcase']

# Adds a few compatibility formats that just expand to others
COMPATIBLE_FORMATS = ['hyphenate', 'underscore']
FORMATS += COMPATIBLE_FORMATS


def format_string(string_to_format, desired_format):
    """
    Takes an un-formatted string and returns it in the desired format
    Acceptable formats are defined in the FORMATS list.
    """
    # handle the rare case where desired_format is None
    if desired_format is None:
        desired_format = "lowercase"

    # Handle COMPATIBLE_FORMATS
    if desired_format in COMPATIBLE_FORMATS:
        desired_format += "-lowercase"

    # Split the string into a list of words to make it easier to operate on
    words = string_to_format.split()

    # Do some error checking on desired_format
    desired_format = desired_format.lower()
    good_to_go = False
    if desired_format in FORMATS:
        good_to_go = True

    # Determine and define separator
    if "hyphenate" in desired_format:
        sep = "-"
    elif "underscore" in desired_format:
        sep = "_"
    else:
        sep = " "

    string_to_return = ""
    if good_to_go and 'lowercase' in desired_format:
        index = 0
        for word in words:
            index += 1
            if index == len(words):
                string_to_return += "{}".format(word.lower())
            else:
                string_to_return += "{}{}".format(word.lower(), sep)
        return string_to_return

    elif good_to_go and 'uppercase' in desired_format:
        index = 0

        for word in words:
            index += 1
            if index == len(words):
                string_to_return += "{}".format(word.upper())
            else:
                string_to_return += "{}{}".format(word.upper(), sep)

        return string_to_return

    elif good_to_go and 'capitalize' in desired_format:
        index = 0

        for word in words:
            index += 1
            if index == len(words):
                string_to_return += "{}".format(word.capitalize())
            else:
                string_to_return += "{}{}".format(word.capitalize(), sep)

        return string_to_return

    elif good_to_go and 'mixedcase' in desired_format:
        index = 0
        first_word = True
        if sep == " ":
            sep = ""

        for word in words:
            index += 1
            if first_word:
                if index == len(words):
                    string_to_return += "{}".format(word.lower())
                else:
                    string_to_return += "{}{}".format(word.lower(), sep)
                first_word = False
            else:
                if index == len(words):
                    string_to_return += "{}".format(word.capitalize())
                else:
                    string_to_return += "{}{}".format(word.capitalize(), sep)

        return string_to_return

    elif good_to_go and 'camelcase' in desired_format:
        index = 0
        if sep == " ":
            sep = ""

        for word in words:
            index += 1
            if index == len(words):
                string_to_return += "{}".format(word.capitalize())
            else:
                string_to_return += "{}{}".format(word.capitalize(), sep)

        return string_to_return

    else:
        return string_to_format


def get_random_word(dictionary, starting_letter=None):
    """
    Takes the dictionary to read from and returns a random word
    optionally accepts a starting letter
    """
    if starting_letter is None:
        starting_letter = random.choice(dictionary.keys())

    return random.choice(dictionary[starting_letter])


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


def main(dictionary=None, count=None, initials=None, seed=None, string_format=None, verbose=None):
    # Seed the PRNG
    # Generate seed for random number generator
    if seed is None:
        random.seed()
        seed = random.randint(0, sys.maxsize)
    random.seed(a=seed)

    if verbose:
        print("seed: {}".format(seed))

    # open the file for the word list and read it into a nested list
    # begin by checking for a dictionary location defined from command line option
    if dictionary is None:
        dictionary_location = "dictionaries/all_en_US.dict"
    else:
        dictionary_location = dictionary

    # import the dictionary into a Python dictionary
    with open(dictionary_location) as dictionary_file:
        dictionary = import_dictionary(dictionary_file)

    # Ensure count and initials aren't set at the same time
    if count is not None and initials is not None:
        print("ERROR: --count and --initials are mutually exclusive, pick one")
        return

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

    return format_string(string_to_print.strip(), string_format)


if __name__ == '__main__':
    # Parse the input arguments
    program_description = "Takes user inputs and returns a random collection of words."
    parser = argparse.ArgumentParser(description=program_description)

    parser.add_argument('-d', '--dictionary',
                        help="Specify a non-default word dictionary to use.")
    parser.add_argument('-c', '--count',
                        help="Specify the number of words to return.",
                        type=int)
    parser.add_argument('-i', '--initials',
                        help="Give a string of letters to form the word list from")
    parser.add_argument('-s', '--seed',
                        help="Specify the seed to use for the random number generator.",
                        type=int)
    parser.add_argument('-f', '--format',
                        help="Specify the format of the returned word list.")
    parser.add_argument('-v', '--verbose',
                        help="""Make the program print extra information, can be useful
especially if you would like to know what seed was used
for the random number generator.""",
                        action='store_true')

    args = parser.parse_args()

    print(main(dictionary=args.dictionary, count=args.count, initials=args.initials, seed=args.seed,
               string_format=args.format, verbose=args.verbose))
