import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

def get_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prayer_requests (
            id SERIAL PRIMARY KEY,
            name TEXT,
            message TEXT NOT NULL,
            contact TEXT,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            replied INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            date_subscribed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def add_prayer_request(name, message, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO prayer_requests (name, message, contact) VALUES (%s, %s, %s)',
        (name, message, contact)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_prayer_requests():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM prayer_requests ORDER BY date_submitted DESC')
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests

def add_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subscribers (email) VALUES (%s)', (email,))
        conn.commit()
        success = True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        success = False
    cursor.close()
    conn.close()
    return success

def export_prayer_requests_csv():
    import csv
    requests = get_all_prayer_requests()
    with open('prayer_requests_backup.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Message', 'Contact', 'Date Submitted'])
        for req in requests:
            writer.writerow([req['id'], req['name'], req['message'], req['contact'], req['date_submitted']])
    return 'prayer_requests_backup.csv'