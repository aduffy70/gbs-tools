#! /usr/bin/python

# trimbarcodes.py
# Trim the barcode-sticky end from the reads and quality scores in a fastq file. 
# Store the sticky end, sample name, and barcode and in the read description.
# Uses a fastq file with the barcodes already corrected (this script
# expects EVERY read to start with one of our barcodes) and a 
# barcode file with sample names.
# Usage: trimbarcodes.py barcodefile.txt correctedfastqdata.fastq
import sys

barcodes = {} # key = barcode and sticky end, value = sample name

with open(sys.argv[1]) as file: # open the barcode file and make a dictionary
    for line in file:
        if line[0] != "#": # Ignore lines starting with a #
            split_line = line.split()
            barcodes[split_line[1]] = split_line[0]
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
        barcode_length = 12
        if fastq_line == 1: # This is the dataline
            # find which barcode
            found_barcode = 0
            barcode = line[0:12]
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
        elif line[0:6] == "@HISEQ": # This is the header, the dataline is next
            # We don't have what we need to edit it yet so store it for now
            header = line
            fastq_line = 1
        elif line == "+\n": # The quality line is next
            marker = line
            fastq_line = 3
        if fastq_line == 0: # time to print the record before we start into the next one
            print header, data, marker, quality,
