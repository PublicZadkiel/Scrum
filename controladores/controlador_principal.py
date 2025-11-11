from modelos.modelo_usuario import ModeloUsuario
from vistas.vista_login import VistaLogin
from vistas.vista_perfil_usuario import VistaPerfilUsuario
from vistas.vista_administrador import VistaAdministrador
from utilidades.vision_gestos import ReconocedorGestos
from utilidades.reconocimiento_facial import ReconocedorFacial
import tkinter as tk

class ControladorPrincipal:
    
    def __init__(self, raiz):
        self.raiz = raiz
        self.modelo = ModeloUsuario()
        self.raiz.title("Sistema MVC Tkinter")
        
        self.recognizer_gestos = ReconocedorGestos('http://192.168.0.7:4747/video') 
        self.recognizer_facial = ReconocedorFacial()
        
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
        
    def manejar_login_gesto_estudiante(self):
        if not self.recognizer_gestos.iniciar_camara():
            return "Error: Cámara no disponible o no se pudo abrir."
            
        return "INICIADO"
        
    def procesar_gesto(self):
        resultado = self.recognizer_gestos.detectar_gesto_pulgar_arriba()
        
        if resultado == "PULGAR_ARRIBA":
            self.recognizer_gestos.detener_camara()
            self.modelo.usuario_actual_id = self.modelo.obtener_id_estudiante_por_defecto()
            return self._cargar_panel("estudiante")
            
        elif resultado in ["CÁMARA_NO_DISPONIBLE", "SALIENDO"]:
            self.recognizer_gestos.detener_camara()
            return "SALIENDO" 
            
        return "ESPERANDO"

    def manejar_login_facial(self):
        if not self.recognizer_facial.iniciar_camara():
            return "Error: Cámara no disponible o no se pudo abrir."
        return "INICIADO"
        
    def procesar_reconocimiento_facial(self):
        rol_o_estado = self.recognizer_facial.reconocer_rostro()

        if rol_o_estado and rol_o_estado not in ["SALIENDO", "ESPERANDO_GESTO"]:
            self.recognizer_facial.detener_camara()
            
            
            usuario_id = self.modelo.obtener_id_por_usuario(rol_o_usuario)
            
            if usuario_id:
                self.modelo.usuario_actual_id = usuario_id
                return self._cargar_panel(rol_o_usuario) 
            else:
                return "USUARIO_NO_AUTORIZADO" 
            
        elif rol_o_estado == "SALIENDO":
            self.recognizer_facial.detener_camara()
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
        self.cambiar_vista(VistaLogin)

    def obtener_info_usuario_actual(self):
        return self.modelo.obtener_info_usuario()

    def actualizar_perfil(self, nuevo_nombre, nueva_contrasena):
        return self.modelo.actualizar_info_usuario(nuevo_nombre, nueva_contrasena)

    def obtener_datos_todos_usuarios(self):
        return self.modelo.obtener_todos_usuarios()