import psycopg2
import psycopg2.extras
import pandas as pd
import sqlalchemy as db
from settings import DB_CONFIG

def show_data_from_db():
    print("get_flight_table!")
    query = "SELECT * FROM Flights"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                df = pd.read_sql(query, conn)
                
                return df
    except psycopg2.Error as e:
        print(f"Ошибка при подключении или выполнении запроса: {e}")
        return []