import socket
import subprocess
import platform
import re
import os
import signal
import json
from getpass import getpass

from utils import success, error, info, color_input, Fore, Style

KNOWN_BACKDOOR_PORTS = {
    4444: "Metasploit Meterpreter default",
    5555: "Android ADB / possible backdoor",
    31337: "Back Orifice / elite",
    1337: "Often used by hackers",
    6667: "IRC bot",
    9001: "Common reverse shell",
    44444: "Meterpreter alternate",
}


# ----------------------------------------------------------------------
def _get_listening_psutil():
    """Try psutil first. Returns list of dicts or raises AccessDenied."""
    import psutil

    results = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "LISTEN":
            proc_name = None
            if conn.pid:
                try:
                    proc_name = psutil.Process(conn.pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_name = "unknown"
            results.append(
                {
                    "ip": conn.laddr.ip,
                    "port": conn.laddr.port,
                    "pid": conn.pid,
                    "process": proc_name,
                }
            )
    return results


# ----------------------------------------------------------------------
def _get_listening_fallback():
    """Fallback to OS commands without sudo. May still require elevated permissions."""
    system = platform.system().lower()
    results = []
    if system == "darwin":
        cmd = ["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"]
    elif system == "linux":
        cmd = ["ss", "-ltnp"]
    elif system == "windows":
        cmd = ["netstat", "-ano"]
    else:
        error("Unsupported OS for fallback scan.")
        return results

    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        error("Fallback command failed (probably also needs admin rights).")
        return results

    # Parse the output
    if system == "darwin":
        lines = output.splitlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) < 9:
                continue
            proc_name = parts[0]
            pid = int(parts[1])
            addr = parts[8]
            ip, port_str = addr.rsplit(":", 1)
            ip = ip if ip != "*" else "0.0.0.0"
            port = int(port_str)
            results.append({"ip": ip, "port": port, "pid": pid, "process": proc_name})
    elif system == "linux":
        for line in output.splitlines()[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            addr = parts[4]
            ip, port_str = addr.rsplit(":", 1)
            ip = ip if ip != "*" else "0.0.0.0"
            port = int(port_str)
            pid = None
            proc_name = "unknown"
            users_field = " ".join(parts[5:])
            match = re.search(r'users:\(\("(\w+)",pid=(\d+)', users_field)
            if match:
                proc_name = match.group(1)
                pid = int(match.group(2))
            results.append({"ip": ip, "port": port, "pid": pid, "process": proc_name})
    elif system == "windows":
        lines = output.splitlines()[4:]
        for line in lines:
            if not line.strip() or "LISTENING" not in line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            local = parts[1]
            pid = int(parts[4])
            ip, port_str = local.rsplit(":", 1)
            ip = ip if ip != "0.0.0.0" else "0.0.0.0"
            port = int(port_str)
            proc_name = "unknown"
            try:
                import psutil

                proc_name = psutil.Process(pid).name()
            except:
                pass
            results.append({"ip": ip, "port": port, "pid": pid, "process": proc_name})
    return results


# ----------------------------------------------------------------------
def _elevated_scan():
    """Ask for sudo password and run lsof (macOS) or ss (Linux) with elevated privileges."""
    system = platform.system().lower()
    if system == "windows":
        info("On Windows, try running the program as Administrator.")
        return []

    if system == "darwin":
        cmd = ["sudo", "-S", "lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"]
    else:
        cmd = ["sudo", "-S", "ss", "-ltnp"]

    password = getpass(
        Fore.CYAN + "Enter your admin (sudo) password: " + Style.RESET_ALL
    )
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input=password + "\n")
        if proc.returncode != 0:
            error(f"Elevated command failed: {stderr.strip()}")
            return []
    except Exception as e:
        error(f"Error running elevated command: {e}")
        return []

    # Parse output exactly like in fallback
    results = []
    if system == "darwin":
        lines = stdout.splitlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) < 9:
                continue
            proc_name = parts[0]
            pid = int(parts[1])
            addr = parts[8]
            ip, port_str = addr.rsplit(":", 1)
            ip = ip if ip != "*" else "0.0.0.0"
            port = int(port_str)
            results.append({"ip": ip, "port": port, "pid": pid, "process": proc_name})
    else:  # linux
        for line in stdout.splitlines()[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            addr = parts[4]
            ip, port_str = addr.rsplit(":", 1)
            ip = ip if ip != "*" else "0.0.0.0"
            port = int(port_str)
            pid = None
            proc_name = "unknown"
            users_field = " ".join(parts[5:])
            match = re.search(r'users:\(\("(\w+)",pid=(\d+)', users_field)
            if match:
                proc_name = match.group(1)
                pid = int(match.group(2))
            results.append({"ip": ip, "port": port, "pid": pid, "process": proc_name})
    return results


# ----------------------------------------------------------------------
def get_listening_connections():
    """
    Try psutil first; on AccessDenied, fallback to OS command; if that still fails
    (or if psutil is denied), ask for sudo and re‑scan.
    """
    try:
        return _get_listening_psutil()
    except Exception as e:
        # psutil.AccessDenied is the most common, but catch all to be safe
        info("Insufficient permissions for psutil. Trying fallback command...")
        results = _get_listening_fallback()
        if results:
            return results
        # If fallback also empty, try elevated scan
        print(
            Fore.YELLOW + "Fallback also failed. Need admin rights." + Style.RESET_ALL
        )
        return _elevated_scan()


# ----------------------------------------------------------------------
def get_process_for_port(port, connections_data=None):
    """Search the provided connections_data for a port (avoid rescan)."""
    if connections_data:
        for c in connections_data:
            if c["port"] == port:
                return c["process"], c["pid"], c["ip"]
    return None, None, None


# ----------------------------------------------------------------------
def banner_grab(ip, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.send(b"\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner[:200]
    except:
        return ""


# ----------------------------------------------------------------------
def analyze_port(port, connections_data, protocol="TCP"):
    proc_name, pid, ip_real = get_process_for_port(port, connections_data)
    if proc_name is None:
        return None
    risk = "Low"
    analysis = ""
    banner = banner_grab(ip_real or "127.0.0.1", port)

    if port in KNOWN_BACKDOOR_PORTS:
        risk = "High"
        analysis = f"Known backdoor port: {KNOWN_BACKDOOR_PORTS[port]}. "
    elif port < 1024:
        risk = "Low"
        analysis = "System/reserved port. "
    else:
        risk = "Medium"
        analysis = "Non-standard port. "

    suspicious_names = [
        "nc",
        "ncat",
        "netcat",
        "bash",
        "sh",
        "python",
        "perl",
        "ruby",
        "node",
        "powershell",
        "cmd",
    ]
    if proc_name.lower() in suspicious_names:
        risk = "High" if risk != "High" else risk
        analysis += f"Suspicious process '{proc_name}' detected. "

    if banner:
        if "SSH" in banner:
            analysis += "SSH service identified. "
            risk = "Low"
        elif "220" in banner and ("FTP" in banner or "FileZilla" in banner):
            analysis += "FTP service. "
            risk = "Medium"
        elif "HTTP" in banner:
            analysis += "HTTP server. "
            risk = "Medium"
        elif any(
            kw in banner.lower() for kw in ["metasploit", "meterpreter", "cobalt"]
        ):
            risk = "High"
            analysis += "Banner matches known C2 framework. "
    else:
        analysis += "No banner returned. "

    return {
        "ip": ip_real or "0.0.0.0",
        "port": port,
        "protocol": protocol,
        "process": proc_name,
        "pid": pid,
        "risk": risk,
        "analysis": analysis,
    }


# ----------------------------------------------------------------------
def kill_process(pid):
    try:
        if os.name == "nt":
            os.kill(pid, signal.SIGTERM)
        else:
            os.kill(pid, signal.SIGKILL)
        success(f"Process {pid} killed.")
    except Exception as e:
        error(f"Failed to kill: {e}")


# ----------------------------------------------------------------------
def run_analyzer():
    info("Scanning listening ports...")
    connections = get_listening_connections()
    if not connections:
        error("Could not obtain any listening ports. Exiting.")
        return

    # Deduplicate by port
    seen = set()
    unique = []
    for c in connections:
        if c["port"] not in seen:
            seen.add(c["port"])
            unique.append(c)

    results = []
    for c in unique:
        res = analyze_port(c["port"], connections_data=connections)
        if res:
            results.append(res)

    # Display table
    print(
        "\n{:<6} {:<16} {:<8} {:<15} {:<8} {:<10} {}".format(
            "Port", "IP", "Protocol", "Process", "PID", "Risk", "Analysis"
        )
    )
    print("-" * 100)
    for r in results:
        color = (
            Fore.GREEN
            if r["risk"] == "Low"
            else (Fore.YELLOW if r["risk"] == "Medium" else Fore.RED)
        )
        print(
            f"{color}{r['port']:<6} {r['ip']:<16} {r['protocol']:<8} "
            f"{r['process']:<15} {str(r['pid']):<8} {r['risk']:<10} "
            f"{r['analysis']}{Style.RESET_ALL}"
        )

    port_to_kill = color_input(
        "\nEnter port number to kill server (or Enter to skip): "
    ).strip()
    if port_to_kill:
        try:
            port = int(port_to_kill)
            proc_name, pid, _ = get_process_for_port(port, connections)
            if pid:
                confirm = input(
                    f"Kill process {proc_name} (PID {pid}) on port {port}? (y/n): "
                )
                if confirm.lower() == "y":
                    kill_process(pid)
            else:
                error("No process found on that port.")
        except ValueError:
            error("Invalid port.")
