// Archivo principal de JavaScript
// Aquí se pueden añadir funcionalidades adicionales

console.log("StudyFlow AI cargado");

// Ejemplo: manejar cierre automático de alertas
document.addEventListener("DOMContentLoaded", function () {
  // Las alertas se cierran automáticamente después de 5 segundos
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const closeBtn = alert.querySelector(".btn-close");
      if (closeBtn) {
        closeBtn.click();
      }
    }, 5000);
  });
});
