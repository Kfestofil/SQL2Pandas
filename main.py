QUERIES = [
    "SELECT * FROM users",
    "SELECT name, age FROM users WHERE age > 18",
    "SELECT DISTINCT city FROM users",
    "SELECT name FROM users WHERE age BETWEEN 18 AND 65",
    "SELECT name FROM users WHERE city IN ('Kraków', 'Warszawa')",
    "SELECT name FROM users WHERE email IS NOT NULL",
    "SELECT name FROM users WHERE name LIKE 'Jan%'",
    "SELECT name, price * 1.23 AS price_vat FROM products",
    "SELECT category, COUNT(*) AS cnt FROM products GROUP BY category",
    "SELECT category, AVG(price) FROM products GROUP BY category HAVING AVG(price) > 100",
    "SELECT name FROM users ORDER BY age DESC LIMIT 10",
    "SELECT u.name, o.total FROM users AS u JOIN orders AS o ON u.id = o.user_id",
    "SELECT u.name, o.total FROM users AS u LEFT JOIN orders AS o ON u.id = o.user_id WHERE o.total > 500 ORDER BY o.total DESC LIMIT 5",
    # INSERT
    "INSERT INTO users (id, name, email) VALUES (1, 'Jan', 'jan@example.com')",
    "INSERT INTO products VALUES (10, 'Laptop', 2500)",
    # UPDATE
    "UPDATE users SET name = 'Jan Kowalski', age = 30 WHERE id = 1",
    "UPDATE products SET price = price * 1.1",
    # DELETE
    "DELETE FROM users WHERE age < 18",
    "DELETE FROM orders",
]

from pathlib import Path

from lark import Lark

from tree_to_ast import TreeToAST

GRAMMAR = Path(__file__).parent / "sql.lark"


def make_parser() -> Lark:
    return Lark(GRAMMAR.read_text(), start="start", parser="earley")


def main():
    parser = make_parser()
    transformer = TreeToAST()
    for q in QUERIES:
        print(q)
        tree = parser.parse(q)
        ast = transformer.transform(tree)
        print(ast)
        print()


if __name__ == "__main__":
    main()
