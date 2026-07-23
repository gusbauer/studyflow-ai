from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, csrf
from models import User
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.dashboard import dashboard_bp
from routes.ai import ai_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    
    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)