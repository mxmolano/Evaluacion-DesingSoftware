import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# Cargar configuración desde config.json
CONFIG_PATH = "modulos/registro/configuracion/config.json"

if not os.path.exists(CONFIG_PATH):
    messagebox.showerror("Error", f"No se encontró el archivo de configuración en:\n{CONFIG_PATH}")
    exit()

try:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)
except json.JSONDecodeError:
    messagebox.showerror("Error", "El archivo config.json no es un JSON válido.")
    exit()

API = config.get("api_base", "").rstrip("/")
ENDPOINTS = config.get("endpoints", {})

SUCCESS_CODES = (200, 201, 204)

def build_url(endpoint):
    if not API or not endpoint:
        return None
    return API.rstrip("/") + "/" + endpoint.lstrip("/")

def show_response_error(r):
    """Muestra información útil cuando la petición falla."""
    try:
        req_info = f"URL: {r.request.url}\nMétodo: {r.request.method}\nStatus: {r.status_code}"
    except Exception:
        req_info = f"Status: {getattr(r, 'status_code', 'N/A')}"
    try:
        body = r.text
    except Exception:
        body = "<no body>"
    messagebox.showerror("Error en petición", f"{req_info}\n\nRespuesta:\n{body}")

def recargar_datos():
    for item in tree.get_children():
        tree.delete(item)
    try:
        url = build_url(ENDPOINTS.get("read_all", ""))
        if not url:
            messagebox.showerror("Error", "Endpoint 'read_all' no configurado.")
            return
        r = requests.get(url)
        if r.status_code in SUCCESS_CODES:
            # Si no hay contenido (204) no intentamos parsear JSON
            if r.status_code == 204:
                return
            try:
                data = r.json()
            except ValueError:
                messagebox.showerror("Error", "La respuesta del servidor no es JSON válido.")
                return
            for p in data:
                # Soportar distintas claves para contraseña
                pwd = p.get("contraseña") or p.get("contraseña") or p.get("password") or ""
                tree.insert("", "end", values=(
                    p.get("id", ""),
                    p.get("nombre", ""),
                    p.get("apellido", ""),
                    p.get("nacimiento", ""),
                    p.get("email", ""),
                    pwd
                ))
        else:
            show_response_error(r)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def crear_registro():
    dialogo_registro("Crear nuevo registro")

def editar_registro():
    seleccionado = tree.focus()
    if not seleccionado:
        messagebox.showwarning("Seleccionar", "Seleccione un registro.")
        return
    valores = tree.item(seleccionado, "values")
    dialogo_registro("Editar registro", valores)

def eliminar_registro():
    seleccionado = tree.focus()
    if not seleccionado:
        messagebox.showwarning("Seleccionar", "Seleccione un registro.")
        return
    id_prod = tree.item(seleccionado, "values")[0]
    if messagebox.askyesno("Eliminar", "¿Seguro que desea eliminar este registro?"):
        try:
            url = build_url(ENDPOINTS.get("delete", "").replace("{id}", str(id_prod)))
            if not url:
                messagebox.showerror("Error", "Endpoint 'delete' no configurado.")
                return
            r = requests.delete(url)
            if r.status_code in SUCCESS_CODES:
                recargar_datos()
                messagebox.showinfo("Éxito", "Registro eliminado.")
            else:
                show_response_error(r)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

def dialogo_registro(titulo, datos=None):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
    nombre = tk.Entry(ventana)
    nombre.grid(row=0, column=1)

    tk.Label(ventana, text="Apellido:").grid(row=1, column=0)
    apellido = tk.Entry(ventana)
    apellido.grid(row=1, column=1)

    tk.Label(ventana, text="Nacimiento:").grid(row=2, column=0)
    nacimiento = tk.Entry(ventana)
    nacimiento.grid(row=2, column=1)

    tk.Label(ventana, text="Email:").grid(row=3, column=0)
    email = tk.Entry(ventana)
    email.grid(row=3, column=1)

    tk.Label(ventana, text="Contraseña:").grid(row=4, column=0)
    contraseña = tk.Entry(ventana, show="*")
    contraseña.grid(row=4, column=1)

    id_prod = None
    if datos:
        # datos viene como tupla/tuple de valores del treeview
        id_prod, nombre_val, apellido_val, nacimiento_val, email_val, contraseña_val = datos
        nombre.insert(0, nombre_val)
        apellido.insert(0, apellido_val)
        nacimiento.insert(0, nacimiento_val)
        email.insert(0, email_val)
        contraseña.insert(0, contraseña_val)

    def guardar():
        payload = {
            "nombre": nombre.get(),
            "apellido": apellido.get(),
            "nacimiento": nacimiento.get(),
            "email": email.get(),
            "contraseña": contraseña.get()
        }
        try:
            if datos:
                url = build_url(ENDPOINTS.get("update", "").replace("{id}", str(id_prod)))
                if not url:
                    messagebox.showerror("Error", "Endpoint 'update' no configurado.")
                    return
                r = requests.put(url, json=payload)
            else:
                url = build_url(ENDPOINTS.get("create", ""))
                if not url:
                    messagebox.showerror("Error", "Endpoint 'create' no configurado.")
                    return
                r = requests.post(url, json=payload)

            if r.status_code in SUCCESS_CODES:
                recargar_datos()
                ventana.destroy()
                messagebox.showinfo("Éxito", "Operación exitosa.")
            # ---
            
            elif r.status_code == 409:
                messagebox.showerror("Email duplicado", "Este email ya está registrado")
            else:
                show_response_error(r)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=5, columnspan=2, pady=6)

# Ventana principal
root = tk.Tk()
root.title("Gestión de registro")

# Tabla
cols = ("ID", "Nombre", "Apellido", "Nacimiento", "Email", "Contraseña")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Botones
botonera = tk.Frame(root)
botonera.pack(pady=10)

tk.Button(botonera, text="Nuevo", command=crear_registro).pack(side="left", padx=5)
tk.Button(botonera, text="Editar", command=editar_registro).pack(side="left", padx=5)
tk.Button(botonera, text="Eliminar", command=eliminar_registro).pack(side="left", padx=5)
tk.Button(botonera, text="Recargar", command=recargar_datos).pack(side="left", padx=5)

recargar_datos()
root.mainloop()

