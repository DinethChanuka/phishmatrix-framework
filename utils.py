import os
import sys
import sqlite3
from colorama import init, Fore, Style
from pyfiglet import Figlet
from rich.console import Console
from rich.text import Text

init(autoreset=True)
console = Console()

DB_NAME = "phishmatrix.db"


def get_db():
    """Return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def banner():
    """Display colorful ASCII art banner."""
    f = Figlet(font="slant")
    ascii_art = f.renderText("PhishMatrix")
    gradient = Text(ascii_art)
    gradient.stylize("bold cyan")
    console.print(gradient)
    console.print("[yellow]         Framework by Mikey[/yellow]\n")
    print(
        Fore.RED
        + "[!] EDUCATIONAL PURPOSE ONLY. Unauthorized use is illegal.\n"
        + Style.RESET_ALL
    )


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def color_input(prompt):
    return input(Fore.CYAN + prompt + Style.RESET_ALL)


def success(msg):
    print(Fore.GREEN + "[+] " + msg + Style.RESET_ALL)


def error(msg):
    print(Fore.RED + "[-] " + msg + Style.RESET_ALL)


def info(msg):
    print(Fore.YELLOW + "[*] " + msg + Style.RESET_ALL)


def ask_yes_no(prompt):
    while True:
        choice = color_input(prompt + " (y/n): ").strip().lower()
        if choice in ("y", "n"):
            return choice == "y"
        error("Please enter 'y' or 'n'.")
