-- Вставка данных в таблицу Flights (Рейсы)
INSERT INTO Flights (flight_number, departure_time, arrival_time, origin, destination) VALUES
('A101', '2024-12-01 08:00:00', '2024-12-01 10:30:00', 'New York', 'Los Angeles'),
('A102', '2024-12-02 09:00:00', '2024-12-02 11:30:00', 'Los Angeles', 'Chicago'),
('A103', '2024-12-03 14:00:00', '2024-12-03 16:00:00', 'Chicago', 'London'),
('A104', '2024-12-04 12:30:00', '2024-12-04 15:00:00', 'London', 'Paris'),
('A105', '2024-12-05 16:00:00', '2024-12-05 18:30:00', 'Paris', 'Berlin');

-- Вставка данных в таблицу Warehouses (Склад)
INSERT INTO Warehouses (warehouse_name, location) VALUES
('Main Warehouse', 'JFK Airport, New York'),
('Secondary Warehouse', 'LAX Airport, Los Angeles'),
('European Warehouse', 'CDG Airport, Paris');

-- Вставка данных в таблицу WarehouseWorkers (Работники склада)
INSERT INTO WarehouseWorkers (full_name, warehouse_id, job_title) VALUES
('Mark Johnson', 1, 'Кладовщик'),
('Sarah Brown', 1, 'Кладовщик'),
('David Smith', 2, 'Кладовщик'),
('Emily Clark', 2, 'Менеджер склада'),
('James White', 3, 'Кладовщик'),
('Laura Green', 3, 'Менеджер склада'),
('Robert Taylor', 3, 'Охранник');
