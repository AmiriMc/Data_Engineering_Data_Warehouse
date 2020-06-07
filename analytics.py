import configparser
import psycopg2
from sql_queries import table_count_queries
import time

def get_table_counts(cur, conn):
    '''
    Load staging tables into Redshift from data stored in S3; use queries defined in sql_queries.py file.
    '''    
    for query in table_count_queries:
        print('Table:', query)
        cur.execute(query)
        results = cur.fetchone()
            
        for row in results:
            print("Number of rows: ", row)
            print()    
            
        
def main():
    '''
    Connect to Redshift cluster. Load staging tables, insert data into analytic tables in Redshift.
    '''
    start_time = time.time()
    print('Running analytics.py')
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    get_table_counts(cur, conn)
    print("analytics.py run time (s)", (time.time() - start_time))

    conn.close()


if __name__ == "__main__":
    main()