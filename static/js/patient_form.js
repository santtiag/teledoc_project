document.addEventListener("DOMContentLoaded", function () {
  const idPaciente = document.getElementById("idPaciente").value;

  if (!idPaciente) {
    alert("ID de paciente no encontrado.");
    return;
  }

  // Verificar si el usuario está autenticado
  fetch("/verify_auth", {
    method: "GET",
    credentials: "include", // Importante para incluir las cookies en la solicitud
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("No autenticado");
      }
      return response.json();
    })
    .then((data) => {
      if (!data.authenticated) {
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      console.error("Error de autenticación:", error);
      window.location.href = "/login";
    });

  // Agregar el idPaciente a los datos del formulario cuando se envíe
  document.getElementById("patientForm").addEventListener("submit", (event) => {
    enviarFormulario(event, idPaciente);
  });

  manejarCamposAdicionales();
});

function enviarFormulario(event, idPaciente) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());

  const payload = {
    consultation_reason: data.motivo,
    allergic:
      data.alergia === "otros" ? data.alergia_especificar : data.alergia,
    medical_history:
      data.antecedentes === "si" ? data.antecedentes_especificar : "Ninguno",
    pharmacological_history:
      data.farmacologicos === "si"
        ? data.farmacologicos_especificar
        : "Ninguno",
    surgical_history:
      data.quirurgicos === "si" ? data.quirurgicos_especificar : "Ninguno",
    suggested_service_type: data.servicio,
    medical_recommendations: data.recomendaciones_medicas,
    pharmacological_recommendations: data.recomendaciones_farmacologicas,
    patient_id: idPaciente,
  };

  fetch("/patient_registration", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    credentials: "include", // Importante para incluir las cookies en la solicitud
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error en la respuesta del servidor");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Éxito:", data);
      alert("Formulario enviado con éxito");
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(
        "Hubo un error al enviar el formulario. Por favor, intenta de nuevo.",
      );
    });
}

function manejarCamposAdicionales() {
  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    radio.addEventListener("change", function () {
      const name = this.name;
      const textarea = document.getElementById(`${name}_especificar`);
      if (textarea) {
        if (this.value === "otros" || this.value === "si") {
          textarea.classList.remove("hidden");
          textarea.classList.add("visible");
        } else {
          textarea.classList.remove("visible");
          textarea.classList.add("hidden");
        }
      }
    });
  });
}
