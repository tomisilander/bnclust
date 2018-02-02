from __future__ import print_function
import sys
if len(sys.argv) != 3:
    sys.exit("Usage: unify_csv infile outfile")

infile = open(sys.argv[1], 'rb')
outfile = open(sys.argv[2], 'wb')
for l in infile:
    if l.strip() == '':
        continue
    l = l.rstrip(' \t\r\n')
    l = l.replace(' ', '\t')
    print(l, file=outfile)
