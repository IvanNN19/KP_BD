import psycopg2
import psycopg2.extras
import asyncpg
import asyncio
from settings import DB_CONFIG


# Функция для получения роли пользователя по его ID
async def get_user_role(user_id):
    conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
    
    if conn:
        try:
            # Запрос для получения роли пользователя
            query = """
                SELECT role FROM Users WHERE user_id = $1;
            """
            # Выполнение запроса и получение результата
            result = await conn.fetchrow(query, user_id)
            if result:
                return result['role']
            else:
                return "Пользователь не найден"
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return "Ошибка запроса"
        finally:
            await conn.close()  # Закрытие соединения
    return "Не удалось подключиться к базе данных"


def role(id):
    return asyncio.run(get_user_role(id))

