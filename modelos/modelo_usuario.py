from typing import Dict, Any

class ModeloUsuario:
    
    def __init__(self):
        self.usuarios: Dict[int, Dict[str, Any]] = {
            1: {"nombre": "Bautista León", "contrasena": "elpepeetesech", "rol": "estudiante"},
            2: {"nombre": "Carlos Carden", "contrasena": "Cardensito", "rol": "profesor"},
            3: {"nombre": "Admin Principal", "contrasena": "admin", "rol": "administrador"}
        }
        self.usuario_actual_id = None

    def iniciar_sesion(self, nombre_usuario, contrasena):
        for user_id, user_data in self.usuarios.items():
            if user_data["nombre"] == nombre_usuario and user_data["contrasena"] == contrasena:
                self.usuario_actual_id = user_id
                return user_data["rol"]
        return None

    def login_facial(self):
        print("Simulación de reconocimiento facial exitosa.")
        self.usuario_actual_id = 1 
        return "estudiante"

    def obtener_info_usuario(self):
        if self.usuario_actual_id in self.usuarios:
            info = self.usuarios[self.usuario_actual_id].copy()
            info['id'] = self.usuario_actual_id
            return info
        return None

    def actualizar_info_usuario(self, nuevo_nombre, nueva_contrasena):
        if self.usuario_actual_id in self.usuarios:
            self.usuarios[self.usuario_actual_id]["nombre"] = nuevo_nombre
            self.usuarios[self.usuario_actual_id]["contrasena"] = nueva_contrasena
            return True
        return False

    def obtener_todos_usuarios(self):
        todos_datos = []
        for uid, data in self.usuarios.items():
            if data["rol"] in ["estudiante", "profesor"]:
                todos_datos.append(f"ID: {uid} | Nombre: {data['nombre']} | Rol: {data['rol'].capitalize()}")
        return todos_datos