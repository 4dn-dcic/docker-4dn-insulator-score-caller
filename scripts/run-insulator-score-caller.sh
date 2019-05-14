#!/bin/bash

INPUT=$1
BINSIZE=$2
WINDOWSIZE=$3
CUTOFF=$4
OUTDIR=$5


FILE_BASE=$(basename $INPUT)
FILE_NAME=${FILE_BASE%%.*}

if [ ! -d "$OUTDIR" ]
then
    mkdir $OUTDIR
fi

python /usr/local/bin/Script.py  --binsize $BINSIZE --window $WINDOWSIZE --cutoff $CUTOFF $INPUT $OUTDIR $FILE_NAME
