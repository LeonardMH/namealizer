# namealizer - A random name generator

[![Build Status](https://travis-ci.org/LeonardMH/namealizer.svg?branch=master)](https://travis-ci.org/LeonardMH/namealizer)

The goal of namealizer is simple, to create a straightforward method for creating random collections of words. If nothing else it is always entertaining to see a few random words thrown together.

**If you are using namealizer feel free to let me know what for!**

The dictionary included with namealizer was compiled from various sources with the main dictionary being the en\_US dictionary used in Hunspell. The dictionary was mirrored on sourceforge at [Kevin's Word List Page](http://wordlist.sourceforge.net).

## Examples

The concept of namealizer is fairly straightforward, in the simplest use case namealizer just returns two random words from the dictionary.

	Input: python namealizer
	Output: forest kite

### Long-format options

Adding a little bit of complexity, the user can supply a number, this is the number of words that will be returned by namealizer. Once again, each randomly selected from the dictionary.

	Input: python namealizer --count=5
	Output: red barracuda car showstopper pillow

For more advanced usage the user can input initials and namealizer will return a collection of words in order of the initials. In addition, the words can be returned in various formats.

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

Namealizer also support the classic-style unix short commandline options. For a full list of the commands just run `namealizer --help` or `namealizer -h`.

In general the commands are just the first letter of the long option and do not require the equals ("=") sign. Using some of the same commands as above:

	namealizer -c5
	namealizer -iCXM -s3008
	namealizer -iCXM -s3008 -fmixedcase

The outputs are the same as shown above in [Long-format options](#long-format-options)

### Command line options

A guaranteed up-to-date list of available command line options can always be determined by `namealizer -h`. The more useful options are described below.

+ `--count` - The count option allows you to specify the number of words returned by namealizer. Count can be combined with any of the other options but if it is used along with `initials` then that option takes priority.
+ `--seed` - The seed option give you the ability to specify the seed number used for the psuedo-random number generator. This allows you to get the same words out of namealizer between runs. I'm not sure if this ports between machines, i.e. if I use seed 300 it may not be the same thing as your seed 300 (I doubt they are the same).
+ `--verbose` - The verbose option is just a command line switch (that is, it doesn't take any further options). This command causes namealizer to spit out information that the user may find valuable. Most usefully, it prints out the seed used for generating the current word collection.
+ `--initials` - Allows the user to specify initials to use for generating the words. This just takes each letter and uses it as the starting letter for each word.
+ `--wordstyle` - Lets the user control the format of the returned words. This option is documented more thoroughly below in [Formatting options](#formatting-options).
+ `--separator` - Specify the separator you would like to use between words, this can be any string that you are allowed to pass into Python so you aren't restricted to single characters.

### Formatting options

The formatting options allowed by the `--wordstyle` and `--separator` are essentially endless. You can do `CamelCase` with: `python namealizer --wordstyle=capitalize --separator=""` or perform the classic [Lil' John Transform](https://www.youtube.com/watch?v=GxBSyx85Kp8) with `python namealizer --wordstyle=uppercase --separator=" YEAH! "`

The full list of options allowed as wordstyles are:
- lowercase - "every word is lowercase"
- uppercase - "EVERY WORD IS UPPERCASE"
- capitalize - Each Word Is Capitalized"
- mixedcase - "all But The First Word Are Capitalized"
 
If you would like to see other wordstyles added [just file a request as an issue](https://github.com/LeonardMH/namealizer/issues/new) or implement it yourself and [create a pull request](https://github.com/LeonardMH/namealizer/compare)!
