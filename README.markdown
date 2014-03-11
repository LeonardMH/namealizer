# namealizer - A random name generator

The goal of namealizer is simple, to create a straightforward method for creating random collections of words.

The apparent usefulness of such a tool isn't immediately obvious but there are situations in which this ability could actually be useful. If nothing else it is always entertaining to see a few random words thrown together.

**If you are using namealizer feel free to let me know what for!**

The dictionary included with namealizer was compiled from various sources with the main dictionary being the en\_US dictionary used in Hunspell. The dictionary was mirrored on sourceforge at [Kevin's Word List Page](http://wordlist.sourceforge.net").

It is my intent to compile a few alternate dictionaries as well. As well as creating a parser tool to easily reformat arbitrary word lists.

## Examples

The concept of namealizer is a bit difficult to understand but its purpose is fairly straightforward.

In the simplest use case namealizer just returns two random words from the dictionary.

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

Namealizer also support the classic style unit short commandling options. For a full list of the commands just run '''namealizer --help''' or '''namealizer -h'''.

In general the commands are just the first letter of the long option and do not require the equals ("=") sign. Using the same commands as above:

	namealizer -c5
	namealizer -iCXM -s3008
	namealizer -iCXM -s3008 -fcamelcase
	namealizer -iCXM -s3008 -fmixedcase
	namealizer -iCXM -s3008 -fhyphenated
	namealizer -iCXM -s3008 -funderscored

The outputs are the same as shown above in [Long-format options](#long-format-options)

## Documentation

Coming soon.
