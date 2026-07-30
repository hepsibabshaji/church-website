import sqlite3
import csv

def export_prayer_requests_csv():
    requests = get_all_prayer_requests()
    with open('prayer_requests_backup.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Message', 'Contact', 'Date Submitted'])
        for req in requests:
            writer.writerow([req['id'], req['name'], req['message'], req['contact'], req['date_submitted']])
    return 'prayer_requests_backup.csv'
def init_db():
    conn = sqlite3.connect('prayers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prayer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT NOT NULL,
            contact TEXT,
            date_submitted TEXT DEFAULT CURRENT_TIMESTAMP,
            replied INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            date_subscribed TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_prayer_request(name, message, contact):
    conn = sqlite3.connect('prayers.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO prayer_requests (name, message, contact) VALUES (?, ?, ?)',
        (name, message, contact)
    )
    conn.commit()
    conn.close()

def get_all_prayer_requests():
    conn = sqlite3.connect('prayers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prayer_requests ORDER BY date_submitted DESC')
    requests = cursor.fetchall()
    conn.close()
    return requests

def add_subscriber(email):
    conn = sqlite3.connect('prayers.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success