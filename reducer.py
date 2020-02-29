#!/usr/bin/python

from operator import itemgetter
import sys


MAX_NUMBER_ITEMS = 25


# input comes from STDIN
for counter, line in enumerate(sys.stdin):
        if counter < MAX_NUMBER_ITEMS:
            # remove leading and trailing whitespace
            line = line.strip()
            # parse the input we got from mapper.py
            level, item = line.split('\t')
            if level[0] == '0' and level[1] == '0':
                level = level[2]
            if level[0] == '0':
                level = level[1] + level[2]

            print ('%s\t%s' % (item, level))
       
        
            

        
        
