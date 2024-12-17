from pages.make_order import show_make_order
from pages.order_status import order_status
from pages.del_order import del_order
from pages.updata import update_package_status
from pages.staff import show_warehouse_employees
import streamlit as st
import repositories.reg
import repositories.logs
import repositories.auth
import repositories.check_user
import re

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"



def login_page():
    st.title("Авторизация / Регистрация")

    # Выбор формы: авторизация или регистрация
    page = st.radio("Выберите действие", ("Авторизация", "Регистрация"))

    if page == "Авторизация":
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")

        if st.button("Войти"):
            user = repositories.auth.authenticate_user(username, password)
            if user:
                # Сохраняем данные о пользователе в session_state
                st.session_state.user = user
                st.session_state.logged_in = True
                
                st.rerun()  # Перезагружаем страницу и направляем на главную
                
            else:
                st.error("Неверное имя пользователя или пароль.")
    
    elif page == "Регистрация":
        username = st.text_input("Имя пользователя")
        email = st.text_input("Электронная почта")
        full_name = st.text_input("Полное имя")
        password = st.text_input("Пароль", type="password")
        role = st.selectbox("Роль", ["пользователь", "администратор"])

        if st.button("Зарегистрироваться"):
            if re.match(pattern, email) is None:
                st.error("Почта введена неверно")
            else:
                try:
                    user_id = repositories.reg.register_user(username, email, full_name, password, role)
                    st.success("Регистрация прошла успешно! Теперь вы можете войти.")
                except Exception as e:
                    st.error(f"Ошибка регистрации: {e}")


def main_page():
    if "user" in st.session_state and st.session_state.logged_in:
        st.title(f"Самый удобный сервис!")
        repositories.logs.log(st.session_state.user)
        print(st.session_state)

        user_role = repositories.check_user.role(st.session_state.user)

        if user_role == "администратор":
            st.sidebar.title("Панель администратора")
            page = st.sidebar.radio(
                "Выберите действие",
                ["Удалить посылку", "Изменить статус", "Посмотреть сотрудников"]
            )

            if page == "Удалить посылку":
                del_order()
            elif page == "Изменить статус":
                update_package_status()  # Функция для изменения статуса заказа
            elif page == "Посмотреть сотрудников":
                show_warehouse_employees()
        
        # Ветка для обычных пользователей
        elif user_role == "пользователь":
            # Страница после успешной авторизации
            page = st.sidebar.radio(
                "Создать посылку",
                ["Узнать статус посылки", "Создать посылку"]
            )

            if page == "Создать посылку":
                show_make_order()
            if page == "Узнать статус посылки":
                order_status()

        else:
            st.warning("Роль пользователя не определена.")
        
        

        # Здесь добавьте функционал для главной страницы, например, просмотр данных или действий
    else:
        st.warning("Пожалуйста, войдите или зарегистрируйтесь, чтобы продолжить.")
        login_page()  # Переходим к форме авторизации/регистрации


def run_app():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        print(st.session_state.user)
        # repositories.logs.log(st.session_state.user)
        main_page()  # Показываем главную страницу при успешной авторизации
    else:
        login_page()

if __name__ == "__main__":
    run_app()


                        


