import psycopg2
from settings import DB_CONFIG
import asyncio
import asyncpg
from datetime import datetime


# Асинхронная функция для добавления записи о входе в таблицу UsersLog
async def log_user_login(user_id: int):
    try:
        # Подключаемся к базе данных асинхронно
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        ) 
        
        # Получаем текущую дату и время
        login_date = datetime.now()  # Текущая дата и время

        # Выполняем запрос для вставки записи в таблицу UsersLog
        query = """
            INSERT INTO UsersLog (user_id, login_date, operation_status)
            VALUES ($1, $2, 'Вход')
        """
        
        # Вставляем user_id и текущую дату/время
        await conn.execute(query, user_id, login_date)
        print(f"Запись о входе для пользователя {user_id} добавлена в таблицу UsersLog.")
    
    except Exception as e:
        print(f"Ошибка при добавлении записи о входе: {e}")
    
    finally:
        await conn.close()

# Пример вызова асинхронной функции
def log(user_id):
    print("~~~~~~~~~~~~~~~~~~`")
    return asyncio.run(log_user_login(user_id))

