import asyncpg
import asyncio
import streamlit as st
from settings import DB_CONFIG  # Параметры подключения к БД из настроек

# Функция для подключения к базе данных
async def connect_to_db():
    try:
        conn = await asyncpg.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["dbname"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )  # Асинхронное подключение к БД
        return conn
    except Exception as e:
        st.error(f"Ошибка подключения к базе данных: {e}")
        return None

# Асинхронная функция для получения информации о сотрудниках склада
async def get_warehouse_employees_as():
    conn = await connect_to_db()  # Подключаемся к БД
    if conn:
        try:
            # Запрос для получения всей информации о сотрудниках склада
            query = """
                SELECT worker_id, full_name, job_title, t2.warehouse_name
                FROM WarehouseWorkers t1
                join 
                Warehouses t2 ON t1.warehouse_id = t2.warehouse_id;
            """
            employees = await conn.fetch(query)  # Выполняем запрос

            if employees:
                st.write("Информация о сотрудниках склада:")
                st.dataframe(employees)  # Выводим информацию в виде таблицы
            else:
                st.warning("Не найдено сотрудников склада.")
        except Exception as e:
            st.error(f"Ошибка при получении данных о сотрудниках склада: {e}")
        finally:
            await conn.close()  # Закрытие соединения
    else:
        st.error("Не удалось подключиться к базе данных.")


def get_warehouse_employees():
    return asyncio.run(get_warehouse_employees_as())


def show_warehouse_employees():
    st.title("Сотрудники склада")
    get_warehouse_employees()
    
    
