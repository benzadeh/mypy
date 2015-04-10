
#! /usr/bin/env python3

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

with urlopen('http://sixty-north.com/c/t.txt') as story:
        story_words = []
        for line in story:
                line_words = line.decode('utf-8').split()
                for word in line_words:
                        story_words.append(word)
for word in story_words:
    print (word)
