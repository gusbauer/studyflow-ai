from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify
)

from flask_login import login_required, current_user
from datetime import datetime

from extensions import db
from models import Task
from forms import TaskForm

from sqlalchemy import or_, case


tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/")
@login_required
def list_tasks():
    """Lista de tareas con búsqueda, filtros y orden."""

    search = request.args.get("search", "").strip()
    priority = request.args.get("priority", "")
    subject = request.args.get("subject", "")
    status = request.args.get("status", "")
    sort = request.args.get("sort", "recent")

    query = Task.query.filter_by(user_id=current_user.id)

    # Búsqueda
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%"),
                Task.subject.ilike(f"%{search}%")
            )
        )

    # Filtro prioridad
    if priority:
        query = query.filter_by(priority=priority)

    # Filtro materia
    if subject:
        query = query.filter_by(subject=subject)

    # Filtro estado
    if status == "completed":
        query = query.filter_by(completed=True)

    elif status == "pending":
        query = query.filter_by(completed=False)

    # Orden
    if sort == "recent":
        query = query.order_by(Task.created_at.desc())

    elif sort == "old":
        query = query.order_by(Task.created_at.asc())

    elif sort == "urgent":
        query = query.order_by(
            Task.due_date.asc().nullslast()
        )

    elif sort == "priority":
        priority_case = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3),
            else_=4
        )

        query = query.order_by(priority_case)

    tasks = query.all()

    subjects = (
        db.session.query(Task.subject)
        .filter_by(user_id=current_user.id)
        .distinct()
        .all()
    )

    subjects = [subject[0] for subject in subjects]

    return render_template(
        "tasks.html",
        tasks=tasks,
        subjects=subjects,
        search=search,
        priority=priority,
        subject=subject,
        status=status,
        sort=sort
    )


@tasks_bp.route("/create", methods=["GET", "POST"])
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

        flash("Tarea creada exitosamente.", "success")

        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "task_form.html",
        form=form,
        title="Nueva Tarea"
    )


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash(
            "No tienes permiso para editar esta tarea.",
            "danger"
        )
        return redirect(url_for("tasks.list_tasks"))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.subject = form.subject.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.estimated_time = form.estimated_time.data

        db.session.commit()

        flash("Tarea actualizada.", "success")

        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "task_form.html",
        form=form,
        title="Editar Tarea",
        task=task
    )


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash(
            "No tienes permiso para eliminar esta tarea.",
            "danger"
        )
        return redirect(url_for("tasks.list_tasks"))

    db.session.delete(task)
    db.session.commit()

    flash("Tarea eliminada.", "success")

    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    """Marca una tarea como completada o pendiente."""

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return jsonify({
            "success": False,
            "error": "No autorizado"
        }), 403

    task.completed = not task.completed

    db.session.commit()

    urgency = task.get_urgency()

    return jsonify({
        "success": True,
        "completed": task.completed,
        "task_id": task.id,
        "urgency": urgency["key"],
        "urgency_label": urgency["label"]
    })


@tasks_bp.route("/calendar")
@login_required
def calendar():
    """Muestra el calendario de tareas."""

    return render_template("calendar.html")


@tasks_bp.route("/calendar/data")
@login_required
def calendar_data():
    """Devuelve las tareas del usuario en formato JSON para el calendario."""

    tasks = (
        Task.query
        .filter(
            Task.user_id == current_user.id,
            Task.due_date.isnot(None)
        )
        .all()
    )

    events = []

    colors = {
        "overdue": "#dc3545",
        "today": "#dc3545",
        "soon": "#fd7e14",
        "week": "#ffc107",
        "future": "#198754",
        "completed": "#6c757d",
        "high": "#dc3545",
        "no-date": "#6c757d"
    }

    for task in tasks:
        urgency = task.get_urgency()

        events.append({
            "id": task.id,
            "title": task.title,
            "start": task.due_date.isoformat(),
            "url": url_for(
                "tasks.task_detail",
                task_id=task.id
            ),
            "backgroundColor": colors.get(
                urgency["key"],
                "#0d6efd"
            ),
            "borderColor": colors.get(
                urgency["key"],
                "#0d6efd"
            ),
            "extendedProps": {
                "subject": task.subject,
                "priority": task.get_priority_label(),
                "urgency": urgency["label"],
                "completed": task.completed
            }
        })

    return jsonify(events)


@tasks_bp.route("/<int:task_id>")
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash(
            "No tienes permiso para ver esta tarea.",
            "danger"
        )
        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "task_detail.html",
        task=task
    )