SELECT * FROM products
SELECT name, price FROM products WHERE category = 'Electronics'
SELECT name, price FROM products WHERE in_stock = 1
SELECT category, AVG(price) FROM products GROUP BY category
SELECT name, price FROM products ORDER BY price DESC LIMIT 3
SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status
SELECT id, total FROM orders WHERE total > 1000 ORDER BY total DESC
UPDATE products SET price = price * 1.1 WHERE category = 'Electronics'
SELECT name, price FROM products WHERE category = 'Electronics'
