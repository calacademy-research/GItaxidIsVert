#!/usr/bin/env python
# python version that will map a gi number to its taxid number using gi_taxid.dmp file
# then use the vert_ids.dmp file to output those records in the input m8 file.
# the default output is the m8 record that matches. the -c (for comment) option
# will output a line with gi, taxid and vert. Also the -n flag reverses this
# so that you get the nonverts.
# the -e flag can set the filter which defaults to 1e+1 (so most everything passes

import sys
import recursive_binary_search
import imp

blastFile = ""
vert_ids = {} # map to hold ids of vertebrates (just maps to True so we get quick look up)

showVerts = True # -n argument will cause us to show nonvertebrates instead of vertebrates
comment = False # write out gi, tax_id and type string if this is set otherwise m8 record
filter = '1e-12' # default to 1e12 filter, must be a number smaller than this to pass the filter, -e sets
curQuery = ""
allHits = False # if False then only top of a query's hits will be output, otherwise all that pass filter will

def usage():
    print "Usage: GItaxidIsVert.py <blast_m8_fmt_file> -dmpDir </path/to/dmp/directory/> [-e <eval_filter#>] [-t|-a] [-n] [-c]\n" \
          "       Writes out m8 records that are vertebrates.\n\n" \
          "       -e eval_filter # sets an eVal number the record must be <= to to be output. Default is 1e-12\n" \
          "          Don't forget a number before e (usually 1) and to use a minus sign after e.\n" \
          "       -dmpDir /path/to/dmp/directory/ # provide full path to directory holding the following dmp files:\n" \
          "            gi_taxid_nucl.dmp\n" \
          "            vert_ids.dmp\n" \
          "          Don't forget to use a '/' at the end of the path.\n" \
          "       -a all hits of suitable eValue for each query\n" \
          "       -t only top hit for each query (default)\n" \
          "       -n reverses meaning so you get nonvertebrates.\n" \
          "       -c writes out a comment line with gi number,tax_id and type instead of m8 record."

def load_vert_ids():
    fh = open(vertidFile, 'rb')
    ln = fh.readline().strip()
    while ln:
        if not ln: break
        flds = ln.split() # split on any whitespace (space or tabs)
        vert_ids[ int(flds[0]) ] = True
        ln = fh.readline().strip()
    
    fh.close()
        
def passesFilter(line):
    global filterVal, curQuery
    ary = line.split(',') # comma is used in the outfmt=10 that blastn gives us that is like m8 for blastall
    if len(ary) > 1:
        curQuery = ary[0]
        evalStr = ary[len(ary)-2]
        eVal = float(evalStr)
        if eVal <= filterVal:
            return True
    return False
    
def getopts():
    global blastFile, showVerts, filter, comment, allHits, dmpDir, taxidFile, vertidFile
    ix = 1
    while ix < len(sys.argv):
        arg = sys.argv[ix]
        if arg == '-n': # show nonverts
            showVerts = False
        elif arg == '-c': # show commentary line instead of m8 record
            comment = True
        elif arg == '-t': # only show top hit that passes the eVal filter (default)
            allHits = False
        elif arg == '-dmpDir': # directory of .dmp files
            ix += 1
            if ix < len(sys.argv):
                dmpDir = sys.argv[ix]
                taxidFile  = dmpDir + 'gi_taxid_nucl.dmp'
                vertidFile = dmpDir + 'vert_ids.dmp'
        elif arg == '-a': # show all hits that passes the eVal filter
            allHits = True
        elif arg == '-e': # eVal filter flag
            ix += 1
            if ix < len(sys.argv):
                filter = sys.argv[ix]
        elif blastFile == "":
            blastFile = arg
        ix += 1

def main():
    global filterVal
    getopts()
    if blastFile == "": # m8 file missing on cmdline
        usage()
        sys.exit(0)
 
    filterVal = float(filter)    
    imp.reload(recursive_binary_search)
    bfh = open(blastFile, 'rb')
    if bfh:
        giTaxID = recursive_binary_search.IntegerKeyTextFile(taxidFile)
        load_vert_ids()
 
        lastQuery = ""
        ln = bfh.readline().strip()
        while ln:
            if passesFilter(ln): # also sets curQuery (fld[0] in m8 line)
                if allHits or curQuery != lastQuery:
                    flds = ln.split('|')
                    gi = int(flds[1])
                    taxid = giTaxID[gi]
                    isVert = taxid in vert_ids
                    if showVerts and isVert:
                        if comment:
                            print gi, taxid, "vert"
                        else:
                            print ln
                    elif not showVerts and not isVert:
                        if comment:
                            print gi, taxid, "nonvert"
                        else:
                            print ln
            lastQuery = curQuery
            ln = bfh.readline().strip()
        bfh.close()
        
main()        
        
