import os
from flask import current_app
from openai import OpenAI


class AIService:

    @staticmethod
    def generate_study_plan(tasks):
        """
        Genera un plan de estudio semanal utilizando OpenAI.

        La IA recibe únicamente las tareas pendientes del usuario
        y devuelve un plan organizado de lunes a domingo.
        """

        if not tasks:
            return None

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            current_app.logger.error(
                "OPENAI_API_KEY no está configurada."
            )
            return None

        try:

            client = OpenAI(api_key=api_key)

            tasks_text = "\n".join([
                (
                    f"- Tarea: {task.title}\n"
                    f"  Materia: {task.subject}\n"
                    f"  Prioridad: {task.get_priority_label()}\n"
                    f"  Fecha límite: "
                    f"{task.due_date.strftime('%d/%m/%Y') if task.due_date else 'Sin fecha'}\n"
                    f"  Tiempo estimado: "
                    f"{task.estimated_time or 30} minutos"
                )
                for task in tasks
            ])

            prompt = f"""
Eres StudyFlow AI, un asistente especializado en organización
y planificación de estudios.

Debes crear un plan de estudio semanal realista utilizando
las tareas pendientes del estudiante.

TAREAS PENDIENTES:

{tasks_text}

REGLAS:

1. Prioriza las tareas con prioridad alta.
2. Da especial importancia a las tareas cuya fecha límite
   esté más próxima.
3. Las tareas vencidas deben aparecer como urgentes.
4. Respeta las fechas límite.
5. Utiliza el tiempo estimado de cada tarea.
6. Distribuye las tareas durante la semana para evitar
   concentrar demasiado trabajo en un único día.
7. Si una tarea requiere mucho tiempo, puedes dividirla
   en varias sesiones.
8. No inventes tareas que no estén en la lista.
9. No marques ninguna tarea como completada.
10. Si una tarea no tiene fecha límite, colócala donde
    tenga sentido según su prioridad.
11. Incluye descansos cuando la carga de trabajo de un día
    sea elevada.

FORMATO:

PLAN DE ESTUDIO SEMANAL

LUNES
- Tarea — Materia — X minutos
- Tarea — Materia — X minutos

MARTES
- Tarea — Materia — X minutos

MIÉRCOLES
...

JUEVES
...

VIERNES
...

SÁBADO
...

DOMINGO
...

AL FINAL incluye:

RECOMENDACIÓN
Una breve explicación de 2-4 frases sobre cómo has
organizado las tareas y cuáles deberían recibir más atención.

IMPORTANTE:
Utiliza solamente las tareas proporcionadas.
No añadas información inventada.
"""

            response = client.responses.create(
                model=current_app.config.get(
                    "OPENAI_MODEL",
                    "gpt-5.6-luna"
                ),
                input=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un asistente de organización "
                            "de estudios. Responde siempre "
                            "en español."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.output_text

        except Exception as e:

            current_app.logger.error(
                f"Error al generar plan con OpenAI: {e}"
            )

            return None