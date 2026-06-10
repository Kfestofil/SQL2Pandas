SELECT * FROM products
SELECT product_name, list_price FROM products
SELECT * FROM customers WHERE state = 'NY'
SELECT product_name, list_price FROM products WHERE list_price > 1000
SELECT product_name, list_price FROM products WHERE list_price <= 500
SELECT * FROM staffs WHERE active != 1
SELECT product_name, list_price FROM products WHERE list_price > 500 AND brand_id = 9
SELECT * FROM customers WHERE state = 'NY' OR state = 'CA'
SELECT product_name FROM products WHERE NOT brand_id = 1
SELECT first_name, last_name FROM staffs WHERE manager_id IS NULL
SELECT first_name, last_name FROM staffs WHERE manager_id IS NOT NULL
SELECT product_name FROM products WHERE product_name LIKE '%Trek%'
SELECT * FROM stores WHERE state IN ('NY', 'CA', 'TX')
SELECT product_name, list_price FROM products WHERE list_price BETWEEN 500 AND 1500
SELECT DISTINCT state FROM customers
SELECT product_name, list_price FROM products ORDER BY list_price DESC
SELECT product_name, list_price FROM products ORDER BY list_price ASC LIMIT 5
SELECT product_name, list_price AS cena FROM products WHERE list_price > 1000
SELECT product_name, list_price * 1.23 AS cena_brutto FROM products LIMIT 5
SELECT COUNT(*) AS total FROM orders
SELECT store_id, COUNT(*) AS cnt FROM orders GROUP BY store_id
SELECT category_id, AVG(list_price) AS avg_price FROM products GROUP BY category_id
SELECT order_id, SUM(quantity) AS total_qty FROM order_items GROUP BY order_id
SELECT brand_id, MIN(list_price) AS min_price, MAX(list_price) AS max_price FROM products GROUP BY brand_id
SELECT store_id, COUNT(*) AS cnt FROM orders GROUP BY store_id HAVING cnt > 3
SELECT products.product_name, brands.brand_name FROM products JOIN brands ON products.brand_id = brands.brand_id
SELECT products.product_name, stocks.quantity FROM products LEFT JOIN stocks ON products.product_id = stocks.product_id
INSERT INTO stores (store_id, store_name, phone, email, street, city, state, zip_code) VALUES (4, 'Test Bikes', '555-0000', 'test@bikes.shop', '1 Main St', 'Austin', 'TX', '73301')
UPDATE products SET list_price = list_price * 1.1 WHERE category_id = 1
DELETE FROM orders WHERE order_status = 3
