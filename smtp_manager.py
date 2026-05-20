import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import get_db, success, error, info, color_input, clear_screen
from colorama import Fore, Style


# ----------------------------------------------------------------------
def view_configs():
    conn = get_db()
    configs = conn.execute(
        "SELECT id, server, port, username, encryption, from_name FROM smtp_configs"
    ).fetchall()
    conn.close()
    if not configs:
        info("No SMTP configurations.")
        return
    print(
        "\n{:<3} {:<20} {:<6} {:<25} {:<8} {:<15}".format(
            "ID", "Server", "Port", "Username", "Enc", "From"
        )
    )
    print("-" * 80)
    for c in configs:
        print(
            "{:<3} {:<20} {:<6} {:<25} {:<8} {:<15}".format(
                c["id"],
                c["server"],
                c["port"],
                c["username"],
                c["encryption"],
                c["from_name"] or "",
            )
        )


# ----------------------------------------------------------------------
def add_config():
    # 1) Server
    while True:
        server = color_input("SMTP server: ").strip()
        if not server:
            error("Server name cannot be empty.")
            continue
        # Optional: simple check for a dot (most mail servers have one)
        if "." not in server:
            info(
                "Server name doesn't contain a dot – are you sure? (Press Enter to keep, or type again)"
            )
            confirm = input("> ").strip().lower()
            if confirm != "":
                continue
        break

    # 2) Port
    while True:
        port_str = color_input("Port (587 for TLS, 465 for SSL): ").strip()
        if not port_str.isdigit():
            error("Port must be a number.")
            continue
        port = int(port_str)
        if port < 1 or port > 65535:
            error("Port must be between 1 and 65535.")
            continue
        break

    # 3) Username
    username = color_input("Username (email): ").strip()
    if not username:
        error("Username cannot be empty.")
        return

    # 4) Password
    password = color_input("Password: ").strip()
    if not password:
        error("Password cannot be empty.")
        return

    # 5) Encryption
    enc = color_input("Encryption (TLS/SSL): ").strip().upper()
    if enc not in ("TLS", "SSL"):
        error("Encryption must be TLS or SSL.")
        return

    # 6) From name (optional)
    from_name = color_input("From name (optional): ").strip()

    # Save
    conn = get_db()
    conn.execute(
        "INSERT INTO smtp_configs (server, port, username, password, encryption, from_name) "
        "VALUES (?,?,?,?,?,?)",
        (server, port, username, password, enc, from_name),
    )
    conn.commit()
    conn.close()
    success("SMTP configuration added.")


# ----------------------------------------------------------------------
def remove_config():
    view_configs()
    cid = color_input("Enter config ID to remove (0 to cancel): ").strip()
    if cid == "0":
        return
    conn = get_db()
    conn.execute("DELETE FROM smtp_configs WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    success("Configuration removed.")


# ----------------------------------------------------------------------
def test_config():
    view_configs()
    cid = color_input("Enter config ID to test: ").strip()
    conn = get_db()
    cfg = conn.execute("SELECT * FROM smtp_configs WHERE id=?", (cid,)).fetchone()
    conn.close()
    if not cfg:
        error("Config not found.")
        return

    server = cfg["server"]
    port = cfg["port"]
    username = cfg["username"]
    password = cfg["password"]
    enc = cfg["encryption"]

    print(
        Fore.YELLOW
        + f"\n[*] Testing SMTP connection to {server}:{port} ({enc})..."
        + Style.RESET_ALL
    )

    # 1) Quick DNS / reachability check (optional but helpful)
    try:
        socket.gethostbyname(server)
    except socket.gaierror:
        error(
            f"Cannot resolve server name '{server}'. Check the address or your internet connection."
        )
        return

    # 2) Attempt SMTP handshake & login
    server_obj = None
    try:
        if enc == "SSL":
            server_obj = smtplib.SMTP_SSL(server, port, timeout=10)
        else:  # TLS
            server_obj = smtplib.SMTP(server, port, timeout=10)
            # Start TLS
            server_obj.starttls()

        # Login
        server_obj.login(username, password)
        server_obj.quit()
        success("SMTP connection successful – all settings are correct.")

    except smtplib.SMTPConnectError:
        error(
            f"Cannot connect to {server} on port {port}. The server may be down or the port is wrong."
        )
    except smtplib.SMTPAuthenticationError:
        error("Authentication failed. Check your username and password.")
    except smtplib.SMTPException as e:
        error(f"SMTP error: {e}")
    except socket.timeout:
        error("Connection timed out. The server is not responding.")
    except Exception as e:
        error(f"Unexpected error: {e}")
    finally:
        # Ensure the connection is closed even if something went wrong
        try:
            if server_obj:
                server_obj.close()
        except:
            pass


# ----------------------------------------------------------------------
def smtp_menu():
    while True:
        clear_screen()
        print(Fore.YELLOW + "[SMTP Configurations]\n" + Style.RESET_ALL)
        print("[1] View SMTP Configs")
        print("[2] Add SMTP Config")
        print("[3] Remove SMTP Config")
        print("[4] Test SMTP Config")
        print("[5] Exit to Main Menu")
        choice = color_input("Choice: ").strip()
        if choice == "1":
            view_configs()
        elif choice == "2":
            add_config()
        elif choice == "3":
            remove_config()
        elif choice == "4":
            test_config()
        elif choice == "5":
            break
        else:
            error("Invalid choice.")
        input("\nPress Enter to continue...")
