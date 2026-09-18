import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Ruta absoluta para la base de datos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "studyflow.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI API
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL') or 'gpt-5.6-luna'
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = 86400  # 24 horas