#! /usr/bin/python

# splitfastq.py
# Splits one fastq file into multiple files based on groups of barcodes.
# Takes csv file with barcodes and the name of the file in which reads with 
# that barcode should be placed.
# Each barcode can only be placed in one file, but multiple barcodes can be
# assigned to the same file. If the file name is "NA" the reads will not be
# written at all. Reports the final count of reads written to each file to 
# standard output.
# Possible uses include:
#    Making a separate file for each barcode
#    Placing groups of barcodes in separate files
#    Removing one or more barcodes from a dataset
#    Pulling out just one or a few barcodes from a dataset
# Expects the fastq data to include the barcode as the final element of 
# a ":" separated headerline (or the only element of the headerline).
# Expects the barcode and filename as the first two items in each line 
# of the csv file. Any items after that (or lines starting with "#"
# are ignored. 
# usage: ./splitfastq.py fastqfile.fastq barcodefile.csv

import sys
import HTSeq

# Read the barcode file into a dictionary and make a dictionary of the filenames and open filehandles
barcodes = {}
files = {}
read_counts = {}
with open(sys.argv[2]) as file:
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.replace(",", " ").split() # allows for comma or space delimited files
            barcode = split_line[0].upper() # allows for upper or lowercase barcodes
            filename = split_line[1]
            if barcode in barcodes: # Barcode is duplicated in barcode file 
                print "Warning: Barcode %s is duplicated in the barcode file!" % (barcode)
            else:
                if filename not in files and filename != "NA": # New filename - add it to the list and open a file for writing
                    files[filename] = open(filename, "w")
                    read_counts[filename] = 0
                barcodes[barcode] = filename # Record the barcode and filename in the dictionary
    read_counts["NA"] = 0
# Step through the fastq file and write each record to the appropriate file
fastq_file = HTSeq.FastqReader(sys.argv[1])
for read in fastq_file:
    barcode = read.name.split(":")[-1] # The barcode is the last colon separated item on the fastq header line
    filename = barcodes[barcode] # Get the name of the file this record to which this record should be written
    if filename != "NA": 
        files[filename].write("@%s\n%s\n+\n%s\n" % (read.name, read.seq, read.qualstr)) # write the fastq record to the appropriate file
    read_counts[filename] += 1
# Report the readcounts in each file
for key in read_counts:
    print "%s : %s reads" % (key, read_counts[key]) 
# Close all the output files
for key in files:
    files[key].close()
