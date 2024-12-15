import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import usuarios
import variablesGlobales
from variablesGlobales import ventana, flechaIcono
import listasVendedor
import os, sys

def path(relative_path:str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def regresar():
    pantallaVendedorV.pack_forget()
    import incio_I
    incio_I.pantallaCuentaVendedor(ventana, pantallaVendedorV)

#Pantalla principal de dueño
def pantallaVendedor(ventana, frameQ):
    global pantallaVendedorV
    #Frame usuarios
    pantallaVendedorV = ctk.CTkFrame(ventana, bg_color="#D9D9D9")
    pantallaVendedorV.pack(fill="both", expand=True)

    #Fondo de cuentas
    bgImg = Image.open(path("img/pantallasDueno/principalDueno.png"))
    bgR = bgImg.resize((variablesGlobales.ancho_pantalla, variablesGlobales.alto_pantalla))
    bgP = ImageTk.PhotoImage(bgR)
    bgLab = ctk.CTkLabel(pantallaVendedorV, image=bgP, text="", anchor="center")
    bgLab.place(relwidth=1, relheight=1, anchor="center", relx=0.5, rely=0.5)

    cerrarSesion = ctk.CTkButton(pantallaVendedorV, text="Cerrar sesión", font=("Roboto", 25, "bold"), border_width=0, corner_radius=30, bg_color="#92ADA7", image=flechaIcono, compound="left", command=lambda:regresar())
    cerrarSesion.place(relx=0.28, rely=0.84, relwidth=0.2, relheight=0.07, anchor="center")
    

    #Quitar y agregar frame
    frameQ.pack_forget()
    pantallaVendedorV.pack(fill="both", expand=True)

    return pantallaVendedorV

def frameSec(ven):
    global frameSecV
    frameSecV = ctk.CTkFrame(ven,fg_color="#D9D9D9")
    frameSecV.columnconfigure(0, weight=1)
    frameSecV.rowconfigure(0, weight=1) 
    frameSecV.pack(fill="both", expand=True, padx=270, pady=(140, 320))
    return frameSecV

