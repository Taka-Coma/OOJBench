# OOJBench

- Benchmark data generator for order-oriented join, an implementation of hinting join.


## How to use
- Requirement
	- Python
		- Validated only for python 2.7
	- Packages of python: json, numpy, psycopg2
	- Here assumes PostgreSQL as database.
- Steps
	1. Set parameters in conf.json 
	1. python dataGen.py
		- output: R.csv, R.sql, S.csv, S.sql, E.csv, E.sql
	1. createdb dbname
		- dbname is as written in conf.json.
		- If already created, skip this step.
	1. python bulkLoad2Postgres.py
		- Drop tables R, S, and E if they exist.
		- Create tables R, S, and E.
		- Store R.csv, S.csv, E.csv into corresponding tables.


## Component
- conf.json: configuration file for the generator
	- Parameters: N, k, l, s, t, z, dbname
		- N: The number of tuples in the joined results.
		- k: The number of attributes on R.
		- l: The number of attributes on S.
		- s: The number of attributes for order-oriented join on R.
		- t: The number of attributes for order-oriented join on S.
		- z: The number tuples per join key value.
		- dbname: The name of database.

	- The following is a sample.
- dataGen.py: data generator
	- Generates
		- Three CSV files (R.csv, S.csv and E.csv) corresponding with relations R, S, and E.
			- All attributes are integer.
		- Three SQL files (R.sql, S.sql and E.sql) for create table statements.
- bulkLoad2Postgres.py: data loader to PostgreSQL database
	- Execute SQL files (R.sql, S.sql and E.sql).
	- Execute COPY command for loading CSV files into corresponding tables.


### Specifications of tables
- Base join keys are the last columns of R and S.
	- Herein, equi-join is assumed.
- Order-oriented join keys are k-s-1 (resp. l-t-1) to k-1 (resp. l-1) columns in R (resp. S).
	- k, l: the numbers of attributes of R and S
	- s, t: the numbers of attrobutes for order-oriented join on R and S
- Other attributes are filled by random values.



### Sample conf.json
```
{
"N": {
        "value": 1000,
        "description": "The number of tuples in the joined result."
},
"k": {
        "value": 10,
        "description": "The number of attributes on R."
},
"l": {
        "value": 10,
        "description": "The number of attributes on S "
},
"s": {
        "value": 1,
        "description": "The number of attributes for order-oriented join on R."
},
"t": {
        "value": 1,
        "description": "The number of attributes for order-oriented join on S."
},
"z": {
        "value": 10,
        "description": "The number tuples per join key value."
},
"dbname": "ooj"
}
```
