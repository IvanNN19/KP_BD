import psycopg2
import psycopg2.extras
import asyncpg
import asyncio
import streamlit as st
from settings import DB_CONFIG

async def chouse_ord():
    query = "SELECT package_id FROM packages;"
    
    try:
        print("52525252")
        # Устанавливаем асинхронное подключение к базе данных
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
    

# Функция для удаления строки по package_id
async def delete_package_by_id(package_id: int):
    conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
    
    if conn:
        try:
            # Запрос на удаление записи по package_id
            query = "DELETE FROM Packages WHERE package_id = $1;"
            # Выполняем запрос на удаление
            return await conn.execute(query, package_id)
        except Exception as e:
            st.error(f"Ошибка при удалении посылки: {e}")
        finally:
            await conn.close()  # Закрытие соединения
    else:
        st.error("Не удалось подключиться к базе данных.")

# Функция для удаления записи по package_id в Streamlit
def delete_package(package_id):
    return asyncio.run(delete_package_by_id(package_id))

