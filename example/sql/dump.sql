CREATE TABLE brands (brand_id INT, brand_name VARCHAR(255));

INSERT INTO brands (brand_id, brand_name) VALUES (1, 'Electra');
INSERT INTO brands (brand_id, brand_name) VALUES (2, 'Haro');
INSERT INTO brands (brand_id, brand_name) VALUES (3, 'Heller');
INSERT INTO brands (brand_id, brand_name) VALUES (4, 'Pure Cycles');
INSERT INTO brands (brand_id, brand_name) VALUES (5, 'Ritchey');
INSERT INTO brands (brand_id, brand_name) VALUES (6, 'Strider');
INSERT INTO brands (brand_id, brand_name) VALUES (7, 'Sun Bicycles');
INSERT INTO brands (brand_id, brand_name) VALUES (8, 'Surly');
INSERT INTO brands (brand_id, brand_name) VALUES (9, 'Trek');

CREATE TABLE categories (category_id INT, category_name VARCHAR(255));

INSERT INTO categories (category_id, category_name) VALUES (1, 'Children Bicycles');
INSERT INTO categories (category_id, category_name) VALUES (2, 'Comfort Bicycles');
INSERT INTO categories (category_id, category_name) VALUES (3, 'Cruisers Bicycles');
INSERT INTO categories (category_id, category_name) VALUES (4, 'Cyclocross Bicycles');
INSERT INTO categories (category_id, category_name) VALUES (5, 'Electric Bikes');
INSERT INTO categories (category_id, category_name) VALUES (6, 'Mountain Bikes');
INSERT INTO categories (category_id, category_name) VALUES (7, 'Road Bikes');

CREATE TABLE customers (customer_id INT, first_name VARCHAR(100), last_name VARCHAR(100), phone VARCHAR(20), email VARCHAR(255), street VARCHAR(255), city VARCHAR(100), state VARCHAR(50), zip_code VARCHAR(20));

INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (1, 'Debra', 'Burks', NULL, 'debra.burks@yahoo.com', '9273 Thorne Ave. ', 'Orchard Park', 'NY', '14127');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (2, 'Kasha', 'Todd', NULL, 'kasha.todd@yahoo.com', '910 Vine Street ', 'Campbell', 'CA', '95008');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (3, 'Tameka', 'Fisher', NULL, 'tameka.fisher@aol.com', '769C Honey Creek St. ', 'Redondo Beach', 'CA', '90278');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (4, 'Daryl', 'Spence', NULL, 'daryl.spence@aol.com', '988 Pearl Lane ', 'Uniondale', 'NY', '11553');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (5, 'Charolette', 'Rice', '(916) 381-6003', 'charolette.rice@msn.com', '107 River Dr. ', 'Sacramento', 'CA', '95820');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (6, 'Lyndsey', 'Bean', NULL, 'lyndsey.bean@hotmail.com', '769 West Road ', 'Fairport', 'NY', '14450');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (7, 'Latasha', 'Hays', '(716) 986-3359', 'latasha.hays@hotmail.com', '7014 Manor Station Rd. ', 'Buffalo', 'NY', '14215');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (8, 'Jacquline', 'Duncan', NULL, 'jacquline.duncan@yahoo.com', '15 Brown St. ', 'Jackson Heights', 'NY', '11372');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (9, 'Genoveva', 'Baldwin', NULL, 'genoveva.baldwin@msn.com', '8550 Spruce Drive ', 'Port Washington', 'NY', '11050');
INSERT INTO customers (customer_id, first_name, last_name, phone, email, street, city, state, zip_code) VALUES (10, 'Pamelia', 'Newman', NULL, 'pamelia.newman@gmail.com', '476 Chestnut Ave. ', 'Monroe', 'NY', '10950');

CREATE TABLE order_items (order_id INT, item_id INT, product_id INT, quantity INT, list_price FLOAT, discount FLOAT);

INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (1, 1, 20, 1, 599.99, 0.2);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (1, 2, 8, 2, 1799.99, 0.07);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (1, 3, 10, 2, 1549.0, 0.05);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (1, 4, 16, 2, 599.99, 0.05);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (1, 5, 4, 1, 2899.99, 0.2);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (2, 1, 20, 1, 599.99, 0.07);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (2, 2, 16, 2, 599.99, 0.05);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (3, 1, 3, 1, 999.99, 0.05);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (3, 2, 20, 1, 599.99, 0.05);
INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount) VALUES (4, 1, 2, 2, 749.99, 0.1);

CREATE TABLE orders (order_id INT, customer_id INT, order_status INT, order_date DATE, required_date DATE, shipped_date DATE, store_id INT, staff_id INT);

INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (1, 259, 4, '2016-01-01', '2016-01-03', '2016-01-03', 1, 2);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (2, 1212, 4, '2016-01-01', '2016-01-04', '2016-01-03', 2, 6);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (3, 523, 4, '2016-01-02', '2016-01-05', '2016-01-03', 2, 7);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (4, 175, 4, '2016-01-03', '2016-01-04', '2016-01-05', 1, 3);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (5, 1324, 4, '2016-01-03', '2016-01-06', '2016-01-06', 2, 6);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (6, 94, 4, '2016-01-04', '2016-01-07', '2016-01-05', 2, 6);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (7, 324, 4, '2016-01-04', '2016-01-07', '2016-01-05', 2, 6);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (8, 1204, 4, '2016-01-04', '2016-01-05', '2016-01-05', 2, 7);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (9, 60, 4, '2016-01-05', '2016-01-08', '2016-01-08', 1, 2);
INSERT INTO orders (order_id, customer_id, order_status, order_date, required_date, shipped_date, store_id, staff_id) VALUES (10, 442, 4, '2016-01-05', '2016-01-06', '2016-01-06', 2, 6);

CREATE TABLE products (product_id INT, product_name VARCHAR(255), brand_id INT, category_id INT, model_year INT, list_price FLOAT);

INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (1, 'Trek 820 - 2016', 9, 6, 2016, 379.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (2, 'Ritchey Timberwolf Frameset - 2016', 5, 6, 2016, 749.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (3, 'Surly Wednesday Frameset - 2016', 8, 6, 2016, 999.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (4, 'Trek Fuel EX 8 29 - 2016', 9, 6, 2016, 2899.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (5, 'Heller Shagamaw Frame - 2016', 3, 6, 2016, 1320.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (6, 'Surly Ice Cream Truck Frameset - 2016', 8, 6, 2016, 469.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (7, 'Trek Slash 8 27.5 - 2016', 9, 6, 2016, 3999.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (8, 'Trek Remedy 29 Carbon Frameset - 2016', 9, 6, 2016, 1799.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (9, 'Trek Conduit+ - 2016', 9, 5, 2016, 2999.99);
INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price) VALUES (10, 'Surly Straggler - 2016', 8, 4, 2016, 1549.0);

CREATE TABLE staffs (staff_id INT, first_name VARCHAR(100), last_name VARCHAR(100), email VARCHAR(255), phone VARCHAR(20), active INT, store_id INT, manager_id INT);

INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (1, 'Fabiola', 'Jackson', 'fabiola.jackson@bikes.shop', '(831) 555-5554', 1, 1, NULL);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (2, 'Mireya', 'Copeland', 'mireya.copeland@bikes.shop', '(831) 555-5555', 1, 1, 1);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (3, 'Genna', 'Serrano', 'genna.serrano@bikes.shop', '(831) 555-5556', 1, 1, 2);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (4, 'Virgie', 'Wiggins', 'virgie.wiggins@bikes.shop', '(831) 555-5557', 1, 1, 2);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (5, 'Jannette', 'David', 'jannette.david@bikes.shop', '(516) 379-4444', 1, 2, 1);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (6, 'Marcelene', 'Boyer', 'marcelene.boyer@bikes.shop', '(516) 379-4445', 1, 2, 5);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (7, 'Venita', 'Daniel', 'venita.daniel@bikes.shop', '(516) 379-4446', 1, 2, 5);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (8, 'Kali', 'Vargas', 'kali.vargas@bikes.shop', '(972) 530-5555', 1, 3, 1);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (9, 'Layla', 'Terrell', 'layla.terrell@bikes.shop', '(972) 530-5556', 1, 3, 7);
INSERT INTO staffs (staff_id, first_name, last_name, email, phone, active, store_id, manager_id) VALUES (10, 'Bernardine', 'Houston', 'bernardine.houston@bikes.shop', '(972) 530-5557', 1, 3, 7);

CREATE TABLE stocks (store_id INT, product_id INT, quantity INT);

INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 1, 27);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 2, 5);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 3, 6);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 4, 23);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 5, 22);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 6, 0);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 7, 8);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 8, 0);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 9, 11);
INSERT INTO stocks (store_id, product_id, quantity) VALUES (1, 10, 15);

CREATE TABLE stores (store_id INT, store_name VARCHAR(255), phone VARCHAR(20), email VARCHAR(255), street VARCHAR(255), city VARCHAR(100), state VARCHAR(50), zip_code VARCHAR(20));

INSERT INTO stores (store_id, store_name, phone, email, street, city, state, zip_code) VALUES (1, 'Santa Cruz Bikes', '(831) 476-4321', 'santacruz@bikes.shop', '3700 Portola Drive', 'Santa Cruz', 'CA', '95060');
INSERT INTO stores (store_id, store_name, phone, email, street, city, state, zip_code) VALUES (2, 'Baldwin Bikes', '(516) 379-8888', 'baldwin@bikes.shop', '4200 Chestnut Lane', 'Baldwin', 'NY', '11432');
INSERT INTO stores (store_id, store_name, phone, email, street, city, state, zip_code) VALUES (3, 'Rowlett Bikes', '(972) 530-5555', 'rowlett@bikes.shop', '8000 Fairway Avenue', 'Rowlett', 'TX', '75088');
