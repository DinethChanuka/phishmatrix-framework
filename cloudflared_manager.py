import subprocess
import platform
import os
import sys
from utils import success, error, info, color_input
import shutil


def is_cloudflared_installed():
    return shutil.which("cloudflared") is not None


def install_cloudflared():
    if is_cloudflared_installed():
        success("Cloudflared is already installed.")
        return
    info("Installing cloudflared...")
    system = platform.system().lower()
    if system == "linux":
        # For simplicity, assume Debian/Ubuntu; user can adjust
        try:
            subprocess.run(
                [
                    "curl",
                    "-L",
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
                    "-o",
                    "cloudflared",
                ],
                check=True,
            )
            os.chmod("cloudflared", 0o755)
            shutil.move("cloudflared", "/usr/local/bin/cloudflared")
            success("Cloudflared installed. Please ensure /usr/local/bin is in PATH.")
        except Exception as e:
            error(
                f"Installation failed: {e}. Download manually from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation"
            )
    elif system == "darwin":  # macOS
        if shutil.which("brew"):
            subprocess.run(
                ["brew", "install", "cloudflare/cloudflare/cloudflared"], check=True
            )
            success("Installed via Homebrew.")
        else:
            try:
                subprocess.run(
                    [
                        "curl",
                        "-L",
                        "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz",
                        "-o",
                        "cloudflared.tgz",
                    ],
                    check=True,
                )
                subprocess.run(["tar", "xzf", "cloudflared.tgz"], check=True)
                os.chmod("cloudflared", 0o755)
                shutil.move("cloudflared", "/usr/local/bin/cloudflared")
                success("Cloudflared installed to /usr/local/bin.")
            except Exception as e:
                error(f"Installation failed: {e}")
    elif system == "windows":
        info(
            "On Windows, download from: https://github.com/cloudflare/cloudflared/releases and add to PATH."
        )
        error(
            "Automatic Windows installation not implemented. Please install manually."
        )
    else:
        error("Unsupported OS.")


def start_cloudflared_tunnel(port):
    """Start a cloudflared tunnel and return the public URL."""
    if not is_cloudflared_installed():
        error("Cloudflared not found. Install it via Option 6.")
        return None
    info("Starting cloudflared tunnel...")
    try:
        process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        # Parse output to find the trycloudflare.com URL
        import re

        url_pattern = re.compile(r"https://[-a-zA-Z0-9]+\.trycloudflare\.com")
        for line in process.stdout:
            print(line.strip())
            match = url_pattern.search(line)
            if match:
                public_url = match.group(0)
                return public_url
        # If we exit loop without finding URL, return None
        return None
    except Exception as e:
        error(f"Tunnel failed: {e}")
        return None
