cd..
cd..
cd xampp\mysql\bin
mysql -u root
CREATE DATABASE perfootdb;
USE perfootdb;
CREATE TABLE User (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
    UNIQUE (username),
	UNIQUE (email)
    );
CREATE TABLE Transportation (
	transportation_id INT PRIMARY KEY AUTO_INCREMENT,
	transportation_type VARCHAR(50),
    carbon_emission_per_unit DECIMAL (10, 2),
    unit VARCHAR(20)
	);
CREATE TABLE Food (
	food_id INT PRIMARY KEY AUTO_INCREMENT,
    food_type VARCHAR(50),
    carbon_emission_per_unit DECIMAL (10, 2),
	unit VARCHAR(20)
    );
CREATE TABLE Household (
	household_id INT PRIMARY KEY AUTO_INCREMENT,
    household_type VARCHAR(50),
    carbon_emission_per_unit DECIMAL (10, 2),
	unit VARCHAR(20)
    );
CREATE TABLE User_Activity (
	activity_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
	category VARCHAR(50),
    category_id VARCHAR(50),
    quantity DECIMAL (10, 2),
    carbon_emission DECIMAL (10, 2),
    activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
    );
INSERT INTO Transportation (transportation_type, carbon_emission_per_unit, unit)
VALUES
    ('Car', 0.18, 'kgCO₂/km'),
    ('Bus', 0.11, 'kgCO₂/km'),
    ('Train', 0.04, 'kgCO₂/km'),
    ('Bicycle', 0.00, 'kgCO₂/km'),
    ('Walking', 0.00, 'kgCO₂/km'),
    ('Motorcycle', 0.15, 'kgCO₂/km'),
    ('Airplane', 0.25, 'kgCO₂/km'),
    ('Electric Car', 0.05, 'kgCO₂/km'),
    ('Jeepney', 0.14, 'kgCO₂/km'),
    ('Tricycle', 0.13, 'kgCO₂/km');
INSERT INTO Food (food_type, carbon_emission_per_unit, unit)
VALUES
    ('Beef', 27.00, 'kgCO₂/kg'),
    ('Chicken', 6.10, 'kgCO₂/kg'),
    ('Pork', 12.00, 'kgCO₂/kg'),
    ('Fish', 5.00, 'kgCO₂/kg'),
    ('Eggs', 4.80, 'kgCO₂/kg'),
    ('Vegetables', 1.20, 'kgCO₂/kg'),
    ('Fruits', 1.50, 'kgCO₂/kg'),
    ('Water', 0.00, 'kgCO₂/L'),
    ('Beverages (e.g., Soft Drinks, Juice)', 0.50, 'kgCO₂/L'),
    ('Dairy', 9.00, 'kgCO₂/kg'),
    ('Grains', 4.00, 'kgCO₂/kg'),
    ('Processed Foods', 5.00, 'kgCO₂/kg');
INSERT INTO Household (household_type, carbon_emission_per_unit, unit)
VALUES
    ('Appliance Usage', 0.30, 'kgCO₂/kWh'),
    ('Laundry', 0.85, 'kgCO₂/kg'),
    ('Air Conditioning', 2.00, 'kgCO₂/h'),
    ('Internet Usage', 0.20, 'kgCO₂/h'),
    ('Waste Disposal', 0.50, 'kgCO₂/kg'),
    ('Water Usage', 0.00, 'kgCO₂/L'),
    ('Vehicle Fuel Usage', 2.30, 'kgCO₂/L'),
    ('Charging (Electronic Device)', 0.10, 'kgCO₂/h'),
    ('Cooking/Heating (Gas Usage)', 5.00, 'kgCO₂/h'),
    ('Electronic Device Usage', 0.20, 'kgCO₂/h');
