from flask import Blueprint, jsonify, request, current_app, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from app.models.models import Document, Note, Task
from app import db, document_reader
from difflib import get_close_matches
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date.asc()).all()
    return render_template('index.html', tasks=tasks)

@main_bp.route('/chat')
def chat():  # Changed from chat_page back to chat
    return render_template('chat.html')

@main_bp.route('/api/chat', methods=['POST'])
def chat_send():
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    # Document queries
    if user_message in ['show documents', 'show my documents', 'list documents']:
        documents = Document.query.order_by(Document.created_at.desc()).all()
        if documents:
            doc_list = "\n".join([f"📄 {doc.title}" for doc in documents])
            response = f"Here are your documents:\n{doc_list}"
        else:
            response = "Ready to store your first document! You can upload one anytime 📄"
            
    # Note queries
    elif user_message in ['show notes', 'show my notes', 'list notes']:
        notes = Note.query.order_by(Note.created_at.desc()).all()
        if notes:
            note_list = "\n".join([f"📝 {note.title}: {note.content[:50]}..." for note in notes])
            response = f"Here are your notes:\n{note_list}"
        else:
            response = "Your notes section is ready for your first entry! Try 'add note [your text]' 📝"
            
    # Task queries
    elif user_message in ['show tasks', 'show my tasks', 'list tasks']:
        tasks = Task.query.order_by(Task.due_date.asc()).all()
        if tasks:
            task_list = "\n".join([f"📋 {task.description}" for task in tasks])
            response = f"Here are your tasks:\n{task_list}"
        else:
            response = "Your task list is clear! Add tasks anytime with 'add task [description]' ✨"
            
    else:
        response = """I'm ready to help! Try these commands:
📄 'show documents' - View your files
📝 'show notes' - Check your notes
📋 'show tasks' - See your to-do list"""

    return jsonify({
        'response': response,
        'status': 'success'
    })

@main_bp.route('/add_task', methods=['POST'])
def add_task():
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority', 'Medium')
    
    if description:
        task = Task(
            description=description,
            due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
            priority=priority
        )
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/task/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/task/<int:id>/edit', methods=['POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    task.description = request.form.get('description', task.description)
    task.due_date = request.form.get('due_date', task.due_date)
    task.priority = request.form.get('priority', task.priority)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            note = Note(title=title, content=content)
            db.session.add(note)
            db.session.commit()
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=notes)

@main_bp.route('/documents', methods=['GET', 'POST'])
def documents():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                processor = DocumentProcessor()
                content = processor.process_document(filepath)
                
                doc = Document(
                    title=filename,
                    content=content['content'],
                    summary=content['summary'],
                    keywords=','.join(content['keywords']),
                    category=content['category'],
                    source=filename
                )
                db.session.add(doc)
                db.session.commit()
                
                os.remove(filepath)
                return redirect(url_for('main.documents'))
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return f"Error processing document: {str(e)}", 400
                
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('documents.html', documents=documents)
@main_bp.route('/documents/<int:id>')
def view_document(id):
    document = Document.query.get_or_404(id)
    return render_template('view_document.html', document=document)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    tasks = Task.query.filter(Task.description.ilike(f'%{query}%')).all()
    notes = Note.query.filter(db.or_(Note.title.ilike(f'%{query}%'), Note.content.ilike(f'%{query}%'))).all()
    documents = Document.query.filter(db.or_(Document.title.ilike(f'%{query}%'), Document.content.ilike(f'%{query}%'))).all()
    return render_template('search.html', tasks=tasks, notes=notes, documents=documents, query=query)

@main_bp.route('/tasks')
def tasks():
    tasks = Task.query.order_by(Task.due_date.asc()).all()
    return render_template('tasks.html', tasks=tasks)