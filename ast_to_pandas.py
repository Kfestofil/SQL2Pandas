import re

import ast_nodes as nodes


# bierze obiekty z ast_nodes.py i generuje kod Pandas jako string
class ASTToPandas:

    # rozpoznaje typ instrukcji i wywoluje odpowiednia metode (select / insert / update / delete)
    def gen(self, stmt) -> str:
        if isinstance(stmt, nodes.SelectStmt):
            return self._gen_select(stmt)
        elif isinstance(stmt, nodes.InsertStmt):
            return self._gen_insert(stmt)
        elif isinstance(stmt, nodes.UpdateStmt):
            return self._gen_update(stmt)
        elif isinstance(stmt, nodes.DeleteStmt):
            return self._gen_delete(stmt)
        raise ValueError(f"nieznany typ: {type(stmt)}")

    # wyrazenia
    def gen_expr(self, expr, df) -> str:
        # col -> df["col"]
        if isinstance(expr, nodes.ColExpr):
            return self._expr_col(expr, df)
        # tabela.kolumna -> df["kolumna"]
        elif isinstance(expr, nodes.QualifiedCol):
            return self._expr_qualified_col(expr, df)
        #  literal liczba 
        elif isinstance(expr, nodes.NumberLiteral):
            return self._expr_number(expr, df)
        # 'napis' na "napis"
        elif isinstance(expr, nodes.StringLiteral):
            return self._expr_string(expr, df)
        # a + b na gen_expr(a) + gen_expr(b)
        elif isinstance(expr, nodes.BinOp):
            return self._expr_binop(expr, df)
        # -a -> -(gen_expr(a))
        elif isinstance(expr, nodes.Neg):
            return self._expr_neg(expr, df)
        # COUNT(*) na "count" (do .agg())
        elif isinstance(expr, nodes.AggStar):
            return self._expr_agg_star(expr, df)
        # AVG(col) na ("col", "mean") (do .agg())
        elif isinstance(expr, nodes.AggExpr):
            return self._expr_agg_expr(expr, df)
        raise ValueError(f"nieznany expr: {type(expr)}")

    # col na df["col"]
    def _expr_col(self, expr, df) -> str:
        return f'{df}["{expr.name}"]'

    # tabela.kolumna na df["kolumna"]
    def _expr_qualified_col(self, expr, df) -> str:
        return f'{df}["{expr.column}"]'

    # liczba na wartosc jako string
    def _expr_number(self, expr, df) -> str:
        return expr.value

    # string SQL na "wartosc" bez cudzyslowow
    def _expr_string(self, expr, df) -> str:
        return f'"{self._strip_quotes(expr.value)}"'

    # a + b, a * b itd. na gen_expr(a) op gen_expr(b)
    def _expr_binop(self, expr, df) -> str:
        left = self.gen_expr(expr.left, df)
        right = self.gen_expr(expr.right, df)
        return f"{left} {expr.op} {right}"

    # -a na -(gen_expr(a))
    def _expr_neg(self, expr, df) -> str:
        return f"-({self.gen_expr(expr.expr, df)})"

    # COUNT(*) na "count" - uzywane w .agg()
    def _expr_agg_star(self, expr, df) -> str:
        return f'"{expr.func.lower()}"'

    # AVG(col) na ("col", "mean") - uzywane w .agg()
    def _expr_agg_expr(self, expr, df) -> str:
        col = self._col_name(expr.expr)
        func = self._agg_func(expr.func)
        return f'("{col}", "{func}")'

    # warunki
    # zamienia warunek SQL na maske booleowska
    def gen_condition(self, cond, df) -> str:
        if isinstance(cond, nodes.Compare):
            return self._cond_compare(cond, df)
        elif isinstance(cond, nodes.IsNull):
            return self._cond_is_null(cond, df)
        elif isinstance(cond, nodes.IsNotNull):
            return self._cond_is_not_null(cond, df)
        elif isinstance(cond, nodes.LikeCond):
            return self._cond_like(cond, df)
        elif isinstance(cond, nodes.NotLike):
            return self._cond_not_like(cond, df)
        elif isinstance(cond, nodes.InCond):
            return self._cond_in(cond, df)
        elif isinstance(cond, nodes.NotIn):
            return self._cond_not_in(cond, df)
        elif isinstance(cond, nodes.Between):
            return self._cond_between(cond, df)
        elif isinstance(cond, nodes.NotBetween):
            return self._cond_not_between(cond, df)
        elif isinstance(cond, nodes.AndCond):
            return self._cond_and(cond, df)
        elif isinstance(cond, nodes.OrCond):
            return self._cond_or(cond, df)
        elif isinstance(cond, nodes.NotCond):
            return self._cond_not(cond, df)
        raise ValueError(f"nieznany condition: {type(cond)}")

    # age > 18 na (df["age"] > 18)
    def _cond_compare(self, cond, df) -> str:
        left = self.gen_expr(cond.left, df)
        right = self.gen_expr(cond.right, df)
        return f"({left} {cond.op} {right})"

    # email IS NULL na (df["email"].isna())
    def _cond_is_null(self, cond, df) -> str:
        return f"({self.gen_expr(cond.expr, df)}.isna())"

    # email IS NOT NULL na (df["email"].notna())
    def _cond_is_not_null(self, cond, df) -> str:
        return f"({self.gen_expr(cond.expr, df)}.notna())"

    # name LIKE 'Jan%' na (df["name"].str.contains(r"^Jan.*$"))
    def _cond_like(self, cond, df) -> str:
        return f'({self.gen_expr(cond.expr, df)}.str.contains(r"{self._like_to_regex(cond.pattern)}"))'

    # name NOT LIKE 'Jan%' na (~df["name"].str.contains(r"^Jan.*$"))
    def _cond_not_like(self, cond, df) -> str:
        return f'(~{self.gen_expr(cond.expr, df)}.str.contains(r"{self._like_to_regex(cond.pattern)}"))'

    # city IN ('a', 'b') na (df["city"].isin(["a", "b"]))
    def _cond_in(self, cond, df) -> str:
        values = [self._gen_literal(v) for v in cond.values]
        return f'({self.gen_expr(cond.expr, df)}.isin([{", ".join(values)}]))'

    # city NOT IN ('a', 'b') na (~df["city"].isin(["a", "b"]))
    def _cond_not_in(self, cond, df) -> str:
        values = [self._gen_literal(v) for v in cond.values]
        return f'(~{self.gen_expr(cond.expr, df)}.isin([{", ".join(values)}]))'

    # age BETWEEN 18 AND 65 na (df["age"].between(18, 65))
    def _cond_between(self, cond, df) -> str:
        low = self.gen_expr(cond.low, df)
        high = self.gen_expr(cond.high, df)
        return f"({self.gen_expr(cond.expr, df)}.between({low}, {high}))"

    # age NOT BETWEEN 18 AND 65 na (~df["age"].between(18, 65))
    def _cond_not_between(self, cond, df) -> str:
        low = self.gen_expr(cond.low, df)
        high = self.gen_expr(cond.high, df)
        return f"(~{self.gen_expr(cond.expr, df)}.between({low}, {high}))"

    # a AND b na (a & b)
    def _cond_and(self, cond, df) -> str:
        return f"({self.gen_condition(cond.left, df)} & {self.gen_condition(cond.right, df)})"

    # a OR b na (a | b)
    def _cond_or(self, cond, df) -> str:
        return f"({self.gen_condition(cond.left, df)} | {self.gen_condition(cond.right, df)})"

    # NOT a na (~a)
    def _cond_not(self, cond, df) -> str:
        return f"(~{self.gen_condition(cond.cond, df)})"

    # instrukcje

    # SELECT: obsluguje joiny (pd.merge), potem deleguje do _gen_simple lub _gen_groupby
    def _gen_select(self, stmt) -> str:
        df = stmt.table.alias or stmt.table.name

        # JOIN na pd.merge, wynik staje sie nowym df
        if stmt.joins:
            lines = []
            current = stmt.table.name
            for join in stmt.joins:
                right_table = join.table.name
                right_alias = join.table.alias or right_table
                left_on, right_on = self._extract_join_keys(join.on, df, right_alias)
                lines.append(
                    f'_df = pd.merge({current}, {right_table}, left_on="{left_on}", right_on="{right_on}", how="{join.kind}")'
                )
                current = "_df"
            df = current
            lines.append(self._gen_select_body(stmt, df))
            return "\n".join(lines)

        return self._gen_select_body(stmt, df)

    # rozpoznaje czy SELECT ma agregacje
    def _gen_select_body(self, stmt, df) -> str:
        has_agg = stmt.columns and any(
            isinstance(item.expr, (nodes.AggStar, nodes.AggExpr))
            for item in stmt.columns
        )
        if has_agg or stmt.groupby:
            return self._gen_groupby(stmt, df)
        return self._gen_simple(stmt, df)

    # SELECT bez agregacji: WHERE -> kolumny -> DISTINCT -> ORDER BY -> LIMIT
    # np. SELECT name FROM users WHERE age > 18 -> users[(users["age"] > 18)][["name"]]
    def _gen_simple(self, stmt, df) -> str:
        base = df

        # WHERE  filtrowanie wierszy
        if stmt.where:
            base = f"{df}[{self.gen_condition(stmt.where, df)}]"

        # SELECT lista kolumn, jezeli sa wyrazenia obliczane to .assign()
        if stmt.columns:
            has_computed = any(
                not isinstance(item.expr, (nodes.ColExpr, nodes.QualifiedCol))
                for item in stmt.columns
            )
            if has_computed:
                assigns = {}
                col_names = []
                for item in stmt.columns:
                    if isinstance(item.expr, (nodes.ColExpr, nodes.QualifiedCol)):
                        col_names.append(item.alias or self._col_name(item.expr))
                    else:
                        alias = item.alias or f"_col{len(assigns)}"
                        assigns[alias] = self.gen_expr(item.expr, df)
                        col_names.append(alias)
                assign_str = ", ".join(f"{k}={v}" for k, v in assigns.items())
                cols_str = ", ".join(f'"{c}"' for c in col_names)
                base = f"{base}.assign({assign_str})[[{cols_str}]]"
            else:
                col_names = [
                    item.alias or self._col_name(item.expr) for item in stmt.columns
                ]
                cols_str = ", ".join(f'"{c}"' for c in col_names)
                base = f"{base}[[{cols_str}]]"

        # DISTINCT na .drop_duplicates()
        if stmt.distinct:
            base = f"{base}.drop_duplicates()"

        # ORDER BY na .sort_values()
        if stmt.orderby:
            base = self._apply_orderby(base, stmt.orderby)

        # LIMIT na .head(n)
        if stmt.limit is not None:
            base = f"{base}.head({stmt.limit})"

        return base

    # SELECT z GROUP BY lub funkcjami agregujacymi na .groupby().agg()
    # np. SELECT category, COUNT(*) FROM products GROUP BY category
    #  na products.groupby("category").agg(count=("category", "count")).reset_index()
    def _gen_groupby(self, stmt, df) -> str:
        base = df

        # WHERE przed grupowaniem
        if stmt.where:
            base = f"{df}[{self.gen_condition(stmt.where, df)}]"

        # GROUP BY klucze
        groupby_cols = [self._col_name(e) for e in stmt.groupby]
        if len(groupby_cols) == 1:
            groupby_str = f'"{groupby_cols[0]}"'
        else:
            groupby_str = "[" + ", ".join(f'"{c}"' for c in groupby_cols) + "]"

        # budujemy agg specs w formacie alias=(kolumna, funkcja)
        agg_parts = []
        for item in stmt.columns:
            if isinstance(item.expr, nodes.AggStar):
                alias = item.alias or "count"
                col = groupby_cols[0] if groupby_cols else "id"
                agg_parts.append(f'{alias}=("{col}", "count")')
            elif isinstance(item.expr, nodes.AggExpr):
                col = self._col_name(item.expr.expr)
                func = self._agg_func(item.expr.func)
                alias = item.alias or f"{func}_{col}"
                agg_parts.append(f'{alias}=("{col}", "{func}")')

        base = (
            f"{base}.groupby({groupby_str}).agg({', '.join(agg_parts)}).reset_index()"
        )

        # HAVING na filtrowanie wyniku grupowania, AggExpr mapujemy na alias z agg
        if stmt.having:
            having_df = "_grouped"
            cond = self._gen_having_condition(stmt.having.cond, having_df, stmt)
            lines = [
                f"{having_df} = {base}",
                f"{having_df} = {having_df}[{cond}]",
            ]
            base = "\n".join(lines)
            if stmt.orderby:
                base = self._apply_orderby(base, stmt.orderby)
            if stmt.limit is not None:
                base = f"{base}.head({stmt.limit})"
            return base

        if stmt.orderby:
            base = self._apply_orderby(base, stmt.orderby)
        if stmt.limit is not None:
            base = f"{base}.head({stmt.limit})"

        return base

    # HAVING condition: AggExpr zamieniamy na nazwe kolumny w zgrupowanym wyniku
    def _gen_having_condition(self, cond, df, stmt) -> str:
        if isinstance(cond, nodes.Compare):
            left = self._having_expr(cond.left, df, stmt)
            right = self._having_expr(cond.right, df, stmt)
            return f"({left} {cond.op} {right})"
        elif isinstance(cond, nodes.AndCond):
            l = self._gen_having_condition(cond.left, df, stmt)
            r = self._gen_having_condition(cond.right, df, stmt)
            return f"({l} & {r})"
        elif isinstance(cond, nodes.OrCond):
            l = self._gen_having_condition(cond.left, df, stmt)
            r = self._gen_having_condition(cond.right, df, stmt)
            return f"({l} | {r})"
        return self.gen_condition(cond, df)

    # szuka aliasu dla AggExpr w liscie kolumn SELECT, zeby HAVING mogl sie do niego odwolac
    def _having_expr(self, expr, df, stmt) -> str:
        if isinstance(expr, nodes.AggExpr):
            col = self._col_name(expr.expr)
            func = self._agg_func(expr.func)
            for item in stmt.columns:
                if isinstance(item.expr, nodes.AggExpr):
                    if (
                        self._col_name(item.expr.expr) == col
                        and self._agg_func(item.expr.func) == func
                    ):
                        alias = item.alias or f"{func}_{col}"
                        return f'{df}["{alias}"]'
            return f'{df}["{func}_{col}"]'
        elif isinstance(expr, nodes.AggStar):
            for item in stmt.columns:
                if isinstance(item.expr, nodes.AggStar):
                    return f'{df}["{item.alias or "count"}"]'
        return self.gen_expr(expr, df)

    # INSERT INTO na pd.concat z nowym DataFrame
    def _gen_insert(self, stmt) -> str:
        table = stmt.table.name
        rows = []
        for row in stmt.rows:
            if stmt.columns:
                pairs = ", ".join(
                    f'"{col}": {self._gen_literal(val)}'
                    for col, val in zip(stmt.columns, row)
                )
            else:
                # bez listy kolumn - indeksy pozycyjne jako klucze
                pairs = ", ".join(
                    f'"{i}": {self._gen_literal(v)}' for i, v in enumerate(row)
                )
            rows.append("{" + pairs + "}")
        rows_str = ", ".join(rows)
        return f"{table} = pd.concat([{table}, pd.DataFrame([{rows_str}])], ignore_index=True)"

    # UPDATE SET na df.loc[warunek, kolumna] = wartosc, lub df["col"] = val bez WHERE
    def _gen_update(self, stmt) -> str:
        table = stmt.table.name
        lines = []
        for col, expr in stmt.assignments:
            val = self.gen_expr(expr, table)
            if stmt.where:
                cond = self.gen_condition(stmt.where, table)
                lines.append(f'{table}.loc[{cond}, "{col}"] = {val}')
            else:
                lines.append(f'{table}["{col}"] = {val}')
        return "\n".join(lines)

    # DELETE FROM na df = df[~warunek], bez WHERE usuwa wszystkie wiersze
    def _gen_delete(self, stmt) -> str:
        table = stmt.table.name
        if stmt.where:
            cond = self.gen_condition(stmt.where, table)
            return f"{table} = {table}[~{cond}]"
        return f"{table} = {table}.iloc[0:0]"

    # pomocnicze

    # ORDER BY na .sort_values()
    def _apply_orderby(self, base, orderby) -> str:
        cols = [f'"{self._col_name(o.expr)}"' for o in orderby]
        ascs = [str(o.ascending) for o in orderby]
        if len(cols) == 1:
            return f"{base}.sort_values({cols[0]}, ascending={ascs[0]})"
        return f"{base}.sort_values([{', '.join(cols)}], ascending=[{', '.join(ascs)}])"

    # wyciaga left_on i right_on z warunku ON w JOIN
    def _extract_join_keys(self, on, left_alias, right_alias) -> tuple[str, str]:
        if isinstance(on, nodes.Compare) and on.op == "==":
            left = on.left
            right = on.right
            if isinstance(left, nodes.QualifiedCol) and isinstance(
                right, nodes.QualifiedCol
            ):
                if left.table == left_alias:
                    return left.column, right.column
                else:
                    return right.column, left.column
        raise ValueError(f"nieobslugiwany warunek JOIN ON: {on}")

    # zwraca nazwe kolumny z ColExpr lub QualifiedCol
    def _col_name(self, expr) -> str:
        if isinstance(expr, nodes.ColExpr):
            return expr.name
        elif isinstance(expr, nodes.QualifiedCol):
            return expr.column
        raise ValueError(f"oczekiwano kolumny: {type(expr)}")

    # mapuje nazwy funkcji agregacji SQL na nazwy funkcji pandas
    def _agg_func(self, func) -> str:
        mapping = {
            "COUNT": "count",
            "SUM": "sum",
            "AVG": "mean",
            "MIN": "min",
            "MAX": "max",
        }
        return mapping[func] if func in mapping else func.lower()

    # zwraca liczbe lub string jako pythonowy literal
    def _gen_literal(self, expr) -> str:
        if isinstance(expr, nodes.NumberLiteral):
            return expr.value
        elif isinstance(expr, nodes.StringLiteral):
            return f'"{self._strip_quotes(expr.value)}"'
        raise ValueError(f"nieznany literal: {type(expr)}")

    # usuwa cudzyslowia z literalow sql ('napis' na napis)
    def _strip_quotes(self, s) -> str:
        if len(s) >= 2 and s[0] in ("'", '"') and s[-1] == s[0]:
            return s[1:-1]
        return s

    # zamienia wzorzec SQL LIKE na regex pythonowy, % na .*, _ na .
    def _like_to_regex(self, pattern) -> str:
        s = self._strip_quotes(pattern)
        s = re.escape(s)
        s = s.replace(re.escape("%"), ".*").replace(re.escape("_"), ".")
        return f"^{s}$"
