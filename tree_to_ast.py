from lark import Token, Transformer

import ast_nodes as nodes


# bierze drzewo Larka
# i zamienia je na obiekty z ast_nodes.py

# jedna funkcja = jedna regula
class TreeToAST(Transformer):

    # NAME -> col
    def col(self, items):
        name = items[0]
        return nodes.ColExpr(name=str(name))

    # qualified_col: NAME "." NAME
    def qualified_col(self, items):
        table = items[0]
        column = items[1]
        return nodes.QualifiedCol(table=str(table), column=str(column))

    # NUMBER -> number
    def number(self, items):
        value = items[0]
        return nodes.NumberLiteral(value=str(value))

    # STRING -> string
    def string(self, items):
        value = items[0]
        return nodes.StringLiteral(value=str(value))

    # add_expr "+" mul_expr -> add
    def add(self, items):
        left = items[0]
        right = items[1]
        return nodes.BinOp(op="+", left=left, right=right)

    # add_expr "-" mul_expr -> sub
    def sub(self, items):
        left = items[0]
        right = items[1]
        return nodes.BinOp(op="-", left=left, right=right)

    # mul_expr "*" unary_expr -> mul
    def mul(self, items):
        left = items[0]
        right = items[1]
        return nodes.BinOp(op="*", left=left, right=right)

    # mul_expr "/" unary_expr -> div
    def div(self, items):
        left = items[0]
        right = items[1]
        return nodes.BinOp(op="/", left=left, right=right)

    # "-" primary_expr -> neg
    def neg(self, items):
        expr = items[0]
        return nodes.Neg(expr=expr)

    # AGG_FUNC "(" "*" ")" -> agg_star
    def agg_star(self, items):
        func = items[0]
        return nodes.AggStar(func=str(func).upper())

    # AGG_FUNC "(" expr ")" -> agg_expr
    def agg_expr(self, items):
        func = items[0]
        expr = items[1]
        return nodes.AggExpr(func=str(func).upper(), expr=expr)

    # warunkowe

    # expr comp_op expr -> compare
    def compare(self, items):
        left = items[0]
        op = items[1]
        right = items[2]
        return nodes.Compare(op=op, left=left, right=right)

    # comp_op: "=" -> eq
    def eq(self, items):
        return "=="

    # comp_op: "!=" | "<>" -> neq
    def neq(self, items):
        return "!="

    # comp_op: "<" -> lt
    def lt(self, items):
        return "<"

    # comp_op: ">" -> gt
    def gt(self, items):
        return ">"

    # comp_op: "<=" -> lte
    def lte(self, items):
        return "<="

    # comp_op: ">=" -> gte
    def gte(self, items):
        return ">="

    # expr "IS"i "NULL"i -> is_null
    def is_null(self, items):
        expr = items[0]
        return nodes.IsNull(expr=expr)

    # expr "IS"i "NOT"i "NULL"i -> is_not_null
    def is_not_null(self, items):
        expr = items[0]
        return nodes.IsNotNull(expr=expr)

    # expr "LIKE"i STRING -> like_cond
    def like_cond(self, items):
        expr = items[0]
        pattern = items[1]
        return nodes.LikeCond(expr=expr, pattern=str(pattern))

    # expr "NOT"i "LIKE"i STRING -> not_like
    def not_like(self, items):
        expr = items[0]
        pattern = items[1]
        return nodes.NotLike(expr=expr, pattern=str(pattern))

    # expr "IN"i "(" value_list ")" -> in_cond
    def in_cond(self, items):
        expr = items[0]
        values = items[1]
        return nodes.InCond(expr=expr, values=values)

    # expr "NOT"i "IN"i "(" value_list ")" -> not_in
    def not_in(self, items):
        expr = items[0]
        values = items[1]
        return nodes.NotIn(expr=expr, values=values)

    # expr "BETWEEN"i expr "AND"i expr -> between_cond
    def between_cond(self, items):
        expr = items[0]
        low = items[1]
        high = items[2]
        return nodes.Between(expr=expr, low=low, high=high)

    # expr "NOT"i "BETWEEN"i expr "AND"i expr -> not_between
    def not_between(self, items):
        expr = items[0]
        low = items[1]
        high = items[2]
        return nodes.NotBetween(expr=expr, low=low, high=high)

    # and_expr "AND"i not_expr -> and_cond
    def and_cond(self, items):
        left = items[0]
        right = items[1]
        return nodes.AndCond(left=left, right=right)

    # or_expr "OR"i and_expr -> or_cond
    def or_cond(self, items):
        left = items[0]
        right = items[1]
        return nodes.OrCond(left=left, right=right)

    # "NOT"i not_expr -> not_cond
    def not_cond(self, items):
        cond = items[0]
        return nodes.NotCond(cond=cond)

    # value_list: literal ("," literal)*
    def value_list(self, items):
        return list(items)

    # elementy select

    # select_item: expr "AS"i NAME | expr
    def select_item(self, items):
        if len(items) == 2:
            expr = items[0]
            alias = items[1]
            return nodes.SelectItem(expr=expr, alias=str(alias))
        expr = items[0]
        return nodes.SelectItem(expr=expr)

    # select_list: "*" -> star
    def star(self, items):
        return []

    # select_list: "*" -> star | select_item ("," select_item)*
    def select_list(self, items):
        if items and isinstance(items[0], list):
            return []  # star
        return list(items)

    # table_ref: NAME ["AS"i NAME]
    def table_ref(self, items):
        if len(items) == 2 and items[1] is not None:
            name = items[0]
            alias = items[1]
            return nodes.TableRef(name=str(name), alias=str(alias))
        name = items[0]
        return nodes.TableRef(name=str(name))

    # join_clause: join_type "JOIN"i table_ref "ON"i condition
    def join_clause(self, items):
        kind = items[0]
        table = items[1]
        on = items[2]
        return nodes.JoinClause(kind=kind, table=table, on=on)

    # join_type: "INNER"i -> inner_join
    def inner_join(self, items):
        return "inner"

    # join_type: "LEFT"i -> left_join
    def left_join(self, items):
        return "left"

    # join_type: "RIGHT"i -> right_join
    def right_join(self, items):
        return "right"

    # join_type: "FULL"i -> full_join
    def full_join(self, items):
        return "outer"

    # where_clause: "WHERE"i condition
    def where_clause(self, items):
        condition = items[0]
        return condition

    # groupby_clause: "GROUP"i "BY"i expr ("," expr)*
    def groupby_clause(self, items):
        return list(items)

    # having_clause: "HAVING"i condition
    def having_clause(self, items):
        condition = items[0]
        return condition

    # orderby_clause: "ORDER"i "BY"i order_item ("," order_item)*
    def orderby_clause(self, items):
        return list(items)

    # order_item: expr ["ASC"i] -> asc
    def asc(self, items):
        expr = items[0]
        return nodes.OrderItem(expr=expr, ascending=True)

    # order_item: expr "DESC"i -> desc
    def desc(self, items):
        expr = items[0]
        return nodes.OrderItem(expr=expr, ascending=False)

    # limit_clause: "LIMIT"i INTEGER
    def limit_clause(self, items):
        n = items[0]
        return int(str(n))

    # instrukcje

    # select_stmt: "SELECT"i distinct? select_list "FROM"i table_ref join_clause* where_clause? groupby_clause? having_clause? orderby_clause? limit_clause?
    def select_stmt(self, items):
        distinct = False
        columns = None
        table = None
        joins = []
        where = None
        groupby = []
        having = None
        orderby = []
        limit = None

        condition_types = (
            nodes.Compare,
            nodes.IsNull,
            nodes.IsNotNull,
            nodes.LikeCond,
            nodes.NotLike,
            nodes.InCond,
            nodes.NotIn,
            nodes.Between,
            nodes.NotBetween,
            nodes.AndCond,
            nodes.OrCond,
            nodes.NotCond,
        )

        # lark zwraca wszystkie klauzule jako plaska lista, rozrozniamy je po typie
        for item in items:
            if isinstance(item, bool):
                # distinct zwraca True, brak distinct nie trafia tutaj w ogole
                distinct = item
            elif isinstance(item, list) and columns is None:
                # select_list zwraca liste SelectItem albo [] dla *, bierzemy pierwszy trafiony
                columns = item
            elif isinstance(item, nodes.TableRef) and table is None:
                # pierwsza TableRef to FROM, kolejne sa juz opakowane w JoinClause
                table = item
            elif isinstance(item, nodes.JoinClause):
                joins.append(item)
            elif isinstance(item, condition_types) and where is None:
                # pierwsze condition to WHERE
                where = item
            elif isinstance(item, condition_types):
                # drugie condition to HAVING, bo where jest juz ustawione
                having = item
            elif isinstance(item, list) and all(isinstance(o, nodes.OrderItem) for o in item):
                # orderby sprawdzamy przed groupby bo oba sa lista, OrderItem je rozroznia
                orderby = item
            elif isinstance(item, list) and len(item) > 0:
                # groupby to lista Expr, nie OrderItem
                groupby = item
            elif isinstance(item, int):
                limit = item

        return nodes.SelectStmt(
            distinct=distinct,
            columns=columns if columns is not None else [],
            table=table,
            joins=joins,
            where=where,
            groupby=groupby,
            having=having,
            orderby=orderby,
            limit=limit,
        )

    # distinct: "DISTINCT"i
    def distinct(self, items):
        return True

    # insert_stmt: "INSERT"i "INTO"i table_ref ["(" column_list ")"] "VALUES"i "(" value_list ")" ("," "(" value_list ")")*
    def insert_stmt(self, items):
        table = items[0]
        rest = [i for i in items[1:] if i is not None]
        if (
            rest
            and isinstance(rest[0], list)
            and rest[0]
            and isinstance(rest[0][0], str)
        ):
            columns = rest[0]
            rows = [list(r) for r in rest[1:]]
        else:
            columns = []
            rows = [list(r) for r in rest]
        return nodes.InsertStmt(table=table, columns=columns, rows=rows)

    # column_list: NAME ("," NAME)*
    def column_list(self, items):
        return [str(i) for i in items]

    # assign_list: assign_item ("," assign_item)*
    def assign_list(self, items):
        return list(items)

    # assign_item: NAME "=" expr
    def assign_item(self, items):
        name = items[0]
        expr = items[1]
        return (str(name), expr)

    # update_stmt: "UPDATE"i table_ref "SET"i assign_list where_clause?
    def update_stmt(self, items):
        table = items[0]
        assignments = items[1]
        where = items[2] if len(items) > 2 else None
        return nodes.UpdateStmt(table=table, assignments=assignments, where=where)

    # delete_stmt: "DELETE"i "FROM"i table_ref where_clause?
    def delete_stmt(self, items):
        table = items[0]
        where = items[1] if len(items) > 1 else None
        return nodes.DeleteStmt(table=table, where=where)

    # start: stmt
    def start(self, items):
        stmt = items[0]
        return stmt
