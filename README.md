# SQL2Pandas - Konwerter SQL do funkcji Pandas
## Zespół
1. Michał Pastuszczak - mpastuszczak@student.agh.edu.pl          
2. Mikołaj Mydel - mmydel@student.agh.edu.pl
## Założenia programu
### Ogólne cele programu
Program ma za zadanie kompilować zapytania SQL do równoważnych operacji pythonowej biblioteki pandas
### Rodzaj translatora
- kompilator
### Planowany wynik działania programu
- konwerter zapytań SQL do operacji na danych w bibliotece pandas
### Planowany język implementacji
- Python
### Generator parsera
- Lark

## Symbole gramatyki

### Symbole nieterminalne

| Symbol | Opis |
|---|---|
| `stmt` | ogólne zapytanie SQL (SELECT, INSERT, UPDATE, DELETE, CREATE) |
| `insert_stmt` | polecenie INSERT INTO |
| `column_list` | opcjonalna lista kolumn do wstawienia danych w INSERT |
| `update_stmt` | polecenie UPDATE |
| `assign_list` | lista przypisań wartości po SET |
| `assign_item` | pojedyncze przypisanie modyfikujące wartość np. `tabela = wartość` |
| `delete_stmt` | polecenie DELETE FROM |
| `select_stmt` | całe zapytanie SELECT |
| `distinct` | opcjonalne DISTINCT po SELECT |
| `select_list` | lista wyrażeń po SELECT |
| `select_item` | pojedyncze wyrażenie z opcjonalnym aliasem AS |
| `table_ref` | nazwa tabeli po FROM z opcjonalnym aliasem |
| `join_clause` | pojedyncza klauzula JOIN … ON |
| `join_type` | rodzaj złączenia (INNER / LEFT / RIGHT / FULL) |
| `where_clause` | klauzula WHERE z warunkiem |
| `groupby_clause` | klauzula GROUP BY z listą wyrażeń |
| `having_clause` | klauzula HAVING z warunkiem po agregacji |
| `orderby_clause` | klauzula ORDER BY z listą kolumn |
| `order_item` | pojedyncza kolumna sortowania z kierunkiem |
| `limit_clause` | klauzula LIMIT z liczbą wierszy |
| `expr` | wyrażenie arytmetyczne lub wartość |
| `qualified_col` | kolumna z nazwa tabeli: `tabela.kolumna` |
| `condition` | wyrażenie logiczne |
| `comp_op` | operator porównania (=, !=, <, >, <=, >=) |
| `value_list` | lista w IN (…) |
| `agg_star` | agregacja z argumentem `*`, np. `COUNT(*)` |
| `agg_expr` | agregacja z wyrażeniem, np. `AVG(price)` |
| `create_stmt` | polecenie CREATE TABLE z listą kolumn i typami |
| `col_def_list` | lista definicji kolumn w CREATE TABLE |
| `col_def` | pojedyncza definicja kolumny: nazwa i typ |
| `col_type` | typ kolumny SQL mapowany na dtype Pandas |

### Symbole terminalne

#### Słowa kluczowe (case-insensitive)
`SELECT`, `DISTINCT`, `INSERT`, `INTO`, `VALUES`, `UPDATE`, `SET`, `DELETE`, `FROM`, `AS`, `JOIN`, `INNER`, `LEFT`, `RIGHT`, `FULL`, `ON`, `WHERE`, `AND`, `OR`, `NOT`, `IS`, `NULL`, `LIKE`, `IN`, `BETWEEN`, `GROUP BY`, `HAVING`, `ORDER BY`, `ASC`, `DESC`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `CREATE`, `TABLE`, `INT`, `INTEGER`, `SMALLINT`, `BIGINT`, `FLOAT`, `DOUBLE`, `REAL`, `DECIMAL`, `NUMERIC`, `VARCHAR`, `CHAR`, `TEXT`, `BOOLEAN`, `BOOL`, `DATE`, `DATETIME`, `TIMESTAMP`

#### Operatory i separatory

| Token | Wartość |
|---|---|
| `=` | równość |
| `!=` / `<>` | różność |
| `<` | mniejszy |
| `>` | większy |
| `<=` | mniejszy lub równy |
| `>=` | większy lub równy |
| `+` | dodawanie |
| `-` | odejmowanie / negacja unaryczna |
| `*` | mnożenie / wszystkie kolumny |
| `/` | dzielenie |
| `,` | separator listy |
| `(` `)` | nawiasy |
| `.` | kwalifikator tabeli |

