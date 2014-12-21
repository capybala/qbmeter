#!/bin/sh

SCRIPTS_DIR=$(cd $(dirname $0); pwd)
BASE_DIR=$(dirname $SCRIPTS_DIR)
OUTPUT_DIR=$BASE_DIR/output

cd $BASE_DIR
. venv/bin/activate

mkdir -p $OUTPUT_DIR
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
scrapy crawl qb -o $OUTPUT_DIR/$TIMESTAMP.jl > $OUTPUT_DIR/$TIMESTAMP.jl.log 2>&1
