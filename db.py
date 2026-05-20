import sqlite3
from utils import get_db


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS email_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS landing_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            redirect_url TEXT NOT NULL DEFAULT 'https://www.google.com',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS smtp_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server TEXT NOT NULL,
            port INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            encryption TEXT CHECK(encryption IN ('TLS','SSL')) NOT NULL,
            from_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attack_type TEXT CHECK(attack_type IN ('local','public')) NOT NULL,
            email_template_id INTEGER,
            landing_page_id INTEGER,
            smtp_config_id INTEGER,
            emails_sent INTEGER DEFAULT 0,
            credentials_captured INTEGER DEFAULT 0,
            status TEXT,
            FOREIGN KEY(email_template_id) REFERENCES email_templates(id),
            FOREIGN KEY(landing_page_id) REFERENCES landing_pages(id),
            FOREIGN KEY(smtp_config_id) REFERENCES smtp_configs(id)
        );

        CREATE TABLE IF NOT EXISTS captured_credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT,
            user_agent TEXT,
            form_data TEXT,
            FOREIGN KEY(attack_id) REFERENCES attacks(id)
        );
    """)

    # Migration: add redirect_url column if it doesn't exist
    try:
        c.execute(
            "ALTER TABLE landing_pages ADD COLUMN redirect_url TEXT NOT NULL DEFAULT 'https://www.google.com'"
        )
    except sqlite3.OperationalError:
        pass  # column already exists

    conn.commit()
    conn.close()