## Gramatyka
 
### Punkt wejścia
 
Program przyjmuje jeden lub więcej poleceń SQL oddzielonych średnikami. Końcowy średnik jest opcjonalny.
 
```
program ::= polecenie (";" polecenie)* ";"?
```
 
---
 
### Rodzaje poleceń
 
Każde polecenie jest jednym z pięciu typów:
 
```
polecenie ::= select_stmt
            | insert_stmt
            | update_stmt
            | delete_stmt
            | create_stmt
```
 
---
 
### CREATE TABLE
 
Tworzy nową tabelę o podanej nazwie z listą kolumn i ich typami.
 
```
create_stmt   ::= CREATE TABLE nazwa "(" lista_kolumn ")"
lista_kolumn  ::= definicja_kolumny ("," definicja_kolumny)*
definicja_kolumny ::= nazwa typ_kolumny
```
 
Obsługiwane typy kolumn i ich mapowanie na typy Pandas:
 
| Typ SQL | Warianty | dtype Pandas |
|---|---|---|
| całkowity | `INT`, `INTEGER`, `SMALLINT`, `BIGINT` | `int64` |
| zmiennoprzecinkowy | `FLOAT`, `DOUBLE`, `REAL`, `DECIMAL[(p,s)]`, `NUMERIC[(p,s)]` | `float64` |
| tekstowy | `VARCHAR[(n)]`, `CHAR[(n)]`, `TEXT` | `object` |
| logiczny | `BOOLEAN`, `BOOL` | `bool` |
| data | `DATE` | `datetime64[ns]` |
| data i czas | `DATETIME`, `TIMESTAMP` | `datetime64[ns]` |
 
---
 
### INSERT INTO
 
Wstawia jeden lub więcej wierszy do tabeli. Lista kolumn jest opcjonalna — jeśli jej brak, wartości przypisywane są po kolei do wszystkich kolumn tabeli.
 
```
insert_stmt ::= INSERT INTO tabela ["(" kolumna ("," kolumna)* ")"]
                VALUES "(" lista_wartości ")" ("," "(" lista_wartości ")")*
```
 
Przykład:
```sql
INSERT INTO products (product_id, name, price) VALUES (1, 'Bike', 999.99), (2, 'Helmet', 49.99);
```
 
---
 
### UPDATE
 
Modyfikuje wartości wybranych kolumn w wierszach spełniających opcjonalny warunek WHERE.
 
```
update_stmt ::= UPDATE tabela SET przypisanie ("," przypisanie)* [warunek_where]
przypisanie ::= kolumna "=" wyrażenie
```
 
Przykład:
```sql
UPDATE products SET price = price * 1.1 WHERE category_id = 3;
```
 
---
 
### DELETE FROM
 
Usuwa wiersze spełniające opcjonalny warunek WHERE. Bez klauzuli WHERE usuwa wszystkie wiersze.
 
```
delete_stmt ::= DELETE FROM tabela [warunek_where]
```
 
Przykład:
```sql
DELETE FROM orders WHERE status = 'cancelled';
```
 
---
 
### SELECT
 
Najbardziej rozbudowane polecenie. Składa się z obowiązkowego rdzenia (`SELECT … FROM`) oraz szeregu opcjonalnych klauzul, które muszą wystąpić w podanej kolejności.
 
```
select_stmt ::= SELECT [DISTINCT] lista_select
                FROM tabela
                join_clause*
                [WHERE warunek]
                [GROUP BY wyrażenie ("," wyrażenie)*]
                [HAVING warunek]
                [ORDER BY element_sortowania ("," element_sortowania)*]
                [LIMIT liczba_całkowita]
```
 
#### Lista SELECT
 
Może być gwiazdką `*` (wszystkie kolumny) lub listą wyrażeń z opcjonalnymi aliasami:
 
```
lista_select   ::= "*"
                 | element_select ("," element_select)*
element_select ::= wyrażenie [AS alias]
```
 
#### Odwołanie do tabeli
 
Tabela może mieć opcjonalny alias:
 
