async function listarRegistros() {
    const res = await fetch(API_BASE + ENDPOINTS.read_all);
    const data = await res.json();
    const lista = document.getElementById("listaRegistros");
    lista.innerHTML = "";
    data.forEach(r => {
        const item = document.createElement("li");
        item.textContent = `ID: ${r.id} - ${r.nombre} ${r.apellido} - ${r.nacimiento} - ${r.email}`;
        lista.appendChild(item);
    });
}

document.getElementById("formRegistro").addEventListener("submit", async function(e) {
    e.preventDefault();
    const body = {
        nombre: document.getElementById("nombre").value,
        apellido: document.getElementById("apellido").value,
        nacimiento: document.getElementById("nacimiento").value,
        email: document.getElementById("email").value,
        contraseña: document.getElementById("contraseña").value
    };
    
    const res = await fetch(API_BASE + ENDPOINTS.create, {  
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });
    
    if (res.status === 409) {
        alert("❌ Este email ya esta registrado");
        return;
    }
    
    
    if (res.ok) {  
        alert("✅ Registro creado.");
        listarRegistros();
        mostrarSeccion('lista');
    } else {
        alert("❌ Error al crear registro");  
    }
});

async function buscarRegistro() {
    const id = document.getElementById("idBuscar").value;
    const res = await fetch(API_BASE + ENDPOINTS.read_one.replace("{id}", id));
    if (res.ok) {
        const data = await res.json();
        document.getElementById("nombreAccion").value = data.nombre;
        document.getElementById("apellidoAccion").value = data.apellido;
        document.getElementById("nacimientoAccion").value = data.nacimiento;
        document.getElementById("emailAccion").value = data.email;
        document.getElementById("contraseñaAccion").value = data.contraseña || "";
        mostrarSeccion('acciones');
        alert("Registro cargado para edición.");
    } else {
        alert("Registro no encontrado.");
    }
}

async function actualizarRegistro() {
    const id = document.getElementById("idBuscar").value;
    const body = {
        nombre: document.getElementById("nombreAccion").value,
        apellido: document.getElementById("apellidoAccion").value,
        nacimiento: document.getElementById("nacimientoAccion").value,
        email: document.getElementById("emailAccion").value,
        contraseña: document.getElementById("contraseñaAccion").value
    };
    const res = await fetch(API_BASE + ENDPOINTS.update.replace("{id}", id), {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });
    const result = await res.json();
    alert(result.mensaje || "Registro actualizado.");
    listarRegistros();
    mostrarSeccion('lista');
}

async function eliminarRegistro() {
    const id = document.getElementById("idBuscar").value;
    const res = await fetch(API_BASE + ENDPOINTS.delete.replace("{id}", id), { method: "DELETE" });
    const result = await res.json();
    alert(result.mensaje || "Registro eliminado.");
    listarRegistros();
    mostrarSeccion('lista');
}

function mostrarSeccion(id) {
    document.querySelectorAll(".seccion").forEach(s => s.style.display = "none");
    document.getElementById(id).style.display = "block";
}

listarRegistros();
mostrarSeccion('crear');
