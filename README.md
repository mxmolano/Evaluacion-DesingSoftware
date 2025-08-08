# 🐍 Proyecto Patrones – Módulo de Gestión de Registros

## 👩‍💻 Autora
**Michelle Molano**  
Estudiante de Ingeniería de Software – Uniempresarial  
VIDEO: https://youtu.be/zYCZEoPorCU 

---

## 📌 Descripción del Proyecto
Este trabajo corresponde al avance individual del **proyecto final de la asignatura Diseño de Software**, en el que se diseñó e implementó un **nuevo módulo funcional** dentro del proyecto base **Lab-ProyectoPatrones**.  

El módulo fue desarrollado en **Python puro** (sin frameworks externos) siguiendo la arquitectura multicapa y aplicando los patrones de diseño:
- **DAO** (Data Access Object)  
- **DTO** (Data Transfer Object)  
- **Router** (Controlador de rutas y endpoints)  
- **Observer** (implementado opcionalmente para notificaciones de cambios)

---

## 🎯 Objetivo General
Diseñar e implementar un nuevo módulo funcional dentro del sistema base, manteniendo la arquitectura, buenas prácticas y estilo del código original, asegurando la modularidad y escalabilidad del proyecto.

---

## 🧱 Estructura del Módulo

El módulo fue integrado en la carpeta `/modulos/registro/` respetando la estructura del proyecto original:

````
/modulos/registro/
├── acceso_datos/
│ ├── registro_dao.py # Lógica de acceso a base de datos (CRUD)
│ ├── registro_dto.py # Objeto de transferencia de datos
│ └── get_factory.py # Fabrica para conexión según motor de BD
├── logica/
│ └── registro_service.py # Lógica de negocio y validaciones
├── router/
│ └── registro_router.py # Endpoints de la API REST
└── notificaciones/ # Implementación opcional de Observer
`````

---

## 🔌 Endpoints Implementados

| Método | Endpoint                 | Descripción |
|--------|--------------------------|-------------|
| POST   | `/registro/`              | Crea un nuevo registro |
| GET    | `/registro/`              | Lista todos los registros |
| GET    | `/registro/{id}`          | Obtiene un registro por ID |
| PUT    | `/registro/{id}`          | Actualiza un registro por ID |
| DELETE | `/registro/{id}`          | Elimina un registro por ID |

---

## ⚙️ Funcionamiento

### **DAO (Data Access Object)**
- Encapsula el acceso a la base de datos.
- Ejecuta sentencias SQL parametrizadas para CRUD.
- Gestiona excepciones y cierra conexiones.

### **DTO (Data Transfer Object)**
- Define un objeto plano para transportar datos entre capas.
- Garantiza independencia entre la estructura de BD y la lógica de negocio.

### **Router**
- Expone los endpoints definidos.
- Recibe las peticiones y delega la lógica al servicio correspondiente.
- Formatea las respuestas en JSON.

### **Observer (Opcional)**
- Implementado para registrar cambios relevantes en un archivo de log.
- Se dispara automáticamente en operaciones de creación y eliminación.

---

## 🧪 Pruebas Realizadas
Las pruebas se hicieron en tres interfaces:

1. **Consola** (`consola.py`) → CRUD por línea de comandos.
2. **Interfaz web** (`index.html`) → Consumo de API vía fetch.
3. **Interfaz escritorio** (`escritorio.py`) → CRUD con Tkinter.

Además:
- Archivo `.http` con pruebas desde VS Code.
- Verificación en dos motores de base de datos (MySQL y PostgreSQL).

---

## 📷 Evidencias
- Capturas de pantalla de CRUD funcionando en las tres interfaces.
- Captura del módulo en `/modulos/` con todos sus archivos.
- Imagen de la tarea completada y actualizada en **Azure DevOps**.

---

## 🎥 Video de Sustentación
En el video (duración: 6 min 48 seg) se explica:
1. Historia de usuario en Azure DevOps.
2. Recorrido por el código (`DTO`, `DAO`, `Service`, `Router`).
3. Pruebas de endpoints en Postman y archivo `.http`.
4. Demostración en interfaz web, consola y escritorio.
5. Cambio en vivo: se añadió validación de formato de email y se probó en ejecución.
6. Confirmación del commit y push a GitHub.
7. Actualización de la tarea en Azure DevOps.

---

## 📄 Documento PDF Entregado
Incluye:
- Historia de usuario implementada.
- Diagrama UML de clases.
- Explicación técnica del diseño.
- Evidencias de pruebas en todas las interfaces.

---

## 📚 Aprendizaje y Conclusiones
- Aprendí a integrar un módulo respetando completamente una arquitectura multicapa existente.
- Consolidé el uso de patrones de diseño para organizar el backend.
- Validé la importancia de aislar la lógica de negocio de la capa de acceso a datos.
- Comprobé que Python, incluso sin frameworks, permite estructurar aplicaciones limpias y escalables.
- El patrón **Observer** resultó útil para registrar eventos importantes sin acoplar el código principal.

---

## 📦 Repositorio
🔗 [Enlace al repositorio GitHub con el módulo integrado](https://github.com/usuario/repositorio)

---

## 📜 Licencia
Este proyecto es académico y fue desarrollado exclusivamente con fines educativos.
