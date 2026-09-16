from models import Task
from datetime import datetime, timedelta


class TaskService:

    @staticmethod
    def get_overdue_tasks(user_id):
        """Obtiene tareas vencidas no completadas."""

        today = datetime.utcnow().date()

        return Task.query.filter(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date < today
        ).all()

    @staticmethod
    def get_tasks_due_soon(user_id, days=3):
        """Obtiene tareas que vencen en los próximos días."""

        today = datetime.utcnow().date()
        future = today + timedelta(days=days)

        return Task.query.filter(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date.between(today, future)
        ).all()