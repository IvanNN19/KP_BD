from datetime import date
import pandas as pd
import asyncio
import streamlit as st
from services.add import AddService
import repositories.flights
import repositories.dataflight
import random


# Хранение добавленных товаров в таблице
if "creations_table" not in st.session_state:
    st.session_state.creations_table = pd.DataFrame(
        columns=["flight", "name", "wight"]
    )


# @st.cache_data
@st.cache_resource
async def get_flight_async():
    print("Получение номера рейса")

    flghts = await repositories.flights.get_flight()
    print(flghts)
    return {flght["flight_id"]: flght["flight_id"] for flght in flghts}

def get_flights():
    return asyncio.run(get_flight_async())



def add_product_event(a, b, c):
    new_row = pd.DataFrame(
        {
            "flight": [a],
            "name": [b],
            "wight": [c],
        }
    )
    st.session_state.creations_table = pd.concat(
        [st.session_state.creations_table, new_row], ignore_index=True
    )


def clear_table_event():
    st.session_state.creations_table = pd.DataFrame(
        columns=["flight", "name", "wight"]
    )


def add_order_async(creations_table: pd.DataFrame, id) -> int:
    order_add_date = date(2024, random.randint(1, 12), random.randint(1, 28))
    id_order_add = AddService().process_add(
        order_add_date,
        creations_table,
        id,
    )

    print(order_add_date)
    
    st.write(f"Продажа за число {order_add_date}")
    return id_order_add



flight = get_flights()

def show_make_order():
    st.title("Создать посылку")

    DF = repositories.dataflight.show_data_from_db()
    if not DF.empty:
        # Отображаем DataFrame в Streamlit
        st.dataframe(DF)
    else:
        st.warning("Нет данных для отображения.")

    # 2)Name_order
    # 2)вес
    # 1)numder_flight
    # 4)выбор склада(?)

    # # Поля для ввода данных
    selected_flight = st.selectbox("ID рейса", flight.keys())
    name_string = st.text_input("Название посылки")
    wight_string = st.text_input("Вес посылки")

    apply_btn = st.button("Подтвердить создание посылки")
    
    if apply_btn:
        add_product_event(selected_flight, name_string, wight_string)
        print(st.session_state.creations_table)
        if len(st.session_state.creations_table) > 0:
            print(1)
            order_id = add_order_async(st.session_state.creations_table, st.session_state.user)
            print(2)
            st.success(f"успешно! ID чека: {order_id}")
            print(3)
            clear_table_event()

            print(f"успешно! ID чека: {order_id}")

    # st.write("Добавленные товары:")
    # st.dataframe(st.session_state.creations_table)
    

