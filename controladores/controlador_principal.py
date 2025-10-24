from modelos.modelo_usuario import ModeloUsuario
from vistas.vista_login import VistaLogin
from vistas.vista_perfil_usuario import VistaPerfilUsuario
from vistas.vista_administrador import VistaAdministrador
from utilidades.vision_gestos import ReconocedorGestos
import tkinter as tk

class ControladorPrincipal:
    
    def __init__(self, raiz):
        self.raiz = raiz
        self.modelo = ModeloUsuario()
        self.raiz.title("Sistema MVC Tkinter")
        
        self.recognizer = ReconocedorGestos(0)
        
        self.vista = VistaLogin(raiz, self)
        self.vista.pack(fill="both", expand=True)

    def cambiar_vista(self, ClaseNuevaVista, **kwargs):
        if self.vista:
            self.vista.destroy()
            
        self.vista = ClaseNuevaVista(self.raiz, self, **kwargs)
        self.vista.pack(fill="both", expand=True)

    def manejar_login(self, nombre_usuario, contrasena):
        rol = self.modelo.iniciar_sesion(nombre_usuario, contrasena)
        if rol:
            return self._cargar_panel(rol)
        return "Credenciales incorrectas."

    def manejar_login_facial(self):
        rol = self.modelo.login_facial() 
        if rol:
            return self._cargar_panel(rol)
        return "Fallo en el reconocimiento facial."
        
    def manejar_login_gesto_estudiante(self):
        if not self.recognizer.iniciar_camara():
            return "Error: Cámara no disponible o no se pudo abrir."
            
        return "INICIADO"
        
    def procesar_gesto(self):
        resultado = self.recognizer.detectar_gesto_pulgar_arriba()
        
        if resultado == "PULGAR_ARRIBA":
            self.recognizer.detener_camara()
            self.modelo.usuario_actual_id = 1 
            return self._cargar_panel("estudiante")
            
        elif resultado in ["CÁMARA_NO_DISPONIBLE", "SALIENDO"]:
            self.recognizer.detener_camara()
            return "SALIENDO" 
            
        return "ESPERANDO"

    def _cargar_panel(self, rol):
        if rol == "administrador":
            self.cambiar_vista(VistaAdministrador)
        elif rol in ["estudiante", "profesor"]:
            self.cambiar_vista(VistaPerfilUsuario)
        return "exito"
    
    def manejar_cerrar_sesion(self):
        self.modelo.usuario_actual_id = None
        self.recognizer.detener_camara()
        self.cambiar_vista(VistaLogin)

    def obtener_info_usuario_actual(self):
        return self.modelo.obtener_info_usuario()

    def actualizar_perfil(self, nuevo_nombre, nueva_contrasena):
        return self.modelo.actualizar_info_usuario(nuevo_nombre, nueva_contrasena)

    def obtener_datos_todos_usuarios(self):
        return self.modelo.obtener_todos_usuarios()