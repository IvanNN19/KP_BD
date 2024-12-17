from pandas import DataFrame
import psycopg2
from settings import DB_CONFIG
from datetime import date
import asyncpg


async def add_order_details_async(sales: DataFrame) -> None:
    query = """
        INSERT INTO Packages (package_id, user_id, 
        package_name, weight, status, flight_id, warehouse_id, date)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
    """
    
    try:
        # Открытие соединения с базой данных
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )

        # Используем executemany, чтобы вставить все данные из DataFrame
        async with conn.transaction():
            print(228)
            await conn.executemany(
                query,
                sales[["package_id", "user_id", "name", "wight", "status", "flight", "warehouse_id", "date"]].itertuples(
                    index=False, name=None
                )
            )
        
        print("Данные успешно добавлены.")
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        await conn.close()
