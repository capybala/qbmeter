# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json
import urllib


def usage():
    print('Usage: {0} CLOUDANT_URL < INPUT.json'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)


def main():
    try:
        cloudant_url = sys.argv[1]
    except IndexError:
        usage()

    stores = json.load(sys.stdin)

    f = urllib.urlopen(cloudant_url + '/_all_docs')
    response_json = json.load(f)

    existings_rows = response_json['rows']
    docs = []

    # Existings docs
    for existings_row in existings_rows:
        store_id = existings_row['id']
        rev = existings_row['value']['rev']

        doc = {
            '_id': store_id,
            '_rev': rev,
        }
        store = stores.pop(store_id, None)

        if store:
            doc.update(store)
        else:
            doc['_deleted'] = True

        docs.append(doc)

    # New docs
    for store_id, store in stores:
        doc = dict(store)
        doc['_id'] = store_id
        docs.append(doc)

    cloudant_data = {'docs': docs}
    json.dump(cloudant_data, sys.stdout, indent=0)


if __name__ == '__main__':
    main()
