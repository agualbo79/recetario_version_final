from PIL import Image, ImageTk
import tkinter as tk
import csv
from tkinter import filedialog
import random


class Receta:
    def __init__(self, nombre, ingredientes, preparacion, tiempo_preparacion, tiempo_coccion,fecha_creacion, imagen=None):
        """
        Crea un objeto Receta con los siguientes atributos:
        
        Args:
        - nombre (str): el nombre de la receta.
        - ingredientes (str): los ingredientes necesarios para hacer la receta.
        - preparacion (str): los pasos necesarios para preparar la receta.
        - tiempo_preparacion (int): el tiempo requerido para preparar la receta, en minutos.
        - tiempo_coccion (int): el tiempo requerido para cocinar la receta, en minutos.
        - fecha_creacion (str): la fecha en que se creó la receta, en formato "DD/MM/AAAA".
        - imagen (str, opcional): una URL a una imagen de la receta.
        """
        
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.preparacion = preparacion
        self.tiempo_preparacion = tiempo_preparacion
        self.tiempo_coccion = tiempo_coccion # Se agrega tiempo de cocción
        self.imagen = imagen
        self.fecha_creacion = fecha_creacion
    def __str__(self):
        """
        Devuelve el nombre de la receta como una cadena de caracteres.
        """
        return self.nombre

class Ingrediente:
    def __init__(self, nombre, unidad_medida, cantidad):
        """
        Crea un objeto Ingrediente con los siguientes atributos:
        
        Args:
        - nombre (str): el nombre del ingrediente.
        - unidad_medida (str): la unidad de medida en que se mide el ingrediente, como "gramos", "tazas", "cucharadas", etc.
        - cantidad (float): la cantidad del ingrediente necesaria para la receta.
        """
        
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.cantidad = cantidad

    def __str__(self):
        """
        Devuelve una cadena de caracteres que representa el ingrediente, en el siguiente formato:
        "<nombre>, <cantidad>, <unidad_medida>"
        """
        return f"{self.nombre}, {self.cantidad}, {self.unidad_medida}"

