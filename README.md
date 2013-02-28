pg_find_bad_utf8
================

Python script that takes a SQL pg_dump as input and outputs COPY commands 
containing the bad utf8 rows to STDOUT and a schema-only pg_dump command 
to STDERR which only dumps the bad tables, for ease of creating a 
temporary DB with only the bad rows.

USAGE: pg_dump mydb | ./pg_find_bad_utf8.py > badtables.sql 2> dumpcommand.sh

Then you can create a db like so:

createdb badtables

Next, load it with the schema from dumpcommand.sh:

pg_dump --schema-only --table badtable1 --table badtable2 mydb | psql badtables

Then load your SQL file full of COPY commands:

psql -f badtables.sql badtables

This script is licensed under the PostgreSQL License. See the LICENSE file for
details.

