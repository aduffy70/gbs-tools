#! /usr/bin/python

# collapsebarcodes.py
# In my list of unique starting sequences, how do they collapse as one
# base is removed from the end? 
# Exploratory - this didn't end up being useful.
# usage: ./collapsebarcodes.py unique12mers.txt

import sys
import operator

sequence_count = 0
unique_sequences = {}
starting_length = 0

with open(sys.argv[1]) as file:
    for line in file:
        if line[0] != "#":
            sequence = line.split() # gives list with sequence in 0 and count in 1
            starting_length = len(sequence[0])
            shortened = sequence[0][:-1]
            if unique_sequences.has_key(shortened):
                unique_sequences[shortened] += int(sequence[1])
            else:
                unique_sequences[shortened] = int(sequence[1])
            sequence_count += 1
print "# Total sequences:", sequence_count
print "# Starting length:", starting_length
print "# Collapsed length:", starting_length - 1
print "# Unique sequences:", len(unique_sequences) 
print "# Count of each unique read:"
sorted_unique_sequences = sorted(unique_sequences.iteritems(), key=operator.itemgetter(1), reverse=True)
for item in sorted_unique_sequences:
    print item[0], item[1]
