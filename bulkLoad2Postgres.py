# -*- coding: utf-8 -*-

import psycopg2 as psql
import json

def main():
    with open('conf.json', 'r') as r:
        data = json.load(r)
        dbname = data['dbname']
        samples = data['samples']['value']
        attrs_r = data['k']['value']

    con = psql.connect('dbname=%s' % dbname)
    cur = con.cursor()

    for target in ['R', 'S', 'E']:
        with open('./generated/%s.sql' % target, 'r') as r:
            cur.execute(r.readline())
        with open('./generated/%s.csv' % target, 'r') as r:
            cur.copy_from(r, target, sep=',')

    cur.execute('''
        drop table if exists G
    ''')
    cur.execute('''
        create table G as 
        select * From E
        where r%d in (
            select *
            from (
                select distinct r%d
                from E
            ) a
            order by random()
            limit %d
        )
    ''' % (attrs_r-1, attrs_r-1, samples))

    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    main()
