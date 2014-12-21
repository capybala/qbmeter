# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json
import sqlite3


def usage():
    print('Usage: {0} DB_PATH < JSON_LINES'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)


def main():
    try:
        db_path = sys.argv[1]
    except IndexError:
        usage()

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS availability')
    c.execute('''
        CREATE TABLE availability (
            store_id int, timestamp time, signal text, num_available int, num_waiting int
        )
    ''')

    avails = []
    for line in sys.stdin:
        avail = json.loads(line)
        if 'store_id' not in avail:
            continue
        if avail['signal'] == 'none':
            continue

        avails.append((
            avail['store_id'],
            avail['timestamp'],
            avail['signal'],
            avail['num_available'],
            avail['num_waiting'],
        ))

        if len(avails) >= 1000:
            c.executemany('INSERT INTO availability VALUES (?, ?, ?, ?, ?)', avails)
            conn.commit()
            avails = []

    if len(avails) > 0:
        c.executemany('INSERT INTO availability VALUES (?, ?, ?, ?, ?)', avails)
        conn.commit()

    conn.close()


if __name__ == '__main__':
    main()
