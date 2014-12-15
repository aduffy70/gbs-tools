#! /usr/bin/python

# trimbarcodes.py
# Trim the barcode-sticky end from the reads and quality scores in a fastq 
# file. Store the barcode and in the read description.
# Uses a fastq file with the barcodes already corrected (this script
# expects EVERY read to start with one of our barcodes) and a 
# barcode file with sample names.
# Usage: trimbarcodes.py barcodefile.txt correctedfastqdata.fastq headerstartstring

import sys

barcodes = {} # key = barcode and sticky end, value = sample name
max_barcode_length = 0 # Just a number smaller than the smallest we expect
min_barcode_length = 99 # Just a number bigger than the biggest we expect
header_start = sys.argv[3]

with open(sys.argv[1]) as file: # open the barcode file and make a dictionary and find the range of barcode lengths
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.replace(",", " ").split() # allows for comma or space delimited barcode files
            new_barcode = split_line[1].upper() # allows for upper or lowercase barcodes
            barcode_length = len(new_barcode)
            if barcode_length < min_barcode_length:
                min_barcode_length = barcode_length
            elif barcode_length > max_barcode_length:
                max_barcode_length = barcode_length
            barcodes[new_barcode] = split_line[0] # key=barcode sequence, value=barcode name or sample name
with open(sys.argv[2]) as file: # open the fastqdata file
    fastq_line = 0
    header = ""
    data = ""
    marker = ""
    quality = ""
    disposition = "" 
    barcode = ""
    barcode_trim_length = 0
    for line in file:
        barcode_length = max_barcode_length
        if fastq_line == 1: # This is the dataline
            # find which barcode
            found_barcode = 0
            barcode = line[0:max_barcode_length]
            while found_barcode == 0:
                if barcodes.has_key(barcode):
                    found_barcode = 1
                else:
                    barcode = barcode[0:-1]
                    barcode_length -= 1                                
            # cut it out
            data = line[barcode_length:]
            # remember the length so we can trim the quality score
            barcode_trim_length = barcode_length
            # We have everything we need to edit the header line now
            header = header[:-1] + ":" + barcode[-4:] + ":" + barcodes[barcode] + ":" + barcode[0:-4] + header[-1]
            fastq_line = 2
        elif fastq_line == 3: # This is the qualityline
            # cut the scores for the barcode and stickyend
            quality = line[barcode_trim_length:]
            fastq_line = 0
        elif line[0:len(header_start)] == header_start: # This is the header, the dataline is next
            # We don't have what we need to edit it yet so store it for now
            header = line
            fastq_line = 1
        elif line == "+\n": # The quality line is next
            marker = line
            fastq_line = 3
        if fastq_line == 0: # time to print the record before we start into the next one
            print header, data, marker, quality,
