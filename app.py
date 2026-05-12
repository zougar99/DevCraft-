import csv
import os
import sqlite3
from pathlib import Path
from functools import wraps
from io import StringIO

from flask import (
    Flask,
    Response,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'medium',
            due_date TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )

    # Add new columns for old databases created before these fields existed.
    existing_columns = {
        row["name"] for row in db.execute("PRAGMA table_info(tasks)").fetchall()
    }
    if "priority" not in existing_columns:
        db.execute(
            "ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'"
        )
    if "due_date" not in existing_columns:
        db.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

    db.commit()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.")
            return render_template("register.html")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash("Account created. You can login now.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This username already exists.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    priority = request.args.get("priority", "all")

    where_parts = ["user_id = ?"]
    params = [session["user_id"]]

    if query:
        where_parts.append("title LIKE ?")
        params.append(f"%{query}%")

    if status == "done":
        where_parts.append("done = 1")
    elif status == "todo":
        where_parts.append("done = 0")

    if priority in {"low", "medium", "high"}:
        where_parts.append("priority = ?")
        params.append(priority)

    where_sql = " AND ".join(where_parts)
    tasks = db.execute(
        f"""
        SELECT id, title, done, priority, due_date, created_at
        FROM tasks
        WHERE {where_sql}
        ORDER BY
          CASE priority
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'low' THEN 3
            ELSE 4
          END,
          created_at DESC
        """,
        params,
    ).fetchall()

    stats = db.execute(
        """
        SELECT
          COUNT(*) AS total,
          SUM(CASE WHEN done = 1 THEN 1 ELSE 0 END) AS done_count,
          SUM(CASE WHEN done = 0 THEN 1 ELSE 0 END) AS todo_count
        FROM tasks
        WHERE user_id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        query=query,
        status=status,
        selected_priority=priority,
        stats=stats,
    )


@app.route("/tasks/create", methods=["POST"])
@login_required
def create_task():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "medium").strip().lower()
    due_date = request.form.get("due_date", "").strip() or None

    if not title:
        flash("Task title is required.")
        return redirect(url_for("dashboard"))

    if priority not in {"low", "medium", "high"}:
        priority = "medium"

    db = get_db()
    db.execute(
        "INSERT INTO tasks (user_id, title, done, priority, due_date) VALUES (?, ?, 0, ?, ?)",
        (session["user_id"], title, priority, due_date),
    )
    db.commit()
    return redirect(url_for("dashboard"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    db = get_db()
    task = db.execute(
        "SELECT id, done FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"]),
    ).fetchone()

    if task is None:
        flash("Task not found.")
        return redirect(url_for("dashboard"))

    new_done = 0 if task["done"] else 1
    db.execute(
        "UPDATE tasks SET done = ? WHERE id = ? AND user_id = ?",
        (new_done, task_id, session["user_id"]),
    )
    db.commit()
    return redirect(url_for("dashboard"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    db = get_db()
    db.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session["user_id"]),
    )
    db.commit()
    return redirect(url_for("dashboard"))


@app.route("/tasks/export")
@login_required
def export_tasks():
    db = get_db()
    tasks = db.execute(
        """
        SELECT title, done, priority, due_date, created_at
        FROM tasks
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (session["user_id"],),
    ).fetchall()

    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["title", "status", "priority", "due_date", "created_at"])
    for task in tasks:
        writer.writerow(
            [
                task["title"],
                "done" if task["done"] else "todo",
                task["priority"],
                task["due_date"] or "",
                task["created_at"],
            ]
        )

    csv_data = stream.getvalue()
    stream.close()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks.csv"},
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, use_reloader=False)
