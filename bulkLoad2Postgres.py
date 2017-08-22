# -*- coding: utf-8 -*-

import psycopg2 as psql
import json

def main():
    with open('conf.json', 'r') as r:
        dbname = json.load(r)['dbname']

    con = psql.connect('dbname=%s' % dbname)
    cur = con.cursor()

    for target in ['R', 'S', 'E']:
        with open('%s.sql' % target, 'r') as r:
            cur.execute(r.readline())
        with open('%s.csv' % target, 'r') as r:
            cur.copy_from(r, target, sep=',')

    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    main()
