from datetime import date
import pandas as pd
import asyncio
import streamlit as st
from services.add import AddService
import repositories.flights
import repositories.dataflight
import repositories.print_data
import random

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
        st.error(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для получения информации о посылках пользователя по user_id
async def get_user_packages(user_id: int):
    conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
    
    if conn:
        try:
            # Запрос для получения информации о посылках
            query = """
                SELECT 
                    p.package_name,
                    p.weight,
                    p.status,
                    w.warehouse_name AS warehousename,
                    f.flight_number,
                    f.origin,
                    f.destination
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

# Функция для отображения данных в Streamlit
def display_user_packages(user_id):
    packages = asyncio.run(get_user_packages(user_id))  # Запуск асинхронной функции
    if isinstance(packages, str):
        st.write(packages)  # Ошибка или сообщение о пустых данных
    else:
        for package in packages:
            st.write(f"Посылка: {package['package_name']}, Статус: {package['status']}, Вес: {package['weight']}, "
                     f"Склад: {package['warehousename']}, Рейс: {package['flight_number']}, "
                     f"Откуда: {package['origin']}, Куда: {package['destination']}")



def order_status():
    st.title("Ваши заказы:")
    display_user_packages(st.session_state.user)