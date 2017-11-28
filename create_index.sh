#!/bin/bash



db_load -T -c duplicates=1 -f ./phase2_out/recs.in -t hash ./phase2_out/re.idx
db_load -T -c duplicates=1 -f ./phase2_out/terms.in -t btree ./phase2_out/te.idx
db_load -T -c duplicates=1 -f ./phase2_out/years.in -t btree ./phase2_out/ye.idx

