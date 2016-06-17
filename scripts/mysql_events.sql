CREATE DATABASE messagebus;

USE DATABASE messagebus;

CREATE TABLE messages (
    message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    message_uuid BINARY(16) NOT NULL,
    message_uuid_text CHAR(36) NOT NULL,
    message_source TEXT NOT NULL,
    message_type TEXT NOT NULL,
    message_json JSON NOT NULL,
    message_timestamp DATETIME NOT NULL,
    message_received DATETIME NOT NULL
) DEFAULT CHARSET=utf8mb4 ENGINE=MyISAM;

CREATE TABLE readings (
    reading_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    message_uuid BINARY(16) NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    sensor_id VARCHAR(255) NOT NULL,
    reading_type VARCHAR(255) NOT NULL,
    reading_value FLOAT NOT NULL,
    raw_value FLOAT,
    reading_timestamp DATETIME NOT NULL
) DEFAULT CHARSET=utf8mb4 ENGINE=MyISAM;
