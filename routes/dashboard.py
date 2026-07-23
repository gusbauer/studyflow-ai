from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Task
from services.statistics_service import StatisticsService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    # Obtener estadísticas
    stats_service = StatisticsService(current_user.id)
    
    total_tasks = stats_service.get_total_tasks()
    completed_tasks = stats_service.get_completed_tasks()
    pending_tasks = total_tasks - completed_tasks
    high_priority_tasks = stats_service.get_high_priority_tasks()
    
    # Calcular productividad (porcentaje de completadas)
    productivity = stats_service.get_productivity()
    
    # Datos para gráficos
    chart_data = stats_service.get_chart_data()
    
    # Tareas recientes para mostrar en el dashboard (últimas 5)
    recent_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks,
                           high_priority_tasks=high_priority_tasks,
                           productivity=productivity,
                           chart_data=chart_data,
                           recent_tasks=recent_tasks)