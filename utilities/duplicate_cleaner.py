"""Removes duplicate entries from dictionaries"""
import sys
import argparse
sys.path.append('../')
import namealizer

def main(dict_path, stat_path):
    dictionary = namealizer.import_dictionary(dict_path)
    sorted_words = []
    updated = {}
    running_total = 0

    statistics = {
        "old": {},
        "new": {}
    }

    print("Removing duplicates")
    for key, item in dictionary.items():
        statistics["old"][key] = len(item)
        updated[key] = sorted(set(item))
        statistics["new"][key] = len(updated[key])
        running_total += len(item) - len(updated[key])
        print(key, len(item), len(updated[key]))

    for key, item in updated.items():
        for word in item:
            sorted_words.append(word)

    print("Beginning sort")
    sorted_words = sorted(sorted_words)
    print("Done sorting")

    # write out the dictionary
    with open(dict_path, "w") as dict_file:
        for word in sorted_words:
            dict_file.write(str(word) + '\n')

    # write out the statistics
    if stat_path is not None:
        with open(stat_path, "w") as stat_file:
            stat_file.write(str(statistics))
    print("Removed a total of: {} words".format(running_total))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dictionary",
                        type=str,
                        help="Dictionary to clean, will be overwritten")
    parser.add_argument("statistics",
                        type=str,
                        nargs="?",
                        default=None,
                        help="Where to put the statistics log")
    args = parser.parse_args()
    main(args.dictionary, args.statistics)
