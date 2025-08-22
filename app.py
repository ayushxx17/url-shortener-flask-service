from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
import string
import random
from urllib.parse import urlparse

# --------------------
# Flask App Setup
# --------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"  # For flash messages in forms

# --------------------
# Database Config
# --------------------
DB_NAME = "urls.db"

def get_conn():
    """Create and return a new SQLite database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create the 'urls' table if it doesn't exist."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL UNIQUE,
                short_code   TEXT NOT NULL UNIQUE,
                clicks       INTEGER DEFAULT 0,
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# Initialize DB on app start
init_db()

# --------------------
# Helper Functions
# --------------------
def normalize_url(url: str) -> str:
    """Ensure URL has a scheme (http/https)."""
    url = (url or "").strip()
    if not url:
        return url
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        url = "http://" + url
    return url

def code_exists(code: str) -> bool:
    """Check if a given short code already exists in DB."""
    with get_conn() as conn:
        row = conn.execute("SELECT 1 FROM urls WHERE short_code=?", (code,)).fetchone()
    return row is not None

def generate_code(length: int = 6) -> str:
    """Generate a unique short code with collision checking."""
    alphabet = string.ascii_letters + string.digits
    for _ in range(10):  # Try short codes of given length first
        code = "".join(random.choices(alphabet, k=length))
        if not code_exists(code):
            return code
    # Increase length if collisions continue
    while True:
        length += 1
        code = "".join(random.choices(alphabet, k=length))
        if not code_exists(code):
            return code

# --------------------
# Routes
# --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """Home page to create short URLs and show recent links."""
    short_url = None
    message = None

    if request.method == "POST":
        original = normalize_url(request.form.get("original_url", ""))
        
        if not original:
            flash("Please enter a valid URL.")
            return redirect(url_for("index"))

        parsed = urlparse(original)
        if parsed.scheme not in ("http", "https"):
            flash("Only HTTP/HTTPS URLs are allowed.")
            return redirect(url_for("index"))

        with get_conn() as conn:
            # Reuse existing short code if URL is already shortened
            row = conn.execute("SELECT short_code FROM urls WHERE original_url=?", (original,)).fetchone()
            if row:
                code = row["short_code"]
                message = "This URL was already shortened."
            else:
                code = generate_code()
                conn.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original, code))
                conn.commit()
                message = "Short URL created successfully."
        short_url = request.host_url + code

    with get_conn() as conn:
        recent = conn.execute("""
            SELECT original_url, short_code, clicks, created_at
            FROM urls
            ORDER BY id DESC LIMIT 10
        """).fetchall()

    return render_template("index.html", short_url=short_url, message=message, recent=recent)

@app.route("/<short_code>")
def follow(short_code):
    """Redirect user from short code to original URL."""
    with get_conn() as conn:
        row = conn.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,)).fetchone()
        if row:
            conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code=?", (short_code,))
            conn.commit()
            return redirect(row["original_url"], code=302)
    return render_template("404.html"), 404

# --------------------
# Main Entry
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
