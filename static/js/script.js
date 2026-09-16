console.log("StudyFlow AI cargado");

document.addEventListener("DOMContentLoaded", function () {
  // Cerrar automáticamente los mensajes de Flask
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    setTimeout(() => {
      const closeBtn = alert.querySelector(".btn-close");

      if (closeBtn) {
        closeBtn.click();
      }
    }, 5000);
  });

  // =========================================================
  // COMPLETAR / DESCOMPLETAR TAREAS
  // =========================================================

  document.querySelectorAll(".toggle-task-form").forEach((form) => {
    form.addEventListener("submit", async function (event) {
      event.preventDefault();

      const button = form.querySelector("button");
      const taskItem = form.closest(".task-item");

      if (!button) {
        return;
      }

      // Evitamos pulsaciones repetidas mientras se procesa
      button.disabled = true;

      try {
        const response = await fetch(form.action, {
          method: "POST",
          headers: {
            "X-CSRFToken":
              form.querySelector('input[name="csrf_token"]')?.value || "",
          },
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error("No se pudo cambiar el estado de la tarea.");
        }

        // =================================================
        // TAREA COMPLETADA
        // =================================================

        if (data.completed) {
          // Añadimos clase visual de completada
          if (taskItem) {
            taskItem.classList.add("task-completed");
          }

          // Cambiamos el botón
          button.classList.remove("btn-outline-success");
          button.classList.add("btn-success");

          button.innerHTML = `
                        <i class="bi bi-check-lg"></i>
                    `;

          button.title = "Marcar como pendiente";
        }

        // =================================================
        // TAREA VUELVE A ESTAR PENDIENTE
        // =================================================
        else {
          if (taskItem) {
            taskItem.classList.remove("task-completed");
          }

          button.classList.remove("btn-success");
          button.classList.add("btn-outline-success");

          button.innerHTML = `
                        <i class="bi bi-circle"></i>
                    `;

          button.title = "Marcar como completada";
        }
      } catch (error) {
        console.error("Error:", error);

        alert("No se pudo actualizar la tarea.");
      } finally {
        button.disabled = false;
      }
    });
  });
});
