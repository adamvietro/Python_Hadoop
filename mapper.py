#!/usr/bin/python
"""mapper.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split('\t')

    lvl = words[2]
    if len(lvl) == 1:
        lvl = '00' + lvl
    if len(lvl) == 2:
        lvl = '0' + lvl
    if len(lvl) == 3:
        lvl = '' + lvl
    print ('%s\t%s' % (lvl, words[1]))

