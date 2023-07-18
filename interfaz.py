import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno
import DB

class Principal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.ventana = parent
        self.salir = lambda: parent.destroy()

        self.columnconfigure(0, weight=1)   # descripcion
        self.columnconfigure(1, weight=1)   # check
        self.columnconfigure(2, weight=1)   # check
        self.columnconfigure(3, weight=0)   # scrollbar

        # self.columnconfigure(3, weight=0)   # scrollbar
        self.rowconfigure(0, weight=1)  # titulo
        self.rowconfigure(1, weight=1)  # tipos
        self.rowconfigure(2, weight=1)  # tareas
        self.rowconfigure(3, weight=1)  # acciones
        self.rowconfigure(4, weight=1)  # salir

        ttk.Label(self, text="Recetario App").grid(row=0, column=0, columnspan=4)
        self.set_botonera1()
        self.set_botonera2()
        self.set_tabla()
        self.cargar_tabla()
        btn_salir = ttk.Button(self, text="Salir", command=self.salir)
        btn_salir.grid(row=4, column=1, columnspan=2, sticky=tk.E)


    def cargar_tabla(self):
        """Cargar la tabla con las recetas."""
        self.vaciar_tabla()
        registros = DB.getNombresIDRecetas()
        # print(registros)
        for id_receta, nombre, tiempo_preparacion in registros:
            self.tabla.insert('', tk.END, values=(id_receta, nombre, tiempo_preparacion))
        # ¡Aca escondemos la primera columna 'ID' con los ids de cada receta.
        self.tabla["displaycolumns"] = ('receta', 'tiempo_preparacion')

    def cargar_recetas_fav(self, bool):
        """Cargar la tabla con las recetas solo que son Favoritas."""
        self.vaciar_tabla()
        registros = DB.getRecetasFav(bool)
        # print(registros)
        for id_receta, nombre, tiempo_preparacion in registros:
            self.tabla.insert('', tk.END, values=(id_receta, nombre, tiempo_preparacion))
        # ¡Aca escondemos la primera columna 'ID' con los ids de cada receta.
        self.tabla["displaycolumns"] = ('receta', 'tiempo_preparacion')

    def vaciar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    def set_tabla(self):
        """Crear la tabla con tres columnas, id, receta y completada.
        
        La columna ID se va a ocultar para que el usuario no la vea,
        ya que no le interesa cual es el id de cada tarea.
        De todas formas podemos obeneter el id de cada tarea despues.
        """
        columnas = ('id', 'receta', 'tiempo_preparacion')
        self.tabla = ttk.Treeview(self, columns=columnas,show='headings', selectmode="browse") # sin multi-seleccion
        self.tabla.grid(row=2, column=0, columnspan=3, sticky=(tk.NSEW))
        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll.grid(row=2, column=3, sticky=tk.NS)
        self.tabla.configure(yscroll=scroll.set)
        self.tabla.heading('id', text='ID')
        self.tabla.heading('receta', text='receta')
        self.tabla.heading('tiempo_preparacion', text='tiempo_preparacion')

    def set_botonera1(self):
        """crear la botonera para mostrar tareas en la tabla"""
        botonera1 = ttk.Frame(self)
        botonera1.grid(row=1, column=0, columnspan=4)
        botonera1.columnconfigure(0, weight=1)
        botonera1.columnconfigure(1, weight=1)
        botonera1.columnconfigure(2, weight=1)
        btn_pendientes = ttk.Button(botonera1, text="Mostrar Favortas", command=lambda:self.cargar_recetas_fav(1))
        btn_pendientes.grid(row=0, column=0, padx=3, pady=3)
        btn_completadas = ttk.Button(botonera1, text="Mostrar No favoritas", command=lambda:self.cargar_recetas_fav(0))
        btn_completadas.grid(row=0, column=1, padx=3, pady=3)
        btn_todo = ttk.Button(botonera1, text="Mostrar todo", command=lambda:self.cargar_tabla())
        btn_todo.grid(row=0, column=2, padx=3, pady=3)
    
    def set_botonera2(self):
        """crear botonera de abm de tareas"""
        botonera2 = ttk.Frame(self)
        botonera2.grid(row=3, column=0, columnspan=4)
        botonera2.columnconfigure(0, weight=1)
        botonera2.columnconfigure(1, weight=1)
        botonera2.columnconfigure(2, weight=1)
        
        btn_editar = ttk.Button(botonera2, text="Editar", command=self.modificar)
        btn_editar.grid(row=0, column=1, padx=3, pady=3)

        btn_eliminar = ttk.Button(botonera2, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=3, pady=3)
        
        btn_nueva = ttk.Button(botonera2, text="Nueva", command=self.agregar)
        btn_nueva.grid(row=0, column=3, padx=3, pady=3)

    def agregar(self):
        """Abrir ventana para crear nueva receta."""
        ventana_tarea = tk.Toplevel(self.ventana)
        Receta(ventana_tarea, self.cargar_tabla).grid(row=0, column=0, sticky=tk.NSEW)

    def modificar(self):
        """Abrir ventana para modificar una tarea."""
    #     seleccion = self.tabla.selection()
    #     if seleccion:
    #         item = self.tabla.item(seleccion[0])
    #         id_tarea = item['values'][0] # id de la tarea obtenida del treeview
    #         tarea = item['values'][1]
    #         ventana_tarea = tk.Toplevel(self.ventana)
    #         frame = Tarea(ventana_tarea, self.cargar_tabla,
    #                       id_tarea=id_tarea, texto_tarea=tarea)
    #         frame.grid(row=0, column=0, sticky=tk.NSEW)
    #     else:
    #         messagebox.showinfo(message="Debe seleccionar una tarea primero")
        pass

    def completar(self):
    #     seleccion = self.tabla.selection()
    #     if seleccion:
    #         item = self.tabla.item(seleccion[0])
    #         id_tarea = item['values'][0] # id de la tarea obtenida del treeview
    #         completada = item['values'][2]
    #         if completada == "Si":
    #             messagebox.showinfo(message="La tarea ya estaba completada   ¬¬")
    #             return
    #         DB.completar_tarea(id_tarea)
    #         messagebox.showinfo(message="Tarea completada :)")
    #         self.cargar_tabla()
    #     else:
    #         messagebox.showinfo(message="Debe seleccionar una tarea primero")
        pass

    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            id_receta = item['values'][0] # id de la receta obtenida del treeview
            receta = item['values'][1]
            mensaje = f"Esta a punto de eliminar la tarea: {receta}.\n¿Desea continuar?"
            if askyesno(title="Eliminar tarea", message=mensaje):
                DB.eliminar_receta(id_receta)
                messagebox.showinfo(message="Receta eliminada.")
                self.cargar_tabla()
        else:
            messagebox.showinfo(message="Debe seleccionar una receta primero")


