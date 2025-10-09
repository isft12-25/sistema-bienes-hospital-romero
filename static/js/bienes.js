document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal-bien");
  const btnGuardar = document.getElementById("guardar-modal");
  const btnCancelar = document.getElementById("cancelar-modal");
  const btnAlta = document.getElementById("btn-alta"); // botón con ícono de tabla
  const tbody = document.querySelector(".tabla-operadores tbody");
  const tituloModal = document.getElementById("modal-titulo");

  let filaEnEdicion = null;

  // Abrir modal al editar
  document.addEventListener("click", (e) => {
    if (e.target.closest(".btn-editar")) {
      filaEnEdicion = e.target.closest("tr");
      tituloModal.textContent = "Editar Bien Patrimonial";
      cargarFormulario(filaEnEdicion);
      modal.classList.remove("oculto");
    }

    if (e.target.closest(".btn-eliminar")) {
      const fila = e.target.closest("tr");
      if (!fila.classList.contains("fila-edicion")) fila.remove();
    }
  });

  // Abrir modal en modo "Alta de Bien"
  btnAlta.addEventListener("click", () => {
    limpiarFormulario();
    filaEnEdicion = null;
    tituloModal.textContent = "Alta de Bien";
    modal.classList.remove("oculto");
  });

  // Cancelar modal
  btnCancelar.addEventListener("click", () => {
    modal.classList.add("oculto");
    limpiarFormulario();
    filaEnEdicion = null;
  });

  // Guardar cambios o alta nueva
  btnGuardar.addEventListener("click", () => {
    const d = obtenerDatosFormulario();
    if (filaEnEdicion) {
      actualizarFila(filaEnEdicion, d);
    } else {
      const nueva = document.createElement("tr");
      actualizarFila(nueva, d);
      tbody.appendChild(nueva);
    }
    modal.classList.add("oculto");
    limpiarFormulario();
    filaEnEdicion = null;
  });

  // Funciones auxiliares
  function obtenerDatosFormulario() {
    return {
      nombre: document.getElementById("nombre").value,
      descripcion: document.getElementById("descripcion").value,
      cantidad: document.getElementById("cantidad").value,
      expediente: document.getElementById("expediente").value,
      compra: document.getElementById("compra").value,
      cuenta: document.getElementById("cuenta").value,
      fecha: document.getElementById("fecha").value,
      origen: document.getElementById("origen").value,
      tipo: document.getElementById("tipo").value,
      estado: document.getElementById("estado").value,
      serie: document.getElementById("serie").value,
      precio: document.getElementById("precio").value,
      id: document.getElementById("id").value,
      nomenclatura: document.getElementById("nomenclatura").value,
      proveedor: document.getElementById("proveedor").value,
      servicio: document.getElementById("servicio").value,
    };
  }

  function actualizarFila(fila, d) {
    fila.innerHTML = `
      <td>${d.nombre}</td>
      <td>${d.descripcion}</td>
      <td>${d.cantidad}</td>
      <td>${d.expediente}</td>
      <td>${d.compra}</td>
      <td>${d.cuenta}</td>
      <td>${d.fecha}</td>
      <td>${d.origen}</td>
      <td>${d.tipo}</td>
      <td>${d.estado}</td>
      <td>${d.serie}</td>
      <td>$${d.precio}</td>
      <td>${d.id}</td>
      <td>${d.nomenclatura}</td>
      <td>${d.proveedor}</td>
      <td>${d.servicio}</td>
      <td><button class="btn-editar"><i class="fa-solid fa-pen"></i></button></td>
      <td><button class="btn-eliminar"><i class="fa-solid fa-trash"></i></button></td>
    `;
  }

  function cargarFormulario(fila) {
    const c = fila.querySelectorAll("td");
    document.getElementById("nombre").value = c[0].innerText;
    document.getElementById("descripcion").value = c[1].innerText;
    document.getElementById("cantidad").value = c[2].innerText;
    document.getElementById("expediente").value = c[3].innerText;
    document.getElementById("compra").value = c[4].innerText;
    document.getElementById("cuenta").value = c[5].innerText;
    document.getElementById("fecha").value = c[6].innerText;
    document.getElementById("origen").value = c[7].innerText;
    document.getElementById("tipo").value = c[8].innerText;
    document.getElementById("estado").value = c[9].innerText;
    document.getElementById("serie").value = c[10].innerText;
    document.getElementById("precio").value = c[11].innerText.replace("$", "");
    document.getElementById("id").value = c[12].innerText;
    document.getElementById("nomenclatura").value = c[13].innerText;
    document.getElementById("proveedor").value = c[14].innerText;
    document.getElementById("servicio").value = c[15].innerText;
  }

  function limpiarFormulario() {
    document.querySelectorAll("#modal-bien input, #modal-bien textarea").forEach(i => i.value = "");
  }
});

