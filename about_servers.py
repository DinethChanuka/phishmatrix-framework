import http.server
import socketserver
import threading
import webbrowser
import socket
from utils import info, color_input


def serve_html(html_content, port=8080):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())

    httpd = socketserver.TCPServer(("", port), Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def about_phishing():
    html = """
    <html>
    <head><title>About Phishing</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f4; }
        h1 { color: #d9534f; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; }
    </style>
    </head>
    <body>
    <div class="container">
        <h1>About Phishing</h1>
        <p>Phishing is a cyber attack that uses disguised email as a weapon. The goal is to trick the email recipient into believing that the message is something they want or need ... </p>
        <h2>How It Works</h2>
        <p>Attackers send fraudulent emails ...</p>
        <h2>How to Prevent Phishing</h2>
        <ul>
            <li>Be cautious with unsolicited emails.</li>
            <li>Check the sender's email address.</li>
            <li>Enable multi‑factor authentication.</li>
            <li>Use email filters and anti‑phishing toolbars.</li>
        </ul>
        <p><em>This page is for educational purposes only.</em></p>
    </div>
    </body>
    </html>
    """
    port = 8080
    info(f"Starting local server on http://localhost:{port}")
    httpd = serve_html(html, port)
    webbrowser.open(f"http://localhost:{port}")
    input("Press Enter to stop server and return to menu...")
    httpd.shutdown()


def about_phishmatrix():
    html = """
    <html>
    <head><title>About PhishMatrix</title>
    <style>
        body { background: #111; color: #0f0; font-family: 'Courier New', monospace; padding: 30px; }
        pre { font-size: 14px; }
        .disclaimer { color: red; font-weight: bold; margin-top: 30px; }
    </style>
    </head>
    <body>
        <pre>
  ____  _     _     _   __  __       _       _       
 |  _ \\| |__ (_)___| |_|  \\/  | __ _| |_ ___| |__    
 | |_) | '_ \\| / __| '_ \\ |\\/| |/ _` | __/ __| '_ \\   
 |  __/| | | | \\__ \\ | | | |  | | (_| | || (__| | | |  
 |_|   |_| |_|_|___/_| |_|_|  |_|\\__,_|\\__\\___|_| |_|  
        </pre>
        <h2>PhishMatrix Framework</h2>
        <p>Developed by Mikey</p>
        <p>A comprehensive phishing simulation tool for educational use.</p>
        <p class="disclaimer">DISCLAIMER: This tool is for educational purposes only. Unauthorized use is illegal. The developer assumes no liability.</p>
    </body>
    </html>
    """
    port = 8081
    info(f"Starting about page on http://localhost:{port}")
    httpd = serve_html(html, port)
    webbrowser.open(f"http://localhost:{port}")
    input("Press Enter to stop server...")
    httpd.shutdown()
