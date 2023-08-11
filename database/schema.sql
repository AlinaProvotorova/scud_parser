-- Создание базы данных
CREATE DATABASE IF NOT EXISTS employee_attendance;

-- Используем созданную базу данных
USE employee_attendance;

-- Создание таблицы employee
CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL UNIQUE
);

-- Создание таблицы attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    work_date DATE NOT NULL,
    arrival_time TIME,
    departure_time TIME,
    comment TEXT,
    UNIQUE KEY unique_employee_work_date (employee_id, work_date),
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

-- Создание таблицы unique_file
CREATE TABLE IF NOT EXISTS unique_file (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number BIGINT NOT NULL UNIQUE
);
