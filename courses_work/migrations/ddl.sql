-- Создание таблицы Users (Пользователи)
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор пользователя
    username VARCHAR(100) UNIQUE NOT NULL,  -- Имя пользователя
    email VARCHAR(100) UNIQUE NOT NULL,  -- Email пользователя
    full_name VARCHAR(255) NOT NULL,  -- Полное имя пользователя
    role VARCHAR(50) NOT NULL  -- Роль (например, "администратор", "оператор")
);

-- Создание таблицы UserPasswords (Пароли пользователей)
CREATE TABLE UserPasswords (
    user_id INT PRIMARY KEY,  -- Ссылаемся на пользователя
    password_hash VARCHAR(255) NOT NULL,  -- Хеш пароля
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Создание таблицы Flights (Рейсы)
CREATE TABLE Flights (
    flight_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор рейса
    flight_number VARCHAR(50) UNIQUE NOT NULL,  -- Номер рейса
    departure_time TIMESTAMP NOT NULL,  -- Время отправления
    arrival_time TIMESTAMP NOT NULL,  -- Время прибытия
    origin VARCHAR(100) NOT NULL,  -- Место отправления
    destination VARCHAR(100) NOT NULL  -- Место назначения
);

-- Создание таблицы Warehouses (Склад)
CREATE TABLE Warehouses (
    warehouse_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор склада
    warehouse_name VARCHAR(100) NOT NULL,  -- Название склада
    location VARCHAR(255) NOT NULL  -- Адрес склада
);

-- Создание таблицы WarehouseWorkers (Работники склада)
CREATE TABLE WarehouseWorkers (
    worker_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор работника
    full_name VARCHAR(255) NOT NULL,  -- Полное имя работника
    warehouse_id INT,  -- Склад, где работает работник
    job_title VARCHAR(100),  -- Должность работника (например, "Кладовщик")
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);

-- Создание таблицы Packages (Посылки)
CREATE TABLE Packages (
    package_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор посылки
    user_id INT,  -- Кто создал посылку
    package_name VARCHAR(100) NOT NULL,  -- Название посылки или описание
    weight DECIMAL(10, 2),  -- Вес посылки
    status VARCHAR(50) NOT NULL DEFAULT 'Создана',  -- Статус посылки (например, "В пути", "Доставлена")
    flight_id INT,  -- Рейс, на котором посылка будет транспортироваться
    warehouse_id INT,  -- Склад, на котором посылка хранится
    date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);

CREATE TABLE UsersLog (
    log_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор записи
    user_id INT NOT NULL,  -- Идентификатор пользователя
    login_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- Дата и время входа
    operation_status VARCHAR(50) NOT NULL DEFAULT 'Вход',  -- Статус операции (в данном случае всегда 'Вход')
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
