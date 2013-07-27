#!/usr/bin/env python
from optparse import OptionParser
import sys
import csv
# Set the limit to 1 billion columns
#csv.field_size_limit(10000000)

import common


def main():
    r"""
    Reads a csv file or stdin, keeps selected columns.  Prints to stdout.

    Examples
    ---------
    Read a comma delimited csv file, data.csv, keep the 'name' column
    $ python cut.py -l name,age test/commafile.csv

    Use a tab delimited dataset 
    $ python cut.py -d'\t' -l name  test/tabfile.csv
    Note that -dt  -dtab -d\t -d'\t' -d\\t  also work
    """
    usage = "usage: %prog [options] dataset"
    usage += '\n'+main.__doc__
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-l", "--keep_list",
        help="Only keep variables in this (comma delimited) list."
        " [default: %default] ",
        action="store", dest='keep_list', default=None)
    parser.add_option(
        "-f", "--keep_file",
        help="Only keep columns whose name appears in this "
        "(newline delimited) file. [default: %default] ",
        action="store", dest='keep_file', default=None)
    parser.add_option(
        "-d", "--delimiter",
        help="Use DELIMITER as the column delimiter.  [default: %default]",
        action="store", dest='delimiter', default=',')
    parser.add_option(
        "-o", "--outfilename",
        help="Write to this file rather than stdout.  [default: %default]",
        action="store", dest='outfilename', default=None)

    (opt, args) = parser.parse_args()

    ### Parse args
    # Raise an exception if the length of args is greater than 1
    assert len(args) <= 1
    # If an argument is given, then it is the 'infilename'
    # If no arguments are given, set infilename equal to None
    infilename = args[0] if args else None

    ## Handle the options
    # Get keep_list as a Python list
    if opt.keep_file:
        with open(opt.keep_file, 'r') as keep_file:
            keep_list = common.get_list_from_filerows(keep_file)
    elif opt.keep_list:
        keep_list = opt.keep_list.split(',')
    else:
        keep_list = []

    # Deal with tabs
    if opt.delimiter in ['t', '\\t', '\t', 'tab']:
        opt.delimiter = '\t'

    ## Get the infile/outfile
    infile, outfile = common.get_inout_files(infilename, opt.outfilename)

    ## Call the function that does the real work
    cut_file(infile, outfile, delimiter=opt.delimiter, keep_list=keep_list)

    ## Close the files iff not stdin, stdout
    common.close_files(infile, outfile)


def cut_file(infile, outfile, delimiter=',', keep_list=None):
    """
    Write later, if module interface is needed.
    """
    ## Get the csv reader and writer.  Use these to read/write the files.
    reader = csv.reader(infile, delimiter=delimiter)
    writer = csv.writer(outfile, delimiter=delimiter)

    ## Extract the first row of the file
    header = reader.next()

    ## Get and write the new header
    new_header = keep_list if keep_list else []
    writer.writerow(new_header)

    ## Get the indices in the file that we will keep
    indices_to_keep = [header.index(item) for item in new_header]

    ## Iterate through the file, printing out lines 
    for row in reader:
        new_row = [row[i] for i in indices_to_keep]
        writer.writerow(new_row)



if __name__=='__main__':
    main()

