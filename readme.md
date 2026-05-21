Here is a **comprehensive `README.md`** for the PhishMatrix‑Framework, using plain text with GitHub‑flavored markdown decorations for a clean, professional look.

---

```markdown
# PhishMatrix‑Framework

**Developed by Mikey**

> ⚠️ **EDUCATIONAL PURPOSE ONLY**  
> This software is intended exclusively for authorised security training,
> academic research, and penetration testing with **explicit written consent**.
> Unauthorised use against individuals, organisations, or systems is illegal.
> The developer assumes no liability for any misuse or damage caused by this tool.
> By using PhishMatrix, you agree to abide by all applicable laws and regulations.

---

## Overview

PhishMatrix‑Framework is a full‑featured phishing simulation toolkit for the command line.
It allows cybersecurity students, educators, and authorised testers to:

- Design realistic phishing email templates
- Host responsive fake login pages (Facebook, Google, PayPal, etc.)
- Launch **local** or **cloud‑exposed** phishing servers
- Automatically harvest submitted credentials
- Test SMTP configurations and send test emails
- Analyse running services on the local machine for potential backdoors
- Study phishing techniques in a safe, controlled environment

Everything is stored in a local SQLite database, making it easy to review past
campaigns, captured data, and server configurations.

---

## Features

- **Colourful CLI** – ASCII art banner, colour‑coded menus and output
- **9 realistic email templates** – Facebook, Google, PayPal, Credit Card, Instagram, Microsoft, Chase, Netflix, Generic Reset
- **9 responsive landing pages** – fully responsive (mobile/tablet/desktop), redirect after capture
- **Email Template Manager** – view, add, remove, validate placeholders (`{{name}}`, `{{email}}`, `{{date}}`, `{{link}}`)
- **Landing Page Manager** – view, add (with custom redirect URL), remove
- **SMTP Manager** – add, view, remove, test multiple SMTP servers (TLS/SSL)
- **Local Attack** – host a phishing server on `localhost`, optionally send emails
- **Public Attack** – expose your server via Cloudflare Tunnel (`cloudflared`)
- **Cloudflared Installer** – one‑click installation for macOS, Linux, and Windows
- **Server Risk Analyser** – scan listening ports, identify processes, banner grab, kill suspicious services
- **Recent Attacks** – review past attacks, view captured credentials in detail, **stop active attacks**
- **About Pages** – local web servers explaining phishing and the framework
- **Persistent storage** – all data saved in `phishmatrix.db` (SQLite)

---

## Project Structure

```
phishmatrix-framework/
├── main.py                  # Entry point – main menu loop
├── utils.py                 # Common utilities, banner, colour helpers
├── db.py                    # Database initialisation & schema migrations
├── email_templates.py       # Email template manager (folder‑based)
├── landing_pages.py         # Landing page manager (database‑based)
├── smtp_manager.py          # SMTP configuration manager with test function
├── attack_manager.py        # Phishing server, email sending, credential capture
├── cloudflared_manager.py   # Cloudflared installation & tunnel launcher
├── risk_analyzer.py         # Port/process scanner and risk analyser
├── about_servers.py         # Local HTTP servers for "About" pages
├── email_templates/         # Folder holding all email HTML files
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Installation

### Prerequisites

- Python 3.9 or newer
- pip (Python package manager)
- (Optional) `cloudflared` – can be installed from within the framework (option 6)

### Steps

