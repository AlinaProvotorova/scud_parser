-- Удаление связей между таблицами
ALTER TABLE attendance DROP FOREIGN KEY fk_attendance_employee;

-- Удаление таблиц
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS employee;

-- Удаление базы данных
DROP DATABASE IF EXISTS employee_attendance;
