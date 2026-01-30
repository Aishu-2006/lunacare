from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# ---------- Database Connection ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Create Tables ----------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # User table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Period data table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS periods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        last_period TEXT,
        cycle_length INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- Home ----------
@app.route("/")
def home():
    return jsonify({"message": "Backend running"})

# ---------- Signup ----------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return {"message": "Signup successful"}
    except:
        return {"error": "User already exists"}
    finally:
        conn.close()

# ---------- Login ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return {"message": "Login successful", "user_id": user["id"]}
    else:
        return {"error": "Invalid credentials"}

# ---------- Add Period Data ----------
@app.route("/add-period", methods=["POST"])
def add_period():
    data = request.json
    user_id = data["user_id"]
    last_period = data["last_period"]
    cycle_length = data["cycle_length"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO periods (user_id, last_period, cycle_length) VALUES (?, ?, ?)",
        (user_id, last_period, cycle_length)
    )

    conn.commit()
    conn.close()

    return {"message": "Period data saved"}

if __name__ == "__main__":
    app.run(debug=True)
