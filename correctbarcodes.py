#! /usr/bin/python

# correctbarcodes.py
# Use the output of sortbarcodes.py to find the reads in a fastq
# file that either start with a valid barcode sequence or have
# a barcode that can be corrected unambiguously to be valid.
# Write those fastq reads to a new file (with the barcodes 
# corrected but still in place for now).
# Write all other fastq reads to a separate files so they can
# be explored further (ambiguous reads w/distance <3 and reads with distance >=3) 
# Usage: correctbarcodes.py sortbarcodesOUTfile.txt fastqdata.fastq correctedreadfile.fastq ambiguousreadfile.fastq distantreadfile.fastq 

import sys
import operator # for sorting dictionaries

barcode_assignments = {} # A lookup dictionary with unique 12mers as key and corrected barcode, distance as value
read_counts = {"CORRECTED": 0, "AMBIGUOUS": 0, "DISTANT": 0}
total_read_count = 0
output_files = {} # Store the 3 output files (saves on if statements later)
output_files["CORRECTED"] = open(sys.argv[3], "w")
output_files["AMBIGUOUS"] = open(sys.argv[4], "w")
output_files["DISTANT"] = open(sys.argv[5], "w")

with open(sys.argv[1]) as file: # open the sortbarcodesOUT file and make a dictionary
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split()
            barcode_assignments[split_line[0]] = [split_line[1], split_line[2]] # key=12mer, value=[barcode, distance]
with open(sys.argv[2]) as file: # open the fastqdata file
    fastq_line = 0
    header = ""
    data = ""
    marker = ""
    quality = ""
    disposition = "" 
    for line in file:
        if fastq_line == 1: # This is the dataline
            twelvemer = line[0:12]
            distance = int(barcode_assignments[twelvemer][1])
            if distance > 2: # This is too distant to assign to a barcode
                disposition = "DISTANT"
                data = line # Keep the read as-is
            else:
                corrected_barcode = barcode_assignments[twelvemer][0]
                if corrected_barcode == "AMBIGUOUS": # This couldn't be assigned unambiguously
                    disposition = "AMBIGUOUS"
                    data = line # Keep the read as-is
                else: # distance is <3 and unambiguously assigned a barcode
                    disposition = "CORRECTED"
                    data = corrected_barcode + line[len(corrected_barcode):] # replace the wrong barcode
            fastq_line = 2
        elif fastq_line == 3: # This is the qualityline
            quality = line
            fastq_line = 0
        elif line[0:6] == "@HISEQ": # This is the header, the dataline is next
            header = line
            fastq_line = 1
        elif line[0] == "+": # The quality line is next
            marker = line
            fastq_line = 3
        if fastq_line == 0: # time to write the record to the appropriate file
            output_files[disposition].writelines([header, data, marker, quality])
            read_counts[disposition] += 1                    
            total_read_count += 1
            if total_read_count % 100000 == 0:
                print "Reads:", total_read_count, "Corrected:", read_counts["CORRECTED"], \
                    "Ambiguous:", read_counts["AMBIGUOUS"], "Distant:", read_counts["DISTANT"]
    print "Reads:", total_read_count, "Corrected:", read_counts["CORRECTED"], \
                    "Ambiguous:", read_counts["AMBIGUOUS"], "Distant:", read_counts["DISTANT"]
for key in output_files:
    output_files[key].close()