```
tabela ::= nazwa [AS alias]
```
 
#### Klauzula JOIN
 
Obsługiwane są cztery rodzaje złączeń. Domyślnym (gdy nie podano słowa kluczowego rodzaju) jest INNER JOIN.
 
```
join_clause ::= [rodzaj_join] JOIN tabela ON warunek
rodzaj_join ::= INNER | LEFT | RIGHT | FULL
```
 
#### Klauzula ORDER BY
 
Każdy element sortowania wskazuje wyrażenie oraz kierunek (domyślnie rosnąco):
 
```
element_sortowania ::= wyrażenie [ASC | DESC]
```
 
---
 
### Wyrażenia arytmetyczne
 
Wyrażenia budowane są hierarchicznie według priorytetów operatorów (od najniższego do najwyższego):
 
```
wyrażenie   ::= wyrażenie_dodawania
wyrażenie_dodawania ::= wyrażenie_dodawania ("+" | "-") wyrażenie_mnożenia
                      | wyrażenie_mnożenia
wyrażenie_mnożenia  ::= wyrażenie_mnożenia ("*" | "/") wyrażenie_unarne
                      | wyrażenie_unarne
wyrażenie_unarne    ::= "-" wyrażenie_pierwotne
                      | wyrażenie_pierwotne
wyrażenie_pierwotne ::= "(" wyrażenie ")"
                      | funkcja_agregująca "(" "*" ")"
                      | funkcja_agregująca "(" wyrażenie ")"
                      | tabela "." kolumna
                      | liczba
                      | tekst
                      | nazwa_kolumny
```
 
Obsługiwane funkcje agregujące: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
 
---
 
### Warunki logiczne
 
Warunki budowane są hierarchicznie według priorytetów operatorów logicznych (od najniższego do najwyższego: `OR` < `AND` < `NOT` < porównanie):
 
```
warunek         ::= warunek OR warunek_and
                  | warunek_and
warunek_and     ::= warunek_and AND warunek_not
                  | warunek_not
warunek_not     ::= NOT warunek_not
                  | warunek_porównania
warunek_porównania ::= wyrażenie operator_porównania wyrażenie
                     | wyrażenie IS [NOT] NULL
                     | wyrażenie [NOT] LIKE tekst
                     | wyrażenie [NOT] IN "(" lista_wartości ")"
                     | wyrażenie [NOT] BETWEEN wyrażenie AND wyrażenie
                     | "(" warunek ")"
```
 
Operatory porównania: `=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`.
 
---
 
### Literały i identyfikatory
 
| Token | Opis | Przykłady |
|---|---|---|
| `nazwa` | identyfikator (litera lub `_` na początku, potem litery/cyfry/`_`) | `users`, `order_id`, `_tmp` |
| `liczba_całkowita` | sekwencja cyfr | `42`, `1000` |
| `liczba` | liczba całkowita lub dziesiętna | `3.14`, `100`, `1.` |
| `tekst` | łańcuch w apostrofach lub cudzysłowach | `'Jan'`, `"ABC"` |
 
---

## Dzialanie programu

1. **Parser (Lark)** - `sql.lark` definiuje gramatykę, Lark buduje drzewo parsowania
2. **TreeToAST** - `tree_to_ast.py` zamienia drzewo Larka na obiekty dataclass z `ast_nodes.py`
3. **ASTToPandas** - `ast_to_pandas.py` przechodzi AST i generuje string z kodem Pandas

## Uruchamianie

Bez argumentów program wyświetla instrukcję obsługi:

```bash
uv run main.py
```

### Flagi

| Flaga | Opis |
|---|---|
| `-i plik` | wczytaj dane z pliku `.csv`, `.sql`/`.dump` lub `.pkl` — można podać wiele razy |
| `-f plik.sql` | tłumacz komendy SQL z pliku |
| `-x` | wykonaj wygenerowany kod (domyślnie program tylko tłumaczy) |
| `-r` | uruchom interaktywny REPL (zawsze wykonuje) |
| `-o plik` | eksportuj tabele do pliku `.csv` lub `.pkl` (wymaga `-x`) |

### Wczytywanie danych (`-i`)

