import argparse
import pickle
import sys
from pathlib import Path

import pandas as pd
from lark import Lark

from ast_nodes import SelectStmt
from ast_to_pandas import ASTToPandas
from import_file import load
from tree_to_ast import TreeToAST

GRAMMAR = Path(__file__).parent / "sql.lark"


def make_parser() -> Lark:
    return Lark(GRAMMAR.read_text(), start="start", parser="earley")


def run_query(
    sql, parser, transformer, generator, active_dataframes, translate_only=False
) -> "tuple[pd.DataFrame | None, str | None]":
    sql = sql.rstrip(";")
    try:
        tree = parser.parse(sql)
        ast = transformer.transform(tree)
        if isinstance(ast, list):
            if not ast:
                print("blad: puste zapytanie")
                return None, None
            ast = ast[0]
        code = generator.gen(ast)

        print("# --- wygenerowany kod pandas ---")
        print(code)
        print("# --------------------------------")

        if translate_only:
            return None, code

        if isinstance(ast, SelectStmt):
            local = {}
            g = {"pd": pd, **active_dataframes}
            lines = code.split("\n")
            if len(lines) > 1:
                exec("\n".join(lines[:-1]), g, local)
                exec(f"_result = {lines[-1]}", {**g, **local}, local)
            else:
                exec(f"_result = {code}", g, local)
            res = local.get("_result")
            if isinstance(res, pd.DataFrame):
                print(res.to_string(index=False))
            return res if isinstance(res, pd.DataFrame) else None, code
        else:
            exec(code, {"pd": pd, **active_dataframes}, active_dataframes)
            return None, code
    except Exception as e:
        print(f"blad: {e}")
    return None, None


def _export_df(df: pd.DataFrame):
    try:
        path_str = input("nazwa pliku (.csv lub .pkl): ").strip()
    except EOFError:
        return
    if not path_str:
        return
    p = Path(path_str)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        df.to_csv(p, index=False)
        print(f"zapisano do {p}")
    elif suffix == ".pkl":
        with open(p, "wb") as f:
            pickle.dump(df, f)
        print(f"zapisano do {p}")
    else:
        print(f"blad: nieznane rozszerzenie {suffix} (obslugiwane: .csv, .pkl)")


def _save_code(snippets: list[str], path: Path | None = None):
    if path is None:
        try:
            path_str = input("nazwa pliku .py: ").strip()
        except EOFError:
            return
        if not path_str:
            return
        path = Path(path_str)
    path.write_text("\n\n".join(snippets), encoding="utf-8")
    print(f"kod zapisano do {path}")


def run_file(path, active_dataframes, translate_only=False) -> list[str]:
    parser = make_parser()
    transformer = TreeToAST()
    generator = ASTToPandas()
    collected: list[str] = []
    for sql in Path(path).read_text().splitlines():
        sql = sql.strip()
        if not sql or sql.startswith("--"):
            continue
        _, code = run_query(
            sql, parser, transformer, generator, active_dataframes,
            translate_only=translate_only,
        )
        if code:
            collected.append(code)
        print()
    return collected


def repl(active_dataframes, translate_only=False):
    parser = make_parser()
    transformer = TreeToAST()
    generator = ASTToPandas()
    last_result: pd.DataFrame | None = None
    session_code: list[str] = []

    tryb = "tlumaczenie" if translate_only else "wykonanie"
    tabele = ", ".join(active_dataframes.keys()) or "(brak)"
    print(f"zaladowane tabele: {tabele} | tryb: {tryb}")
    print("komendy: q=wyjscie  e=eksport danych  c=zapis kodu sesji")

    while True:
        try:
            prompt = "sql> " if sys.stdin.isatty() else ""
            sql = input(prompt).strip()
        except EOFError:
            break
        if sql == "q":
            break
        if sql == "e":
            if translate_only:
                print("tryb tlumaczenia: brak danych do eksportu")
            elif last_result is None:
                print("brak wynikow do eksportu")
            else:
                _export_df(last_result)
            print()
            continue
        if sql == "c":
            if not session_code:
                print("brak kodu do zapisania")
            else:
                _save_code(session_code)
            print()
            continue
        if not sql or sql.startswith("--"):
            continue
        result, code = run_query(
            sql, parser, transformer, generator, active_dataframes,
            translate_only=translate_only,
        )
        if result is not None:
            last_result = result
        if code is not None:
            session_code.append(code)
        print()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Interpreter SQL -> pandas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "przyklady:\n"
            "  %(prog)s -i dane.csv                     # REPL z danymi\n"
            "  %(prog)s -t                               # REPL, tylko tlumaczenie\n"
            "  %(prog)s -f kwerendy.sql -i dane.csv      # wykonaj plik SQL\n"
            "  %(prog)s -f kwerendy.sql -c wynik.py      # przetlumacz plik, zapisz kod\n"
            "  %(prog)s -t -f kwerendy.sql -c wynik.py  # tlumacz bez wykonania\n"
        ),
    )
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
    arg_parser.add_argument(
        "-c",
        metavar="plik.py",
        help="zapisz wygenerowany kod pandas do pliku .py (dziala z -f)",
    )
    arg_parser.add_argument(
        "-t", "--translate",
        action="store_true",
        help="tylko tlumacz SQL na pandas, bez wykonania",
    )
    args = arg_parser.parse_args()

    # pokaż pomoc jeśli nie ma żadnych sensownych argumentów
    if not args.i and not args.f and not args.translate and sys.stdin.isatty():
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

    collected_code: list[str] = []

    if args.f:
        collected_code = run_file(args.f, active_dataframes, translate_only=args.translate)

    if args.c:
        if collected_code:
            _save_code(collected_code, Path(args.c))
        else:
            print("brak kodu do zapisania (uzyj -f zeby podac plik SQL)")

    if args.o:
        if args.translate:
            print("ostrzezenie: -o ignorowane w trybie tlumaczenia (-t)")
        else:
            p = Path(args.o)
            suffix = p.suffix.lower()
            if suffix == ".pkl":
                with open(p, "wb") as f:
                    pickle.dump(active_dataframes, f)
                print(f"zapisano {list(active_dataframes.keys())} -> {p}")
            elif suffix == ".csv":
                if len(active_dataframes) == 1:
                    name, df = next(iter(active_dataframes.items()))
                    df.to_csv(p, index=False)
                    print(f"zapisano {name} -> {p}")
                else:
                    for name, df in active_dataframes.items():
                        out = p.parent / f"{p.stem}_{name}.csv"
                        df.to_csv(out, index=False)
                        print(f"zapisano {name} -> {out}")
            else:
                print(f"blad: nieznane rozszerzenie {suffix} (obslugiwane: .csv, .pkl)")
                sys.exit(1)
    else:
        repl(active_dataframes, translate_only=args.translate)