import sqlite3
import random
import string
import time
from flask import Flask, request, jsonify, redirect, abort, render_template

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('database.db')

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            expires_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("original_url")
    custom_url = data.get("custom_url")
    expires_in_hours = data.get("expires_in_hours")
    original_url = data.get("original_url")

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    conn = get_db_connection()
    cursor = conn.cursor()

    # CUSTOM ALIAS LOGIC
    if custom_url:
        cursor.execute("SELECT short_code FROM urls WHERE short_code = ?", (custom_url,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "That custom alias is already taken!"}), 400
        short_code = custom_url
    else:
        short_code = generate_short_code()

    # EXPIRATION LOGIC
    expires_at = None
    if expires_in_hours:
        expires_at = int(time.time() + (int(expires_in_hours) * 3600))

    # SAVE TO DATABASE
    cursor.execute(
        "INSERT INTO urls (short_code, original_url, expires_at) VALUES (?, ?, ?)", 
        (short_code, original_url, expires_at)
    )
    
    conn.commit()
    conn.close()

    return jsonify({
        "short_code": short_code,
        "short_url": f"{request.host_url}{short_code}"
    }), 201

@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT original_url, expires_at FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()

    if result:
        original_url = result[0]
        expires_at = result[1]

        if expires_at and int(time.time()) > expires_at:
            cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
            conn.commit()
            conn.close()
            abort(410)

        conn.close()
        return redirect(original_url)
    else:
        conn.close()
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)