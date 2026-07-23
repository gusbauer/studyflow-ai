import os
from flask import current_app

class AIService:
    @staticmethod
    def generate_study_plan(tasks):
        """Genera un plan de estudio semanal basado en las tareas pendientes.
        Si no hay clave de OpenAI o hay error, devuelve un plan de ejemplo."""
        if not tasks:
            return "No hay tareas pendientes para generar un plan."

        # Verificar si hay clave de OpenAI configurada
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key or api_key == 'tu_openai_api_key_aqui':
            # Si no hay clave, devolver un plan de ejemplo
            return AIService._generate_example_plan(tasks)

        try:
            import openai
            client = openai.OpenAI(api_key=api_key)

            # Construir el prompt con las tareas
            tasks_text = "\n".join([
                f"- {task.title} (Materia: {task.subject}, Prioridad: {task.get_priority_label()}, "
                f"Tiempo estimado: {task.estimated_time or 30} min, Vence: {task.due_date.strftime('%d/%m/%Y') if task.due_date else 'Sin fecha'})"
                for task in tasks
            ])

            prompt = f"""
            Eres un asistente de organización de estudios. Genera un plan de estudio semanal detallado para las siguientes tareas pendientes.

            Tareas:
            {tasks_text}

            Instrucciones:
            - Organiza las tareas por día de la semana (Lunes a Domingo).
            - Asigna las tareas de mayor prioridad primero.
            - Respeta las fechas límite.
            - Incluye el tiempo estimado para cada tarea.
            - Si hay muchas tareas, distribúyelas uniformemente.
            - Devuelve el plan en formato claro, con días y tareas.

            Formato de salida:
            **Lunes**
            - Tarea 1 (Materia) - X minutos
            - Tarea 2 (Materia) - X minutos

            **Martes**
            ...

            Responde solo con el plan, sin información adicional.
            """

            response = client.chat.completions.create(
                model=current_app.config.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "Eres un asistente de organización de estudios."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content

        except Exception as e:
            current_app.logger.error(f"Error al generar plan con IA: {e}")
            # Fallback a plan de ejemplo
            return AIService._generate_example_plan(tasks)

    @staticmethod
    def _generate_example_plan(tasks):
        """Genera un plan de estudio de ejemplo basado en las tareas (sin IA)."""
        # Si no hay tareas, devolver mensaje
        if not tasks:
            return "No hay tareas pendientes para generar un plan."

        # Días de la semana
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Ordenar tareas por prioridad (alta primero) y por fecha (más urgente primero)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(tasks, key=lambda t: (priority_order.get(t.priority, 1), t.due_date or "9999-12-31"))

        # Distribuir tareas entre los días (repartir uniformemente)
        plan = "**Plan de estudio semanal (generado automáticamente)**\n\n"
        
        if len(sorted_tasks) <= 7:
            # Si hay pocas tareas, una por día
            for i, task in enumerate(sorted_tasks):
                day = days[i % len(days)]
                plan += f"**{day}**\n- {task.title} ({task.subject}) - {task.estimated_time or 30} min\n\n"
        else:
            # Si hay muchas, agrupar varias por día
            tasks_per_day = len(sorted_tasks) // len(days) + 1
            for i, day in enumerate(days):
                start = i * tasks_per_day
                end = min(start + tasks_per_day, len(sorted_tasks))
                if start >= len(sorted_tasks):
                    break
                plan += f"**{day}**\n"
                for task in sorted_tasks[start:end]:
                    plan += f"- {task.title} ({task.subject}) - {task.estimated_time or 30} min\n"
                plan += "\n"

        return plan