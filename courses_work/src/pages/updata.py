import asyncpg
import asyncio
import streamlit as st
import repositories.back_order
from settings import DB_CONFIG  # Параметры подключения к БД из настроек


@st.cache_resource
async def get_choose_as():
    print("Получение айди всех посылок")

    orders = await repositories.back_order.chouse_ord()

    return {ord["package_id"]: ord["package_id"] for ord in orders}

def get_choose():
    return asyncio.run(get_choose_as())
mas = get_choose()

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

# Функция для изменения статуса посылки по package_id
async def update_package_status_as(package_id: int, status: str):
    conn = await connect_to_db()  # Подключаемся к БД
    if conn:
        try:
            # Запрос на обновление статуса посылки
            query = "UPDATE Packages SET status = $1 WHERE package_id = $2;"
            # Выполняем запрос на обновление статуса
            result = await conn.execute(query, status, package_id)
            return result
        except Exception as e:
            st.error(f"Ошибка при изменении статуса посылки: {e}")
        finally:
            await conn.close()  # Закрытие соединения
    else:
        st.error("Не удалось подключиться к базе данных.")

# Функция для изменения статуса посылки в Streamlit
def change_status(package_id, status):
    return asyncio.run(update_package_status_as(package_id, status))

# Пример использования в Streamlit
def update_package_status():
    st.title("изменить статус")
    package_id = st.selectbox("ID посылки", mas.keys())
    status = st.selectbox("Выберите новый статус посылки", ["Создан", "В пути", "Прибыл"])
    del_btn = st.button("Изменить")
    print(package_id, status)
    # Ввод данных в Streamlit
    if del_btn:
        print(package_id, status)
        ans = change_status(package_id, status)
        if ans:
            st.success(f"Статус посылки с package_id {package_id} изменен на '{status}'.")
        else:
            st.warning(f"Посылка с package_id {package_id} не найдена.")

