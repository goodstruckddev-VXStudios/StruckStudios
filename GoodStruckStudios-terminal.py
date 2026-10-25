
#!/usr/bin/env python3
"""STRUCKSTUDIOS Terminal — by GoodStruckdDev."""

import ast
import datetime
import math
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "STRUCKSTUDIOS Terminal"
VERSION = "1.0.0"
PROMPT = "STRUCKSTUDIOS /$ "
history = []


def calculate(expression):
    """Safely evaluate basic mathematical expressions."""
    allowed = (
        ast.Expression, ast.Constant, ast.BinOp, ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.Load,
    )

    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise ValueError("Only basic mathematical expressions are allowed.")
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Numbers only.")
            if abs(node.value) > 10**100:
                raise ValueError("Number is too large.")
        if isinstance(node, ast.Pow) and isinstance(node, ast.Constant):
            pass

    result = eval(compile(tree, "<calculator>", "eval"), {"__builtins__": {}}, {})
    if isinstance(result, (int, float)) and abs(result) > 10**100:
        raise ValueError("Result is too large.")
    return result


def help_menu():
    print("""
Commands:
  help                  Show this help
  version               Show version
  clear                 Clear the terminal
  exit                  Exit STRUCKSTUDIOS Terminal
  date                  Show today's date
  time                  Show current time
  sysinfo               Show system information
  pwd                   Show current folder
  ls [folder]           List files
  cd <folder>           Change folder
  mkdir <folder>        Create a folder
  touch <file>          Create an empty file
  cat <file>            Display a text file
  write <file> <text>   Write text to a file
  rm <file>             Delete a file
  cp <source> <dest>    Copy a file
  mv <source> <dest>    Move a file
  rename <old> <new>    Rename a file
  calc <expression>     Calculate a math expression
  count <file>          Count lines and words
  find <text> <file>    Search for text in a file
  history               Show previous commands
  run <script.py>       Run a Python script
""")


def main():
    print("=" * 42)
    print(APP_NAME)
    print("Created by GoodStruckdDev")
    print(f"Version {VERSION}")
    print("Type 'help' to see available commands.")
    print("=" * 42)

    while True:
        try:
            command_line = input(PROMPT).strip()
            if not command_line:
                continue

            history.append(command_line)
            parts = command_line.split()
            command = parts[0].lower()
            args = parts[1:]

            if command in ("exit", "quit"):
                print("Goodbye!")
                break

            elif command == "help":
                help_menu()

            elif command == "version":
                print(f"{APP_NAME} v{VERSION}")

            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif command == "date":
                print(datetime.date.today().isoformat())

            elif command == "time":
                print(datetime.datetime.now().strftime("%H:%M:%S"))

            elif command == "sysinfo":
                print("System:", platform.system())
                print("Release:", platform.release())
                print("Python:", platform.python_version())
                print("Architecture:", platform.machine())
                print("Working folder:", Path.cwd())

            elif command == "pwd":
                print(Path.cwd())

            elif command == "ls":
                folder = Path(args[0]).expanduser() if args else Path.cwd()
                for item in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
                    suffix = "/" if item.is_dir() else ""
                    print(item.name + suffix)

            elif command == "cd":
                if not args:
                    print("Usage: cd <folder>")
                else:
                    os.chdir(Path(" ".join(args)).expanduser())

            elif command == "mkdir":
                if not args:
                    print("Usage: mkdir <folder>")
                else:
                    Path(" ".join(args)).expanduser().mkdir(parents=True, exist_ok=False)
                    print("Folder created.")

            elif command == "touch":
                if not args:
                    print("Usage: touch <file>")
                else:
                    Path(" ".join(args)).expanduser().touch(exist_ok=True)
                    print("File ready.")

            elif command == "cat":
                if not args:
                    print("Usage: cat <file>")
                else:
                    print(Path(" ".join(args)).expanduser().read_text(encoding="utf-8"))

            elif command == "write":
                if len(args) < 2:
                    print("Usage: write <file> <text>")
                else:
                    file_path = Path(args[0]).expanduser()
                    file_path.write_text(" ".join(args[1:]) + "\n", encoding="utf-8")
                    print("File saved.")

            elif command == "rm":
                if not args:
                    print("Usage: rm <file>")
                else:
                    file_path = Path(" ".join(args)).expanduser()
                    if file_path.is_dir():
                        print("Use a file path, not a folder.")
                    else:
                        file_path.unlink()
                        print("File deleted.")

            elif command == "cp":
                if len(args) != 2:
                    print("Usage: cp <source> <destination>")
                else:
                    shutil.copy2(Path(args[0]).expanduser(),
                                 Path(args[1]).expanduser())
                    print("File copied.")

            elif command == "mv":
                if len(args) != 2:
                    print("Usage: mv <source> <destination>")
                else:
                    shutil.move(str(Path(args[0]).expanduser()),
                                str(Path(args[1]).expanduser()))
                    print("File moved.")

            elif command == "rename":
                if len(args) != 2:
                    print("Usage: rename <old> <new>")
                else:
                    Path(args[0]).expanduser().rename(Path(args[1]).expanduser())
                    print("Renamed.")

            elif command == "calc":
                if not args:
                    print("Usage: calc <expression>")
                else:
                    print(calculate(" ".join(args)))

            elif command == "count":
                if not args:
                    print("Usage: count <file>")
                else:
                    content = Path(" ".join(args)).expanduser().read_text(
                        encoding="utf-8"
                    )
                    print("Lines:", len(content.splitlines()))
                    print("Words:", len(content.split()))
                    print("Characters:", len(content))

            elif command == "find":
                if len(args) < 2:
                    print("Usage: find <text> <file>")
                else:
                    term = args[0]
                    file_path = Path(" ".join(args[1:])).expanduser()
                    matches = [
                        (number, line.rstrip())
                        for number, line in enumerate(
                            file_path.read_text(encoding="utf-8").splitlines(), 1
                        )
                        if term.casefold() in line.casefold()
                    ]
                    for number, line in matches:
                        print(f"{number}: {line}")
                    print(f"{len(matches)} matching line(s).")

            elif command == "history":
                for number, entry in enumerate(history, 1):
                    print(f"{number}: {entry}")

            elif command == "run":
                if not args:
                    print("Usage: run <script.py>")
                else:
                    script = Path(" ".join(args)).expanduser().resolve()
                    if not script.is_file() or script.suffix != ".py":
                        print("Please provide an existing .py file.")
                    else:
                        subprocess.run([sys.executable, str(script)], check=False)

            else:
                print(f"Unknown command: {command}. Type 'help'.")

        except KeyboardInterrupt:
            print("\nUse 'exit' to close the terminal.")
        except (OSError, ValueError, SyntaxError, ZeroDivisionError) as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
