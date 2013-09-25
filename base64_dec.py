#!/usr/bin/python2
import base64, sys

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')
base64.decode(infile, outfile)
infile.close()
outfile.close()
