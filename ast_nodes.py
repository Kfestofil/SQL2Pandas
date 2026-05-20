from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# wyrazenia


@dataclass
class ColExpr:
    name: str


@dataclass
class QualifiedCol:
    table: str
    column: str


@dataclass
class NumberLiteral:
    value: str


@dataclass
class StringLiteral:
    value: str


# '+', '-', '*', '/'
@dataclass
class BinOp:
    op: str
    left: Expr
    right: Expr


@dataclass
class Neg:
    expr: Expr


@dataclass
class AggStar:
    func: str  # COUNT


@dataclass
class AggExpr:
    func: str  # COUNT, SUM, AVG, MIN, MAX
    expr: Expr


Expr = (
    ColExpr
    | QualifiedCol
    | NumberLiteral
    | StringLiteral
    | BinOp
    | Neg
    | AggStar
    | AggExpr
)


# warunkowe


@dataclass
class Compare:
    op: str  # '==', '!=', '<', '>', '<=', '>='
    left: Expr
    right: Expr


@dataclass
class IsNull:
    expr: Expr


@dataclass
class IsNotNull:
    expr: Expr


@dataclass
class LikeCond:
    expr: Expr
    pattern: str


@dataclass
class NotLike:
    expr: Expr
    pattern: str


# in (x1, x2, ...)
@dataclass
class InCond:
    expr: Expr
    values: list[Expr]


# not in (x1, x2, ...)
@dataclass
class NotIn:
    expr: Expr
    values: list[Expr]


@dataclass
class Between:
    expr: Expr
    low: Expr
    high: Expr


@dataclass
class NotBetween:
    expr: Expr
    low: Expr
    high: Expr


@dataclass
class AndCond:
    left: Condition
    right: Condition


@dataclass
class OrCond:
    left: Condition
    right: Condition


@dataclass
class NotCond:
    cond: Condition


Condition = (
    Compare
    | IsNull
    | IsNotNull
    | LikeCond
    | NotLike
    | InCond
    | NotIn
    | Between
    | NotBetween
    | AndCond
    | OrCond
    | NotCond
)


# klauzula having (wrapper zeby odroznic od where podczas parsowania)
@dataclass
class Having:
    cond: Condition


# elementy z select


# jedna kolumna z select
@dataclass
class SelectItem:
    expr: Expr
    alias: Optional[str] = None


# nazwa tabeli z opcjonalnym aliasem
@dataclass
class TableRef:
    name: str
    alias: Optional[str] = None


@dataclass
class JoinClause:
    kind: str  # 'inner', 'left', 'right', 'outer'
    table: TableRef
    on: Condition


@dataclass
class OrderItem:
    expr: Expr
    ascending: bool = True


# instrukcje


@dataclass
class SelectStmt:
    distinct: bool
    columns: list[SelectItem]
    table: TableRef
    joins: list[JoinClause] = field(default_factory=list)
    where: Optional[Condition] = None
    groupby: list[Expr] = field(default_factory=list)
    having: Optional[Having] = None
    orderby: list[OrderItem] = field(default_factory=list)
    limit: Optional[int] = None


@dataclass
class InsertStmt:
    table: TableRef
    columns: list[str]  # pusta lista = wszystkie kolumny z VALUES
    rows: list[list[Expr]]


@dataclass
class UpdateStmt:
    table: TableRef
    assignments: list[tuple[str, Expr]]
    where: Optional[Condition] = None


@dataclass
class DeleteStmt:
    table: TableRef
    where: Optional[Condition] = None


Stmt = SelectStmt | InsertStmt | UpdateStmt | DeleteStmt
