from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models import Task
from forms import TaskForm
from services.task_service import TaskService
from sqlalchemy import or_

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def list_tasks():
    """Lista de tareas con filtros y búsqueda"""
    # Obtener parámetros de consulta
    search = request.args.get('search', '')
    priority = request.args.get('priority', '')
    subject = request.args.get('subject', '')
    status = request.args.get('status', '')  # 'completed' o 'pending'
    sort = request.args.get('sort', 'recent')  # recent, old, urgent, priority
    
    # Construir consulta base
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Aplicar filtros
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%'),
                Task.subject.ilike(f'%{search}%')
            )
        )
    if priority:
        query = query.filter_by(priority=priority)
    if subject:
        query = query.filter_by(subject=subject)
    if status == 'completed':
        query = query.filter_by(completed=True)
    elif status == 'pending':
        query = query.filter_by(completed=False)
    
    # Aplicar orden
    if sort == 'recent':
        query = query.order_by(Task.created_at.desc())
    elif sort == 'old':
        query = query.order_by(Task.created_at.asc())
    elif sort == 'urgent':
        # Ordenar por fecha límite más cercana (NULL al final)
        query = query.order_by(Task.due_date.asc().nullslast())
    elif sort == 'priority':
        # Ordenar por prioridad: high -> medium -> low
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        # No se puede hacer directamente con SQLAlchemy, usamos sorting en Python o case
        # Usamos case para ordenar
        from sqlalchemy import case
        priority_case = case(
            (Task.priority == 'high', 1),
            (Task.priority == 'medium', 2),
            (Task.priority == 'low', 3),
            else_=4
        )
        query = query.order_by(priority_case)
    
    tasks = query.all()
    
    # Obtener lista de materias únicas del usuario para el filtro
    subjects = db.session.query(Task.subject).filter_by(user_id=current_user.id).distinct().all()
    subjects = [s[0] for s in subjects]
    
    return render_template('tasks.html', tasks=tasks, subjects=subjects,
                          search=search, priority=priority, subject=subject,
                          status=status, sort=sort)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            estimated_time=form.estimated_time.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarea creada exitosamente.', 'success')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('task_form.html', form=form, title='Nueva Tarea')

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.subject = form.subject.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.estimated_time = form.estimated_time.data
        db.session.commit()
        flash('Tarea actualizada.', 'success')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('task_form.html', form=form, title='Editar Tarea', task=task)

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada.', 'success')
    return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    task.completed = not task.completed
    db.session.commit()
    
    return jsonify({
        'success': True,
        'completed': task.completed,
        'task_id': task.id
    })

@tasks_bp.route('/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No tienes permiso para ver esta tarea.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    return render_template('task_detail.html', task=task)