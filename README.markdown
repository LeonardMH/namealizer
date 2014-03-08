# namealizer - A random word generator

The goal of namealizer is simple, to create a straightforward method for creating random collections of words.

## Examples

The concept of namealizer is a bit difficult to understand but its purpose is fairly straightforward.

In the simplest use case namealizer just returns two random words from the dictionary.

	Input: namealizer
	Output: forest kite

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

## Documentation

Coming soon.
