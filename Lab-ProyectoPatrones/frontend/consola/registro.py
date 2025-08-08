import requests
import json

# === Cargar configuración ===
try:
    with open("modulos/registro/configuracion/config.json", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ No se encontró el archivo config.json en la ruta especificada.")
    exit()
except json.JSONDecodeError:
    print("❌ Error al leer config.json. Verifique que el formato sea válido.")
    exit()

API = config.get("api_base", "").rstrip("/")
ENDPOINTS = config.get("endpoints", {})

# === Funciones de utilidad ===
def imprimir_registro(p):
    """
    Imprime un registro en formato legible.
    """
    print(" ")
    print("-" * 30)
    print(f"ID: {p.get('id')}")
    print(f"Nombre: {p.get('nombre')}")
    print(f"Apellido: {p.get('apellido')}")
    print(f"Nacimiento: {p.get('nacimiento')}")
    print(f"Email: {p.get('email')}")
    print(f"Contraseña: {p.get('contraseña')}")
    print("-" * 30)

def mostrar_error(r):
    """Muestra error HTTP de forma clara."""
    print(f"❌ Error {r.status_code}: {r.text}")

# === Operaciones CRUD ===
def ingresar():
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
    email = input("Email: ").strip()
    contraseña = input("Contraseña: ").strip()

    try:
        r = requests.post(
            f"{API}/{ENDPOINTS['create']}",
            json={
                "nombre": nombre,
                "apellido": apellido,
                "nacimiento": nacimiento,
                "email": email,
                "contraseña": contraseña
            }
        )
        if r.status_code in (200, 201):
            print("✅ Registro creado con éxito.")
            imprimir_registro(r.json())
        elif r.status_code in (409):
            print(" ❌ Este email ya esta registrado")
        else:
            mostrar_error(r)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def listar():
    try:
        r = requests.get(f"{API}/{ENDPOINTS['read_all']}")
        if r.status_code == 200:
            data = r.json()
            if not data:
                print("📭 No hay registros.")
                return
            for p in data:
                imprimir_registro(p)
        else:
            mostrar_error(r)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def obtener():
    id_reg = input("ID del registro: ").strip()
    url = ENDPOINTS["read_one"].replace("{id}", id_reg)
    try:
        r = requests.get(f"{API}/{url}")
        if r.status_code == 200:
            imprimir_registro(r.json())
        else:
            print("⚠️ Registro no encontrado.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def actualizar():
    id_reg = input("ID a actualizar: ").strip()
    nombre = input("Nuevo nombre: ").strip()
    apellido = input("Nuevo apellido: ").strip()
    nacimiento = input("Nueva fecha de nacimiento (YYYY-MM-DD): ").strip()
    email = input("Nuevo email: ").strip()
    contraseña = input("Nueva contraseña: ").strip()

    url = ENDPOINTS["update"].replace("{id}", id_reg)
    try:
        r = requests.put(
            f"{API}/{url}",
            json={
                "nombre": nombre,
                "apellido": apellido,
                "nacimiento": nacimiento,
                "email": email,
                "contraseña": contraseña
            }
        )
        if r.status_code in (200, 201):
            print("✅ Registro actualizado con éxito.")
            imprimir_registro(r.json())
        else:
            mostrar_error(r)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def eliminar():
    id_reg = input("ID a eliminar: ").strip()
    url = ENDPOINTS["delete"].replace("{id}", id_reg)
    try:
        r = requests.delete(f"{API}/{url}")
        if r.status_code == 200:
            print("🗑️ Registro eliminado con éxito.")
        else:
            mostrar_error(r)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

# === Menú principal ===
def menu():
    print("\n===== Menú Registro =====")
    print("1. Ingresar nuevo registro")
    print("2. Listar registros")
    print("3. Obtener registro por ID")
    print("4. Actualizar registro")
    print("5. Eliminar registro")
    print("6. Salir")

if __name__ == "__main__":
    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            ingresar()
        elif opcion == "2":
            listar()
        elif opcion == "3":
            obtener()
        elif opcion == "4":
            actualizar()
        elif opcion == "5":
            eliminar()
        elif opcion == "6":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción inválida.")
