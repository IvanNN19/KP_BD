from datetime import date
import pandas as pd
import asyncio
import asyncpg
import streamlit as st
from services.add import AddService
import repositories.back_order
import repositories.dataflight
import random



@st.cache_resource
async def get_choose_as():
    print("Получение айди всех посылок")
    orders = await repositories.back_order.chouse_ord()
    return {ord["package_id"]: ord["package_id"] for ord in orders}

def get_choose():
    return asyncio.run(get_choose_as())

mas = get_choose()

def del_order():
    st.title("Удалить посылку")
    selected_orders =  st.selectbox("ID посылки", mas.keys())
    del_btn = st.button("Подтвердить удаление")
    
    if del_btn:
        ans = repositories.back_order.delete_package(selected_orders)

        if ans:
            st.success(f"Посылка с package_id {selected_orders} успешно удалена.")
        else:
            st.warning(f"Посылка с package_id {selected_orders} не найдена.")