class Receta(ttk.Frame):
    """
    Frame para la ventana que muestra una tarea para modificacion
    o el formulario para crear una nueva.
    """
    def __init__(self, parent, actualizar_tareas, id_tarea=None, texto_tarea=None):
        super().__init__(parent, padding=10)
        parent.focus()
        parent.grab_set()
        self.cerrar_ventana = lambda:parent.destroy()
        self.actualizar_tareas = actualizar_tareas
        self.id_tarea = id_tarea

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        # label
        ttk.Label(self, text="Nombre").grid(row=0, column=0)
        ttk.Label(self, text="ingredientes").grid(row=1, column=0)
        ttk.Label(self, text="pasos").grid(row=2, column=0)
        ttk.Label(self, text="tiempo preparacion (min)").grid(row=3, column=0)
        ttk.Label(self, text="coccion (min)").grid(row=4, column=0)
        ttk.Label(self, text="etiquetas").grid(row=5, column=0)
        ttk.Label(self, text="favorito (Si: 1 | No: 0)").grid(row=6, column=0)

        # entry + var
        self.nombre = tk.StringVar()
        self.ingredientes = tk.StringVar()
        self.pasos = tk.StringVar()
        self.preparacion = tk.StringVar()
        self.coccion = tk.StringVar()
        self.etiquetas = tk.StringVar()
        self.fav = tk.StringVar()

        # Entrys
        entryNombre = ttk.Entry(self, textvariable=self.nombre, width=60)
        entryNombre.grid(row=0, column=1, padx=3, pady=3)
        entryNombre.focus_set()

        entryIngre = ttk.Entry(self, textvariable=self.ingredientes, width=60)
        entryIngre.grid(row=1, column=1, padx=3, pady=3)
        entryIngre.focus_set()

        entryPasos = ttk.Entry(self, textvariable=self.pasos, width=60)
        entryPasos.grid(row=2, column=1, padx=3, pady=3)
        entryPasos.focus_set()

        entryPreparacion = ttk.Entry(self, textvariable=self.preparacion, width=60)
        entryPreparacion.grid(row=3, column=1, padx=3, pady=3)
        entryPreparacion.focus_set()

        entryCoccion = ttk.Entry(self, textvariable=self.coccion, width=60)
        entryCoccion.grid(row=4, column=1, padx=3, pady=3)
        entryCoccion.focus_set()

        entryEtiquetas = ttk.Entry(self, textvariable=self.etiquetas, width=60)
        entryEtiquetas.grid(row=5, column=1, padx=3, pady=3)
        entryEtiquetas.focus_set()

        entryFav = ttk.Entry(self, textvariable=self.fav, width=60)
        entryFav.grid(row=6, column=1, padx=3, pady=3)
        entryFav.focus_set()


        # botonera
        botonera = ttk.Frame(self)
        botonera.grid(row=7, column=0, columnspan=2, sticky=tk.E)
        # boton cancelar
        btn_cancelar = ttk.Button(botonera, text="Cancelar", command=self.cerrar_ventana)
        btn_cancelar.grid(row=0, column=0, padx=3, pady=3, sticky=tk.E)
        # boton agregar
        btn_guardar = ttk.Button(botonera, text="Agregar", command=self.guardar)
        btn_guardar.grid(row=0, column=1, padx=3, pady=3, sticky=tk.E)

        # if id_tarea is not None:
        #     # modificar la tarea
        #     self.tarea_text.set(texto_tarea)
        #     btn_guardar.configure(text="Modificar")
        
        parent.bind('<Return>', lambda e: btn_guardar.invoke())

    def guardar(self):
        recetaNueva = {'nombre': self.nombre.get(),
                            'ingredientes': self.ingredientes.get(),
                            'preparacion': self.pasos.get(),
                            'tiempo_preparacion': int(self.preparacion.get()),
                            'tiempo_coccion': int(self.coccion.get()),
                            'etiquetas': self.etiquetas.get(),
                            'fav': self.fav.get()
                            }

        if self.id_tarea is not None:
            DB.actualizar_tarea(self.id_tarea, recetaNueva)
        else:
            DB.nueva_receta(recetaNueva)
        # actualizar tabla
        self.actualizar_tareas()
        # cerrar ventana
        self.cerrar_ventana()