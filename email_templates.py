import os
import shutil
from utils import success, error, info, color_input, clear_screen, Fore, Style

TEMPLATE_FOLDER = "email_templates"


def ensure_template_folder():
    """Create the templates folder if it doesn't exist, and seed with realistic templates."""
    if not os.path.exists(TEMPLATE_FOLDER):
        os.makedirs(TEMPLATE_FOLDER)
        _create_builtin_templates()


def _create_builtin_templates():
    """Add 9 real‑world email templates matching the built‑in landing pages."""
    templates = [
        # 1. Facebook security notice
        (
            "facebook_security.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background: #f5f6f7; margin:0; padding:20px; }
  .container { max-width:600px; margin:auto; background:white; padding:30px; border-radius:8px; }
  .logo { text-align:center; font-size:32px; color:#1877f2; font-weight:bold; margin-bottom:20px; }
  .btn { display:inline-block; padding:12px 24px; background:#1877f2; color:white; text-decoration:none; border-radius:6px; font-weight:bold; }
  .footer { margin-top:25px; font-size:12px; color:#90949c; text-align:center; }
</style></head>
<body>
<div class="container">
  <div class="logo">facebook</div>
  <p>Hi {{name}},</p>
  <p>We noticed a login to your account <strong>{{email}}</strong> from a new device on <strong>{{date}}</strong>.</p>
  <p>If this was you, no further action is required. If you don’t recognise this activity, please secure your account immediately.</p>
  <p style="text-align:center; margin:25px 0;">
    <a href="{{link}}" class="btn">Review Recent Activity</a>
  </p>
  <div class="footer">Facebook © 2025 · This is an automated message</div>
</div>
</body>
</html>""",
        ),
        # 2. Google security alert
        (
            "google_alert.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Roboto, Arial, sans-serif; background:#f1f3f4; margin:0; padding:20px; }
  .card { max-width:560px; margin:auto; background:white; border-radius:8px; padding:30px; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
  .logo { margin-bottom:20px; }
  .btn { background:#1a73e8; color:white; padding:12px 30px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; margin:20px 0; }
  .footer { color:#5f6368; font-size:12px; margin-top:30px; }
</style></head>
<body>
<div class="card">
  <div class="logo"><img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google" width="120"></div>
  <p>Hello {{name}},</p>
  <p>Google detected unusual activity on your account (<strong>{{email}}</strong>) on <strong>{{date}}</strong>.</p>
  <p>To help keep your account safe, we’ve temporarily locked some features until you verify it was you.</p>
  <p style="text-align:center;">
    <a href="{{link}}" class="btn">Verify your account</a>
  </p>
  <div class="footer">Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043</div>
</div>
</body>
</html>""",
        ),
        # 3. PayPal payment confirmation
        (
            "paypal_invoice.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background:#f4f4f4; padding:20px; }
  .main { max-width:600px; margin:auto; background:white; padding:25px; border-radius:8px; }
  .logo { text-align:center; font-size:30px; color:#003087; font-weight:bold; margin-bottom:25px; }
  .btn { background:#0070ba; color:white; padding:12px 20px; text-decoration:none; border-radius:25px; display:inline-block; font-weight:bold; }
  .footer { font-size:12px; color:#6c7378; margin-top:30px; }
</style></head>
<body>
<div class="main">
  <div class="logo">PayPal</div>
  <p>Dear {{name}},</p>
  <p>We’ve just processed a payment from your account (<strong>{{email}}</strong>) on {{date}}.</p>
  <p>Amount: <strong>$49.99</strong> – Reference: PPL-{{date}}.</p>
  <p>If you did not authorise this transaction, please cancel it immediately:</p>
  <p style="text-align:center;">
    <a href="{{link}}" class="btn">Cancel Payment</a>
  </p>
  <div class="footer">PayPal Pte. Ltd. · This is an educational simulation</div>
</div>
</body>
</html>""",
        ),
        # 4. Credit Card update reminder (matches Credit Card Update page)
        (
            "credit_card_update.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background:#e6e6e6; padding:20px; }
  .form-card { max-width:500px; margin:auto; background:white; padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.2); }
  .logo { font-size:22px; color:#d32f2f; font-weight:bold; margin-bottom:15px; }
  .btn { background:#d32f2f; color:white; padding:12px 24px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; }
  .footer { font-size:12px; color:#888; margin-top:25px; }
</style></head>
<body>
<div class="form-card">
  <div class="logo">Payment Security</div>
  <p>Dear {{name}},</p>
  <p>We need you to update the payment information linked to your account <strong>{{email}}</strong>. This is required by <strong>{{date}}</strong> to avoid service interruption.</p>
  <p>Please confirm your card details and billing address now.</p>
  <p style="text-align:center; margin:20px 0;">
    <a href="{{link}}" class="btn">Update Payment Info</a>
  </p>
  <div class="footer">Card Services · Educational simulation only</div>
</div>
</body>
</html>""",
        ),
        # 5. Instagram suspicious login
        (
            "instagram_security.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background:#fafafa; padding:20px; }
  .card { max-width:500px; margin:auto; background:white; border:1px solid #dbdbdb; padding:30px; }
  .logo { text-align:center; font-size:30px; margin-bottom:20px; font-weight:bold; }
  .btn { background:#0095f6; color:white; padding:10px 20px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; }
  .footer { color:#8e8e8e; font-size:12px; margin-top:30px; }
</style></head>
<body>
<div class="card">
  <div class="logo">Instagram</div>
  <p>Hello {{name}},</p>
  <p>We noticed a login to your Instagram account (<strong>{{email}}</strong>) from a new browser on {{date}}.</p>
  <p>If this was you, ignore this message. Otherwise, secure your account.</p>
  <p style="text-align:center; margin:20px 0;">
    <a href="{{link}}" class="btn">This Was Me</a>
  </p>
  <div class="footer">Instagram · Facebook © 2025</div>
</div>
</body>
</html>""",
        ),
        # 6. Microsoft 365 security alert
        (
            "microsoft_alert.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: 'Segoe UI', Tahoma, sans-serif; background:#f3f2f1; padding:20px; }
  .container { max-width:500px; margin:auto; background:white; padding:30px; box-shadow:0 2px 6px rgba(0,0,0,0.1); }
  .logo { margin-bottom:20px; }
  .btn { background:#0078d4; color:white; padding:12px 24px; text-decoration:none; border-radius:2px; font-weight:bold; display:inline-block; margin:20px 0; }
  .footer { color:#605e5c; font-size:12px; margin-top:30px; }
</style></head>
<body>
<div class="container">
  <div class="logo"><img src="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c15" alt="Microsoft" width="108"></div>
  <p>Dear {{name}},</p>
  <p>Microsoft account <strong>{{email}}</strong> was accessed from an unrecognised location on {{date}}.</p>
  <p>If this wasn’t you, we recommend you reset your password immediately.</p>
  <p style="text-align:center;">
    <a href="{{link}}" class="btn">Review Activity</a>
  </p>
  <div class="footer">Microsoft Corporation · One Microsoft Way, Redmond, WA 98052</div>
</div>
</body>
</html>""",
        ),
        # 7. Chase Bank security update
        (
            "chase_security.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background:#f4f4f4; padding:20px; }
  .box { max-width:500px; margin:auto; background:white; padding:30px; border-radius:8px; }
  .logo { font-size:28px; color:#003b7a; font-weight:bold; margin-bottom:20px; }
  .btn { background:#003b7a; color:white; padding:12px 24px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; margin:20px 0; }
  .footer { font-size:12px; color:#777; margin-top:30px; }
</style></head>
<body>
<div class="box">
  <div class="logo">CHASE 🏦</div>
  <p>Dear {{name}},</p>
  <p>We require you to verify your identity for your account (<strong>{{email}}</strong>) as of <strong>{{date}}</strong>.</p>
  <p>This is part of our regular security maintenance. Please complete the verification to avoid any disruption to your banking services.</p>
  <p style="text-align:center;">
    <a href="{{link}}" class="btn">Verify Now</a>
  </p>
  <div class="footer">Chase Bank, N.A. · Member FDIC · Educational simulation</div>
</div>
</body>
</html>""",
        ),
        # 8. Netflix billing update
        (
            "netflix_billing.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { background:#000; color:#fff; font-family: Arial, sans-serif; padding:20px; }
  .box { max-width:500px; margin:auto; background:#111; padding:30px; border-radius:4px; }
  .logo { font-size:32px; color:#e50914; font-weight:bold; text-transform:uppercase; }
  .btn { background:#e50914; color:white; padding:14px 28px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; margin:20px 0; }
  .footer { color:#737373; font-size:12px; margin-top:20px; }
</style></head>
<body>
<div class="box">
  <div class="logo">NETFLIX</div>
  <p>Hi {{name}},</p>
  <p>Your Netflix payment method (<strong>{{email}}</strong>) was declined on {{date}}.</p>
  <p>To continue watching, please update your billing information now.</p>
  <p style="text-align:center;">
    <a href="{{link}}" class="btn">Update Payment</a>
  </p>
  <div class="footer">This email was sent by Netflix · Educational simulation only</div>
</div>
</body>
</html>""",
        ),
        # 9. Generic urgent password reset (matches Generic Login with Error)
        (
            "urgent_password_reset.html",
            """\
<html>
<head><meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background:#f9f9f9; padding:20px; }
  .main { max-width:500px; margin:auto; background:white; border-top:4px solid #d9534f; padding:30px; }
  .btn { background:#d9534f; color:white; padding:12px 30px; text-decoration:none; border-radius:4px; font-weight:bold; display:inline-block; }
  .footer { font-size:12px; color:#aaa; margin-top:30px; }
</style></head>
<body>
<div class="main">
  <h2 style="color:#d9534f;">⚠ Action Required</h2>
  <p>Hi {{name}},</p>
  <p>A request was made to reset the password for <strong>{{email}}</strong> on {{date}}.</p>
  <p>If you made this request, click the button below. Otherwise, contact support immediately.</p>
  <p style="text-align:center; margin:25px 0;">
    <a href="{{link}}" class="btn">Reset Password</a>
  </p>
  <div class="footer">This is an automated message · Please do not reply</div>
</div>
</body>
</html>""",
        ),
    ]

    for filename, content in templates:
        filepath = os.path.join(TEMPLATE_FOLDER, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    success("9 realistic email templates created (matching landing pages).")


# ---------- Utility functions ----------
def list_templates():
    """Return a sorted list of template filenames (without path)."""
    if not os.path.exists(TEMPLATE_FOLDER):
        return []
    files = [f for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(".html")]
    return sorted(files)


def view_templates():
    templates = list_templates()
    if not templates:
        info("No email templates found.")
        return
    print("\n{:<5} {:<30}".format("ID", "Template Name"))
    print("-" * 40)
    for idx, name in enumerate(templates, start=1):
        print("{:<5} {:<30}".format(idx, name))


def get_template_content(index):
    """Return the full HTML content of a template by its list index (1‑based)."""
    templates = list_templates()
    if index < 1 or index > len(templates):
        return None
    filename = templates[index - 1]
    filepath = os.path.join(TEMPLATE_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def add_template():
    source = color_input("Enter path to HTML file: ").strip()
    if not os.path.isfile(source):
        error("File not found.")
        return
    with open(source, "r", encoding="utf-8") as f:
        content = f.read()
    required = ["{{name}}", "{{email}}", "{{date}}", "{{link}}"]
    missing = [p for p in required if p not in content]
    if missing:
        error("Missing placeholders: " + ", ".join(missing))
        info("Required: {{name}}, {{email}}, {{date}}, {{link}}")
        return
    filename = os.path.basename(source)
    dest = os.path.join(TEMPLATE_FOLDER, filename)
    if os.path.exists(dest):
        overwrite = (
            color_input(f"'{filename}' already exists. Overwrite? (y/n): ")
            .strip()
            .lower()
        )
        if overwrite != "y":
            info("Template not added.")
            return
    shutil.copy2(source, dest)
    success(f"Template '{filename}' added to {TEMPLATE_FOLDER}.")


def remove_template():
    view_templates()
    idx_str = color_input("Enter template ID to remove (0 to cancel): ").strip()
    if idx_str == "0":
        return
    try:
        idx = int(idx_str)
    except ValueError:
        error("Invalid number.")
        return
    templates = list_templates()
    if idx < 1 or idx > len(templates):
        error("Invalid ID.")
        return
    filename = templates[idx - 1]
    filepath = os.path.join(TEMPLATE_FOLDER, filename)
    confirm = color_input(f"Delete '{filename}'? (y/n): ").strip().lower()
    if confirm == "y":
        os.remove(filepath)
        success("Template deleted.")


def email_template_menu():
    ensure_template_folder()
    while True:
        clear_screen()
        print(Fore.YELLOW + "[Email Template Settings]\n" + Style.RESET_ALL)
        print("[1] View Email Templates")
        print("[2] Add New Email Template")
        print("[3] Remove Email Template")
        print("[4] Exit to Main Menu")
        choice = color_input("Choice: ").strip()
        if choice == "1":
            view_templates()
        elif choice == "2":
            add_template()
        elif choice == "3":
            remove_template()
        elif choice == "4":
            break
        else:
            error("Invalid choice.")
        input("\nPress Enter to continue...")
