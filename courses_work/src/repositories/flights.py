import psycopg2
import psycopg2.extras
import asyncpg
from settings import DB_CONFIG

async def get_flight() -> list[dict]:
    
    query = "SELECT flight_number, flight_id FROM Flights;"
    
    try:
        print("get_flight! 52")
        # Устанавливаем асинхронное подключение к базе данных
        
        
        # conn = await asyncpg.connect(**DB_CONFIG)
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        
        # Выполняем асинхронный запрос
        result = await conn.fetch(query)
        # Закрываем соединение с БД
        await conn.close()
        
        return result
    
    except Exception as e:
        print(f"Ошибка при подключении или выполнении запроса: {e}")
        return []