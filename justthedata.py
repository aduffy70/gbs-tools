#! /usr/bin/python

# justthedata.py
# Outputs just the datalines of a fastq file to make a smaller, more
# manageable file for scripts that don't need the header or quality
# values.

# Usage: justthedata.py fastqfile.fastq

import sys

with open(sys.argv[1]) as file: # open the fastqdata file
    line_count = 0
    for line in file:
        if line_count % 4 == 1: # This is the dataline
            print line,
        line_count += 1
