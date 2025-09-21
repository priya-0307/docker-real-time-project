import os
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Read DB config from environment
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "todo_db")
DB_USER = os.getenv("DB_USER", "todo_user")
DB_PASS = os.getenv("DB_PASS", "todo_pass")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

def wait_for_db(retries=8, delay=3):
    for i in range(retries):
        try:
            # attempt to create engine connection
            with app.app_context():
                db.session.execute("SELECT 1")
            app.logger.info("DB is available")
            return
        except OperationalError:
            app.logger.warning(f"DB not ready yet, retry {i+1}/{retries}...")
            time.sleep(delay)
    app.logger.error("Could not connect to DB after retries.")

@app.before_first_request
def setup_db():
    # Wait for DB then create tables
    wait_for_db()
    db.create_all()

# HTML UI
@app.route("/", methods=["GET"])
def index():
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template("index.html", todos=todos)

# API endpoints
@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return jsonify([t.to_dict() for t in todos])

@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json() or request.form
    title = data.get("title")
    if not title:
        return jsonify({"error": "title required"}), 400
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json() or {}
    if "done" in data:
        todo.done = bool(data["done"])
    else:
        todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"result": "deleted"})

if __name__ == "__main__":
    # Run on 0.0.0.0 so container exposes it
    app.run(host="0.0.0.0", port=5000, debug=True)
