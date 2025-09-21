from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for simplicity
todos = []

# Home route
@app.route('/')
def index():
    return render_template('index.html', todos=todos)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos.append(task)
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(todos):
        todos.pop(task_id)
    return redirect(url_for('index'))

# Initialize the app (instead of before_first_request)
def init_app():
    print("To-Do App starting...")

if __name__ == '__main__':
    init_app()
    # Run on 0.0.0.0 so Docker can expose the port
    app.run(host='0.0.0.0', port=5000, debug=True)
