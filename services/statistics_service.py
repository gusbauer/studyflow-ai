from models import Task
from extensions import db
from datetime import datetime, timedelta

class StatisticsService:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_total_tasks(self):
        return Task.query.filter_by(user_id=self.user_id).count()
    
    def get_completed_tasks(self):
        return Task.query.filter_by(user_id=self.user_id, completed=True).count()
    
    def get_high_priority_tasks(self):
        return Task.query.filter_by(user_id=self.user_id, priority='high', completed=False).count()
    
    def get_productivity(self):
        total = self.get_total_tasks()
        if total == 0:
            return 0
        completed = self.get_completed_tasks()
        return int((completed / total) * 100)
    
    def get_chart_data(self):
        """Devuelve datos para los gráficos de Chart.js"""
        # Tareas por estado
        completed_count = self.get_completed_tasks()
        pending_count = Task.query.filter_by(user_id=self.user_id, completed=False).count()
        
        # Tareas por prioridad
        priority_counts = {}
        for p in ['low', 'medium', 'high']:
            count = Task.query.filter_by(user_id=self.user_id, priority=p).count()
            priority_counts[p] = count
        
        # Tareas por materia (top 5)
        from sqlalchemy import func
        subject_counts = db.session.query(
            Task.subject, func.count(Task.id)
        ).filter_by(user_id=self.user_id).group_by(Task.subject).order_by(func.count(Task.id).desc()).limit(5).all()
        
        # Tareas completadas en los últimos 7 días (para productividad diaria)
        daily_completed = []
        today = datetime.utcnow().date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            start = datetime(day.year, day.month, day.day)
            end = start + timedelta(days=1)
            count = Task.query.filter(
                Task.user_id == self.user_id,
                Task.completed == True,
                Task.created_at >= start,
                Task.created_at < end
            ).count()
            daily_completed.append({
                'day': day.strftime('%a'),
                'count': count
            })
        
        # Tareas por fecha de vencimiento (próximas)
        upcoming_deadlines = []
        for i in range(7):
            day = today + timedelta(days=i)
            count = Task.query.filter(
                Task.user_id == self.user_id,
                Task.due_date == day,
                Task.completed == False
            ).count()
            upcoming_deadlines.append({
                'day': day.strftime('%a %d'),
                'count': count
            })
        
        return {
            'status': {
                'labels': ['Completadas', 'Pendientes'],
                'values': [completed_count, pending_count]
            },
            'priority': {
                'labels': ['Baja', 'Media', 'Alta'],
                'values': [priority_counts.get('low', 0), priority_counts.get('medium', 0), priority_counts.get('high', 0)]
            },
            'subjects': {
                'labels': [item[0] for item in subject_counts],
                'values': [item[1] for item in subject_counts]
            },
            'daily_completed': {
                'labels': [item['day'] for item in daily_completed],
                'values': [item['count'] for item in daily_completed]
            },
            'upcoming_deadlines': {
                'labels': [item['day'] for item in upcoming_deadlines],
                'values': [item['count'] for item in upcoming_deadlines]
            }
        }