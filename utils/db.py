import sqlite3
from pathlib import Path

# =========================
# DATABASE CONFIG
# =========================

DB_PATH = Path("database/farmo.db")


def get_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# DATABASE INITIALIZATION
# =========================

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT
    )
    """)

    # Settings (Default Rates)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        work_type TEXT PRIMARY KEY,
        rate REAL NOT NULL
    )
    """)

    # Work Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        work_date TEXT NOT NULL,
        work_type TEXT NOT NULL,
        hours REAL DEFAULT 0,
        minutes INTEGER DEFAULT 0,
        trips INTEGER DEFAULT 0,
        rate REAL NOT NULL,
        amount REAL NOT NULL,
        credit_given REAL DEFAULT 0,
        notes TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Payments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        payment_date TEXT NOT NULL,
        amount REAL NOT NULL,
        notes TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Fuel Expenses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fuel_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_date TEXT NOT NULL,
        litres REAL NOT NULL,
        cost REAL NOT NULL,
        notes TEXT
    )
    """)

    # Service Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_date TEXT NOT NULL,
        service_type TEXT NOT NULL,
        cost REAL NOT NULL,
        notes TEXT
    )
    """)

    # Default Rates
    default_rates = [
        ("Rotavator", 1200),
        ("Nangarat", 900),
        ("Fanadi", 900),
        ("Trolley Trip", 500),
        ("Water Tanker Trip", 500)
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO settings(work_type, rate)
    VALUES (?, ?)
    """, default_rates)

    conn.commit()
    conn.close()


# =========================
# CUSTOMER FUNCTIONS
# =========================

def add_customer(name, mobile):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers (name, mobile)
    VALUES (?, ?)
    """, (name, mobile))

    conn.commit()
    conn.close()


def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM customers
    ORDER BY name ASC
    """)

    customers = cursor.fetchall()

    conn.close()

    return customers


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM customers
    WHERE id = ?
    """, (customer_id,))

    conn.commit()
    conn.close()


def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM customers
    WHERE id = ?
    """, (customer_id,))

    customer = cursor.fetchone()

    conn.close()

    return customer


# =========================
# WORK RECORD FUNCTIONS
# =========================

def add_work_record(
    customer_id,
    work_date,
    work_type,
    hours,
    minutes,
    trips,
    rate,
    amount,
    credit_given,
    notes
 ):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO work_records (
        customer_id,
        work_date,
        work_type,
        hours,
        minutes,
        trips,
        rate,
        amount,
        credit_given,
        notes
     )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_id,
        work_date,
        work_type,
        hours,
        minutes,
        trips,
        rate,
        amount,
        credit_given,
        notes
     ))

    conn.commit()
    conn.close()


def get_work_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM work_records
    ORDER BY work_date DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


# =========================
# SETTINGS FUNCTIONS
# =========================

def get_rates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM settings
    """)

    rates = cursor.fetchall()

    conn.close()

    return rates


def get_rate(work_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT rate
    FROM settings
    WHERE work_type = ?
    """, (work_type,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result["rate"]

    return 0


# =========================
# PAYMENT FUNCTIONS
# =========================

def add_payment(
    customer_id,
    payment_date,
    amount,
    notes
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO payments (
        customer_id,
        payment_date,
        amount,
        notes
    )
    VALUES (?, ?, ?, ?)
    """, (
        customer_id,
        payment_date,
        amount,
        notes
    ))

    conn.commit()
    conn.close()


def get_payments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM payments
    ORDER BY payment_date DESC
    """)

    payments = cursor.fetchall()

    conn.close()

    return payments


def get_customer_payments(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM payments
    WHERE customer_id = ?
    ORDER BY payment_date DESC
    """, (customer_id,))

    payments = cursor.fetchall()

    conn.close()

    return payments


# =========================
# LEDGER FUNCTIONS
# =========================