class App:
    def __init__(self, root):
        """
        Crea un objeto App con los siguientes atributos:
        
        Args:
        - root (tk.Tk): la ventana principal de la aplicación.
        """
        self.root = root
        self.recetas = []
         # Carga la imagen y la establece como fondo de la ventana
        img = Image.open("images/brand4.png")
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(self.root, image=photo)
        label.image = photo  # Esta línea previene que la imagen sea eliminada por el recolector de basura
        label.place(x=0, y=0, relwidth=1, relheight=1)
        self.imagen = Image.open("images/123.gif")
        self.frames = []
       
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(self.imagen))
                self.imagen.seek(len(self.frames))
        except EOFError:
            pass

        # Mostrar los frames de la imagen en una etiqueta
        self.label_imagen = tk.Label(self.root, image=self.frames[0])
        self.label_imagen.pack()
        self.timer_id = None
        
        # Esperar 3 segundos antes de mostrar la ventana principal
        self.root.after(4000, self.mostrar_ventana_principal)

        # Actualizar la imagen en la etiqueta cada cierto tiempo
        def actualizar_imagen(ind):
            frame = self.frames[ind]
            self.label_imagen.configure(image=frame)
            self.timer_id = self.root.after(100, actualizar_imagen, (ind+1)%len(self.frames))
            if ind == len(self.frames)-1:
                self.root.after(4000, actualizar_imagen, 0)

        # Actualizar la imagen en la etiqueta cada cierto tiempo
        self.root.after(0, actualizar_imagen, 0)
        
        self.imagen = None  # variable de instancia para la imagen
        
        
        #busqueda
        self.frame_busqueda = tk.Frame(self.root)
        self.frame_busqueda.pack(side="top")
        
        self.entry_busqueda = tk.Entry(self.frame_busqueda, width=35, bg="#747a8a", fg="#FFFFFF", bd=8)
        self.entry_busqueda.pack(side="left")

        self.entry_busqueda.insert(0, "Buscar receta...")
        
        self.button_buscar = tk.Button(self.frame_busqueda, text="Buscar", command=self.buscar_recetas,borderwidth=2, relief=tk.RIDGE, bg='#ED1525', fg='white',
                                                font=('Arial Rounded MT Bold',8), padx=8, pady=5, cursor='hand2',)
        self.button_buscar.pack(side="left")
        
        #receta del dia
        self.button_recipe_of_the_day = tk.Button(self.root, text="Receta del día", command=self.show_random_recipe, borderwidth=2, relief=tk.RIDGE, bg='#00D9FC', fg='black', font=('Arial Rounded MT Bold',8), padx=8, pady=5, cursor='hand2',)
        self.button_recipe_of_the_day.pack(side="top", padx=0)
      
        self.label_titulo = tk.Label(self.root, text="¡Encuentra la receta perfecta para hoy!", bg="#FF8CFF", fg="black", font=('Arial Rounded MT Bold',10))
        self.label_titulo.pack(fill=tk.BOTH, expand=True)

        self.frame_recetas = tk.Frame(self.root)
        self.frame_recetas.pack()

        self.label_recetas = tk.Label(self.frame_recetas, text="Recetas:")
        self.label_recetas.pack(side="left")

        self.listbox_recetas = tk.Listbox(self.frame_recetas, width=30, height=10, font=("Arial", 12))
        self.listbox_recetas.pack(side="left")
        self.listbox_recetas.configure(bg="black", fg="white")
       
        self.frame_botones = tk.Frame(self.root)
        self.frame_botones.pack(side="left")
        
        self.button_agregar = tk.Button(self.frame_botones, text="Agregar", command=self.agregar_receta,
                                                borderwidth=2, relief=tk.RIDGE, bg='#ED1525', fg='white',
                                                font=('Arial Rounded MT Bold',12), padx=8, pady=5, cursor='hand2',)
        self.button_agregar.pack(side="left")

        self.button_modificar = tk.Button(self.frame_botones, text="Modificar ", command=self.modificar_receta,borderwidth=2, relief=tk.RIDGE, bg='#ED1525', fg='white',
                                                font=('Arial Rounded MT Bold',12), padx=8, pady=5, cursor='hand2')
        self.button_modificar.pack(side="left")

        self.button_eliminar = tk.Button(self.frame_botones, text="Eliminar ", command=self.eliminar_receta,borderwidth=2, relief=tk.RIDGE, bg='#ED1525', fg='white',
                                                font=('Arial Rounded MT Bold',12), padx=8, pady=5, cursor='hand2')
        self.button_eliminar.pack(side="left")

        self.button_mostrar = tk.Button(self.root, text="Mostrar", command=self.mostrar_receta,borderwidth=2, relief=tk.RIDGE, bg='#ED1525', fg='white',
                                                font=('Arial Rounded MT Bold',12), padx=8, pady=5, cursor='hand2')
        self.button_mostrar.pack(side="right")
                
        self.root.protocol("WM_DELETE_WINDOW", self.guardar_recetas_en_csv)
        
        
    
    # Agregar receta predeterminada
        imagen_tor = Image.open("tor.png")
        imagen_tor_tk = ImageTk.PhotoImage(imagen_tor)
    
        receta_predeterminada = Receta(
            nombre="Tortilla española",
            ingredientes=[
                Ingrediente(nombre="Ingrediente 1", unidad_medida="gramos", cantidad=100),
                Ingrediente(nombre="Ingrediente 2", unidad_medida="tazas", cantidad=1),
            ],
            preparacion="Instrucciones de la receta predeterminada.",
            tiempo_preparacion=30,
            tiempo_coccion=60,
            fecha_creacion='2022-03-08',
            imagen=imagen_tor_tk
        )
        self.recetas.append(receta_predeterminada)
        self.listbox_recetas.insert(tk.END, receta_predeterminada.nombre)
        
        imagen_cesar = Image.open("cesar.png")
        imagen_cesar_tk = ImageTk.PhotoImage(imagen_cesar)
        
        receta_predeterminada2 = Receta(
            nombre="Ensalada César",
            ingredientes=[
                Ingrediente(nombre="Ingrediente 1", unidad_medida="gramos", cantidad=100),
                Ingrediente(nombre="Ingrediente 2", unidad_medida="tazas", cantidad=1),
            ],
            preparacion="Instrucciones de la receta predeterminada.",
            tiempo_preparacion=30,
            tiempo_coccion=60,
            fecha_creacion='2022-03-08',
            imagen=imagen_cesar_tk
        )
        self.recetas.append(receta_predeterminada2)
        self.listbox_recetas.insert(tk.END, receta_predeterminada2.nombre)
        
        imagen_pizza = Image.open("pizza.png")
        imagen_pizza_tk = ImageTk.PhotoImage(imagen_pizza)
        
        receta_predeterminada3 = Receta(
            nombre="Pizza Napolitana",
            ingredientes=[
                Ingrediente(nombre="Ingrediente 1", unidad_medida="gramos", cantidad=100),
                Ingrediente(nombre="Ingrediente 2", unidad_medida="tazas", cantidad=1),
            ],
            preparacion="Instrucciones de la receta predeterminada.",
            tiempo_preparacion=30,
            tiempo_coccion=60,
            fecha_creacion='2022-03-08',
            imagen=imagen_pizza_tk
        )
        self.recetas.append(receta_predeterminada3)
        self.listbox_recetas.insert(tk.END, receta_predeterminada3.nombre)
        
        self.root.title("RecetasYa")
        
    def show_random_recipe(self):
        """
    Muestra una receta aleatoria de la lista de recetas disponibles.

    Selecciona una receta aleatoria de la lista de recetas disponibles y muestra su información en una nueva ventana. La información mostrada incluye el nombre de la receta, los ingredientes, la preparación, el tiempo de preparación y cocción y la fecha de creación.
    """
        
        # Seleccionar una receta aleatoria de la lista de recetas disponibles.
        random_recipe = random.choice(self.recetas)

        # Mostrar la receta en la interfaz de usuario.
        top = tk.Toplevel(self.root)
        tk.Label(top, text=random_recipe.nombre).pack()
        tk.Label(top, text="Ingredientes:").pack()
        for ingrediente in random_recipe.ingredientes:
            tk.Label(top, text=str(ingrediente)).pack()
        tk.Label(top, text="Preparación:").pack()
        tk.Label(top, text=random_recipe.preparacion).pack()
        tk.Label(top, text=f"Tiempo de preparación: {random_recipe.tiempo_preparacion} minutos").pack()
        tk.Label(top, text=f"Tiempo de cocción: {random_recipe.tiempo_coccion} minutos").pack()
        tk.Label(top, text=f"Fecha de creación: {random_recipe.fecha_creacion}").pack()
        
        # Verificar si la receta tiene una imagen asociada
        if random_recipe.imagen:
            # Usar el objeto PhotoImage directamente
            photo = random_recipe.imagen

            # Crear un widget Canvas y mostrar la imagen
            canvas = tk.Canvas(top, width=photo.width(), height=photo.height())
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.pack()
            
    def buscar_recetas(self):
        """
    Busca recetas que coincidan con el término de búsqueda ingresado por el usuario.

    Obtiene el término de búsqueda ingresado por el usuario y filtra la lista de recetas para mostrar solo aquellas que coinciden con el término de búsqueda. Las recetas coincidentes se muestran en la Listbox de recetas.
    """
        # Obtener el término de búsqueda ingresado por el usuario
        termino_busqueda = self.entry_busqueda.get()

        # Filtrar la lista de recetas para mostrar solo aquellas que coinciden con el término de búsqueda
        recetas_coincidentes = list(filter(lambda receta: termino_busqueda.lower() in receta.nombre.lower(), self.recetas))

        # Limpiar la Listbox y mostrar las recetas coincidentes
        self.listbox_recetas.delete(0, tk.END)
        for receta in recetas_coincidentes:
            self.listbox_recetas.insert(tk.END, receta.nombre)
                
    def mostrar_ventana_principal(self):
        """
    Muestra la ventana principal de la aplicación.

    Detiene la actualización de la imagen en la etiqueta después de tres segundos y carga una imagen en el widget label_imagen. También desactiva la capacidad de cambiar el tamaño de la ventana.
    """ 
        # Detener la actualización de la imagen en la etiqueta después de tres segundos
        self.root.after_cancel(self.timer_id)

        # Cargar la imagen y actualizar el widget label_imagen
        imagen = Image.open("images/brand1.png")
        imagen = imagen.resize((370, 198), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(imagen)
        self.label_imagen.configure(image=imagen)
        self.label_imagen.image = imagen # importante para evitar un error de referencia
        
        # Desactivar la capacidad de cambiar el tamaño de la ventana
        root.resizable(False, False)

   
    def agregar_receta(self):
        """
        Abre una nueva ventana para agregar una nueva receta.
        Permite al usuario ingresar el nombre de la receta y luego agregar ingredientes a la misma.
        Los ingredientes se agregan a la lista de ingredientes de la receta.
        """
        
        top = tk.Toplevel(self.root)

        tk.Label(top, text="Nombre de la receta").pack()
        entry_nombre = tk.Entry(top)
        entry_nombre.pack()

        self.ingredientes = []

        def agregar_ingrediente():
            """
            Abre una nueva ventana para agregar un nuevo ingrediente a la lista de ingredientes de la receta.
            Permite al usuario ingresar el nombre del ingrediente, cantidad y unidad de medida.
            El nuevo ingrediente se agrega a la lista de ingredientes de la receta.
            """
            
            ingrediente_dialog = tk.Toplevel(top)

            tk.Label(ingrediente_dialog, text="Nombre del ingrediente").pack()
            entry_nombre = tk.Entry(ingrediente_dialog)
            entry_nombre.pack()

            tk.Label(ingrediente_dialog, text="Cantidad").pack()
            entry_cantidad = tk.Entry(ingrediente_dialog)
            entry_cantidad.pack()

            tk.Label(ingrediente_dialog, text="Unidad de medida").pack()
            entry_unidad_medida = tk.Entry(ingrediente_dialog)
            entry_unidad_medida.pack()
            def guardar_ingrediente():
                """
                Crea un objeto Ingrediente a partir de los valores ingresados por el usuario y lo agrega a la lista de ingredientes de la receta.
                Cierra la ventana de diálogo de ingreso de ingredientes.
                """
                
                ingrediente = Ingrediente(entry_nombre.get(), entry_unidad_medida.get(), entry_cantidad.get())
                self.ingredientes.append(ingrediente)
                ingrediente_dialog.destroy()

            tk.Button(ingrediente_dialog, text="Guardar", command=guardar_ingrediente).pack()

        tk.Button(top, text="Agregar ingrediente", command=agregar_ingrediente).pack()

        tk.Label(top, text="Tiempo de preparación (en minutos)").pack()
        tiempo_preparacion = tk.StringVar()
        entry_tiempo_preparacion = tk.Spinbox(top, from_=0, to=120, textvariable=tiempo_preparacion)
        entry_tiempo_preparacion.pack()

        tk.Label(top, text="Tiempo de cocción (en minutos)").pack()
        tiempo_coccion = tk.StringVar()
        entry_tiempo_coccion = tk.Spinbox(top, from_=0, to=120, textvariable=tiempo_coccion)
        entry_tiempo_coccion.pack()

        tk.Label(top, text="Preparación").pack()
        entry_preparacion = tk.Text(top, height=10, width=50)
        entry_preparacion.pack()

        tk.Label(top, text="Fecha de creación").pack()
        entry_fecha_creacion = tk.Entry(top)
        entry_fecha_creacion.pack()

        button_cargar_imagen = tk.Button(top, text="Cargar imagen", command=lambda: self.cargar_imagen(top))
        button_cargar_imagen.pack()

        def guardar_receta():
            """
            Esta función guarda una nueva receta en la lista de recetas.

            Crea una nueva instancia de la clase Receta con los valores obtenidos de las entradas de la interfaz gráfica y la agrega a la lista de recetas. También agrega el nombre de la receta a un Listbox y cierra la ventana emergente.
            """
            receta = Receta(entry_nombre.get(), self.ingredientes, entry_preparacion.get("1.0", tk.END), entry_tiempo_preparacion.get(), entry_tiempo_coccion.get(), self.imagen)
            receta.fecha_creacion = entry_fecha_creacion.get()
            self.recetas.append(receta)
            self.listbox_recetas.insert(tk.END, receta.nombre)
            top.destroy()

        tk.Button(top, text="Guardar receta", command=guardar_receta).pack()

    def cargar_imagen(self, top):
        """
    Carga una imagen seleccionada por el usuario y la muestra en un widget Label.

    :param top: El widget padre en el que se mostrará la imagen.
    :type top: Tkinter widget

    Abre un cuadro de diálogo para que el usuario seleccione un archivo de imagen. Si se selecciona un archivo válido, se carga en un objeto PhotoImage y se muestra en un widget Label. Si ocurre un error al cargar la imagen, se muestra un mensaje de error.
    """
        
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        print("Selected file:", filename)

        try:
            # Cargar la imagen en un PhotoImage y asignarla a la variable de instancia
            self.imagen = tk.PhotoImage(file=filename)

            # Mostrar la imagen en un widget Label
            label_imagen = tk.Label(top, image=self.imagen)
            label_imagen.pack()
        except:
            # Mostrar mensaje de error si no se puede cargar la imagen
            tk.messagebox.showerror("Error", "No se pudo cargar la imagen.")
     
    def guardar_receta(self, nombre, ingredientes, preparacion, tiempo_preparacion, tiempo_coccion, fecha_creacion, imagen=None):
        if imagen is None:
            # Usar la variable de instancia si no se proporciona una imagen
            imagen = self.imagen

        receta = Receta(nombre, ingredientes, preparacion, tiempo_preparacion, tiempo_coccion, imagen)
        receta.fecha_creacion = fecha_creacion
        self.recetas.append(receta)
        self.listbox_recetas.insert(tk.END, receta.nombre)

    def guardar_recetas_en_csv(self):
        """
        Esta función guarda todas las recetas en un archivo CSV.

        Abre un archivo llamado 'recetas.csv' en modo de escritura y escribe la primera fila con los nombres de las columnas. Luego, para cada receta en la lista de recetas, escribe una fila con los valores de los atributos de la receta. Finalmente, cierra el archivo y destruye la ventana principal.
        """
        with open('recetas.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nombre', 'ingredientes', 'preparacion', 'tiempo_preparacion', 'tiempo_coccion', 'fecha_creacion', 'imagen'])
            for receta in self.recetas:
                writer.writerow([receta.nombre, receta.ingredientes, receta.preparacion, receta.tiempo_preparacion, receta.tiempo_coccion, receta.fecha_creacion, receta.imagen])
            self.root.destroy()

    def buscar_receta(self, nombre_receta):
        """
        Esta función busca una receta por su nombre.

        Recorre la lista de recetas y compara el nombre de cada receta con el nombre proporcionado como argumento. Si encuentra una coincidencia, devuelve la instancia de la receta. Si no encuentra ninguna coincidencia, devuelve None.

        Args:
            nombre_receta (str): El nombre de la receta a buscar.

        Returns:
            Receta: La instancia de la receta encontrada o None si no se encuentra ninguna coincidencia.
        """
        
        for receta in self.recetas:
            if receta.nombre.lower() == nombre_receta.lower():
                return receta
        return None
    
    def mostrar_receta(self):
        """
    Esta función muestra los detalles de una receta seleccionada en un Listbox.

    Obtiene el índice de la receta seleccionada en el Listbox y recupera la instancia de la receta correspondiente de la lista de recetas. Crea una nueva ventana emergente y muestra los detalles de la receta en etiquetas. Si la receta tiene una imagen asignada, también muestra la imagen.
    """
        
        seleccion = self.listbox_recetas.curselection()
        if seleccion:
            indice = seleccion[0]
            receta = self.recetas[indice]

            top = tk.Toplevel(self.root)

            tk.Label(top, text=receta.nombre).pack()
            tk.Label(top, text="Ingredientes:").pack()
            tk.Label(top, text=receta.ingredientes).pack()
            tk.Label(top, text="Preparación:").pack()
            tk.Label(top, text=receta.preparacion).pack()
            tk.Label(top, text="Tiempo de preparación (en minutos)").pack()
            tk.Label(top, text=receta.tiempo_preparacion).pack()
            tk.Label(top, text="Tiempo de cocción (en minutos)").pack()
            tk.Label(top, text=receta.tiempo_coccion).pack() # Se agrega etiqueta para el tiempo de cocción

            # Mostrar la imagen asignada a la receta si existe
            if receta.imagen:
                tk.Label(top, image=receta.imagen).pack()
            else:
                tk.Label(top, text="No hay imagen disponible").pack()

    def eliminar_receta(self):
        """
    Esta función elimina una receta seleccionada en un Listbox.

    Obtiene el índice de la receta seleccionada en el Listbox y recupera la instancia de la receta correspondiente de la lista de recetas. Elimina el elemento del Listbox y de la lista de recetas.
    """
        
        seleccion = self.listbox_recetas.curselection()
        if seleccion:
            indice = seleccion[0]
            receta = self.recetas[indice]

            self.listbox_recetas.delete(indice)
            self.recetas.remove(receta)
    
    def modificar_receta(self):
        """
    Esta función permite modificar una receta seleccionada en un Listbox.

    Obtiene el índice de la receta seleccionada en el Listbox y recupera la instancia de la receta correspondiente de la lista de recetas. Crea una nueva ventana emergente con entradas para modificar los atributos de la receta. También permite agregar nuevos ingredientes a la receta.
    """
        
        seleccion = self.listbox_recetas.curselection()
        if seleccion:
            indice = seleccion[0]
            receta = self.recetas[indice]

            top = tk.Toplevel(self.root)

            tk.Label(top, text="Nombre de la receta").pack()
            entry_nombre = tk.Entry(top, textvariable=tk.StringVar(value=receta.nombre))
            entry_nombre.pack()

            self.ingredientes = []

            def agregar_ingrediente():
                ingrediente_dialog = tk.Toplevel(top)

                tk.Label(ingrediente_dialog, text="Nombre del ingrediente").pack()
                entry_nombre = tk.Entry(ingrediente_dialog)
                entry_nombre.pack()

                tk.Label(ingrediente_dialog, text="Cantidad").pack()
                entry_cantidad = tk.Entry(ingrediente_dialog)
                entry_cantidad.pack()

                tk.Label(ingrediente_dialog, text="Unidad de medida").pack()
                entry_unidad_medida = tk.Entry(ingrediente_dialog)
                entry_unidad_medida.pack()

                def guardar_ingrediente():
                    ingrediente = Ingrediente(entry_nombre.get(), entry_unidad_medida.get(), entry_cantidad.get())
                    self.ingredientes.append(ingrediente)
                    ingrediente_dialog.destroy()

                tk.Button(ingrediente_dialog, text="Guardar", command=guardar_ingrediente).pack()

            tk.Button(top, text="Agregar ingrediente", command=agregar_ingrediente).pack()

            tk.Label(top, text="Tiempo de preparación (en minutos)").pack()
            tiempo_preparacion = tk.StringVar(value=receta.tiempo_preparacion)
            entry_tiempo_preparacion = tk.Spinbox(top, from_=0, to=120, textvariable=tiempo_preparacion)
            entry_tiempo_preparacion.pack()

            tk.Label(top, text="Tiempo de cocción (en minutos)").pack()
            tiempo_coccion = tk.StringVar(value=receta.tiempo_coccion)
            entry_tiempo_coccion = tk.Spinbox(top, from_=0, to=120, textvariable=tiempo_coccion)
            entry_tiempo_coccion.pack()

            tk.Label(top, text="Preparación").pack()
            entry_preparacion = tk.Text(top, height=10, width=50)
            entry_preparacion.insert(tk.END, receta.preparacion)
            entry_preparacion.pack()

            tk.Label(top, text="Fecha de creación").pack()
            entry_fecha_creacion = tk.Entry(top, textvariable=tk.StringVar(value=receta.fecha_creacion))
            entry_fecha_creacion.pack()

            button_cargar_imagen = tk.Button(top, text="Cargar imagen", command=lambda: self.cargar_imagen(top))
            button_cargar_imagen.pack()

            def guardar_receta():
                receta.nombre = entry_nombre.get()
                receta.ingredientes = self.ingredientes
                receta.preparacion = entry_preparacion.get("1.0", tk.END)
                receta.tiempo_preparacion = tiempo_preparacion.get()
                receta.tiempo_coccion = tiempo_coccion.get()
                receta.fecha_creacion = entry_fecha_creacion.get()
                receta.imagen = self.imagen

                self.listbox_recetas.delete(indice)
                self.listbox_recetas.insert(indice, receta.nombre)
                self.recetas[indice] = receta
                top.destroy()

            tk.Button(top, text="Guardar receta", command=guardar_receta).pack()
    
root = tk.Tk()
root.iconbitmap('favicon.ico')
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.guardar_recetas_en_csv)
root.mainloop()
