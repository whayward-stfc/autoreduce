-- Create Test user
-- Starting with MySQL 8 you no longer can (implicitly) create a user using the GRANT command. 
-- Use CREATE USER instead, followed by the GRANT statement as below
USE mysql;

--Assuming user exists, so delete it if it does
DROP USER 'test-user'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'test-user'@'localhost' IDENTIFIED BY 'Abcdefg!123';
GRANT ALL ON autoreduction.* TO 'test-user'@'localhost';
FLUSH PRIVILEGES;

-- Create DB
-- ToDo: Add a test to ensure that testing db is in use before table drop
DROP DATABASE IF EXISTS autoreduction;
CREATE DATABASE autoreduction;

