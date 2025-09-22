from flask import Blueprint, request, jsonify
from . import db
from .models import Todo

bp = Blueprint('todo', __name__)

@bp.route('/todos', methods=['GET'])
def list_todos():
    todos = Todo.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'done': t.done} for t in todos])

@bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.json or {}
    t = Todo(title=data.get('title', 'Untitled'))
    db.session.add(t); db.session.commit()
    return jsonify({'id': t.id, 'title': t.title, 'done': t.done}), 201
