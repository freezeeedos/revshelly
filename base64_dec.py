#!/usr/bin/python2
import base64, sys

if len(sys.argv) < 3:
    print '''Usage:\n    %s <input file> <output file>''' % sys.argv[0]
    exit(0)

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')
base64.decode(infile, outfile)
infile.close()
outfile.close()
