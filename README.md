# namealizer - A random name generator

The goal of namealizer is simple, to create a straightforward method for creating random collections of words.

The apparent usefulness of such a tool isn't immediately obvious but there are situations in which this ability could actually be useful. If nothing else it is always entertaining to see a few random words thrown together.

**If you are using namealizer feel free to let me know what for!**

The dictionary included with namealizer was compiled from various sources with the main dictionary being the en\_US dictionary used in Hunspell. The dictionary was mirrored on sourceforge at [Kevin's Word List Page](http://wordlist.sourceforge.net").

It is my intent to compile a few alternate dictionaries as well. As well as creating a parser tool to easily reformat arbitrary word lists.

## Examples

The concept of namealizer is fairly straightforward, in the simplest use case namealizer just returns two random words from the dictionary.

	Input: namealizer
	Output: forest kite

### Long-format options

Adding a little bit of complexity, the user can supply a number, this is the number of words that will be returned by namealizer. Once again, each randomly selected from the dictionary.

	Input: namealizer --count=5
	Output: red barracuda car showstopper pillow

For more advanced usage the user can input initials and namealizer will return a collection of words in order of the initials. In addition, the words can be returned in various formats.

	Input: namealizer --initials=CXM --seed=3008
	Output: crossing xylophone maid
	
	Input: namealizer --initials=CXM --seed=3008 --format=camelcase
	Output CrossingXylophoneMaid
	
	Input: namealizer --initials=CXM --seed=3008 --format=mixedcase
	Output crossingXylophoneMaid

	Input: namealizer --initials=CXM --seed=3008 --format=hyphenated
	Output: crossing-xylophone-maid

	Input: namealizer --initials=CXM --seed=3008 --format=underscored
	Output: crossing_xylophone_maid

### Short-format options

Namealizer also support the classic-style unix short commandline options. For a full list of the commands just run `namealizer --help` or `namealizer -h`.

In general the commands are just the first letter of the long option and do not require the equals ("=") sign. Using the same commands as above:

	namealizer -c5
	namealizer -iCXM -s3008
	namealizer -iCXM -s3008 -fcamelcase
	namealizer -iCXM -s3008 -fmixedcase
	namealizer -iCXM -s3008 -fhyphenated
	namealizer -iCXM -s3008 -funderscored

The outputs are the same as shown above in [Long-format options](#long-format-options)

### Command line options

A guaranteed up-to-date list of available command line options can always be determined by `namealizer -h`. The more useful options are described below.

+ `--count` - The count option allows you to specify the number of words returned by namealizer. Count can be combined with any of the other options.
+ `--seed` - The seed option give you the ability to specify the seed number used for the psuedo-random number generator. This allows you to get the same words out of namealizer between runs. Though I'm not sure if this works from one machine to another.
+ `--verbose` - The verbose option is just a command line switch (that is, it doesn't take any further options). This command causes namealizer to spit out information that the user may find valuable. Most interestingly perhaps, it prints out the seed used for generating the current word collection.
+ `--initials` - Allows the user to specify initials to use for generating the words. This just takes each letter and uses it as the starting letter for each word.
+ `--format` - Lets the user control the format of the returned words. This option is documented more thoroughly below in [Formatting options](#formatting-options).

### Formatting options

The formatting options allowed by the `--format` option are listed and briefly described below.

+ `hyphenated` - This is actually just a compatibility wrapper which maps directly to `hyphenated-lowercase`. See `hyphenated-lowercase` for more information.
+ `underscored` - This is also a compatibility wrapper mapping directl to `underscored-lowercase`, see `underscored-lowercase` for more information.
+ `lowercase` - The lowercase option is the default format for namealizer and returns the words in lowercase format separated by spaces. E.g. `rat tree banana`
+ `uppercase` - Uppercase option returns the words in completely uppercase and separated by spaces. E.g. `RAT TREE BANANA`
+ `capitalized` - Returns each word capitalized and separated by spaces. E.g. `Rat Tree Banana`
+ `mixedcase` - This option returns the words in mixed case format with no separation by default. E.g. `ratTreeBanana`. This is a common naming convention for programmers.
+ `camelcase` - The camelcase option is very similar to mixed case except the first word is also capitalized. E.g. `RatTreeBanana`

In addition to these base formats, each command listed above can be prefixed with `hyphenated-` or `underscored-` to change the word separator to a hyphen or an underscore, respectively.

A few examples would be:
	
	namealizer --format=hyphenated-camelcase
	namealizer --format=underscored-mixedcase
	namealizer --format=hyphenated-uppercase
