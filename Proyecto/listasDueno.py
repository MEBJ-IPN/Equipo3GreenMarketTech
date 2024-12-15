import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import os
import customtkinter as ctk
import variablesGlobales
from variablesGlobales import ventana
import menuDueno
from PIL import Image, ImageTk, ImageOps

style = ttk.Style()

class Producto:
    def __init__(self, nombre, tipo, precio, cantidad):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.cantidad = cantidad
        self.cantidadS = self.cantidad
        self.precio_venta = 0
        self.cantidad_vendida = 0
        self.ventas_diarias = 0  # Nuevo atributo para ventas del día
        self.comprado = False
        self.ganancia_total_acumulada = 0 - (self.precio * self.cantidad)


    def calcular_ganancia_total(self):
        ingreso_total = self.precio_venta * self.cantidad_vendida
        costo_total = self.precio * self.cantidad
        return ingreso_total - costo_total

    def calcular_ganancia_del_dia(self):
        return self.cantidad_vendida * self.precio_venta

    def calcular_merma(self):
        merma_real = self.cantidadS
        merma_esperada = self.cantidad * 0.13
        return merma_esperada, merma_real



class Lista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []
        self.ultima_modificacion = "00/00/0000"

    def agregar_producto(self, producto):
        producto.lista = self  # Asignar la lista al producto
        self.productos.append(producto)
        self.actualizar_fecha()

    def actualizar_fecha(self):
        self.ultima_modificacion = datetime.now().strftime("%d/%m/%Y")


class SistemaListas:
    def __init__(self):
        self.listas = []
        self.cargar_datos()

    def eliminar_lista(self, nombre):
        self.listas = [lista for lista in self.listas if lista.nombre != nombre]
        self.guardar_datos()

    def guardar_datos(self):
        try:
            with open("datos.txt", "w") as archivo:
                for lista in self.listas:
                    archivo.write(f"Lista: {lista.nombre}\n")
                    for producto in lista.productos:
                        archivo.write(
                            f"{producto.nombre},{producto.tipo},{producto.precio},{producto.cantidad}," 
                            f"{producto.cantidadS},{producto.precio_venta},{producto.cantidad_vendida},"
                            f"{producto.ganancia_total_acumulada},{producto.comprado}\n"
                        )
                    archivo.write(f"Última Modificación: {lista.ultima_modificacion}\n")
                    archivo.write("\n")
            print("Datos guardados exitosamente.")  # Mensaje de depuración
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def cargar_datos(self):
        try:
            with open("datos.txt", "r") as archivo:
                lista_actual = None
                for linea in archivo:
                    linea = linea.strip()
                    if linea.startswith("Lista:"):
                        nombre_lista = linea.split(":")[1].strip()
                        lista_actual = Lista(nombre_lista)
                        self.listas.append(lista_actual)
                    elif lista_actual and linea.startswith("Última Modificación:"):
                        lista_actual.ultima_modificacion = linea.split(":")[1].strip()
                    elif lista_actual and linea:
                        datos = linea.split(",")
                        if len(datos) == 9:
                            (nombre, tipo, precio, cantidad, cantidadS, precio_venta,
                            cantidad_vendida, ganancia_total, comprado) = datos
                            producto = Producto(
                                nombre=nombre,
                                tipo=tipo,
                                precio=float(precio),
                                cantidad=int(cantidad)
                            )
                            producto.cantidadS = int(cantidadS)
                            producto.precio_venta = float(precio_venta)
                            producto.cantidad_vendida = int(cantidad_vendida)
                            producto.ganancia_total_acumulada = float(ganancia_total)
                            producto.comprado = comprado == "True"
                            producto.lista = lista_actual
                            lista_actual.productos.append(producto)
            print("Datos cargados exitosamente.")  # Mensaje de depuración
        except FileNotFoundError:
            print("No se encontró el archivo de datos, se creará uno nuevo al guardar.")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")


    def crear_lista(self, nombre):
        nueva_lista = Lista(nombre)
        nueva_lista.actualizar_fecha()
        self.listas.append(nueva_lista)

    def obtener_listas_recientes(self):
        return sorted(self.listas, key=lambda x: x.ultima_modificacion, reverse=True)[:8]

    def buscar_lista_por_nombre(self, busqueda):
        return [lista for lista in self.listas if busqueda.lower() in lista.nombre.lower()]
    
    def copiar_lista(self, lista_original, nuevo_nombre):
        nueva_lista = Lista(nuevo_nombre)
        for producto in lista_original.productos:
            producto_copiado = Producto(
                nombre=producto.nombre,
                tipo=producto.tipo,
                precio=producto.precio,
                cantidad=producto.cantidad,
            )
            # No copiar precio_venta ni cantidad_vendida
            nueva_lista.agregar_producto(producto_copiado)
        self.listas.append(nueva_lista)


