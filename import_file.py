from pathlib import Path

import pandas as pd
from lark import Lark

from ast_to_pandas import ASTToPandas
from ast_nodes import CreateStmt, InsertStmt
from tree_to_ast import TreeToAST


def _make_pipeline(grammar_path: Path):
    parser = Lark(grammar_path.read_text(), start="start", parser="earley")
    transformer = TreeToAST()
    generator = ASTToPandas()
    return parser, transformer, generator


def _load_csv(path: Path) -> dict[str, pd.DataFrame]:
    name = path.stem
    df = pd.read_csv(path)
    print(f"zaladowano {path} jako tabele '{name}' ({len(df)} wierszy)")
    return {name: df}


def _load_sql(path: Path, grammar_path: Path) -> dict[str, pd.DataFrame]:
    parser, transformer, generator = _make_pipeline(grammar_path)
    active_dataframes: dict[str, pd.DataFrame] = {}

    for line in path.read_text().splitlines():
        sql = line.strip().rstrip(";")
        if not sql or sql.startswith("--"):
            continue
        try:
            ast = transformer.transform(parser.parse(sql))
            code = generator.gen(ast)
            # CREATE i INSERT modyfikuja active_dataframes
            if isinstance(ast, (CreateStmt, InsertStmt)):
                exec(code, {"pd": pd, **active_dataframes}, active_dataframes)
                if isinstance(ast, CreateStmt):
                    print(f"utworzono tabele '{ast.table}'")
        except Exception:
            # pomijamy linie ktorych nie umiemy sparsowac (np. DROP, ALTER, komentarze blokowe)
            pass

    for name, df in active_dataframes.items():
        print(f"tabela '{name}': {len(df)} wierszy")

    return active_dataframes


def load(path_str: str, grammar_path: Path) -> dict[str, pd.DataFrame]:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"plik nie istnieje: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _load_csv(path)
    elif suffix in (".sql", ".dump"):
        return _load_sql(path, grammar_path)
    else:
        raise ValueError(f"nieznane rozszerzenie: {suffix} (obslugiwane: .csv, .sql, .dump)")
