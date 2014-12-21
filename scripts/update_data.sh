#!/bin/sh

set -ex

SCRIPTS_DIR=$(cd $(dirname $0); pwd)
BASE_DIR=$(dirname $SCRIPTS_DIR)
OUTPUT_DIR=$BASE_DIR/output

cd $BASE_DIR
. venv/bin/activate
. .env

ls $OUTPUT_DIR/*.jl | xargs cat | python $SCRIPTS_DIR/insert_into_sqlite3.py $OUTPUT_DIR/qbmeter.sqlite3

python $SCRIPTS_DIR/aggregate.py $OUTPUT_DIR/qbmeter.sqlite3 > $OUTPUT_DIR/qbmeter.json

python $SCRIPTS_DIR/build_cloudant_data.py $CLOUDANT_URL < $OUTPUT_DIR/qbmeter.json > $OUTPUT_DIR/cloudant.json

curl  --fail -d @$OUTPUT_DIR/cloudant.json $CLOUDANT_URL/_bulk_docs -H "Content-Type:application/json" --user $CLOUDANT_USER:$CLOUDANT_PASSWORD
