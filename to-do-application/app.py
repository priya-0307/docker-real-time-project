from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="example",
        database="todo_db"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route('/add', methods=["POST"])
def add():
    task = request.form.get("task")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
