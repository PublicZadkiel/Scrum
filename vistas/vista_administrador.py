import tkinter as tk
from tkinter import ttk

class VistaAdministrador(tk.Frame):
    
    def __init__(self, maestro, controlador):
        super().__init__(maestro)
        self.controlador = controlador
        
        tk.Label(self, text="PANEL DE ADMINISTRADOR", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self, text="Lista de Estudiantes y Profesores:").pack(pady=10)

        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=10, padx=20, fill="x")

        self.caja_lista_usuarios = tk.Listbox(frame_lista, height=10, width=50)
        self.caja_lista_usuarios.pack(side="left", fill="both", expand=True)

        barra_desplazamiento = tk.Scrollbar(frame_lista, orient="vertical", command=self.caja_lista_usuarios.yview)
        barra_desplazamiento.pack(side="right", fill="y")
        self.caja_lista_usuarios.config(yscrollcommand=barra_desplazamiento.set)
        
        self.cargar_usuarios()
        
        tk.Button(self, text="Cerrar Sesión", command=self.controlador.manejar_cerrar_sesion).pack(pady=20)

    def cargar_usuarios(self):
        datos_usuarios = self.controlador.obtener_datos_todos_usuarios()
        
        self.caja_lista_usuarios.delete(0, tk.END) 
        
        if datos_usuarios:
            for linea in datos_usuarios:
                self.caja_lista_usuarios.insert(tk.END, linea)
        else:
            self.caja_lista_usuarios.insert(tk.END, "No hay usuarios o profesores registrados.")