1. **Download or clone the repository**
   ```bash
   git clone https://github.com/DinethChanuka/phishmatrix-framework.git
   cd phishmatrix-framework
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the framework**
   ```bash
   python main.py
   ```

On first run, the SQLite database and the `email_templates/` folder are created
automatically, pre‑populated with built‑in templates and landing pages.

---

## Usage – Menu Walkthrough

Launch `main.py`. You will see the ASCII banner and the main menu:

```
[0] Recent Attacks
[1] Local Attack (localhost server only)
[2] Public Attack (cloudflared tunnel)
[3] Email Template Settings
[4] Landing Page Template
[5] SMTP Configurations
[6] Install Cloudflared
[7] Server Risk Analyser
[8] About Phishing
[9] About PhishMatrix
[10] Exit
```

---

### [0] Recent Attacks

- Lists the last 20 attacks with type, templates used, emails sent, credentials captured, and status.
- **Enter an attack ID** to manage it:
  - `1` View all captured credentials (IP, timestamp, form fields)
  - `2` Stop a currently running attack (deactivates the server)
  - `0` Back to attack list
- **Type `exit`** or press Enter to return to the main menu.

---

### [1] Local Attack

1. Choose an email template (e.g., `facebook_security.html`).
2. Choose a landing page (e.g., `Facebook Login`). The page’s redirect URL is shown.
3. The framework checks for SMTP configurations.
   - If none are saved, you will be prompted to add one first (option 5).
   - If multiple configurations exist, you can select which to use.
4. Decide whether to send a phishing email:
   - **Yes** → Enter a target email address. The email is sent with the chosen template, and the phishing link points to your local server.
   - **No** → Only the server is started; you can manually share the link.
5. A local HTTP server starts on a random port. The phishing link is displayed.
6. Any submitted credentials are shown in real‑time and stored in the database.
7. Press `Ctrl+C` to stop the server. The attack is marked as `completed`.

---

### [2] Public Attack

Works exactly like a local attack, but after starting the server, the framework launches a **Cloudflare Tunnel** (`cloudflared tunnel`).  
The public `https://****.trycloudflare.com` URL is parsed and used as the phishing link.

- If `cloudflared` is not installed, you will be redirected to option 6.
- The server still runs locally; `cloudflared` forwards traffic securely.

---

### [3] Email Template Settings

Sub‑menu:
- **[1] View Email Templates** – lists all HTML files in the `email_templates/` folder.
- **[2] Add New Email Template** – imports an HTML file. The file must contain all four placeholders: `{{name}}`, `{{email}}`, `{{date}}`, `{{link}}`. Missing placeholders cause rejection with a detailed error.
- **[3] Remove Email Template** – deletes a template by its ID.
- **[4] Exit to Main Menu**

On first run, 9 realistic email templates are automatically created.

---

### [4] Landing Page Template

Sub‑menu:
- **[1] View Landing Pages** – shows each page’s ID, name, and redirect URL.
- **[2] Add New Landing Page** – imports an HTML file and asks for a redirect URL (must start with `http`).
- **[3] Remove Landing Page** – deletes a page by its ID.
- **[4] Exit to Main Menu**

On first run, 9 responsive, real‑world login clones are seeded into the database.

---

### [5] SMTP Configurations

Sub‑menu:
- **[1] View SMTP Configs** – lists all saved configurations.
- **[2] Add SMTP Config** – guided input: server, port (validated), username, password, TLS/SSL.
- **[3] Remove SMTP Config** – delete by ID.
- **[4] Test SMTP Config** – attempts a login to the server and reports success or the exact failure reason (DNS, authentication, timeout).
- **[5] Exit to Main Menu**

---

### [6] Install Cloudflared

- Detects your operating system.
- On macOS/Linux, downloads and installs the `cloudflared` binary to `/usr/local/bin`.
- On Windows, provides a manual download link.
- After installation, public attacks can be used immediately.

---

### [7] Server Risk Analyser

- Scans all listening TCP ports on the machine.
- If `psutil` is denied, it falls back to `lsof` (macOS) or `ss` (Linux), and if still needed, asks for your `sudo` password for an elevated scan.
- For each port it displays:
  - IP, port, protocol, process name, PID
  - Risk level: **Low** (safe), **Medium** (uncommon), **High** (known backdoor / suspicious)
  - Analysis: banner‑based identification, backdoor signature matching
- After the scan, you can **kill a process** by entering its port number.
- Results are colour‑coded (green/yellow/red).

---

### [8] About Phishing

Starts a local web server on port 8080 and opens your browser to an educational page explaining:
- What phishing is
- How it works
- How to prevent it

Press `Enter` in the terminal to stop the server.

---

### [9] About PhishMatrix

Similar to option 8, but serves a page about the framework itself, including the ASCII logo, developer credit, and the educational‑use disclaimer. Runs on port 8081.

---

### [10] Exit

Terminates the program.

---

## Built‑in Templates

### Email Templates (in `email_templates/`)

