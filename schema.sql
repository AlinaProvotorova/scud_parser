-- Создание базы данных
CREATE DATABASE IF NOT EXISTS employee_attendance;

-- Используем созданную базу данных
USE employee_attendance;

-- Создание таблицы employee
CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL
);

-- Создание таблицы attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    work_date DATE NOT NULL,
    arrival_time TIME,
    departure_time TIME,
    comment TEXT,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);
