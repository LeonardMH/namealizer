# namealizer - A random name generator

[![Build Status](https://travis-ci.org/LeonardMH/namealizer.svg?branch=master)](https://travis-ci.org/LeonardMH/namealizer)
[![Coverage Status](https://coveralls.io/repos/LeonardMH/namealizer/badge.svg?branch=master&service=github)](https://coveralls.io/github/LeonardMH/namealizer?branch=master)
[![Code Climate](https://codeclimate.com/github/LeonardMH/namealizer/badges/gpa.svg)](https://codeclimate.com/github/LeonardMH/namealizer)

The goal of namealizer is simple, to create a straightforward method
for creating random collections of words. If nothing else it is always
entertaining to see a few random words thrown together.

**If you are using namealizer feel free to let me know what for!**

The dictionary included with namealizer was compiled from various
sources with the main dictionary being the en\_US dictionary used in
Hunspell. The dictionary was mirrored on sourceforge at [Kevin's Word
List Page](http://wordlist.sourceforge.net).

## Installation

The easiest install method is through pip with:

    pip install namealizer

This will get the latest released version of namealizer. If you'd
like to clone from github and use the source files directly, I make
no guarantees that the command line interface will work correctly.
Importing as a module should still work correctly though.

## Command Line Use

The concept of namealizer is fairly straightforward, in the simplest use
case namealizer just returns two random words from the dictionary.

	Input: python namealizer
	Output: forest kite

### Long-format options

Adding a little bit of complexity, the user can supply a number, this
is the number of words that will be returned by namealizer. Once again,
each randomly selected from the dictionary.

	Input: python namealizer --count=5
	Output: red barracuda car showstopper pillow

For more advanced usage the user can input initials and namealizer will
return a collection of words in order of the initials. In addition, the
words can be returned in various formats.

	Input: python namealizer --initials=CXM --seed=3008
	Output: crossing xylophone maid
	
	Input: python namealizer --initials=CXM --seed=3008 --wordstyle=capitalize --separator=""
	Output CrossingXylophoneMaid
	
	Input: python namealizer --initials=CXM --seed=3008 --wordstyle=mixedcase --separator=""
	Output crossingXylophoneMaid

	Input: namealizer --initials=CXM --seed=3008 --separator="-"
	Output: crossing-xylophone-maid

	Input: namealizer --initials=CXM --seed=3008 --separator="_"
	Output: crossing_xylophone_maid

### Short-format options

Namealizer also support the classic-style unix short commandline
options. For a full list of the commands just run `namealizer --help` or
`namealizer -h`.

In general the commands are just the first letter of the long option and
do not require the equals ("=") sign. Using some of the same commands as
above:

	namealizer -c5
	namealizer -iCXM -s3008
	namealizer -iCXM -s3008 -fmixedcase

The outputs are the same as shown above in [Long-format
options](#long-format-options)

### Command line options

A guaranteed up-to-date list of available command line options can
always be determined by `namealizer -h`. The more useful options are
described below.

+ `--count` - The count option allows you to specify the number of words
returned by namealizer. Count can be combined with any of the other
options but if it is used along with `initials` then that option takes
priority.
+ `--seed` - The seed option give you the ability to specify the seed
number used for the psuedo-random number generator. This allows you to
get the same words out of namealizer between runs. I'm not sure if this
ports between machines, i.e. if I use seed 300 it may not be the same
thing as your seed 300 (I doubt they are the same).
+ `--initials` - Allows the user to specify initials to use for
generating the words. This just takes each letter and uses it as the
starting letter for each word.
+ `--wordstyle` - Lets the user control the format of the returned
words. This option is documented more thoroughly below in [Formatting
options](#formatting-options).
+ `--separator` - Specify the separator you would like to use between
words, this can be any string that you are allowed to pass into Python
so you aren't restricted to single characters.

### Formatting options

The formatting options allowed by the `--wordstyle` and `--separator`
are essentially endless. You can do `CamelCase` with: `python namealizer
--wordstyle=capitalize --separator=""` or perform the classic [Lil' John
Transform](https://www.youtube.com/watch?v=GxBSyx85Kp8) with `python
namealizer --wordstyle=uppercase --separator=" YEAH! "`

The full list of options allowed as wordstyles are:
- lowercase - "every word is lowercase"
- uppercase - "EVERY WORD IS UPPERCASE"
- capitalize - Each Word Is Capitalized"
- mixedcase - "all But The First Word Are Capitalized"
 
If you would like to see other wordstyles added [just file a request
as an issue](https://github.com/LeonardMH/namealizer/issues/new)
or implement it yourself and [create a pull
request](https://github.com/LeonardMH/namealizer/compare)!

## Use as a Module

Namealizer is also well suited for use in your own Python tools by
importing it as a module. The `namealizer.WordGenerator` class is
provided which mirrors all of the functionality of the command line.

The remaining examples in this section will assume that you have
performed the following steps:

    import namealizer
    wg = namealizer.WordGenerator("dictionaries/all_en_US.dict")

This creates a new `WordGenerator` object with a default separator of `" "`
a default wordstyle of `lowercase` and a randomly selected PRNG seed.
If the dictionary provided cannot be found, this will raise the
`namealizer.DictionaryNotFoundError`.

### Retrieving Words

In keeping with the *dictionary* paradigm of accessing words there are
two ways in which to retrieve random words from your dictionary. Both
methods use the dictionary access method to decide what to do.

- `wg["abc"]` - Returns three words where the starting letter of each
word is given by the letter corresponding to that word's position.
This is functionally equivalent to the command line options: `python
namealizer.py --initials="abc"`. The separator and wordstyle used will
be whatever is currently set as the current separator and wordstyle for
this `WordGenerator` object. This is referred to as the "string access
method".
- `wg[3]` - Returns three words where the starting letter of each word
is randomly determined. This is functionally equivalent to the command
line options: `python namealizer.py --count=3`. The separator and
wordstyle used will be whatever is currently set as the separator and
wordstyle for this `WordGenerator` object. This is referred to as the
"integer access method"

When using the *integer access method* if there is not a word in
the dictionary which can satisfy the starting letter requested,
a `namealizer.NoWordForLetter` exception is raised. If anything
other than a string (`str`) or integer (`int`) is used to access the
`WordGenerator` a `TypeError` will be raised.

### Changing Formatting Options

The formatting options are the same as allowed from the command line.
You can directly change wordstyle, separator, and seed options for the
object by directly setting their related properties.

To change the wordstyle just use:

    wg.wordstyle = <wordstyle>

Where `<wordstyle>` is one of the following:

- "lowercase" - **Default**. Example: "this is lowercase"
- "uppercase" - Example: "THIS IS UPPERCASE"
- "mixedcase" - Example: "this Is Mixed Case"
- "capitalize" - Example: "This Is Capitalize"

Changing the separator is much the same, and is done by:

    wg.separator = <separator>

Where `<separator>` is any valid ascii character or control sequence.

And finally, changing the seed is done by:

    wg.seed = <seed>

Where `<seed>` is any valid integer.
