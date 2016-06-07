CREATE DATABASE messagebus;

USE DATABASE messagebus;

CREATE TABLE events (
    event_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_uuid BINARY(16) NOT NULL,
    device_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_json JSON NOT NULL,
    event_timestamp DATETIME NOT NULL
) DEFAULT CHARSET=utf8mb4 ENGINE=MyISAM;

CREATE TABLE readings (
    reading_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_uuid BINARY(16) NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    sensor_id VARCHAR(255) NOT NULL,
    reading_type VARCHAR(255) NOT NULL,
    reading_value FLOAT NOT NULL,
    raw_value FLOAT,
    event_timestamp DATETIME NOT NULL
) DEFAULT CHARSET=utf8mb4 ENGINE=MyISAM;