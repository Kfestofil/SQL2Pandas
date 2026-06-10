CREATE TABLE products (id INT, name VARCHAR(255), category VARCHAR(100), price FLOAT, in_stock BOOLEAN);

INSERT INTO products (id, name, category, price, in_stock) VALUES (1, 'Laptop', 'Electronics', 3500.00, 1);
INSERT INTO products (id, name, category, price, in_stock) VALUES (2, 'Myszka', 'Electronics', 89.99, 1);
INSERT INTO products (id, name, category, price, in_stock) VALUES (3, 'Biurko', 'Furniture', 750.00, 0);
INSERT INTO products (id, name, category, price, in_stock) VALUES (4, 'Krzeslo', 'Furniture', 450.00, 1);
INSERT INTO products (id, name, category, price, in_stock) VALUES (5, 'Monitor', 'Electronics', 1200.00, 1);

CREATE TABLE orders (id INT, product_id INT, quantity INT, total FLOAT, status VARCHAR(50));

INSERT INTO orders (id, product_id, quantity, total, status) VALUES (1, 1, 1, 3500.00, 'completed');
INSERT INTO orders (id, product_id, quantity, total, status) VALUES (2, 2, 3, 269.97, 'completed');
INSERT INTO orders (id, product_id, quantity, total, status) VALUES (3, 5, 2, 2400.00, 'pending');
INSERT INTO orders (id, product_id, quantity, total, status) VALUES (4, 3, 1, 750.00, 'cancelled');
INSERT INTO orders (id, product_id, quantity, total, status) VALUES (5, 1, 1, 3500.00, 'completed');
