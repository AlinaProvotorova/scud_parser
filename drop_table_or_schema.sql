-- Удаление связей между таблицами
ALTER TABLE attendance DROP FOREIGN KEY fk_attendance_employee;

-- Удаление таблиц
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS employees;

-- Удаление базы данных
DROP DATABASE IF EXISTS your_database_name;
