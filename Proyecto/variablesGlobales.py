import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps
import os, sys

def path(relative_path:str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ventana = ctk.CTk()
ventana.title("GreenMarket Tech")

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

flechaIcono = ctk.CTkImage(Image.open(path("img/iconos/flechaIcono.png")), size=(20, 20))
buscarIcono = ctk.CTkImage(Image.open(path("img/iconos/buscarIcono.png")), size=(20, 20))
masIcono = ctk.CTkImage(Image.open(path("img/iconos/masIcono.png")), size=(20, 20))
indicacionesIcono = ctk.CTkImage(Image.open(path("img/iconos/indicacionesIcono.png")), size=(20, 20))
copiarIcono = ctk.CTkImage(Image.open(path("img/iconos/copiarIcono.png")), size=(20, 20))

#Pantalla principal

ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventana.config(background="#D0D0D0")

inicioSIcono = ctk.CTkImage(Image.open(path("img/iconos/inicioSIcono.png")), size=(20, 20))