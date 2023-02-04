import configparser
import psycopg2
from sql_queries import analytics_table_test_queries


def query_data(cur, conn):
    """
    Running some example queries on Redshift

    @type cur: Psycopg Cursor object
    @type conn: Psycopg Connection object
    """
    for query in analytics_table_test_queries:
        print('----')
        print(query)
        cur.execute(query)
        conn.commit()
        results = cur.fetchall()

        for row in results:
            print("   ", row)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    query_data(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()