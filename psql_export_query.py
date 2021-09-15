import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
NEW_DATABASE_NAME = os.getenv("NEW_DATABASE_NAME")


def main():
    # establishing the connection
    conn = psycopg2.connect(
        database=NEW_DATABASE_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    q1 = """                              
    SELECT * FROM information_schema.tables WHERE table_schema = 'cdm_synthea10'
    """

    outputquery1 = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(q1)

    with open("cdm_synthea10.csv", "w") as f:
        cursor.copy_expert(outputquery1, f)

    cdm_synthea10_df = pd.read_csv("cdm_synthea10.csv")

    table_name_list = cdm_synthea10_df["table_name"].tolist()

    outputquery2 = "COPY (SELECT * FROM cdm_synthea10.{}) TO STDOUT WITH CSV HEADER;"

    for table in table_name_list:

        out_query = outputquery2.format(table)

        with open("omop/{}.csv".format(table), "w") as f:
            cursor.copy_expert(out_query, f)

    # Closing the connection
    conn.close()


if __name__ == "__main__":
    main()
