# app/routes/api.py
from flask import Blueprint, jsonify, request
from app.models.models import Task, Note, Document
from app import db

api = Blueprint('api', __name__)

@api.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'description': t.description,
        'due_date': t.due_date,
        'priority': t.priority,
        'completed': t.completed
    } for t in tasks])

@api.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        description=data['description'],
        due_date=data.get('due_date'),
        priority=data.get('priority', 'Medium')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'status': 'success'})

@api.route('/api/documents', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    # Process document with DocumentReader
    return jsonify({'status': 'success'})