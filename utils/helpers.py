from flask import flash, redirect, url_for
from functools import wraps
from flask_login import current_user

def role_required(role):
    """Decorador para requerir un rol específico (no usado en este proyecto, pero se puede ampliar)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Necesitas iniciar sesión.', 'warning')
                return redirect(url_for('auth.login'))
            # Aquí se podría verificar rol si se añade
            return f(*args, **kwargs)
        return decorated_function
    return decorator