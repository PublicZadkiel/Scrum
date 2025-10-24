import tkinter as tk
from tkinter import messagebox

class VistaLogin(tk.Frame):
    
    def __init__(self, maestro, controlador):
        super().__init__(maestro)
        self.controlador = controlador
        self.estado_reconocimiento = None
        
        tk.Label(self, text="INICIO DE SESIÓN", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="Usuario (o Nombre):").pack(pady=5)
        self.entrada_usuario = tk.Entry(self)
        self.entrada_usuario.pack(pady=5)
        
        tk.Label(self, text="Contraseña:").pack(pady=5)
        self.entrada_contrasena = tk.Entry(self, show="*")
        self.entrada_contrasena.pack(pady=5)

        tk.Button(self, text="Login con Contraseña", command=self.login_contrasena).pack(pady=10)
        
        self.btn_gesto = tk.Button(self, 
                                   text="Login con Gesto (Pulgar Arriba)", 
                                   command=self.iniciar_login_gesto)
        self.btn_gesto.pack(pady=10)

    def login_contrasena(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()
        
        resultado = self.controlador.manejar_login(usuario, contrasena)
        
        if resultado != "exito":
            messagebox.showerror("Error de Login", resultado)

    def iniciar_login_gesto(self):
        resultado_inicio = self.controlador.manejar_login_gesto_estudiante()
        
        if resultado_inicio != "INICIADO":
            messagebox.showerror("Error de Cámara", resultado_inicio)
            return

        self.btn_gesto.config(state=tk.DISABLED, text="ESPERANDO GESTO...")
        self.estado_reconocimiento = self.after(10, self.verificar_gesto)

    def verificar_gesto(self):
        resultado = self.controlador.procesar_gesto()
        
        if resultado == "exito":
            self.after_cancel(self.estado_reconocimiento)
            self.estado_reconocimiento = None
            
        elif resultado == "SALIENDO":
            messagebox.showinfo("Cámara", "Ventana de cámara cerrada.")
            self.btn_gesto.config(state=tk.NORMAL, text="Login con Gesto (Pulgar Arriba)")
            self.after_cancel(self.estado_reconocimiento)
            self.estado_reconocimiento = None
            
        elif resultado == "ESPERANDO":
            self.estado_reconocimiento = self.after(10, self.verificar_gesto)