#!/usr/bin/python

import sys
import re

def isUTF8(text):
    try:
        text = unicode(text, 'UTF-8', 'strict')
        return True
    except UnicodeDecodeError:
        return False

COPY = re.compile('^COPY .+ FROM stdin;$')
ENDCOPY = re.compile('\\\.')
SEARCHPATH = re.compile('^SET search_path')

incopy = 0
linenum = 0
copyline = ''
badtables = []

for line in sys.stdin:
        if COPY.match(line):
                incopy = 1
                copyline = line

        elif ENDCOPY.match(line):
                if linenum > 0:
                        sys.stdout.write("\.\n\n")
                        linenum = 0
                        incopy = 0

        elif SEARCHPATH.match(line):
                searchpath = line
                
        if not isUTF8(line):
                linenum += 1
                if linenum == 1:
                        sys.stdout.write(searchpath)
                        sys.stdout.write(copyline)
                        schema = re.sub(r"SET search_path = (.*), .*$", r"\1", searchpath.replace('\n', '') )
                        table = re.sub(r"^COPY (\w+) .+ FROM stdin;$", r"\1", copyline.replace('\n', '') )
                        fqtable = schema + '.' + table
                        badtables.append(fqtable)
                sys.stdout.write(line)

sys.stderr.write("pg_dump --schema-only")
for mytable in badtables:
        sys.stderr.write(" --table " + mytable)
