#! /usr/bin/python

# compare12merquality.py
# For reads that don't exactly match a barcode, determine if the quality 
# scores for the nonmatching reads differs from the quality scores for the 
# matching reads.
# Provides an overall comparison, as well as comparisons matching and
# non-matching quality scores at each base to control for quality differences
# by base position.


# Usage: compare12merquality.py sortbarcodesOUTfile.txt fastqdata.fastq 

import sys
import operator # for sorting dictionaries

# Make a list of the quality characters in order from lowest quality to
# highest. In our calculations we will use the index of the character in the
# list to assign a quality value. 
quality_chars = ["!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/"]
quality_chars.extend(["0","1","2","3","4","5","6","7","8","9",":",";","<","="])
quality_chars.extend([">","?","@","A","B","C","D","E","F","G","H","I","J","K"])
quality_chars.extend(["L","M","N","O","P","Q","R","S","T","U","V","W","X","Y"])
quality_chars.extend(["Z","[","\\","]","^","_","`","a","b","c","d","e","f","g"])
quality_chars.extend(["h","i","j","k","l","m","n","o","p","q","r","s","t","u"])
quality_chars.extend(["v","w","x","y","z","{","|","}","~"])

# With these we can get an average match and mismatch quality score for each position in the first 12 bases
# and by summing acrossed all 12 bases we can get an overall average
mismatch_score_by_position = [0,0,0,0,0,0,0,0,0,0,0,0] #sum of mismatch quality scores at each position
match_score_by_position = [0,0,0,0,0,0,0,0,0,0,0,0] # sum of match quality scores at each position
mismatch_count_by_position = [0,0,0,0,0,0,0,0,0,0,0,0] # count of mismatches at each position
match_count_by_position = [0,0,0,0,0,0,0,0,0,0,0,0] # count of matches at each postion

# With these we can get an average match and mismatch quality score for each distance between reads and
# the best matching barcode.
mismatch_score_by_distance = [0,0,0,0,0,0,0,0,0,0,0,0]
match_score_by_distance = [0,0,0,0,0,0,0,0,0,0,0,0]
mismatch_count_by_distance = [0,0,0,0,0,0,0,0,0,0,0,0]
match_count_by_distance = [0,0,0,0,0,0,0,0,0,0,0,0]


barcode_assignments = {} # A lookup dictionary with unique 12mers as key and corrected barcode, distance as value
total_read_count = 0
ambiguous_read_count = 0

with open(sys.argv[1]) as file: # open the sortbarcodesOUT file and make a dictionary
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split()
            barcode_assignments[split_line[0]] = [split_line[1], split_line[2]] # key=12mer, value=[barcode, distance]
with open(sys.argv[2]) as file: # open the fastqdata file
    fastq_line = 0
    twelvemer = ""
    barcode = ""
    quality_twelvemer = ""
    for line in file:
        if fastq_line == 1: # This is the dataline
            twelvemer = line[0:12]
            distance = int(barcode_assignments[twelvemer][1])
            barcode = barcode_assignments[twelvemer][0]
            fastq_line = 2
        elif fastq_line == 3: # This is the qualityline
            quality_twelvemer = line[0:12]
            fastq_line = 0
        elif line[0:6] == "@HISEQ": # This is the header, the dataline is next
            fastq_line = 1
        elif line == "+\n": # The quality line is next
            fastq_line = 3
        else:
            print "fastq format problem at ", total_read_count
        if fastq_line == 0: # We have the 12mer and the quality score. Lets do some calculations.
            if barcode != "AMBIGUOUS": # We can't really do this if we can't unambiguously assign a barcode
                for index in range(0,len(barcode)):
                    quality_value = quality_chars.index(quality_twelvemer[index]) # get a quality value based on the quality character
                    if index == len(barcode) - 3: # special case for the W in the sticky end
                        if twelvemer[index] == "T" or twelvemer[index] == "A":
                            match_score_by_distance[distance] += quality_value
                            match_count_by_distance[distance] += 1
                            match_score_by_position[index] += quality_value
                            match_count_by_position[index] += 1
                        else: # mismatching base
                            mismatch_score_by_distance[distance] += quality_value
                            mismatch_count_by_distance[distance] += 1
                            mismatch_score_by_position[index] += quality_value
                            mismatch_count_by_position[index] += 1
                    else:
                        if twelvemer[index] == barcode[index]: # matching base
                            match_score_by_distance[distance] += quality_value
                            match_count_by_distance[distance] += 1
                            match_score_by_position[index] += quality_value
                            match_count_by_position[index] += 1
                        else: # mismatching base
                            mismatch_score_by_distance[distance] += quality_value
                            mismatch_count_by_distance[distance] += 1
                            mismatch_score_by_position[index] += quality_value
                            mismatch_count_by_position[index] += 1
                total_read_count += 1
            else:
                ambiguous_read_count += 1
    total_match_quality_score = 0
    total_match_quality_count = 0
    total_mismatch_quality_score = 0
    total_mismatch_quality_count = 0
    print "Reads compared:", total_read_count
    print "Ambiguous reads:", ambiguous_read_count                                           
    print "Mismatch average quality by position:",
    for x in range(0,12):
        if mismatch_count_by_position[x] != 0:
            print "%.1f" % (mismatch_score_by_position[x] / float(mismatch_count_by_position[x])),
        else:
            print "0.0",
        total_mismatch_quality_score += mismatch_score_by_position[x]
        total_mismatch_quality_count += mismatch_count_by_position[x]
    print ""
    print "Match average quality by position:   ",
    for x in range(0,12):
        if match_count_by_position[x] != 0:
            print "%.1f" % (match_score_by_position[x] / float(match_count_by_position[x])),
        else:
            print "0.0",
        total_match_quality_score += match_score_by_position[x]
        total_match_quality_count += match_count_by_position[x]
    print ""
    print "Mismatch percent by position:        ",
    for x in range(0,12):
        print "%.1f" % ((mismatch_count_by_position[x] / float(mismatch_count_by_position[x] + match_count_by_position[x])) * 100),
    print ""
    print "Mismatch average quality by distance:",
    for x in range(0,12):
        if mismatch_count_by_distance[x] != 0:
            print "%.1f" % (mismatch_score_by_distance[x] / float(mismatch_count_by_distance[x])),
        else:
            print "0.0",
    print ""
    print "Match average quality by distance:   ",
    for x in range(0,12):
        if match_count_by_distance[x] != 0:
            print "%.1f" % (match_score_by_distance[x] / float(match_count_by_distance[x])),
        else:
            print "0.0",
    print ""
    print "Total mismatch average:",
    print "%.1f" % (total_mismatch_quality_score / float(total_mismatch_quality_count))
    print "Total match average:",
    print "%.1f" % (total_match_quality_score / float(total_match_quality_count))
    print "Total mismatch percent:",
    print "%.1f" % ((total_mismatch_quality_count / float(total_mismatch_quality_count + total_match_quality_count)) * 100)

    
