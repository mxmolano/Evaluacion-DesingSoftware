import pymysql.cursors
import psycopg2
from modulos.registro.acceso_datos.conexion import ConexionDB
from modulos.registro.acceso_datos.registro_dto import RegistroDTO

class RegistroDAOMySQL:
    def __init__(self):
        self.conn = ConexionDB().obtener_conexion()

    def verificar_email_duplicado(self, email):
        try: 
            with self.conn.cursor() as c:
                sql = "SELECT COUNT(*) FROM registro WHERE email = %s"
                c.execute(sql, (email,))
                resultado = c.fetchone()
                return resultado [0]> 0
        except Exception as e:
            raise e

            
    def guardar(self, registro: RegistroDTO):
        if self.verificar_email_duplicado(registro.email):
            raise ValueError(f"El email {registro.email} ya esta registrado")
    
        try:
            with self.conn.cursor() as c:
                sql = "INSERT INTO registro (nombre, apellido, nacimiento, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
                c.execute(sql, (
                    registro.nombre,
                    registro.apellido,
                    registro.nacimiento,
                    registro.email,
                    registro.contraseña
                ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def obtener_todos(self):
        try:
            with self.conn.cursor() as c:
                c.execute("SELECT * FROM registro")
                rows = c.fetchall()
                return [RegistroDTO(*row) for row in rows]
        except Exception as e:
            raise e

    def obtener_por_id(self, id):
        try:
            with self.conn.cursor() as c:
                c.execute("SELECT * FROM registro WHERE id = %s", (id,))
                row = c.fetchone()
                return RegistroDTO(*row) if row else None
        except Exception as e:
            raise e

    def actualizar(self, id, registro: RegistroDTO):
        try:
            with self.conn.cursor() as c:
                sql_check = "SELECT COUNT(*) FROM registro WHERE email = %s AND id != %s"
                c.execute(sql_check, (registro.email, id))
                if c.fetchone()[0] > 0:
                    raise ValueError(f"El email '{registro.email}' ya está registrado por otro usuario")
                
                sql = "UPDATE registro SET nombre=%s, apellido=%s, nacimiento=%s, email=%s, contraseña=%s WHERE id=%s"
                c.execute(sql, (
                    registro.nombre,
                    registro.apellido,
                    registro.nacimiento,
                    registro.email,
                    registro.contraseña,
                    id
                ))
            self.conn.commit()
        except ValueError:
            raise
        except Exception as e:
            self.conn.rollback()
            raise e

    def eliminar(self, id):
        try:
            with self.conn.cursor() as c:
                c.execute("DELETE FROM registro WHERE id=%s", (id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


class RegistroDAOPostgres:
    def __init__(self):
        self.conn = ConexionDB().obtener_conexion(postgres=True)

    def verificar_email_duplicado(self, email):
        """Verifica si un email ya existe en la base de datos"""
        try:
            with self.conn.cursor() as c:
                sql = "SELECT COUNT(*) FROM registro WHERE email = %s"
                c.execute(sql, (email,)) 
                resultado = c.fetchone()
                return resultado[0] > 0
        except Exception as e:
            raise e

    def guardar(self, registro: RegistroDTO):
        if self.verificar_email_duplicado(registro.email):
            raise ValueError(f"El email '{registro.email}' ya está registrado")

        try:
            with self.conn.cursor() as c:
                sql = "INSERT INTO registro (nombre, apellido, nacimiento, email, contraseña) VALUES (%s, %s, %s, %s, %s)"
                c.execute(sql, (
                    registro.nombre,
                    registro.apellido,
                    registro.nacimiento,
                    registro.email,
                    registro.contraseña
                ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def obtener_todos(self):
        try:
            with self.conn.cursor() as c:
                c.execute("SELECT * FROM registro")
                rows = c.fetchall()
                return [RegistroDTO(*row) for row in rows]
        except Exception as e:
            raise e

    def obtener_por_id(self, id):
        try:
            with self.conn.cursor() as c:
                c.execute("SELECT * FROM registro WHERE id = %s", (id,))
                row = c.fetchone()
                return RegistroDTO(*row) if row else None
        except Exception as e:
            raise e

    def actualizar(self, id, registro: RegistroDTO):
        try:
            with self.conn.cursor() as c:
                # Verificar si el email ya existe en otro registro diferente
                sql_check = "SELECT COUNT(*) FROM registro WHERE email = %s AND id != %s"
                c.execute(sql_check, (registro.email, id))
                if c.fetchone()[0] > 0:
                    raise ValueError(f"El email '{registro.email}' ya está registrado por otro usuario")
                
                # Proceder con la actualización
                sql = "UPDATE registro SET nombre=%s, apellido=%s, nacimiento=%s, email=%s, contraseña=%s WHERE id=%s"
                c.execute(sql, (
                    registro.nombre,
                    registro.apellido,
                    registro.nacimiento,
                    registro.email,
                    registro.contraseña,
                    id
                ))
            self.conn.commit()
        except ValueError:
            # Re-lanzar ValueError para que sea capturado por la API como 409
            raise
        except Exception as e:
            self.conn.rollback()
            raise e

    def eliminar(self, id):
        try:
            with self.conn.cursor() as c:
                c.execute("DELETE FROM registro WHERE id=%s", (id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e