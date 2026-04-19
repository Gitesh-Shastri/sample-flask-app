"""
Sample Flask REST API — intentionally missing production-readiness features.
Used as a demo target for production-ready-buddy / ShipReady.

Missing:
  - No health-check endpoint
  - No structured logging
  - No input validation
  - Secrets hard-coded (bad practice demo)
  - No rate limiting
  - No request timeouts
  - No proper error handlers
"""

from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# ❌ Hard-coded secret — never do this in production
SECRET_KEY = "super-secret-key-12345"
DB_PATH = os.environ.get("DB_PATH", "data.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done  INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/tasks", methods=["GET"])
def list_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/tasks", methods=["POST"])
def create_task():
    # ❌ No input validation
    data = request.get_json()
    title = data["title"]  # will crash if key missing
    conn = get_db()
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return jsonify({"id": task_id, "title": title, "done": 0}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    done = data.get("done", 0)
    conn = get_db()
    conn.execute("UPDATE tasks SET done=? WHERE id=?", (done, task_id))
    conn.commit()
    conn.close()
    return jsonify({"id": task_id, "done": done})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return "", 204


# ❌ No /health endpoint — will fail load-balancer health checks
# ❌ No /metrics endpoint — no observability
# ❌ Debug mode always on
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
