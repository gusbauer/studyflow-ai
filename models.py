from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con tareas
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high
    due_date = db.Column(db.Date, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)  # en minutos
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def is_overdue(self):
        """Verifica si la tarea está vencida (si tiene fecha y no está completada)"""
        if not self.due_date or self.completed:
            return False
        return datetime.utcnow().date() > self.due_date
    
    def get_priority_label(self):
        """Devuelve la etiqueta de prioridad en español"""
        labels = {
            'low': 'Baja',
            'medium': 'Media',
            'high': 'Alta'
        }
        return labels.get(self.priority, 'Media')