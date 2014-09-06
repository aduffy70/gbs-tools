gbs-tools
=========

Tools for processing genotyping-by-sequencing data 

checkfastqformat.py - Checks a fastq file for formatting issues. 
findNs.py - Reports on Ns in the first 12 nucleotides of reads in a fastq file. 
exploreabmiguous.py - For 12mers that are equally distant to more than one 
                      barcode/stickyend with a distance of 1 or 2, return the 
                      12mer, the distance, and the list of equally distant barcodes. 