def get_customer_work_records(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM work_records
    WHERE customer_id = ?
    ORDER BY work_date DESC
    """, (customer_id,))

    records = cursor.fetchall()

    conn.close()

    return records


def get_customer_summary(customer_id):

    work_records = get_customer_work_records(customer_id)
    payments = get_customer_payments(customer_id)

    summary = {
        "rot_hours": 0,
        "rot_amount": 0,

        "nangarat_hours": 0,
        "nangarat_amount": 0,

        "fanadi_hours": 0,
        "fanadi_amount": 0,

        "trolley_trips": 0,
        "trolley_amount": 0,

        "tanker_trips": 0,
        "tanker_amount": 0,

        "total_work_amount": 0,
        "total_credit": 0,
        "total_payments": 0,
        "balance": 0
    }

    for row in work_records:

        work_type = row["work_type"]
        amount = row["amount"]
        credit = row["credit_given"]

        summary["total_work_amount"] += amount
        summary["total_credit"] += credit

        if work_type == "Rotavator":
            summary["rot_hours"] += row["hours"] + (row["minutes"] / 60)
            summary["rot_amount"] += amount

        elif work_type == "Nangarat":
            summary["nangarat_hours"] += row["hours"] + (row["minutes"] / 60)
            summary["nangarat_amount"] += amount

        elif work_type == "Fanadi":
            summary["fanadi_hours"] += row["hours"] + (row["minutes"] / 60)
            summary["fanadi_amount"] += amount

        elif work_type == "Trolley Trip":
            summary["trolley_trips"] += row["trips"]
            summary["trolley_amount"] += amount

        elif work_type == "Water Tanker Trip":
            summary["tanker_trips"] += row["trips"]
            summary["tanker_amount"] += amount

    for payment in payments:
        summary["total_payments"] += payment["amount"]

    summary["balance"] = (
        summary["total_work_amount"]
        - summary["total_credit"]
        - summary["total_payments"]
    )

    return summary



# =========================
# DASHBOARD FUNCTIONS
# =========================

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # Customers
    cursor.execute("SELECT COUNT(*) as total FROM customers")
    stats["total_customers"] = cursor.fetchone()["total"]

    # Work Entries
    cursor.execute("SELECT COUNT(*) as total FROM work_records")
    stats["total_work_entries"] = cursor.fetchone()["total"]

    # Payments
    cursor.execute("SELECT COUNT(*) as total FROM payments")
    stats["total_payments"] = cursor.fetchone()["total"]

    # Total Work Amount
    cursor.execute("""
    SELECT COALESCE(SUM(amount),0) as total
    FROM work_records
    """)
    stats["total_work_amount"] = cursor.fetchone()["total"]

    # Advance Received
    cursor.execute("""
    SELECT COALESCE(SUM(credit_given),0) as total
    FROM work_records
    """)
    stats["total_advance"] = cursor.fetchone()["total"]

    # Payments Received
    cursor.execute("""
    SELECT COALESCE(SUM(amount),0) as total
    FROM payments
    """)
    stats["total_payments_received"] = cursor.fetchone()["total"]

    # Rotavator
    cursor.execute("""
    SELECT
        COALESCE(SUM(hours + (minutes/60.0)),0) as total
    FROM work_records
    WHERE work_type='Rotavator'
    """)
    stats["rot_hours"] = cursor.fetchone()["total"]

    # Nangarat
    cursor.execute("""
    SELECT
        COALESCE(SUM(hours + (minutes/60.0)),0) as total
    FROM work_records
    WHERE work_type='Nangarat'
    """)
    stats["nangarat_hours"] = cursor.fetchone()["total"]

    # Fanadi
    cursor.execute("""
    SELECT
        COALESCE(SUM(hours + (minutes/60.0)),0) as total
    FROM work_records
    WHERE work_type='Fanadi'
    """)
    stats["fanadi_hours"] = cursor.fetchone()["total"]

    # Trolley
    cursor.execute("""
    SELECT
        COALESCE(SUM(trips),0) as total
    FROM work_records
    WHERE work_type='Trolley Trip'
    """)
    stats["trolley_trips"] = cursor.fetchone()["total"]

    # Tanker
    cursor.execute("""
    SELECT
        COALESCE(SUM(trips),0) as total
    FROM work_records
    WHERE work_type='Water Tanker Trip'
    """)
    stats["tanker_trips"] = cursor.fetchone()["total"]

    stats["pending_balance"] = (
        stats["total_work_amount"]
        - stats["total_advance"]
        - stats["total_payments_received"]
    )

    conn.close()

    return stats


# =========================
# REPORT FUNCTIONS
# =========================

def get_monthly_work_records(month, year):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        w.*,
        c.name as customer_name
    FROM work_records w
    JOIN customers c
        ON w.customer_id = c.id
    WHERE strftime('%m', w.work_date) = ?
    AND strftime('%Y', w.work_date) = ?
    ORDER BY w.work_date
    """, (
        f"{month:02d}",
        str(year)
    ))

    records = cursor.fetchall()

    conn.close()

    return records


def get_monthly_payments(month, year):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        p.*,
        c.name as customer_name
    FROM payments p
    JOIN customers c
        ON p.customer_id = c.id
    WHERE strftime('%m', p.payment_date) = ?
    AND strftime('%Y', p.payment_date) = ?
    ORDER BY p.payment_date
    """, (
        f"{month:02d}",
        str(year)
    ))

    records = cursor.fetchall()

    conn.close()

    return records


def get_monthly_summary(month, year):

    work_records = get_monthly_work_records(month, year)
    payments = get_monthly_payments(month, year)

    total_work_amount = sum(
        row["amount"]
        for row in work_records
    )

    total_advance = sum(
        row["credit_given"]
        for row in work_records
    )

    total_payments = sum(
        row["amount"]
        for row in payments
    )

    pending_balance = (
        total_work_amount
        - total_advance
        - total_payments
    )

    return {
        "total_work_amount": total_work_amount,
        "total_advance": total_advance,
        "total_payments": total_payments,
        "pending_balance": pending_balance
    }


