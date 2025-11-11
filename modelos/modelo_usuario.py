import mysql.connector
from mysql.connector import Error

class ModeloUsuario:
    
    def __init__(self):
        self.usuario_actual_id = None
        self.db_config = {
            'host': 'localhost',  
            'database': 'mi_proyecto_db', 
            'user': 'root',     
            'password': 'MiP-MySQL25!'
        }

    def _conectar(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def obtener_id_estudiante_por_defecto(self):
        conn = self._conectar()
        if conn is None: return None
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM usuarios WHERE usuario = 'estudiante' LIMIT 1")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Error:
            return None
        finally:
            cursor.close()
            conn.close()

    def obtener_id_por_usuario(self, nombre_usuario):
        conn = self._conectar()
        if conn is None: return None
        cursor = conn.cursor()
        
        try:
            # Nuevo método para buscar el ID necesario para el reconocimiento facial
            cursor.execute("SELECT id FROM usuarios WHERE usuario = %s LIMIT 1", (nombre_usuario,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Error:
            return None
        finally:
            cursor.close()
            conn.close()

    def iniciar_sesion(self, nombre_usuario, contrasena):
        conn = self._conectar()
        if conn is None: return None
            
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, rol FROM usuarios WHERE usuario = %s AND contrasena = %s"
        
        try:
            cursor.execute(query, (nombre_usuario, contrasena))
            usuario = cursor.fetchone()
            
            if usuario:
                self.usuario_actual_id = usuario['id']
                return usuario['rol']
            return None
        except Error as e:
            print(f"Error al ejecutar inicio_sesion: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def obtener_info_usuario(self):
        if self.usuario_actual_id is None:
            return None
            
        conn = self._conectar()
        if conn is None:
            return None
            
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, usuario AS nombre, contrasena, rol FROM usuarios WHERE id = %s" 
        
        try:
            cursor.execute(query, (self.usuario_actual_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al ejecutar obtener_info_usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def actualizar_info_usuario(self, nuevo_nombre, nueva_contrasena):
        if self.usuario_actual_id is None:
            return "Error: Usuario no autenticado."
        
        if not nuevo_nombre or not nueva_contrasena:
            return "Error: Los campos no pueden estar vacíos."
        
        conn = self._conectar()
        if conn is None:
            return "Error al conectar con la base de datos."
            
        cursor = conn.cursor()
        query = "UPDATE usuarios SET usuario = %s, contrasena = %s WHERE id = %s"
        
        try:
            cursor.execute(query, (nuevo_nombre, nueva_contrasena, self.usuario_actual_id))
            conn.commit()
            return "Perfil actualizado con éxito."
        except Error as e:
            print(f"Error al ejecutar actualizar_info_usuario: {e}")
            return "Error al guardar cambios en la base de datos."
        finally:
            cursor.close()
            conn.close()

    def obtener_todos_usuarios(self):
        conn = self._conectar()
        if conn is None:
            return []
            
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, usuario AS nombre, contrasena, rol FROM usuarios" 
        
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al ejecutar obtener_todos_usuarios: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
