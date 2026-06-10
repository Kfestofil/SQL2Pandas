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
| `-i plik` | wczytaj dane z pliku `.csv` lub `.sql`/`.dump` - można podać wiele razy |
| `-f plik.sql` | wykonaj komendy SQL z pliku (jedna per linia) |
| `-o plik` | eksportuj wszystkie tabele po wykonaniu (`.csv` lub `.pkl`) |

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

### Wykonywanie komend z pliku (`-f`)

```bash
# podstawowe zapytania z dumpa SQL
uv run main.py -i example/dump.sql -f example/queries.sql

# dwie tabele, komendy z pliku
uv run main.py -i example/dump.sql -i example/orders.csv -f example/queries.sql
```

Plik z komendami - jedno zapytanie SQL per linia, linie zaczynające się od `--` są pomijane.

Można też przekazać komendy przez stdin:

```bash
cat example/queries.sql | uv run main.py -i example/dump.sql

# lub operatorem przekierowania
uv run main.py -i example/dump.sql < example/queries.sql
```

Przez stdin można też przekazać dump SQL (CREATE TABLE + INSERT INTO):

```bash
cat example/dump.sql | uv run main.py
```

### Eksport danych (`-o`)

```bash
# eksport do CSV - jedna tabela: wynik.csv, wiele tabel: wynik_products.csv, wynik_orders.csv
uv run main.py -i example/dump.sql -i example/orders.csv -o wynik.csv

# eksport do pickle - wszystkie tabele w jednym pliku jako slownik
uv run main.py -i example/dump.sql -i example/orders.csv -o wynik.pkl
```

Po eksporcie program kończy działanie bez otwierania REPL.

### REPL

Po wczytaniu danych (bez flagi `-o`) program uruchamia interaktywny REPL. Wpisz zapytanie SQL, program wypisze wynik jako tabelę oraz wygenerowany kod Pandas.

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
