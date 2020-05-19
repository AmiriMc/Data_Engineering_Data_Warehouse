import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """    
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates staging, fact, and dimensional tables using the `create_table_queries` list in sql_queries.py. 
    """
    
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Connect to Redshift cluster. Setup and configure database and tables.
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    print('You are now connected to Redshift cluster. Database and tables have been created, and configured.')

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()