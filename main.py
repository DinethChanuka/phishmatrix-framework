import signal
import sys
from utils import banner, clear_screen, color_input, success, error, info, get_db
from colorama import Fore, Style  # <-- crucial import added
from db import init_db
from email_templates import email_template_menu
from landing_pages import landing_page_menu
from smtp_manager import smtp_menu
from attack_manager import attack_flow, recent_attacks
from cloudflared_manager import install_cloudflared
from risk_analyzer import run_analyzer
from about_servers import about_phishing, about_phishmatrix


def main():
    init_db()
    while True:
        clear_screen()
        banner()
        menu = [
            "[0] Recent Attacks",
            "[1] Local Attack (localhost server only)",
            "[2] Public Attack (cloudflared tunnel)",
            "[3] Email Template Settings",
            "[4] Landing Page Template",
            "[5] SMTP Configurations",
            "[6] Install Cloudflared",
            "[7] Server Risk Analyser",
            "[8] About Phishing",
            "[9] About PhishMatrix",
            "[10] Exit",
        ]
        for item in menu:
            # colour the number and the text differently
            print(
                Fore.CYAN
                + item.split("]")[0]
                + "]"
                + Fore.YELLOW
                + " ".join(item.split("]")[1:])
                + Style.RESET_ALL
            )
        choice = color_input("\nChoice: ").strip()
        if choice == "0":
            recent_attacks()
        elif choice == "1":
            attack_flow(is_public=False)
        elif choice == "2":
            attack_flow(is_public=True)
        elif choice == "3":
            email_template_menu()
        elif choice == "4":
            landing_page_menu()
        elif choice == "5":
            smtp_menu()
        elif choice == "6":
            install_cloudflared()
        elif choice == "7":
            run_analyzer()
        elif choice == "8":
            about_phishing()
        elif choice == "9":
            about_phishmatrix()
        elif choice == "10":
            print(Fore.RED + "\nExiting. Stay ethical." + Style.RESET_ALL)
            sys.exit(0)
        else:
            error("Invalid choice.")
        if choice not in ("8", "9"):  # those manage their own input wait
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Graceful shutdown of server threads on Ctrl+C
    def signal_handler(sig, frame):
        print("\nInterrupted. Exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    main()
