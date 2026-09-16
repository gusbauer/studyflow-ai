from flask_login import UserMixin
from datetime import datetime
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    priority = db.Column(
        db.String(20),
        nullable=False,
        default="medium"
    )
    due_date = db.Column(db.Date, nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Task {self.title}>"

    def is_overdue(self):
        """Comprueba si la tarea está vencida."""
        if not self.due_date or self.completed:
            return False

        return datetime.utcnow().date() > self.due_date

    def days_until_due(self):
        """Devuelve los días que faltan para la fecha límite."""
        if not self.due_date:
            return None

        return (self.due_date - datetime.utcnow().date()).days

    def get_priority_label(self):
        """Devuelve la prioridad traducida al español."""
        labels = {
            "low": "Baja",
            "medium": "Media",
            "high": "Alta"
        }

        return labels.get(self.priority, "Media")

    def get_urgency(self):
        """
        Calcula visualmente la urgencia de una tarea.

        Devuelve:
        - key: identificador interno
        - label: texto que verá el usuario
        - css: clase CSS
        """

        if self.completed:
            return {
                "key": "completed",
                "label": "Completada",
                "css": "urgency-completed"
            }

        if not self.due_date:
            if self.priority == "high":
                return {
                    "key": "high",
                    "label": "Alta prioridad",
                    "css": "urgency-high"
                }

            return {
                "key": "no-date",
                "label": "Sin fecha",
                "css": "urgency-none"
            }

        days = self.days_until_due()

        if days < 0:
            return {
                "key": "overdue",
                "label": "Vencida",
                "css": "urgency-overdue"
            }

        if days == 0:
            return {
                "key": "today",
                "label": "Vence hoy",
                "css": "urgency-today"
            }

        if days <= 2:
            return {
                "key": "soon",
                "label": "Muy próxima",
                "css": "urgency-soon"
            }

        if days <= 7:
            return {
                "key": "week",
                "label": "Esta semana",
                "css": "urgency-week"
            }

        return {
            "key": "future",
            "label": "Con margen",
            "css": "urgency-future"
        }