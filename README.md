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

```bash
uv run main.py -i dump.sql -i orders.csv
```

### Wykonywanie komend z pliku (`-f`)

```bash
uv run main.py -i dane.sql -f komendy.sql
```

Plik z komendami - jedno zapytanie SQL per linia, linie zaczynające się od `--` są pomijane.

Można też przekazać komendy przez stdin:

```bash
uv run main.py -i dane.sql < komendy.sql
```

### Eksport danych (`-o`)

```bash
uv run main.py -i dane.sql -f komendy.sql -o wynik.csv
```

Eksportuje każdą tabelę do osobnego pliku `{nazwa}.csv` lub `{nazwa}.pkl`. Po eksporcie program kończy działanie bez otwierania REPL.

### REPL

Po wczytaniu danych (bez flagi `-o`) program uruchamia interaktywny REPL. Wpisz zapytanie SQL, program wypisze wynik jako tabelę oraz wygenerowany kod Pandas. Wyjście przez `q`.

### Przykładowe pliki

W katalogu `example/` znajdują się:
- `dump.sql` - dump z `CREATE TABLE` i `INSERT INTO`
- `orders.csv` - dane w formacie CSV
- `queries.sql` - przykładowe zapytania

```bash
uv run main.py -i example/dump.sql -i example/orders.csv < example/queries.sql
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