class InterfazSistema:
    def __init__(self, root, sistema, main_frame):
        self.sistema = sistema
        self.root = root
        self.main_frame = main_frame
        self.root.title("Gestión de Listas")

        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        # Botones principales
        ctk.CTkButton(self.main_frame, text="Crear Lista", font=("Roboto", 18, "bold"), command=self.abrir_crear_lista, corner_radius=20, image=variablesGlobales.masIcono, compound="left").place(relx=0.2, rely=0.09, anchor="center", relwidth=0.17, relheight=0.07)
        ctk.CTkButton(self.main_frame, text="Consultar Listas", font=("Roboto", 18, "bold"), command=self.abrir_consultar_listas, corner_radius=20, image=variablesGlobales.buscarIcono, compound="left").place(relx=0.4, rely=0.09, anchor="center", relwidth=0.19, relheight=0.07)
        ctk.CTkButton(self.main_frame, text="Indicaciones", font=("Roboto", 18, "bold"), command=self.mostrar_indicaciones, corner_radius=20, image=variablesGlobales.indicacionesIcono, compound="left").place(relx=0.6, rely=0.09, anchor="center", relwidth=0.17, relheight=0.07)
        ctk.CTkButton(self.main_frame, text="Copiar Lista", font=("Roboto", 18, "bold"), command=self.abrir_copiar_lista, corner_radius=20, image=variablesGlobales.copiarIcono, compound="left").place(relx=0.8, rely=0.09, anchor="center", relwidth=0.17, relheight=0.07)
        

        # Tabla de listas recientes
        self.tabla_frame = tk.Frame(self.main_frame, pady=0)
        self.tabla_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.tabla = ttk.Treeview(self.tabla_frame, columns=("Nombre", "Última Modificación"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Última Modificación", text="Última Modificación")
        self.tabla.pack()

        self.mostrar_listas_recientes()

    def salir(self):
        self.sistema.guardar_datos()
        self.root.destroy()


    def abrir_copiar_lista(self):
        ventana_copiar = tk.Toplevel(self.root)
        ventana_copiar.title("Copiar Lista")

        tk.Label(ventana_copiar, text="Selecciona una lista para copiar:").pack(pady=10)
        
        lista_desplegable = ttk.Combobox(
            ventana_copiar,
            values=[lista.nombre for lista in self.sistema.listas],
            state="readonly"
        )
        lista_desplegable.pack(pady=5)

        tk.Label(ventana_copiar, text="Nuevo nombre para la lista copiada:").pack(pady=10)
        entrada_nombre = tk.Entry(ventana_copiar)
        entrada_nombre.pack(pady=5)

        def copiar():
            lista_seleccionada = next(
                (lista for lista in self.sistema.listas if lista.nombre == lista_desplegable.get()),
                None
            )
            nuevo_nombre = entrada_nombre.get().strip()
            if lista_seleccionada and nuevo_nombre:
                self.sistema.copiar_lista(lista_seleccionada, nuevo_nombre)
                self.mostrar_listas_recientes()
                messagebox.showinfo("Éxito", f"La lista '{lista_seleccionada.nombre}' fue copiada como '{nuevo_nombre}'.")
                self.sistema.guardar_datos()
                ventana_copiar.destroy()
            else:
                messagebox.showerror("Error", "Debes seleccionar una lista y especificar un nombre válido.")

        ctk.CTkButton(ventana_copiar, text="Copiar Lista", command=copiar).pack(pady=10)



    def mostrar_listas_recientes(self):
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        columnas = ("Nombre", "Última Modificación")
        tabla = ttk.Treeview(self.tabla_frame, columns=columnas, show="headings", height=8)
        tabla.pack(pady=(0, 25)) 

        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Última Modificación", text="Última Modificación")

        style.configure("Treeview.Heading", font=("Ubuntu", 14, "bold"))
        style.configure("Treeview", rowheight=40, font="Ubuntu")
        tabla.column("Nombre", width=700, anchor="w")
        tabla.column("Última Modificación", width=400, anchor="center")

        listas_recientes = self.sistema.obtener_listas_recientes()

        for lista in listas_recientes:
            tabla.insert("", "end", values=(lista.nombre, lista.ultima_modificacion))

        tabla.pack(fill="both", expand=True)

        def seleccionar_lista(event):
            item = tabla.selection()
            if item:
                nombre_lista = tabla.item(item, "values")[0]
                lista_seleccionada = next((lista for lista in self.sistema.listas if lista.nombre == nombre_lista), None)
                if lista_seleccionada:
                    self.mostrar_productos_de_lista(lista_seleccionada)

        tabla.bind("<Double-1>", seleccionar_lista)

    def mostrar_listas_en_tabla(self, listas):
        for row in self.tabla_listas.get_children():
            self.tabla_listas.delete(row)

        for lista in listas:
            self.tabla_listas.insert("", "end", values=(lista.nombre, lista.ultima_modificacion))

    def eliminar_lista(self):
        seleccion = self.tabla_listas.selection()
        if seleccion:
            item = self.tabla_listas.item(seleccion)
            nombre_lista = item["values"][0]
            self.sistema.eliminar_lista(nombre_lista)
            self.mostrar_listas_en_tabla(self.sistema.listas)
            messagebox.showinfo("Éxito", f"La lista '{nombre_lista}' fue eliminada.")

    def abrir_crear_lista(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Lista")
        tk.Label(ventana, text="Nombre de la nueva lista:").pack(pady=10)
        entrada_nombre = tk.Entry(ventana)
        entrada_nombre.pack(pady=10)

        def crear():
            nombre = entrada_nombre.get().strip()
            if nombre:
                self.sistema.crear_lista(nombre)
                self.mostrar_listas_recientes()
                tk.Label(ventana, text=f"Lista '{nombre}' creada con éxito.").pack(pady=10)
                self.sistema.guardar_datos()

        ctk.CTkButton(ventana, text="Crear", command=crear).pack(pady=10)

    def abrir_consultar_listas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar Listas")

        frame_busqueda = tk.Frame(ventana, padx=10, pady=10)
        frame_busqueda.pack()

        tk.Label(frame_busqueda, text="Buscar lista por nombre:").grid(row=0, column=0, padx=5, pady=5)
        entrada_busqueda = tk.Entry(frame_busqueda)
        entrada_busqueda.grid(row=0, column=1, padx=5, pady=5)

        def buscar_listas():
            busqueda = entrada_busqueda.get().strip().lower()
            listas_encontradas = self.sistema.buscar_lista_por_nombre(busqueda)
            self.mostrar_listas_en_tabla(listas_encontradas)

        ctk.CTkButton(frame_busqueda, text="Buscar", command=buscar_listas).grid(row=0, column=2, padx=5, pady=5)

        frame_listas = tk.Frame(ventana, padx=10, pady=10)
        frame_listas.pack()

        self.tabla_listas = ttk.Treeview(frame_listas, columns=("Nombre", "Última Modificación"), show="headings")
        self.tabla_listas.heading("Nombre", text="Nombre")
        self.tabla_listas.heading("Última Modificación", text="Última Modificación")
        self.tabla_listas.pack()

        self.mostrar_listas_en_tabla(self.sistema.listas)

        def seleccionar_lista(event):
            seleccion = self.tabla_listas.selection()
            if seleccion:
                item = self.tabla_listas.item(seleccion)
                nombre_lista = item["values"][0]
                lista_seleccionada = next((lista for lista in self.sistema.listas if lista.nombre == nombre_lista), None)
                if lista_seleccionada:
                    self.mostrar_productos_de_lista(lista_seleccionada)

        self.tabla_listas.bind("<Double-1>", seleccionar_lista)

        def eliminar_lista():
            seleccion = self.tabla_listas.selection()
            if seleccion:
                item = self.tabla_listas.item(seleccion)
                nombre_lista = item["values"][0]
                self.sistema.eliminar_lista(nombre_lista)
                self.mostrar_listas_en_tabla(self.sistema.listas)
                messagebox.showinfo("Éxito", f"La lista '{nombre_lista}' fue eliminada.")

        tk.Button(ventana, text="Eliminar Lista", command=eliminar_lista).pack(pady=10)

    

    def mostrar_productos_de_lista(self, lista, ventana_actual=None):
        global ventana_productos
        if ventana_actual:
            ventana_actual.destroy()

        ventana_productos = tk.Toplevel(self.root)
        ventana_productos.title(f"Productos de {lista.nombre}")

        frame_productos = tk.Frame(ventana_productos, padx=10, pady=10)
        frame_productos.pack()

        tabla_productos = ttk.Treeview(
            frame_productos, 
            columns=("Producto", "Tipo", "Precio", "Cantidad", "Comprado"), 
            show="headings"
        )
        tabla_productos.heading("Producto", text="Producto")
        tabla_productos.heading("Tipo", text="Tipo")
        tabla_productos.heading("Precio", text="Precio")
        tabla_productos.heading("Cantidad", text="Cantidad")
        tabla_productos.heading("Comprado", text="Comprado")
        tabla_productos.pack()

        for producto in lista.productos:
            tabla_productos.insert(
                "", 
                "end", 
                values=(
                    producto.nombre, 
                    producto.tipo, 
                    f"${producto.precio:.2f}", 
                    f"{producto.cantidad}kg", 
                    "Sí" if producto.comprado else "No"
                )
            )

        def marcar_comprado(event):
            seleccion = tabla_productos.selection()
            if seleccion:
                item = tabla_productos.item(seleccion)
                nombre_producto = item["values"][0]
                producto_seleccionado = next(
                    (p for p in lista.productos if p.nombre == nombre_producto), 
                    None
                )
                if producto_seleccionado:
                    producto_seleccionado.comprado = not producto_seleccionado.comprado
                    self.mostrar_productos_de_lista(lista, ventana_productos)
            self.sistema.guardar_datos()

        tabla_productos.bind("<Double-1>", marcar_comprado)

        def abrir_ganancias():
            self.abrir_ganancias(lista)

        ctk.CTkButton(ventana_productos, text="Ganancias", command=abrir_ganancias).pack(pady=10)


    def abrir_ganancias(self, lista, ventana_actual=None):
        global ventanaG
        if ventana_actual:
            ventana_actual.destroy()

        ventanaG = tk.Toplevel(self.root)
        ventanaG.title(f"Ganancias de {lista.nombre}")

        frame_ganancias = tk.Frame(ventanaG, padx=10, pady=10)
        frame_ganancias.pack()

        tabla_ganancias = ttk.Treeview(
            frame_ganancias,
            columns=("Producto", "Precio Venta", "Cant. Vendida", "Ganancia Total", "Ganancia del Día", "Merma Esperada", "Merma Real"),
            show="headings"
        )
        tabla_ganancias.column("Producto", width=150)
        tabla_ganancias.heading("Producto", text="Producto")
        tabla_ganancias.heading("Precio Venta", text="Precio Venta")
        tabla_ganancias.heading("Cant. Vendida", text="Cantidad Vendida")
        tabla_ganancias.heading("Ganancia Total", text="Ganancia Total")
        tabla_ganancias.heading("Ganancia del Día", text="Ganancia del Día")
        tabla_ganancias.heading("Merma Esperada", text="Merma Esperada")
        tabla_ganancias.heading("Merma Real", text="Merma Real")
        tabla_ganancias.pack()

        productos_comprados = [producto for producto in lista.productos if producto.comprado]

        for producto in productos_comprados:
            ganancia_total = producto.calcular_ganancia_total()
            ganancia_del_dia = producto.ventas_diarias
            merma_esperada, merma_real = producto.calcular_merma()
            tabla_ganancias.insert(
                "",
                "end",
                values=(
                    producto.nombre,
                    f"${producto.precio_venta:.2f}",
                    f"{producto.cantidad_vendida}kg",
                    f"${producto.ganancia_total_acumulada:.2f}",
                    f"${ganancia_del_dia:.2f}",
                    f"{merma_esperada:.2f}kg",
                    f"{merma_real:.2f}kg"
                )
            )

        def mostrar_recomendaciones():
            total_merma_real = sum(p.calcular_merma()[1] for p in productos_comprados)
            total_cantidad_comprada = sum(p.cantidad for p in productos_comprados)
            porcentaje_merma = (total_merma_real / total_cantidad_comprada) * 100 if total_cantidad_comprada != 0 else 0

            recomendaciones = [f"Total merma real: {total_merma_real:.2f}kg"]
            recomendaciones.append(f"Porcentaje de merma: {porcentaje_merma:.2f}%")

            # Leer recomendaciones desde el archivo de texto
            with open("recomendaciones.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Procesar las recomendaciones
            recomendaciones_dict = {}
            for line in lines:
                if line.startswith("Recomendacion"):
                    try:
                        key, value = line.split(": ", 1)
                        if key not in recomendaciones_dict:
                            recomendaciones_dict[key] = []
                        recomendaciones_dict[key].append(value.strip())
                    except ValueError:
                # Handle the case where the line doesn't split correctly
                        continue

            # Seleccionar recomendaciones basadas en el porcentaje de merma
            if porcentaje_merma >= 40:
                recomendaciones.extend(recomendaciones_dict.get("Recomendacion40", []))
            elif porcentaje_merma >= 30:
                recomendaciones.extend(recomendaciones_dict.get("Recomendacion30", []))
            elif porcentaje_merma >= 20:
                recomendaciones.extend(recomendaciones_dict.get("Recomendacion20", []))
            elif porcentaje_merma >= 10:
                recomendaciones.extend(recomendaciones_dict.get("Recomendacion10", []))
            else:
                recomendaciones.append("La merma está bajo control.")

            recomendaciones_texto = "\n".join(recomendaciones)
            messagebox.showinfo("Recomendaciones", recomendaciones_texto)

        ctk.CTkButton(ventanaG, text="Recomendaciones", command=mostrar_recomendaciones).pack(pady=10)

    def mostrar_indicaciones(self):
        indicacionesV = tk.Toplevel(ventana)
        indicacionesV.title("Escribir Indicaciones")

        opcion_seleccionada = tk.StringVar(value="Sin modificaciones")  

        tk.Label(indicacionesV, text="Seleccione una opción:", font=("Arial", 12, "bold")).pack(pady=5)
        opciones = [("Aumento", "Aumento"), ("Decremento", "Decremento"), ("Otro", "Otro")]
        for texto, valor in opciones:
            tk.Radiobutton(indicacionesV, text=texto, variable=opcion_seleccionada, value=valor).pack(anchor="w", padx=20)

        tk.Label(indicacionesV, text="Escriba las indicaciones para el vendedor:", font=("Arial", 12)).pack(pady=10)
        texto_indicaciones = tk.Text(indicacionesV, height=10, width=50)
        texto_indicaciones.pack(pady=10)

        def guardar_indicaciones():
            indicaciones = texto_indicaciones.get("1.0", tk.END).strip()
            opcion = opcion_seleccionada.get()
            if indicaciones:
                with open("indicaciones.txt", "w") as file:
                    file.write(f"{opcion}\n")  # Guardar la opción seleccionada
                    file.write(indicaciones)
                messagebox.showinfo("Indicaciones Guardadas", "Las indicaciones han sido guardadas correctamente.")
                indicacionesV.destroy()

                # Aquí no cambiamos el color del botón vendedor, ya que solo el vendedor debe verlo en rojo.
            else:
                messagebox.showerror("Error", "Las indicaciones no pueden estar vacías.")

        ctk.CTkButton(indicacionesV, text="Guardar", command=guardar_indicaciones).pack(pady=10)


ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")


def iniciarDueno():
    global app
    sistema = SistemaListas()
    root = menuDueno.pantallaDuenoV
    
    main_frame = menuDueno.frameSec(root)
    main_frame.pack()
    app = InterfazSistema(ventana, sistema, main_frame)

