# app/chat.py
from flask_socketio import emit
import nltk
from app import socketio, db
from app.models.models import Task, Note
from datetime import datetime

def analyze_intent(message):
    tokens = nltk.word_tokenize(message.lower())
    
    if any(word in tokens for word in ['add', 'create', 'new']):
        if 'task' in tokens:
            return 'add_task'
        elif 'note' in tokens:
            return 'add_note'
    elif any(word in tokens for word in ['show', 'list', 'view']):
        if 'task' in tokens:
            return 'show_tasks'
        elif 'note' in tokens:
            return 'show_notes'
    
    return 'unknown'

@socketio.on('connect')
def handle_connect():
    emit('response', {
        'text': "Hello! I'm your personal assistant. How can I help you today?",
        'suggestions': [
            {'text': 'Add Task', 'action': 'suggest', 'value': 'add task'},
            {'text': 'New Note', 'action': 'suggest', 'value': 'add note'},
            {'text': 'Show Tasks', 'action': 'suggest', 'value': 'show tasks'}
        ]
    })

@socketio.on('message')
def handle_message(data):
    user_message = data.get('text', '')
    intent = analyze_intent(user_message)
    
    if 'task' in user_message.lower():
        tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
        task_list = "\n".join([f"- {task.description}" for task in tasks])
        emit('response', {
            'text': f"Here are your recent tasks:\n{task_list}",
            'suggestions': [
                {'text': 'Add New Task', 'action': 'suggest', 'value': 'add task'},
                {'text': 'Show All Tasks', 'action': 'suggest', 'value': 'show all tasks'}
            ]
        })
    else:
        emit('response', {
            'text': "I understand you said: " + user_message + "\nWhat would you like to do?",
            'suggestions': [
                {'text': 'Add Task', 'action': 'suggest', 'value': 'add task'},
                {'text': 'New Note', 'action': 'suggest', 'value': 'add note'},
                {'text': 'Show Tasks', 'action': 'suggest', 'value': 'show tasks'}
            ]
        })