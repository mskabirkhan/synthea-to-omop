import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
NEW_DATABASE_NAME = os.getenv('NEW_DATABASE_NAME')

def main():
    #establishing the connection
    conn = psycopg2.connect(
    database="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Preparing query to create a database
    QUERY_1 = '''CREATE DATABASE {};'''.format(NEW_DATABASE_NAME)
    #Creating a database
    cursor.execute(QUERY_1)
    print("Creation of the database '{}' successful!".format(NEW_DATABASE_NAME))

    #Closing the connection
    conn.close()

    conn = psycopg2.connect(
    database=NEW_DATABASE_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    QUERY_2 = '''CREATE SCHEMA native;'''
    QUERY_3 = '''CREATE SCHEMA cdm_synthea10;'''

    cursor.execute(QUERY_2)
    print("Creation of the 'native' schema in database '{}' successful!".format(NEW_DATABASE_NAME))
    cursor.execute(QUERY_3)
    print("Creation of the 'cdm_synthea10' schema in database '{}' successful!".format(NEW_DATABASE_NAME))

    #Closing the connection
    conn.close()

if __name__ == '__main__':
    main()