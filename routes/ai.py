from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import Task
from services.ai_service import AIService

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/plan')
@login_required
def plan():
    tasks = Task.query.filter_by(user_id=current_user.id, completed=False).all()
    return render_template('ai_plan.html', tasks=tasks, plan=None)

@ai_bp.route('/generate_plan', methods=['POST'])
@login_required
def generate_plan():
    tasks = Task.query.filter_by(user_id=current_user.id, completed=False).all()
    if not tasks:
        flash('No tienes tareas pendientes para generar un plan.', 'warning')
        return redirect(url_for('ai.plan'))

    plan = AIService.generate_study_plan(tasks)
    if plan is None:
        flash('Hubo un error al generar el plan. Verifica tu clave de OpenAI.', 'danger')
        return redirect(url_for('ai.plan'))

    return render_template('ai_plan.html', tasks=tasks, plan=plan)