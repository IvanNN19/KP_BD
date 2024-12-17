import bcrypt
import asyncpg
import asyncio
import streamlit as st
from settings import DB_CONFIG



async def connect_to_db():
    try:
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        return conn
    except Exception as e:
        st.error(f"Ошибка подключения к базе данных: {e}")
        return None


# Асинхронная функция для авторизации пользователя
async def authenticate_user_async(username, password):
    conn = await connect_to_db()
    if conn is not None:
        query = """
            SELECT user_id, password_hash 
            FROM UserPasswords 
            WHERE user_id = (SELECT user_id FROM Users WHERE username = $1);
        """
        try:
            result = await conn.fetchrow(query, username)
            if result is None:
                st.error("Пользователь не найден.")
                await conn.close()
                return None

            user_id, stored_password_hash = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print("Авторизация успешна!")
                st.success("Авторизация успешна!")
                await conn.close()
                return user_id
            else:
                st.error("Неверный пароль.")
                await conn.close()
                return None
        except Exception as e:
            st.error(f"Ошибка при авторизации: {e}")
            await conn.close()
            return None
    return None


# Функция для вызова асинхронной авторизации пользователя
def authenticate_user(username, password):
    return asyncio.run(authenticate_user_async(username, password))


# Функция для подключения к базе данных
# def connect_to_db():
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)  # Используем настройки подключения из DB_CONFIG
#         return conn
#     except Exception as e:
#         st.error(f"Ошибка подключения к базе данных: {e}")
#         return None
    
# def authenticate_user(username, password):
#     conn = connect_to_db()
#     if conn is not None:
#         query = "SELECT user_id, password_hash FROM UserPasswords WHERE user_id = (SELECT user_id FROM Users WHERE username = %s);"
#         with conn.cursor() as cur:
#             cur.execute(query, (username,))
#             result = cur.fetchone()
#             print(result)

#             if result is None:
#                 st.error("Пользователь не найден.")
#                 return None

#             user_id, stored_password_hash = result
#             if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
#                 print("Авторизация успешна!")
#                 st.success("Авторизация успешна!")
#                 return user_id
#             else:
#                 st.error("Неверный пароль.")
#                 return None
#     return None