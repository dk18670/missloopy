#!/bin/bash

LENGTH=50000

JUNK_AUTO=junk-auto.log
JUNK_REPORTED=junk-reported.log
JUNK_TEMP=/tmp/junk.log

# Truncate the log to max $LENGTH lines
uniq $JUNK_AUTO | tail -$LENGTH > $JUNK_TEMP
cmp -s $JUNK_AUTO $JUNK_TEMP || (mv $JUNK_TEMP $JUNK_AUTO; chmod 666 $JUNK_AUTO)
uniq $JUNK_REPORTED | tail -$LENGTH > $JUNK_TEMP
cmp -s $JUNK_REPORTED $JUNK_TEMP || (mv $JUNK_TEMP $JUNK_REPORTED; chmod 666 $JUNK_REPORTED)
# Analyse its contents and create spam keyword list
python analyse-junk.py $JUNK_AUTO $JUNK_REPORTED
