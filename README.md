# StudyFlow AI

**Video Demo**: [URL del vídeo aquí]

**Descripción**:

StudyFlow AI es una aplicación web diseñada para estudiantes que desean organizar sus tareas académicas de manera eficiente y aprovechar la inteligencia artificial para optimizar su tiempo de estudio. Desarrollado como proyecto final para el curso CS50x de Harvard, este proyecto combina técnicas modernas de desarrollo web con la potencia de la IA para ofrecer una experiencia completa de gestión del aprendizaje.

## Características principales

- **Gestión de tareas**: CRUD completo con campos como título, descripción, materia, prioridad, fecha límite y tiempo estimado.
- **Filtros y búsqueda**: Filtrado por prioridad, materia, estado y búsqueda por texto.
- **Dashboard interactivo**: Visualización de estadísticas con gráficos (Chart.js) que muestran el estado de las tareas, prioridades, distribución por materias y productividad diaria.
- **Plan de estudio con IA**: Generación automática de un plan de estudio semanal basado en las tareas pendientes, considerando prioridad, fechas límite y tiempo estimado.
- **Autenticación de usuarios**: Registro, inicio de sesión y cierre de sesión con contraseñas cifradas y protección de rutas.
- **Diseño responsivo**: Interfaz moderna con Bootstrap 5, modo oscuro y animaciones suaves.

## Tecnologías utilizadas

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF.
- **Base de datos**: SQLite (con soporte para migrar a otras bases de datos).
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js, Bootstrap Icons.
- **IA**: OpenAI API (modelo GPT-3.5-turbo) para la generación de planes de estudio.
- **Control de versiones**: Git y GitHub.
- **Entorno**: Variables de entorno con python-dotenv.

## Arquitectura del proyecto

El proyecto sigue una arquitectura modular y profesional, separando las responsabilidades en diferentes capas:

- **app.py**: Punto de entrada de la aplicación, configura los blueprints y la aplicación Flask.
- **config.py**: Configuración centralizada utilizando variables de entorno.
- **extensions.py**: Inicialización de extensiones (SQLAlchemy, LoginManager, CSRF).
- **models.py**: Definición de los modelos de datos (User, Task).
- **forms.py**: Definición de formularios usando WTForms.
- **routes/**: Contiene los blueprints para agrupar las rutas por funcionalidad:
  - `auth.py`: Autenticación (registro, login, logout).
  - `tasks.py`: CRUD de tareas, búsqueda y filtros.
  - `dashboard.py`: Panel de control con estadísticas.
  - `ai.py`: Generación del plan de estudio con IA.
- **services/**: Lógica de negocio extraída de las rutas:
  - `ai_service.py`: Interacción con la API de OpenAI.
  - `statistics_service.py`: Cálculo de estadísticas para el dashboard.
  - `task_service.py`: Operaciones avanzadas con tareas.
- **utils/**: Funciones auxiliares (helpers).
- **templates/**: Plantillas HTML utilizando Jinja2.
- **static/**: Archivos estáticos (CSS, JavaScript).

Esta separación facilita el mantenimiento, las pruebas y la escalabilidad del proyecto.

## Decisiones de diseño

- **Uso de Blueprints**: Permite una organización clara de las rutas y evita un único archivo app.py con cientos de líneas.
- **Servicios**: La lógica de negocio se aísla en servicios para que las rutas solo manejen solicitudes HTTP y renderizado.
- **Seguridad**: Se utilizan contraseñas hasheadas con Werkzeug, protección CSRF en todos los formularios, y variables sensibles en .env.
- **IA como característica principal**: La integración con OpenAI no es un simple "extra"; es una funcionalidad clave que analiza todas las tareas del usuario y genera un plan personalizado.
- **Modo oscuro**: Por defecto, la interfaz usa el tema oscuro para reducir la fatiga visual durante el estudio nocturno.
- **Gráficos interactivos**: Chart.js proporciona visualizaciones atractivas que ayudan al usuario a comprender su progreso.

## Instalación y ejecución

### Requisitos previos

- Python 3.8 o superior.
- pip (gestor de paquetes de Python).
- Una clave API de OpenAI (obtén una en [platform.openai.com](https://platform.openai.com/)).

### Pasos

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/studyflow-ai.git
   cd studyflow-ai
   ```