Typ pliku wykrywany jest po rozszerzeniu:
- `.csv` - wczytuje plik jako DataFrame, nazwa tabeli = nazwa pliku
- `.sql` / `.dump` - wykonuje `CREATE TABLE` i `INSERT INTO` z pliku, pomija nieobsługiwane komendy
- `.pkl` - wczytuje pojedynczy DataFrame lub słownik DataFrames zapisany wcześniej przez `-o`

```bash
# dwie tabele naraz
uv run main.py -i example/dump.sql -i example/orders.csv

# import z wcześniej wyeksportowanego pickle
uv run main.py -i wynik.pkl
```

### Tłumaczenie bez wykonania (`-f` / stdin)

Domyślnie program tylko tłumaczy SQL na kod Pandas — nie potrzeba danych:

```bash
# z pliku
uv run main.py -f example/queries.sql

# ze stdin
cat example/queries.sql | uv run main.py
```

Zapytania oddzielone są średnikami, cały plik parsowany jako jedno drzewo.

### Wykonywanie (`-x`)

Flaga `-x` powoduje wykonanie wygenerowanego kodu. Wymaga załadowanych danych przez `-i`:

```bash
# tłumacz i wykonaj
uv run main.py -i example/csv/products.csv -f example/queries.sql -x

# ze stdin
cat example/queries.sql | uv run main.py -i example/csv/products.csv -x
```

### Eksport danych (`-o`)

Eksportuje tabele po wykonaniu. Wymaga `-x`:

```bash
# eksport do CSV - jedna tabela: wynik.csv, wiele tabel: wynik_products.csv, wynik_orders.csv
uv run main.py -i example/csv/products.csv -x -o wynik.csv

# eksport do pickle - wszystkie tabele w jednym pliku jako slownik
uv run main.py -i example/csv/products.csv -i example/csv/orders.csv -x -o wynik.pkl
```

### REPL (`-r`)

Interaktywna powłoka — zawsze wykonuje zapytania i wyświetla wyniki:

```bash
uv run main.py -i example/csv/products.csv -r
```

Komendy REPL:
- `q` - wyjście
- `e` - eksportuj ostatni wynik SELECT do pliku (pyta o nazwę, obsługuje `.csv` i `.pkl`)

### Przykładowe pliki

W katalogu `example/` znajdują się:
- `csv/` - dane sklepu rowerowego (9 tabel: produkty, zamówienia, klienci, itp.) — źródło: [Bike Store Sample Database (Kaggle)](https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database?resource=download)
- `sql/dump.sql` - wygenerowany dump SQL z tych samych danych (10 wierszy na tabelę)
- `queries.sql` - przykładowe zapytania

```bash
./skrypt.sh
```

#### Typy danych

| Typ SQL | dtype Pandas |
|---|---|
| `INT`, `INTEGER`, `BIGINT`, `SMALLINT` | `int64` |
| `FLOAT`, `DOUBLE`, `REAL` | `float64` |
| `DECIMAL(p,s)`, `NUMERIC(p,s)` | `float64` |
| `VARCHAR(n)`, `TEXT`, `CHAR(n)` | `object` |
| `BOOLEAN`, `BOOL` | `bool` |
| `DATE`, `DATETIME`, `TIMESTAMP` | `datetime64[ns]` |

#### Literały i identyfikatory

| Token | Przykład | Wyrażenie Regularne (Regex) |
| :--- | :--- | :--- |
| `NAME` | `users`, `price` | `/[a-zA-Z_][a-zA-Z0-9_]*/` |
| `INTEGER` | `42` | `/[0-9]+/` |
| `NUMBER` | `3.14`, `1.` | `/[0-9]+\.[0-9]*/` |
| `STRING` | `'Jan'`, `"ABC"` | `/('[^']*')|("[^"]*")/` |

## Przykład działania

**Wejście (SQL):**

```sql
SELECT * FROM products;
SELECT product_name, list_price FROM products;
SELECT * FROM customers WHERE state = 'NY';
SELECT product_name, list_price FROM products WHERE list_price > 1000;
SELECT product_name, list_price FROM products WHERE list_price <= 500;
```

**Wyjście (Pandas):**

```python
products
products[["product_name", "list_price"]]
customers[(customers["state"] == "NY")]
products[(products["list_price"] > 1000)][["product_name", "list_price"]]
products[(products["list_price"] <= 500)][["product_name", "list_price"]]
```
