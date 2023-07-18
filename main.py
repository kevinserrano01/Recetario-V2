import tkinter as tk
import interfaz
import DB
import config

def main():
    # crear la base de datos y tabla si no existe.
    DB.create_if_not_exists()
    
    # Inicializacion de interfaz.
    root = tk.Tk()
    root.iconbitmap(default=config.icono)
    root.title("RECETARIO with MySQL")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    interfaz.Principal(root).grid(sticky=tk.NSEW)
    root.mainloop()

if __name__ == "__main__":
    main()