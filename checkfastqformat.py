#! /usr/bin/python

# checkfastqformat.py
# Checks fastq files looking for extra blank lines, missing lines, etc.
# It expects to find in order (and complains if it doesn't find):
#   a header line starting with a specified string (@HISEQ for my Tint data), 
#   a data line with N, A, G, T, or C as the first character,
#   a marker line with ONLY +, and
#   a quality line that matches the length of dataline 
# If there is a blank line at the end of the file it will complain that it is 
# expecting a header line. Don't ignore this! A blank line at the end causes 
# problems for some tools (I'm looking at YOU cutadapt!).
# When it finds a problem it reports the type, the line number, and prints the line.
# Usage: checkfastqformat.py fastqfiletobechecked.fastq expectedheaderstartstring
import sys

with open(sys.argv[1]) as file: # open the fastq file
    line_count = 0
    header_start = sys.argv[2]
    header_start_length = len(header_start)
    next_line = "header"
    for line in file:
        if line_count % 4 == 0:
            #should be a header
            if line[0:header_start_length] != header_start:
                print "Expected header", line_count, line
        elif line_count % 4 == 1:
            #should be a dataline
            if line[0] not in ["N", "G", "A","T", "C"]:
                print "Expected dataline", line_count, line
            else:
                dataline_length = len(line)
        elif line_count % 4 == 2:
            #should be a "+"
            if line != "+\n":
                print "Expected +", line_count, line
        elif line_count % 4 == 3:
            #should be quality line
            if line[0:6] == header_start or line == "+\n":
                print "Expected qualityline", line_count, line
            elif dataline_length != len(line):
                print "Quality line length doesn't match data line", line_count, line
        line_count += 1
    if line_count % 4 == 0:
        print "Ended with a complete record"
    else:
        print "Ended with incomplete record"
