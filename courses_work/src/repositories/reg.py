
import streamlit as st
import psycopg2
from psycopg2 import sql
import asyncpg
import asyncio
import bcrypt
# from database import get_db_connection  # Подключение к БД
from settings import DB_CONFIG

# Асинхронная функция для подключения к базе данных
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
        print(f"Ошибка подключения к базе данных: {e}")
        return None


# Асинхронная функция для регистрации нового пользователя
async def register_user_async(username, email, full_name, password, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = await connect_to_db()
    if not conn:
        return None  # Если не удалось подключиться к базе данных, выходим
    
    try:
        # Вставка нового пользователя в таблицу Users
        user_id = await conn.fetchval(
            "INSERT INTO users (username, email, full_name, role) VALUES ($1, $2, $3, $4) RETURNING user_id",
            username, email, full_name, role
        )

        # Вставка пароля в таблицу UserPasswords
        await conn.execute(
            "INSERT INTO userpasswords (user_id, password_hash) VALUES ($1, $2)",
            user_id, hashed_password
        )

        await conn.close()
        return user_id
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        await conn.close()
        return None
    


def register_user(username, email, full_name, password, role):
    return asyncio.run(register_user_async(username, email, full_name, password, role))
    
# # Функция для подключения к базе данных
# def connect_to_db():
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)  # Используем настройки подключения из DB_CONFIG
#         return conn
#     except Exception as e:
#         st.error(f"Ошибка подключения к базе данных: {e}")
#         return None

# # Функция для проверки пользователя по имени и паролю


# def register_user(username, email, full_name, password, role):
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     # Вставка нового пользователя в таблицу Users
#     cursor.execute(
#         "INSERT INTO users (username, email, full_name, role) VALUES (%s, %s, %s, %s) RETURNING user_id",
#         (username, email, full_name, role)
#     )
#     user_id = cursor.fetchone()[0]

#     # Вставка пароля в таблицу UserPasswords
#     cursor.execute(
#         "INSERT INTO userpasswords (user_id, password_hash) VALUES (%s, %s)",
#         (user_id, hashed_password)
#     )

#     conn.commit()
#     conn.close()

#     return user_id