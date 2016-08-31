# GItaxidIsVert

This set of scripts parses a BLAST m8 file (BLAST tabular output file) for results that sequences derived from vertebrate sources.  

This tool includes these scripts  
recursive\_binary\_search.py: used as a module in GItaxidIsVert.py  
GItaxidIsVert.py: primary script  


### GItaxidIsVert.py options

$ python GItaxidIsVert.py  
```
Usage: GItaxidIsVert.py <blast_m8_fmt_file> [-e <eval_filter#>] [-t|-a] [-n] [-c]
       Writes out m8 records that are vertebrates.

       -e eval_filter# sets an eVal number the record must be <= to to be output. Default is 1e-12
          Don't forget a number before e (usually 1) and to use a minus sign after e.
       -a all hits of suitable eValue for each query
       -t only top hit for each query (default)
       -n reverses meaning so you get nonvertebrates.
       -c writes out a comment line with gi number,tax_id and type instead of m8 record.
```

### Authorship

recursive\_binary\_search.py authors: Joe Koberg (http://stackoverflow.com/questions/744256/reading-huge-file-in-python), Zena Ng  
GItaxidIsVert.py author: James B. Henderson, jhenderson@calacademy.org  
README.md authors: Zachary R. Hanna, James B. Henderson  