| # | File Name                  | Description                     |
|---|----------------------------|---------------------------------|
| 1 | `facebook_security.html`   | Facebook security notice        |
| 2 | `google_alert.html`        | Google unusual activity alert   |
| 3 | `paypal_invoice.html`      | PayPal payment confirmation     |
| 4 | `credit_card_update.html`  | Payment information update      |
| 5 | `instagram_security.html`  | Instagram suspicious login      |
| 6 | `microsoft_alert.html`     | Microsoft 365 sign‑in alert     |
| 7 | `chase_security.html`      | Chase Bank identity verification|
| 8 | `netflix_billing.html`     | Netflix billing problem         |
| 9 | `urgent_password_reset.html` | Generic urgent password reset  |

All templates include the placeholders `{{name}}`, `{{email}}`, `{{date}}`, `{{link}}`.

---

### Landing Pages (stored in database)

| # | Name                   | Redirect URL                        |
|---|------------------------|-------------------------------------|
| 1 | Facebook Login         | https://www.facebook.com/           |
| 2 | Google Sign‑In         | https://accounts.google.com/        |
| 3 | PayPal Checkout        | https://www.paypal.com/signin       |
| 4 | Credit Card Update     | https://www.paypal.com/myaccount/   |
| 5 | Instagram Login        | https://www.instagram.com/accounts/login/ |
| 6 | Office 365 Login       | https://login.microsoftonline.com/  |
| 7 | Bank Login (Generic)   | https://www.chase.com/              |
| 8 | Netflix Login          | https://www.netflix.com/login       |
| 9 | Generic Login with Error | https://www.google.com/           |

All pages are fully responsive and include a `POST` form pointing to `/login`.

---

## Database Schema (`phishmatrix.db`)

| Table                    | Description                                      |
|--------------------------|--------------------------------------------------|
| `email_templates`        | Legacy table (currently unused; templates are in the folder) |
| `landing_pages`          | `id`, `name`, `content`, `redirect_url`, `created_at` |
| `smtp_configs`           | `id`, `server`, `port`, `username`, `password`, `encryption`, `from_name` |
| `attacks`                | `id`, `timestamp`, `attack_type`, `email_template_id`, `landing_page_id`, `smtp_config_id`, `emails_sent`, `credentials_captured`, `status` |
| `captured_credentials`   | `id`, `attack_id`, `timestamp`, `ip`, `user_agent`, `form_data` (JSON) |

Tables are created automatically on first launch.

---

## How It Works (Technical Summary)

1. **Email Templates** are stored as `.html` files in the `email_templates/` folder. When an attack is launched, the selected template is loaded, and its placeholders are replaced with actual data (target name, email, date, and the phishing link).
2. **Landing Pages** are stored in the database. A custom Python HTTP server (`http.server`) serves the chosen page on `GET /` and listens for `POST /login`.
3. **Phishing Link** – for local attacks, it’s `http://localhost:<port>`; for public attacks, the Cloudflare Tunnel URL is used.
4. **Credential Capture** – when a victim submits the login form, the server extracts all form fields, stores them in the database, prints them in real‑time, and then **redirects** the victim to the legitimate website (the `redirect_url` you configured).
5. **Attack Lifecycle** – each attack is tracked in the `attacks` table with a status (`preparing`, `active`, `completed`, `stopped`, `failed`). You can stop an active attack from the **Recent Attacks** menu.
6. **Risk Analyser** – scans all listening ports using `psutil` (with fallback to `lsof`/`ss` and optional `sudo`), identifies processes, performs banner grabbing, and flags suspicious ports or processes.

---

## Dependencies

Listed in `requirements.txt`:

```
colorama>=0.4.6
pyfiglet>=0.8.post1
rich>=13.0.0
psutil>=5.9.0
```

Install them with `pip install -r requirements.txt`.

---

## Important Legal Notice

This software is created **only for educational and authorised testing purposes**.
The user is solely responsible for complying with all local, state, and federal laws.
Never use this tool against systems you do not own or have explicit written permission to test.
Phishing real users without consent is a criminal offence.

**The developer assumes no liability for any misuse of this software.**

---

*Stay ethical. Stay curious.*
