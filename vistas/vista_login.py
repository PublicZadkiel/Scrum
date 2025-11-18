import tkinter as tk
from tkinter import messagebox

class VistaLogin(tk.Frame):
    
    def __init__(self, maestro, controlador):
        super().__init__(maestro)
        self.controlador = controlador
        self.estado_reconocimiento = None
        self.estado_reconocimiento_facial = None 
        
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

        self.btn_facial = tk.Button(self, 
                                    text="Login Facial (Reconocimiento)", 
                                    command=self.iniciar_reconocimiento_facial)
        self.btn_facial.pack(pady=10)
        
        self.lbl_estado_facial = None

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


    def iniciar_reconocimiento_facial(self):
        resultado_inicio = self.controlador.manejar_login_facial()
        
        if resultado_inicio != "INICIADO":
            messagebox.showerror("Error de Cámara", resultado_inicio)
            return
        
        self.btn_facial.config(state=tk.DISABLED, text="RECONOCIENDO ROSTRO...")
        
        if self.lbl_estado_facial:
            self.lbl_estado_facial.destroy()

        self.lbl_estado_facial = tk.Label(self, text="Mirando a la cámara... (Presiona 'Q' para salir)", fg="blue")
        self.lbl_estado_facial.pack(pady=5)
        
        self.estado_reconocimiento_facial = self.after(50, self.verificar_rostro)

    def verificar_rostro(self):
        resultado = self.controlador.procesar_reconocimiento_facial()
        
        if resultado == "exito":
            messagebox.showinfo("Éxito", "Inicio de sesión facial exitoso.")
            if self.lbl_estado_facial: self.lbl_estado_facial.destroy()
            if self.estado_reconocimiento_facial: self.after_cancel(self.estado_reconocimiento_facial)
            self.estado_reconocimiento_facial = None
            
        elif resultado == "USUARIO_NO_AUTORIZADO":
            messagebox.showerror("Error de Reconocimiento", "Rostro reconocido, pero el usuario no está registrado en la base de datos.")
            if self.lbl_estado_facial: self.lbl_estado_facial.destroy()
            self.btn_facial.config(state=tk.NORMAL, text="Login Facial (Reconocimiento)")
            if self.estado_reconocimiento_facial: self.after_cancel(self.estado_reconocimiento_facial)
            self.estado_reconocimiento_facial = None
            
        elif resultado == "SALIENDO":
            messagebox.showinfo("Cámara", "Ventana de cámara cerrada.")
            if self.lbl_estado_facial: self.lbl_estado_facial.destroy()
            self.btn_facial.config(state=tk.NORMAL, text="Login Facial (Reconocimiento)")
            if self.estado_reconocimiento_facial: self.after_cancel(self.estado_reconocimiento_facial)
            self.estado_reconocimiento_facial = None
            
        elif resultado == "ESPERANDO":
            self.estado_reconocimiento_facial = self.after(50, self.verificar_rostro)
            
        elif resultado and resultado != "ESPERANDO":
            messagebox.showerror("Error de Reconocimiento", "Rostro detectado, pero no coincide con los usuarios registrados.")
            if self.lbl_estado_facial: self.lbl_estado_facial.destroy()
            self.btn_facial.config(state=tk.NORMAL, text="Login Facial (Reconocimiento)")
            if self.estado_reconocimiento_facial: self.after_cancel(self.estado_reconocimiento_facial)
            self.estado_reconocimiento_facial = None