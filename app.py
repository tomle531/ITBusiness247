from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "MeIT2015"  # change to any random string


# ---------- DATABASE HELPERS ----------

def get_db_connection():
    conn = sqlite3.connect("contact.db")
    conn.row_factory = sqlite3.Row  # lets us use row["name"]
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# create DB and table if not exist
init_db()


# ---------- PUBLIC ROUTES ----------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # save to SQLite
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()

        return render_template("contact.html", success=True, name=name)

    return render_template("contact.html", success=False)


# ---------- LOGIN / LOGOUT ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # SIMPLE HARDCODED CREDENTIALS (change these!)
        if username == "admin" and password == "MeIT123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_messages"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))


# ---------- PROTECTED ADMIN ROUTE ----------

@app.route("/admin/messages")
def admin_messages():
    # if not logged in, send to login page
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC")
    messages = c.fetchall()
    conn.close()
    return render_template("admin_messages.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
