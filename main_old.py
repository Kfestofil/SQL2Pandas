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


def run_query(sql, parser, transformer, generator, active_dataframes) -> "pd.DataFrame | None":
  sql = sql.rstrip(";")
  try:
    tree = parser.parse(sql)
    ast = transformer.transform(tree)
    code = generator.gen(ast)
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
      print(code)
      return res if isinstance(res, pd.DataFrame) else None
    else:
      exec(code, {"pd": pd, **active_dataframes}, active_dataframes)
      print(code)
  except Exception as e:
    print(f"blad: {e}")
  return None


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
  last_result: pd.DataFrame | None = None
  print(f"zaladowane tabele: {', '.join(active_dataframes.keys())}")
  while True:
    try:
      prompt = "podaj sql (wyjscie q, eksport e): " if sys.stdin.isatty() else ""
      sql = input(prompt).strip()
    except EOFError:
      break
    if sql == "q":
      break
    if sql == "e":
      if last_result is None:
        print("brak wynikow do eksportu")
      else:
        _export_df(last_result)
      print()
      continue
    if not sql or sql.startswith("--"):
      continue
    result = run_query(sql, parser, transformer, generator, active_dataframes)
    if result is not None:
      last_result = result
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

  if not args.i and not args.f and sys.stdin.isatty():
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
    repl(active_dataframes)