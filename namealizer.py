# Imports
import argparse
import sys
import os
import random
import string

# Define global constants
FORMATS = ['lowercase', 'uppercase', 'capitalized', 'mixedcase', 'camelcase',
            'hyphenated-lowercase', 'hyphenated-uppercase', 'hyphenated-capitalized',
            'hyphenated-mixedcase', 'hyphenated-camelcase', 'underscored-lowercase',
            'underscored-uppercase', 'underscored-capitalized', 
            'underscored-mixedcase', 'underscored-camelcase']

# Adds a few compatibility formats that just expand to others
COMPAT_FORMATS = ['hyphenated', 'underscored']
FORMATS += COMPAT_FORMATS

def format_string(string_to_format, desired_format):
    '''
    Takes an unformatted string and returns it in the desired format
    Acceptable formats are defined in the FORMATS list.
    '''
    
    # Handle COMPAT_FORMATS
    if desired_format in COMPAT_FORMATS: desired_format += "-lowercase"

    # Split the string into a list of words to make it easier to operate on
    words = string_to_format.split()

    # Do some error checking on desired_format
    desired_format = desired_format.lower()
    good_to_go = False
    if desired_format in FORMATS:
        good_to_go = True
   
    # Determine and define separator
    if "hyphenated" in desired_format: sep = "-"
    elif "underscored" in desired_format: sep = "_"
    else: sep = " "
 
    string_to_return = ""
    if good_to_go == True and 'lowercase' in desired_format:
        index = 0
        for word in words:
            index += 1
            if index == len(words): string_to_return += "{}".format(word.lower())
            else: string_to_return += "{}{}".format(word.lower(), sep)
        return string_to_return

    elif good_to_go == True and 'uppercase' in desired_format:
        index = 0
        for word in words:
            index += 1
            if index == len(words): string_to_return += "{}".format(word.upper())
            else: string_to_return += "{}{}".format(word.upper(), sep)
        return string_to_return

    elif good_to_go == True and 'capitalized' in desired_format:
        index = 0
        for word in words:
            index += 1
            if index == len(words): string_to_return += "{}".format(word.capitalize())
            else: string_to_return += "{}{}".format(word.capitalize(), sep)
        return string_to_return

    elif good_to_go == True and 'mixedcase' in desired_format:
        index = 0
        first_word = True
        if sep == " ": sep = ""
        for word in words:
            index += 1
            if first_word: 
                if index == len(words): string_to_return += "{}".format(word.lower())
                else: string_to_return += "{}{}".format(word.lower(), sep)
                first_word = False
            else:
                if index == len(words): string_to_return += "{}".format(word.capitalize())
                else: string_to_return += "{}{}".format(word.capitalize(), sep)
        return string_to_return
    
    elif good_to_go == True and 'camelcase' in desired_format:
        index = 0
        if sep == " ": sep = ""
        for word in words:
            index += 1
            if index == len(words): string_to_return += "{}".format(word.capitalize())
            else: string_to_return += "{}{}".format(word.capitalize(), sep)
        return string_to_return

    else: return string_to_format


    # Now get a random number that fits in this letter group
    return dictionary[letter_group][0]
        
def get_random_word(dictionary, starting_letter = None):
    '''
    Takes the dictionary to read from and returns a random word
    optionally accepts a starting letter
    '''
    if starting_letter == None:
        starting_letter = random.randint(0, NUM_LETTER_GROUPS)
    else:
        starting_letter = starting_letter.lower()
        index = 0
        for letter in string.ascii_lowercase:
            if letter == starting_letter: 
                starting_letter = index
                break
            else: index += 1

    word_index = random.randint(0, len(dictionary[starting_letter]) - 1)
    return dictionary[starting_letter][word_index]

def import_dictionary(opened_file):
    '''
    Function used to import the dictionary file into memory
    opened_file should be an already opened dictionary file
    '''
    # Create the dictionary to hold the words
    dictionary = []
    
    index = -1 
    for line in opened_file:
        if line is "\n": 
            dictionary.append([])
            index += 1
        else: 
            dictionary[index].append(line.rstrip())

    return dictionary

def main():
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
    
    # Define special variables for use in main
    # Seed the PRNG
    seed = None
    if args.seed == None:
        # Generate seed for random number generator
        random.seed()
        seed = random.randint(0, sys.maxsize)
        random.seed(a = seed)
    else:
        random.seed(a = args.seed)
        seed = args.seed
    if args.verbose: print("Seed used: {}".format(seed)) 

    # Open the file for the word list and read it into a nested list
    # Begin by checking for a dictionary location defined from command line option
    if args.dictionary != None:
        # First verify that the file exists
        is_file = os.path.isfile(args.dictionary)
        dictionary_location = args.dictionary
    else:
        dictionary_location = "/usr/share/namealizer/all_en_US.dict"

    f = open(dictionary_location)
    try:
        dictionary = import_dictionary(f)    
    finally:
        f.close()

    # Redefine NUM_LETTER_GROUPS based on current dictionary size
    global NUM_LETTER_GROUPS
    NUM_LETTER_GROUPS = len(dictionary)

    # Ensure args.count and args.initials aren't set at the same time
    if args.count != None and args.initials != None:
            print("ERROR: --count and --initials are mutually exclusive, pick one")
            return

    string_to_print = ""
    if args.count != None:
        for index in range(args.count):
            string_to_print += "{} ".format(get_random_word(dictionary))

    elif args.initials != None:
        for letter in args.initials:
            string_to_print += "{} ".format(get_random_word(dictionary, letter.lower()))

    else:
        string_to_print = "{} {}".format(get_random_word(dictionary), get_random_word(dictionary))

    if args.format != None:
        string_to_print = format_string(string_to_print, args.format)

    print(string_to_print)

if __name__ == '__main__':
	main()
