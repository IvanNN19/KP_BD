# def main():
#     st.title("Регистрация и Авторизация")

#     choice = st.selectbox("Выберите действие", ["Регистрация", "Авторизация"])

#     if choice == "Регистрация":
#         st.subheader("Регистрация нового пользователя")

#         username = st.text_input("Имя пользователя")
#         email = st.text_input("Email")
#         full_name = st.text_input("Полное имя")
#         role = st.selectbox("Роль", ["оператор", "администратор"])
#         password = st.text_input("Пароль", type="password")
#         confirm_password = st.text_input("Подтвердите пароль", type="password")

#         if st.button("Зарегистрироваться"):
#             if password == confirm_password:
#                 register_user(username, email, full_name, role, password)
#             else:
#                 st.error("Пароли не совпадают!")

#     elif choice == "Авторизация":
#         st.subheader("Авторизация пользователя")

#         username = st.text_input("Имя пользователя")
#         password = st.text_input("Пароль", type="password")

#         if st.button("Авторизоваться"):
#             user_id = authenticate_user(username, password)
#             if user_id:
#                 st.write(f"Добро пожаловать, {username}!")
#             else:
#                 st.error("Ошибка при авторизации")

# if __name__ == "__main__":
#     main()