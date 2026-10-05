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

INSERT INTO categories (category_id, name) VALUES 
(1, 'Swimwear'),
(2, 'Swim Caps'),
(3, 'Goggles');

INSERT INTO users (username, password_hash, full_name, role) VALUES 
('admin', 'adminpassword', 'Store Manager', 'ADMIN'),
('seller', 'password', 'Miley Worker', 'SELLER');

INSERT INTO products (category_id, name, brand, price, cost_price, stock_quantity, min_stock_level, size) VALUES
(1, 'Arena Mens Low Waist Trunks', 'Arena', 39.99, 15.00, 10, 3, 'Large'),
(1, 'Arena Mens Low Waist Trunks', 'Arena', 39.99, 15.00, 10, 3, 'Medium'),
(2, 'Speedo Black Cap', 'Speedo', 19.99, 7.99, 15, 5, 'Medium'),
(2, 'Arena Classic Silicone Cap', 'Arena', 16.99, 7.99, 20, 5, 'Medium'),
(1, 'Jaked Mens Briefs', 'Jaked', 26.99, 10.00, 15, 5, 'Small'),
(3, 'Tyr Black Google', 'TYR', 65.99, 35.00, 10, 3, 'NA');

SET FOREIGN_KEY_CHECKS = 1;