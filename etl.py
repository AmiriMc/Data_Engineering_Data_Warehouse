import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    '''
    Load staging tables into Redshift from data stored in S3; use queries defined in sql_queries.py file.
    '''    
    print('Running etl.py function: `load_staging_tables`')
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    Insert data from staging tables in Redshift into analytic tables in Redshift.
    '''   
    print('Running etl.py function: `insert_tables`')
    for query in insert_table_queries:
        print('Running query:', query)
        cur.execute(query)
        conn.commit()


def main():
    '''
    Connect to Redshift cluster. Load staging tables, insert data into analytic tables in Redshift.
    '''
    print('Running etl.py function: `main`, connecting to Redshift cluster')
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()