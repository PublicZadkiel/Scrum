import tkinter as tk

from controladores.controlador_principal import ControladorPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x450") 
    
    app = ControladorPrincipal(root) 
    
    root.mainloop()
    
    print("El programa ha finalizado.")