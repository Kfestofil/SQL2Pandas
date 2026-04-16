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
| `select_stmt` | całe zapytanie SELECT |
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

### Symbole terminalne

#### Słowa kluczowe (case-insensitive)
`SELECT`, `DISTINCT`, `FROM`, `AS`, `JOIN`, `INNER`, `LEFT`, `RIGHT`, `FULL`, `ON`, `WHERE`, `AND`, `OR`, `NOT`, `IS`, `NULL`, `LIKE`, `IN`, `BETWEEN`, `GROUP BY`, `HAVING`, `ORDER BY`, `ASC`, `DESC`, `LIMIT`

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

| Token | Przykład |
|---|---|
| `NAME` | `users`, `price` |
| `INTEGER` | `42` |
| `NUMBER` | `3.14`, `1.` |
| `STRING` | `'Jan'`, `"ABC"` |
