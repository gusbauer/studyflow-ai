from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange, Optional
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado.')
    
    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Las contraseñas no coinciden.')

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar sesión')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descripción', validators=[Optional()])
    subject = StringField('Materia', validators=[DataRequired(), Length(max=100)])
    priority = SelectField('Prioridad', choices=[
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta')
    ], validators=[DataRequired()])
    due_date = DateField('Fecha límite', validators=[Optional()], format='%Y-%m-%d')
    estimated_time = IntegerField('Tiempo estimado (minutos)', validators=[Optional(), NumberRange(min=1)])
    submit = SubmitField('Guardar tarea')