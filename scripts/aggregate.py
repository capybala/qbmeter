# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json
import sqlite3


def usage():
    print('Usage: {0} DB_PATH > OUTPUT.json'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)


def main():
    try:
        db_path = sys.argv[1]
    except IndexError:
        usage()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''
        SELECT store_id, MIN(timestamp) AS since, MAX(timestamp) AS until
        FROM availability
        GROUP BY store_id
    ''')

    stores = {}
    for row in c.fetchall():
        d = dict(row)
        store_id = unicode(d.pop('store_id'))
        d['congestions'] = []
        stores[store_id] = d

    c.execute('''
        SELECT
            store_id,
            day_of_week,
            (hour || minute) AS timebox,
            AVG(congestion) AS congestion
        FROM (
            SELECT
                store_id,
                CASE
                    WHEN signal = "g" THEN 0.0
                    WHEN signal = "y" THEN 0.5
                    WHEN signal = "r" THEN 1.0
                END AS congestion,
                CAST(strftime("%w", timestamp) AS int) AS day_of_week,
                strftime("%H", timestamp) AS hour,
                substr("0" ||
                    CAST(CAST(CAST(strftime("%M", timestamp) AS real) / 30 AS int) * 30 AS TEXT),
                    -2, 2) AS minute
            FROM availability
        )
        GROUP BY
            store_id, day_of_week, timebox
    ''')

    congestions = {}
    for row in c.fetchall():
        d = dict(row)
        store_id = unicode(d.pop('store_id'))
        congestions = stores[store_id]['congestions']
        congestions.append(d)

    json.dump(stores, sys.stdout, indent=0)

    conn.close()


if __name__ == '__main__':
    main()
