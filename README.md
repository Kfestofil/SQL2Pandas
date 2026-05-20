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
| `stmt` | ogólne zapytanie SQL (SELECT, INSERT, UPDATE, DELETE) |
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

### Symbole terminalne

#### Słowa kluczowe (case-insensitive)
`SELECT`, `DISTINCT`, `INSERT`, `INTO`, `VALUES`, `UPDATE`, `SET`, `DELETE`, `FROM`, `AS`, `JOIN`, `INNER`, `LEFT`, `RIGHT`, `FULL`, `ON`, `WHERE`, `AND`, `OR`, `NOT`, `IS`, `NULL`, `LIKE`, `IN`, `BETWEEN`, `GROUP BY`, `HAVING`, `ORDER BY`, `ASC`, `DESC`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`

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

#### Literały i identyfikatory

| Token | Przykład | Wyrażenie Regularne (Regex) |
| :--- | :--- | :--- |
| `NAME` | `users`, `price` | `/[a-zA-Z_][a-zA-Z0-9_]*/` |
| `INTEGER` | `42` | `/[0-9]+/` |
| `NUMBER` | `3.14`, `1.` | `/[0-9]+\.[0-9]*/` |
| `STRING` | `'Jan'`, `"ABC"` | `/('[^']*')|("[^"]*")/` |
