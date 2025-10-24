import tkinter as tk
from tkinter import messagebox

class VistaPerfilUsuario(tk.Frame):
    
    def __init__(self, maestro, controlador):
        super().__init__(maestro)
        self.controlador = controlador
        self.datos_usuario = self.controlador.obtener_info_usuario_actual()
        
        if not self.datos_usuario:
            messagebox.showerror("Error", "No se encontró información del usuario.")
            self.controlador.manejar_cerrar_sesion()
            return
            
        tk.Label(self, text=f"PERFIL DE USUARIO | Rol: {self.datos_usuario['rol'].capitalize()}", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self, text=f"ID: {self.datos_usuario['id']}").pack(pady=5)

        tk.Label(self, text="Nombre:").pack(pady=5)
        self.var_nombre = tk.StringVar(value=self.datos_usuario['nombre'])
        self.entrada_nombre = tk.Entry(self, textvariable=self.var_nombre)
        self.entrada_nombre.pack(pady=5)

        tk.Label(self, text="Nueva Contraseña:").pack(pady=5)
        self.var_contrasena = tk.StringVar(value=self.datos_usuario['contrasena'])
        self.entrada_contrasena = tk.Entry(self, textvariable=self.var_contrasena, show="*")
        self.entrada_contrasena.pack(pady=5)

        tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios).pack(pady=10)
        tk.Button(self, text="Cerrar Sesión", command=self.controlador.manejar_cerrar_sesion).pack(pady=10)

    def guardar_cambios(self):
        nuevo_nombre = self.var_nombre.get()
        nueva_contrasena = self.var_contrasena.get()
        
        if self.controlador.actualizar_perfil(nuevo_nombre, nueva_contrasena):
            messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")
        else:
            messagebox.showerror("Error", "Fallo al actualizar el perfil.")