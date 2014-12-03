gbs-tools
=========

Tools for processing genotyping-by-sequencing data 

checkfastqformat.py - Checks a fastq file for formatting issues. 
findNs.py - Reports on Ns in the first 12 nucleotides of reads in a fastq file. 
exploreabmiguous.py - For 12mers that are equally distant to more than one 
                      barcode/stickyend with a distance of 1 or 2, return the 
                      12mer, the distance, and the list of equally distant 
                      barcodes. 
findbarcode.py - Searches for a specific barcode anywhere within the reads of 
                 a fastq file.
makerandom12mers.py - Generates a dummy fasta file of random 12bp sequences.
                      Useful for checking whether my pipeline is returning 
                      better results than are expected just by chance in a 
                      large dataset.
collapsebarcodes.py - Removes a single nucleotide from the end of a set of 
                      12mer (or whatever-mer) sequences to see how the list 
                      of unique sequences collapses. Didn't end up being useful.
countsbysample.py - Returns a count of how many reads in a fastq file were 
                    assigned to each barcode.
compare12merquality.py - Compares 12mers to the closest matching barcode and 
                         reports the average quality of matching vs mismatched
                         bases.
compare12merquality-zd.py - Same, but for data with 14-16mers instead of 12mers.
categorizemismatch.py - Compares 12mers to the closest matching barcode and
                        categorizes the mismatches by type (A to C, C to G,
                        etc).

"Pipeline" used to clean up T. intricatum GBS dataset:

1) Make a list of unique 12mer starting sequences found in the fastq file.
      findunique12mers.py
2) Double check that the list is really unique 12mers.
      doublecheckdups.py
3) For each 12mer, determine which of our barcode-stickyends is the nearest 
   match and the distance.
      sortbarcodes-wobble.py - for data with "wobble" bases in the cutsite 
                               (R, W, etc.)
      sortbarcodes-indels.py - if you don't have wobble bases and want to 
                               allow for indels when calculating distances
4) Where the nearest match is unambiguous and the distance is <3, replace the
   starting 8-12mer of each read in the fastq data with the corrected
   barcode-stickyend. Sort reads with ambiguous matches or distance >=3 into
   files to be explored separately.
      correctbarcodes.py
5) Trim the barcode-stickyends from the reads and store the sticky end, sample
   name, and barcode in the fastq description line. Trim the fastq quality 
   line to match.
      trimbarcodes.py
6) Trim any Illumina primer sequence from the 3' end of the reads and trim the
   quality line to match.
     Used "cutadapt"

