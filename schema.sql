CREATE DATABASE IF NOT EXISTS SwimShop;
USE SwimShop;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('ADMIN', 'SELLER') NOT NULL DEFAULT 'SELLER'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    min_stock_level INT NOT NULL DEFAULT 5,
    size VARCHAR(20),
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    user_id INT NOT NULL,
    order_datetime DATETIME NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('completed', 'cancelled', 'pending') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
) ENGINE=InnoDB;

-- Initial data
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;
DELETE FROM users;
DELETE FROM categories;

INSERT INTO categories (category_id, name) VALUES 
(1, 'Swimwear'),
(2, 'Swim Caps'),
(3, 'Goggles');

INSERT INTO users (username, password_hash, full_name, role) VALUES 
('admin', '$sha256$swim_salt_123$ff3a7828e8be8c2d400cbe5a8075155d9a310743864d04f9cd4694f6ad8601d7', 'Store Manager', 'ADMIN'),
('seller', '$sha256$swim_salt_123$b2328d8c71eec206c4c600b58b224dd5c092c30b37853b86e43c451c4772dc6d', 'Miley Worker', 'SELLER');

INSERT INTO customers (customer_id, full_name, email, phone, address) VALUES 
(1, 'John Doe', 'john.doe@example.com', '555-0100', '123 Ocean Ave'),
(2, 'Jane Smith', 'jane.smith@example.com', '555-0200', '456 Pool St');

INSERT INTO products (category_id, name, brand, price, cost_price, stock_quantity, min_stock_level, size) VALUES
(1, 'Arena Mens Low Waist Trunks', 'Arena', 39.99, 15.00, 10, 3, 'Large'),
(1, 'Arena Mens Low Waist Trunks', 'Arena', 39.99, 15.00, 10, 3, 'Medium'),
(2, 'Speedo Black Cap', 'Speedo', 19.99, 7.99, 15, 5, 'Medium'),
(2, 'Arena Classic Silicone Cap', 'Arena', 16.99, 7.99, 20, 5, 'Medium'),
(1, 'Jaked Mens Briefs', 'Jaked', 26.99, 10.00, 15, 5, 'Small'),
(3, 'Tyr Black Google', 'TYR', 65.99, 35.00, 10, 3, 'NA');

INSERT INTO orders (order_id, customer_id, user_id, order_datetime, total_amount, status) VALUES 
(1, 1, 2, '2026-10-08 14:30:00', 59.98, 'completed'),
(2, 2, 2, '2026-10-09 10:15:00', 65.99, 'completed');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES 
(1, 1, 1, 1, 39.99),
(2, 1, 3, 1, 19.99),
(3, 2, 6, 1, 65.99);

SET FOREIGN_KEY_CHECKS = 1;