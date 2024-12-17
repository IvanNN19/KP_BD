import asyncpg
import asyncio
import streamlit as st
from settings import DB_CONFIG  # Параметры подключения к БД из настроек

# Функция для подключения к базе данных
async def connect_to_db():
    try:
        conn = await asyncpg.connect(**DB_CONFIG)  # Асинхронное подключение к БД
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для получения информации о посылках пользователя по user_id
async def get_user_packages(user_id: int):
    conn = await connect_to_db()  # Подключаемся к БД
    if conn:
        try:
            # Запрос для получения информации о посылках
            query = """
                SELECT 
                    p.package_name,
                    p.weight,
                    w.name AS warehouse_name,
                    f.flight_number,
                    f.departure_city,
                    f.arrival_city
                FROM 
                    Packages p
                JOIN 
                    Warehouses w ON p.warehouse_id = w.warehouse_id
                JOIN 
                    Flights f ON p.flight_id = f.flight_id
                WHERE 
                    p.user_id = $1;
            """
            # Выполнение запроса и получение результата
            result = await conn.fetch(query, user_id)
            if result:
                return result
            else:
                return "Нет посылок для данного пользователя."
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return "Ошибка запроса"
        finally:
            await conn.close()  # Закрытие соединения
    return "Не удалось подключиться к базе данных"

# async def main(id):
#     user_id = id # Пример user_id
#     packages = await get_user_packages(user_id)
    
#     if isinstance(packages, str):
#         print(packages)  # Ошибка или сообщение о пустых данных
#     else:
#         for package in packages:
#             print(f"Посылка: {package['package_name']}, Вес: {package['weight']}, "
#                   f"Склад: {package['warehouse_name']}, Рейс: {package['flight_number']}, "
#                   f"Откуда: {package['departure_city']}, Куда: {package['arrival_city']}")
            
def display_user_packages(user_id):
    packages = asyncio.run(get_user_packages(user_id))  # Запуск асинхронной функции
    if isinstance(packages, str):
        st.write(packages)  # Ошибка или сообщение о пустых данных
    else:
        for package in packages:
            st.write(f"Посылка: {package['package_name']}, Вес: {package['weight']}, "
                     f"Склад: {package['warehouse_name']}, Рейс: {package['flight_number']}, "
                     f"Откуда: {package['departure_city']}, Куда: {package['arrival_city']}")
