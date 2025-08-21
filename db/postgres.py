"""
Database shenanigans
"""

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

BASE_DIR = os.path.abspath(os.path.dirname(".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# DB params global. This is a map that handles the db connection. For simplicity, we're using the same .env file that docker uses
DB_PARAMS = {
    'host': 'localhost',
    'port': '5432',
    'database': os.getenv('PG_DB'),
    'user': os.getenv('PG_USER'),
    'password': os.getenv('PG_PASSWORD')
}

def insert_indicators(list_of_indicators):
    # define an insert query that will handle PK exist conflicts. It will overwrite the existing indicator with the latest time of that indicator's existence (from last_updated)
    insert_query = '''
INSERT INTO {} (indicator, feeds, type, last_updated)
VALUES (%s, %s, %s, %s)
ON CONFLICT (indicator) DO UPDATE SET
indicator=EXCLUDED.indicator, feeds=EXCLUDED.feeds, type=EXCLUDED.type, last_updated=EXCLUDED.last_updated
'''

    table_name = 'indicators'

    try:
        # Attempt connection using global dict
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # This can be a big ole task, so utilize transactions and handle failures semi-gracefully
        cursor.execute('BEGIN')

        # Parameterize the query to prevent injections (it's a local db but best practices and what not)
        insert_query = sql.SQL(insert_query).format(sql.Identifier(table_name))
        for indicator in list_of_indicators:
            cursor.execute(insert_query, indicator)  # This will map the tuple that contains the things needed for the DB and put them in the right spots in the query

        cursor.execute('COMMIT')
        print(f"Full transaction executed successfully")

    except Exception as e:
        print(f"Failed to execute transaction with error: {e}")

    finally:
        # Regardless of how you get here, close cursor and end connection
        cursor.close()
        conn.close()

# Handle searching using SELECT
def select_indicator(indicator):
    select_query = '''
SELECT * FROM {} WHERE {} = %s
'''
    table_name = 'indicators'
    primary_key = 'indicator'
    list_of_found = []

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        select_query = sql.SQL(select_query).format(sql.Identifier(table_name), sql.Identifier(primary_key))

        # the cursor expects a tuple, but we don't have a tuple, so pretend we have a tuple with a , and nothing after
        cursor.execute(select_query, (indicator,))

        while True:
            result = cursor.fetchone()

            if result is None:
                break
            else:
                list_of_found.append(result)

    except Exception as e:
        print(f"Failed to execute search with error: {e}")
        return list_of_found

    finally:
        # Regardless of how you get here, close cursor and end connection
        cursor.close()
        conn.close()

    return list_of_found
