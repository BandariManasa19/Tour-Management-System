import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

import pymysql
from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DB_TYPE = os.getenv("DB_TYPE", "sqlite")


def get_connection():
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(BASE_DIR / "tour_ai_local.db")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "tour_ai_db"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    except Exception:
        conn = sqlite3.connect(BASE_DIR / "tour_ai_local.db")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor = conn.cursor()
            yield cursor, conn
        else:
            with conn.cursor() as cursor:
                yield cursor, conn
        conn.commit()
    finally:
        conn.close()


SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tour_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    destination TEXT NOT NULL,
    category TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    available_slots INTEGER DEFAULT 10,
    rating REAL DEFAULT 4.5,
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    travel_date TEXT NOT NULL,
    num_people INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'Confirmed',
    booking_status TEXT DEFAULT 'Pending',
    payment_status TEXT DEFAULT 'Pending',
    payment_deadline TEXT,
    cancellation_reason TEXT,
    journey_start_date TEXT,
    journey_end_date TEXT,
    booking_notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(package_id) REFERENCES tour_packages(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'Paid',
    paid_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(booking_id) REFERENCES bookings(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES tour_packages(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    prediction_label TEXT NOT NULL,
    recommended_category TEXT NOT NULL,
    confidence REAL,
    features_json TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS itinerary_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    destination TEXT NOT NULL,
    days INTEGER NOT NULL,
    budget REAL NOT NULL,
    interests TEXT,
    travel_type TEXT,
    response_text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""


MYSQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tour_packages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    destination VARCHAR(120) NOT NULL,
    category VARCHAR(50) NOT NULL,
    duration INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    available_slots INT DEFAULT 10,
    rating DECIMAL(3,2) DEFAULT 4.50,
    image_url VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    package_id INT NOT NULL,
    travel_date DATE NOT NULL,
    num_people INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed',
    booking_status VARCHAR(50) DEFAULT 'Pending',
    payment_status VARCHAR(50) DEFAULT 'Pending',
    payment_deadline DATETIME,
    cancellation_reason TEXT,
    journey_start_date DATE,
    journey_end_date DATE,
    booking_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (package_id) REFERENCES tour_packages(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Paid',
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    package_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES tour_packages(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ai_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    prediction_label VARCHAR(80) NOT NULL,
    recommended_category VARCHAR(80) NOT NULL,
    confidence DECIMAL(5,4),
    features_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS itinerary_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    destination VARCHAR(120) NOT NULL,
    days INT NOT NULL,
    budget DECIMAL(10,2) NOT NULL,
    interests TEXT,
    travel_type VARCHAR(80),
    response_text LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;
"""


def execute_sql(sql):
    with get_cursor() as (cursor, conn):
        if isinstance(conn, sqlite3.Connection):
            cursor.executescript(sql)
        else:
            cursor.execute(sql)


def get_sqlite_columns(table_name):
    connection = get_connection()
    try:
        if not isinstance(connection, sqlite3.Connection):
            return set()
        cursor = connection.execute(f"PRAGMA table_info({table_name})")
        return {row[1] for row in cursor.fetchall()}
    finally:
        connection.close()


def get_mysql_columns(table_name):
    connection = get_connection()
    try:
        if isinstance(connection, sqlite3.Connection):
            return set()
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            return {row["Field"] for row in cursor.fetchall()}
    finally:
        connection.close()


def column_exists(table_name, column_name):
    if DB_TYPE == "sqlite":
        return column_name in get_sqlite_columns(table_name)
    return column_name in get_mysql_columns(table_name)


def migrate_bookings_schema():
    if DB_TYPE == "sqlite":
        columns = get_sqlite_columns("bookings")
        if "booking_status" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN booking_status TEXT DEFAULT 'Pending'")
        if "payment_status" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN payment_status TEXT DEFAULT 'Pending'")
        if "payment_deadline" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN payment_deadline TEXT")
        if "cancellation_reason" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN cancellation_reason TEXT")
        if "journey_start_date" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN journey_start_date TEXT")
        if "journey_end_date" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN journey_end_date TEXT")
        if "booking_notes" not in columns:
            execute_sql("ALTER TABLE bookings ADD COLUMN booking_notes TEXT")
        return

    columns = get_mysql_columns("bookings")
    alterations = [
        "ADD COLUMN booking_status VARCHAR(50) DEFAULT 'Pending'",
        "ADD COLUMN payment_status VARCHAR(50) DEFAULT 'Pending'",
        "ADD COLUMN payment_deadline DATETIME",
        "ADD COLUMN cancellation_reason TEXT",
        "ADD COLUMN journey_start_date DATE",
        "ADD COLUMN journey_end_date DATE",
        "ADD COLUMN booking_notes TEXT",
    ]

    for alteration in alterations:
        column_name = alteration.split()[2]
        if column_name not in columns:
            execute_sql(f"ALTER TABLE bookings {alteration}")


def remove_duplicate_packages():
    if DB_TYPE == "sqlite":
        duplicates = fetch_all(
            "SELECT title, MIN(id) AS keep_id FROM tour_packages GROUP BY title HAVING COUNT(*) > 1"
        )
        for row in duplicates:
            title = row[0] if isinstance(row, tuple) else row["title"]
            keep_id = row[1] if isinstance(row, tuple) else row["keep_id"]
            execute("DELETE FROM tour_packages WHERE title = ? AND id != ?", (title, keep_id))
        execute_sql("CREATE UNIQUE INDEX IF NOT EXISTS idx_tour_packages_title ON tour_packages(title)")
        return

    duplicates = fetch_all(
        "SELECT title, MIN(id) AS keep_id FROM tour_packages GROUP BY title HAVING COUNT(*) > 1"
    )
    for row in duplicates:
        title = row["title"] if isinstance(row, dict) else row[0]
        keep_id = row["keep_id"] if isinstance(row, dict) else row[1]
        execute("DELETE FROM tour_packages WHERE title = %s AND id != %s", (title, keep_id))
    try:
        execute_sql("CREATE UNIQUE INDEX idx_tour_packages_title ON tour_packages(title)")
    except Exception:
        pass


def ensure_demo_admin():
    if get_admin_by_email("admin@example.com") is None:
        create_admin("Demo Admin", "admin@example.com", generate_password_hash("admin123"))


def init_database():
    connection = get_connection()
    is_sqlite = isinstance(connection, sqlite3.Connection)
    connection.close()
    schema = SQLITE_SCHEMA if is_sqlite else MYSQL_SCHEMA
    try:
        execute_sql(schema)
        migrate_bookings_schema()
        remove_duplicate_packages()
        seed_demo_data()
        ensure_demo_admin()
    except Exception as exc:
        print(f"Database initialization error: {exc}")


def seed_demo_data():
    packages = [
        ("Goa Sunset Kayak", "Goa", "Adventure", 3, 9200, "Kayak through coastal waters, relax at beach cafes, and enjoy an easy sunset itinerary.", 14, 4.7, "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=900&q=80"),
        ("Manali Mountain Trek", "Manali", "Adventure", 5, 13500, "Guided mountain treks, river rafting, and cozy guesthouse stays in the hills.", 10, 4.6, "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=900&q=80"),
        ("Kashmir Valley Retreat", "Kashmir", "Luxury", 6, 29200, "Luxury houseboat nights, meadow walks, and private valley transfers.", 5, 4.9, "https://images.unsplash.com/photo-1561484938-a643aee9ae61?auto=format&fit=crop&w=900&q=80"),
        ("Ooty Tea Garden Stay", "Ooty", "Hill Station", 4, 11200, "Tea estate tours, lake boating, and hill-resort relaxation.", 12, 4.7, "https://images.unsplash.com/photo-1512572631757-2e11f2fd8472?auto=format&fit=crop&w=900&q=80"),
        ("Kerala Backwater Escape", "Kerala", "Honeymoon", 5, 14800, "Romantic houseboat cruise, spa treatments, and scenic backwater views.", 8, 4.8, "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80"),
        ("Jaipur Palace & Culture", "Jaipur", "Cultural", 4, 10800, "Heritage hotels, palace tours, and evening cultural performances.", 10, 4.7, "https://images.unsplash.com/photo-1526481280697-3bfa7568dafe?auto=format&fit=crop&w=900&q=80"),
        ("Shimla Heritage Journey", "Shimla", "Hill Station", 4, 9800, "Historic hill station walks, colonial hotels, and local bakery tastings.", 12, 4.5, "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?auto=format&fit=crop&w=900&q=80"),
        ("Ladakh High Pass Tour", "Leh", "Adventure", 7, 23800, "High-altitude routes, monasteries, and scenic lake stops with expert guides.", 7, 4.8, "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80"),
        ("Andaman Beach Hideaway", "Andaman", "Beach", 5, 19200, "Island snorkeling, glass-bottom boat rides, and beachside resorts.", 8, 4.8, "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80"),
        ("Pondicherry Coastal Weekend", "Pondicherry", "Romantic", 3, 9200, "French quarter stays, coastal walks, and relaxed seaside dining.", 10, 4.6, "https://images.unsplash.com/photo-1499613837595-7cf5368ad8b8?auto=format&fit=crop&w=900&q=80"),
        ("Darjeeling Tea & Mountain", "Darjeeling", "Hill Station", 4, 11800, "Toy train rides, tea garden visits, and panoramic mountain views.", 10, 4.7, "https://images.unsplash.com/photo-1544797834-2662f09c537e?auto=format&fit=crop&w=900&q=80"),
        ("Munnar Luxury Resort", "Munnar", "Luxury", 4, 17500, "Private resort villas, spice garden walks, and premium wellness experiences.", 6, 4.9, "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80"),
        ("Mysore Royal Family", "Mysore", "Family", 3, 8400, "Palace tours, zoo visits, and family-friendly heritage lodging.", 12, 4.6, "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=80"),
        ("Coorg Coffee & Nature", "Coorg", "Relax", 4, 10900, "Plantation stays, forest trails, and coffee-tasting experiences.", 9, 4.7, "https://images.unsplash.com/photo-1483683804023-6ccdb62f86ef?auto=format&fit=crop&w=900&q=80"),
        ("Rishikesh Adventure Camp", "Rishikesh", "Adventure", 4, 9600, "River rafting, campfire evenings, and yoga by the Ganges.", 14, 4.6, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"),
        ("Agra History Break", "Agra", "Cultural", 2, 6200, "Taj Mahal sunrise, heritage hotel stay, and city food tour.", 18, 4.5, "https://images.unsplash.com/photo-1460898173510-0a1010f9ddc6?auto=format&fit=crop&w=900&q=80"),
        ("Udaipur Lake Palace Stay", "Udaipur", "Honeymoon", 4, 15500, "Luxury lakefront hotel, boat rides, and palace dining experiences.", 7, 4.8, "https://images.unsplash.com/photo-1507149833265-60c372daea22?auto=format&fit=crop&w=900&q=80"),
        ("Meghalaya Waterfall Trail", "Meghalaya", "Wildlife", 5, 12800, "Waterfall treks, living root bridges, and forest camps.", 9, 4.7, "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80"),
        ("Sikkim Mountain Discovery", "Sikkim", "Adventure", 6, 14200, "Mountain passes, monasteries, and scenic valley stays.", 8, 4.7, "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80"),
        ("Kodaikanal Cool Escape", "Kodaikanal", "Romantic", 3, 10200, "Lake views, cottage stays, and candlelit dinners.", 10, 4.6, "https://images.unsplash.com/photo-1483683804023-6ccdb62f86ef?auto=format&fit=crop&w=900&q=80"),
        ("Dubai City & Desert", "Dubai", "International", 5, 32500, "City attractions, desert safari, and luxury hotel comforts.", 7, 4.8, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"),
        ("Bali Island Retreat", "Bali", "International", 5, 22800, "Beach villas, temple visits, and island wellness sessions.", 8, 4.9, "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80"),
        ("Maldives Overwater Stay", "Maldives", "Luxury", 5, 29800, "Overwater villa stay, snorkeling, and private beach dining.", 5, 4.9, "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80"),
        ("Swiss Alps Scenic Rail", "Switzerland", "International", 6, 34500, "Alpine rail journey, lakeside stays, and luxury mountain lodges.", 5, 4.9, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"),
        ("Paris Art & Cuisine", "Paris", "International", 5, 33000, "Museum tours, fine dining, and Seine river evenings.", 6, 4.8, "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80"),
        ("Thailand Beach & Culture", "Thailand", "International", 5, 17800, "Island beach time, cultural temple tours, and street food evenings.", 8, 4.7, "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=900&q=80"),
        ("Kanyakumari Sunset Tour", "Kanyakumari", "Beach", 3, 8900, "Sunrise and sunset views at India's southern tip with coastal heritage stays.", 12, 4.5, "https://images.unsplash.com/photo-1483683804023-6ccdb62f86ef?auto=format&fit=crop&w=900&q=80"),
        ("Khajuraho Temple Journey", "Khajuraho", "Spiritual", 3, 9200, "UNESCO temples, light and sound show, and heritage hotel support.", 10, 4.6, "https://images.unsplash.com/photo-1460898173510-0a1010f9ddc6?auto=format&fit=crop&w=900&q=80"),
        ("Ranthambore Wildlife Safari", "Ranthambore", "Wildlife", 3, 12900, "Safari drives, wildlife sightings, and lodge stays near the tiger reserve.", 7, 4.7, "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80"),
    ]

    with get_cursor() as (cursor, conn):
        if isinstance(conn, sqlite3.Connection):
            cursor.executemany(
                "INSERT OR IGNORE INTO tour_packages (title, destination, category, duration, price, description, available_slots, rating, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                packages,
            )
        else:
            cursor.executemany(
                "INSERT IGNORE INTO tour_packages (title, destination, category, duration, price, description, available_slots, rating, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                packages,
            )


# Generic query helpers

def fetch_all(query, params=None):
    with get_cursor() as (cursor, conn):
        if params is None:
            params = ()
        cursor.execute(query, params)
        return cursor.fetchall()


def fetch_one(query, params=None):
    with get_cursor() as (cursor, conn):
        if params is None:
            params = ()
        cursor.execute(query, params)
        return cursor.fetchone()


def execute(query, params=None):
    with get_cursor() as (cursor, conn):
        if params is None:
            params = ()
        cursor.execute(query, params)
        return cursor.lastrowid


def create_user(full_name, email, password_hash, phone=None):
    query = "INSERT INTO users (full_name, email, password_hash, phone) VALUES (%s, %s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO users (full_name, email, password_hash, phone) VALUES (?, ?, ?, ?)"
    params = (full_name, email, password_hash, phone)
    return execute(query, params)


def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s" if DB_TYPE != "sqlite" else "SELECT * FROM users WHERE email = ?"
    return fetch_one(query, (email,))


def get_admin_by_email(email):
    query = "SELECT * FROM admins WHERE email = %s" if DB_TYPE != "sqlite" else "SELECT * FROM admins WHERE email = ?"
    return fetch_one(query, (email,))


def create_admin(full_name, email, password_hash):
    query = "INSERT INTO admins (full_name, email, password_hash) VALUES (%s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO admins (full_name, email, password_hash) VALUES (?, ?, ?)"
    return execute(query, (full_name, email, password_hash))


def get_all_packages(search=None, category=None, destination=None, budget=None, page=None, per_page=None):
    query = "SELECT * FROM tour_packages WHERE 1=1"
    params = []
    if search:
        query += " AND (title LIKE %s OR destination LIKE %s OR description LIKE %s)" if DB_TYPE != "sqlite" else " AND (title LIKE ? OR destination LIKE ? OR description LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    if category:
        query += " AND category = %s" if DB_TYPE != "sqlite" else " AND category = ?"
        params.append(category)
    if destination:
        query += " AND destination = %s" if DB_TYPE != "sqlite" else " AND destination = ?"
        params.append(destination)
    if budget is not None:
        query += " AND price <= %s" if DB_TYPE != "sqlite" else " AND price <= ?"
        params.append(float(budget))
    query += " ORDER BY rating DESC"
    if per_page is not None and page is not None:
        query += " LIMIT %s OFFSET %s" if DB_TYPE != "sqlite" else " LIMIT ? OFFSET ?"
        params.extend([int(per_page), int((page - 1) * per_page)])
    return fetch_all(query, tuple(params))


def count_packages(search=None, category=None, destination=None, budget=None):
    query = "SELECT COUNT(*) AS total FROM tour_packages WHERE 1=1"
    params = []
    if search:
        query += " AND (title LIKE %s OR destination LIKE %s OR description LIKE %s)" if DB_TYPE != "sqlite" else " AND (title LIKE ? OR destination LIKE ? OR description LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    if category:
        query += " AND category = %s" if DB_TYPE != "sqlite" else " AND category = ?"
        params.append(category)
    if destination:
        query += " AND destination = %s" if DB_TYPE != "sqlite" else " AND destination = ?"
        params.append(destination)
    if budget is not None:
        query += " AND price <= %s" if DB_TYPE != "sqlite" else " AND price <= ?"
        params.append(float(budget))
    result = fetch_one(query, tuple(params))
    return result[0] if DB_TYPE == "sqlite" else result["total"]


def get_package_by_id(package_id):
    query = "SELECT * FROM tour_packages WHERE id = %s" if DB_TYPE != "sqlite" else "SELECT * FROM tour_packages WHERE id = ?"
    return fetch_one(query, (package_id,))


def create_booking(user_id, package_id, travel_date, num_people, total_amount, payment_method="Card", payment_deadline=None, journey_end_date=None, booking_notes=""):
    if payment_deadline is None:
        payment_deadline = (datetime.utcnow() + timedelta(minutes=5)).replace(microsecond=0).isoformat() + "Z"
    if journey_end_date is None:
        journey_end_date = travel_date

    query = (
        "INSERT INTO bookings (user_id, package_id, travel_date, num_people, total_amount, status, booking_status, payment_status, payment_deadline, journey_start_date, journey_end_date, booking_notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if DB_TYPE != "sqlite"
        else "INSERT INTO bookings (user_id, package_id, travel_date, num_people, total_amount, status, booking_status, payment_status, payment_deadline, journey_start_date, journey_end_date, booking_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    booking_id = execute(query, (user_id, package_id, travel_date, num_people, total_amount, "Pending", "Pending", "Pending", payment_deadline, travel_date, journey_end_date, booking_notes))
    payment_query = "INSERT INTO payments (booking_id, payment_method, amount, status) VALUES (%s, %s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO payments (booking_id, payment_method, amount, status) VALUES (?, ?, ?, ?)"
    execute(payment_query, (booking_id, payment_method, total_amount, "Pending"))
    return booking_id


def confirm_booking_payment(booking_id):
    execute(
        "UPDATE bookings SET status = %s, booking_status = %s, payment_status = %s WHERE id = %s" if DB_TYPE != "sqlite" else "UPDATE bookings SET status = ?, booking_status = ?, payment_status = ? WHERE id = ?",
        ("Confirmed", "Confirmed", "Paid", booking_id),
    )
    execute(
        "UPDATE payments SET status = %s WHERE booking_id = %s" if DB_TYPE != "sqlite" else "UPDATE payments SET status = ? WHERE booking_id = ?",
        ("Paid", booking_id),
    )
    return booking_id


def cancel_booking(booking_id, reason=""):
    execute(
        "UPDATE bookings SET status = %s, booking_status = %s, payment_status = %s, cancellation_reason = %s WHERE id = %s" if DB_TYPE != "sqlite" else "UPDATE bookings SET status = ?, booking_status = ?, payment_status = ?, cancellation_reason = ? WHERE id = ?",
        ("Cancelled", "Cancelled", "Cancelled", reason, booking_id),
    )
    return booking_id


def get_booking_by_id(booking_id):
    query = "SELECT * FROM bookings WHERE id = %s" if DB_TYPE != "sqlite" else "SELECT * FROM bookings WHERE id = ?"
    return fetch_one(query, (booking_id,))


def get_user_bookings(user_id):
    query = """
    SELECT b.*, p.title, p.destination, p.category, p.duration
    FROM bookings b
    JOIN tour_packages p ON p.id = b.package_id
    WHERE b.user_id = %s
    ORDER BY b.created_at DESC
    """ if DB_TYPE != "sqlite" else """
    SELECT b.*, p.title, p.destination, p.category, p.duration
    FROM bookings b
    JOIN tour_packages p ON p.id = b.package_id
    WHERE b.user_id = ?
    ORDER BY b.created_at DESC
    """
    return fetch_all(query, (user_id,))


def get_all_bookings():
    query = """
    SELECT b.*, u.full_name, p.title, p.destination
    FROM bookings b
    JOIN users u ON u.id = b.user_id
    JOIN tour_packages p ON p.id = b.package_id
    ORDER BY b.created_at DESC
    """
    return fetch_all(query)


def get_all_users():
    return fetch_all("SELECT * FROM users ORDER BY created_at DESC")


def save_prediction(user_id, prediction_label, recommended_category, confidence, features_json):
    query = "INSERT INTO ai_predictions (user_id, prediction_label, recommended_category, confidence, features_json) VALUES (%s, %s, %s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO ai_predictions (user_id, prediction_label, recommended_category, confidence, features_json) VALUES (?, ?, ?, ?, ?)"
    return execute(query, (user_id, prediction_label, recommended_category, confidence, features_json))


def save_itinerary_history(user_id, destination, days, budget, interests, travel_type, response_text):
    query = "INSERT INTO itinerary_history (user_id, destination, days, budget, interests, travel_type, response_text) VALUES (%s, %s, %s, %s, %s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO itinerary_history (user_id, destination, days, budget, interests, travel_type, response_text) VALUES (?, ?, ?, ?, ?, ?, ?)"
    return execute(query, (user_id, destination, days, budget, interests, travel_type, response_text))


def get_itinerary_history(user_id):
    query = "SELECT * FROM itinerary_history WHERE user_id = %s ORDER BY created_at DESC" if DB_TYPE != "sqlite" else "SELECT * FROM itinerary_history WHERE user_id = ? ORDER BY created_at DESC"
    return fetch_all(query, (user_id,))


def add_review(package_id, user_id, rating, comment):
    query = "INSERT INTO reviews (package_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)" if DB_TYPE != "sqlite" else "INSERT INTO reviews (package_id, user_id, rating, comment) VALUES (?, ?, ?, ?)"
    return execute(query, (package_id, user_id, rating, comment))


def get_reviews_for_package(package_id):
    query = """
    SELECT r.*, u.full_name
    FROM reviews r
    JOIN users u ON u.id = r.user_id
    WHERE r.package_id = %s
    ORDER BY r.created_at DESC
    """ if DB_TYPE != "sqlite" else """
    SELECT r.*, u.full_name
    FROM reviews r
    JOIN users u ON u.id = r.user_id
    WHERE r.package_id = ?
    ORDER BY r.created_at DESC
    """
    return fetch_all(query, (package_id,))


def get_dashboard_summary():
    total_bookings = fetch_one("SELECT COUNT(*) AS count FROM bookings")[0] if DB_TYPE == "sqlite" else fetch_one("SELECT COUNT(*) AS count FROM bookings")["count"]
    total_users = fetch_one("SELECT COUNT(*) AS count FROM users")[0] if DB_TYPE == "sqlite" else fetch_one("SELECT COUNT(*) AS count FROM users")["count"]
    revenue = fetch_one("SELECT COALESCE(SUM(total_amount), 0) AS total FROM bookings")[0] if DB_TYPE == "sqlite" else fetch_one("SELECT COALESCE(SUM(total_amount), 0) AS total FROM bookings")["total"]
    return {
        "total_bookings": total_bookings,
        "total_users": total_users,
        "revenue": float(revenue),
    }


def get_destination_stats():
    query = """
    SELECT p.destination, COUNT(b.id) AS bookings
    FROM bookings b
    JOIN tour_packages p ON p.id = b.package_id
    GROUP BY p.destination
    ORDER BY bookings DESC
    """
    return fetch_all(query)


def get_recent_predictions():
    query = "SELECT * FROM ai_predictions ORDER BY created_at DESC LIMIT 5"
    return fetch_all(query)
