import argparse
import sys
from pathlib import Path

import pandas as pd
from lark import Lark

from ast_to_pandas import ASTToPandas
from import_file import load
from tree_to_ast import TreeToAST

GRAMMAR = Path(__file__).parent / "sql.lark"


def make_parser() -> Lark:
    return Lark(GRAMMAR.read_text(), start="start", parser="earley")


def run_query(sql, parser, transformer, generator, active_dataframes):
    try:
        tree = parser.parse(sql)
        ast = transformer.transform(tree)
        code = generator.gen(ast)
        try:
            local = {}
            exec(f"_result = {code}", {"pd": pd, **active_dataframes}, local)
            res = local.get("_result")
            if isinstance(res, pd.DataFrame):
                print(res.to_string(index=False))
                print(code)
                return
        except SyntaxError:
            pass
        exec(code, {"pd": pd, **active_dataframes}, active_dataframes)
        print(code)
    except Exception as e:
        print(f"blad: {e}")


def run_file(path, active_dataframes):
    parser = make_parser()
    transformer = TreeToAST()
    generator = ASTToPandas()
    queries = Path(path).read_text().splitlines()
    for sql in queries:
        sql = sql.strip()
        if not sql or sql.startswith("--"):
            continue
        run_query(sql, parser, transformer, generator, active_dataframes)
        print()


def repl(active_dataframes):
    parser = make_parser()
    transformer = TreeToAST()
    generator = ASTToPandas()
    print(f"zaladowane tabele: {', '.join(active_dataframes.keys())}")
    while True:
        try:
            prompt = "podaj sql (wyjscie q): " if sys.stdin.isatty() else ""
            sql = input(prompt).strip()
        except EOFError:
            break
        if sql == "q":
            break
        if not sql or sql.startswith("--"):
            continue
        run_query(sql, parser, transformer, generator, active_dataframes)
        print()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", metavar="plik.sql", help="plik z komendami SQL")
    arg_parser.add_argument(
        "-i",
        metavar="plik",
        action="append",
        help="wczytaj dane (.csv lub .sql/.dump), mozna podac wiele razy",
    )
    arg_parser.add_argument(
        "-o",
        metavar="plik",
        help="eksportuj tabele po wykonaniu (.csv lub .pkl)",
    )
    args = arg_parser.parse_args()

    if not args.i and not args.f:
        arg_parser.print_help()
        sys.exit(0)

    active_dataframes = {}

    if args.i:
        for file_path in args.i:
            try:
                active_dataframes.update(load(file_path, GRAMMAR))
            except (FileNotFoundError, ValueError) as e:
                print(f"blad: {e}")
                sys.exit(1)
        print()

    if args.f:
        run_file(args.f, active_dataframes)

    if args.o:
        p = Path(args.o)
        suffix = p.suffix.lower()
        for name, df in active_dataframes.items():
            if suffix == ".csv":
                out = p.parent / f"{name}.csv"
                df.to_csv(out, index=False)
            elif suffix == ".pkl":
                out = p.parent / f"{name}.pkl"
                df.to_pickle(out)
            else:
                print(f"blad: nieznane rozszerzenie {suffix} (obslugiwane: .csv, .pkl)")
                sys.exit(1)
            print(f"zapisano {name} -> {out}")
        sys.exit(0)

    repl(active_dataframes)
