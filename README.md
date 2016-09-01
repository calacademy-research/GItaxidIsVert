# GItaxidIsVert

This set of scripts parses a BLAST m8 file (BLAST tabular output file) for results that are sequences derived from vertebrate sources.  
  
### Contents
This tool includes the following scripts:  
recursive\_binary\_search.py: used as a module in GItaxidIsVert.py  
nodes\_to\_vertebrate\_ids.py: used to make a list of all of the GenBank GIs that are vertebrates  
GItaxidIsVert.py: primary script  
  
### Usage
\# Please note that these tools, which rely on NCBI GenBank GI numbers will not be useful once GI numbers are phased out <http://www.ncbi.nlm.nih.gov/news/03-02-2016-phase-out-of-GI-numbers/>.

$ git clone https://github.com/calacademy-research/GItaxidIsVert.git  
  
\# You can choose to follow all or parts of this tutorial.  
  
\# If you want to perform a BLAST to a local copy of NCBI's nt database,  
\# First obtain the PERL script "update\_blastdb.pl" from XXX  
\# Then do the following in an empty directory:  
$ perl update_blastdb.pl --timeout 300 --force --verbose nt  
\# Uncompress the downloaded files with your favorite method  
$ for f in *.tar.gz; do tar xvfz $f; done  
  
\# Perform a BLAST search  
$ blastn -db \<\/path/to/downloaded/NCBI/database/nt\> -query \<\fasta\_query\_file\> -outfmt 10 -out \<\BLAST\_output\_file.m8\>  
  
\# The next sections are more relevant specifically to GItaxidIsVert.py  
  
\# Obtain the following and uncompress them  
$ wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz  
$ wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi\_taxid\_nucl.dmp.gz    
$ tar xvfz taxdump.tar.gz  
$ gunzip gi\_taxid\_nucl.dmp.gz  

\# Make a list of all of the GenBank GIs that are vertebrates in the same directory as the files above  
\# You need to execute this in the same directory as the .dmp files or provide the full path to the nodes.dmp file  
$ nodes\_to\_vertebrate\_ids.py \<\nodes.dmp\> >vert\_ids.dmp  

\# The directory where your .dmp files are is hard-coded into the script, so you will need to do the following:  
\# Get the full path to the directory where the above .dmp files are found
$ pwd  

$ GItaxidIsVert.py \<\BLAST\_output\_file.m8\>  
  
### GItaxidIsVert.py options
  
$ python GItaxidIsVert.py  
```
Usage: GItaxidIsVert.py <blast_m8_fmt_file> -dmpDir </path/to/dmp/directory/> [-e <eval_filter#>] [-t|-a] [-n] [-c]
       Writes out m8 records that are vertebrates.

       -e eval_filter # sets an eVal number the record must be <= to to be output. Default is 1e-12
          Don't forget a number before e (usually 1) and to use a minus sign after e.
       -dmpDir /path/to/dmp/directory/ # provide full path to directory holding the following dmp files:
            gi_taxid_nucl.dmp
            vert_ids.dmp
          Don't forget to use a '/' at the end of the path.
       -a all hits of suitable eValue for each query
       -t only top hit for each query (default)
       -n reverses meaning so you get nonvertebrates.
       -c writes out a comment line with gi number,tax_id and type instead of m8 record.
```
  
### Citing
#### Authorship
  
recursive\_binary\_search.py authors: Joe Koberg (http://stackoverflow.com/questions/744256/reading-huge-file-in-python), Zena Ng  
GItaxidIsVert.py author: James B. Henderson, jhenderson@calacademy.org  
README.md authors: Zachary R. Hanna, James B. Henderson  
