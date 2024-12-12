import os 
import customtkinter as ctk
contraUni = ""
contraUniConf = ""
cuentasD = []
cuentasV = []
DATOSV = "datosVendedor.txt"
DATOSD = "datosDueno.txt"


def cargarDatosD():
    global contraUni
    dueño = {}
    if os.path.exists(DATOSD):
        with open(DATOSD, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith("contrasenaUniversal:"):
                    contraUni = (linea.split(": ")[1])
                elif linea.startswith("usuario"):
                    if dueño:
                        cuentasD.append(dueño)
                        dueño = {}
                    dueño["usuario"] = linea.split(": ")[1]
                elif linea.startswith("contrasena:"):
                    dueño["contrasena"] = linea.split(": ")[1]
            if dueño:
                cuentasD.append(dueño)
    return contraUni

def cargarDatosV():
    vendedor = {}
    if os.path.exists(DATOSV):
        with open(DATOSV, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()

                if linea.startswith("usuario"):
                    if vendedor:
                        cuentasV.append(vendedor)
                        vendedor = {}
                    vendedor["usuario"] = linea.split(": ")[1]
                elif linea.startswith("contrasena:"):
                    vendedor["contrasena"] = linea.split(": ")[1]
            if vendedor:
                cuentasV.append(vendedor)

def guardarDatosD():
    with open(DATOSD, "w", encoding="utf-8") as f:
        f.write(f"contrasenaUniversal: {contraUni}\n\n")
        for i in cuentasD:
            f.write(f"usuario: {i["usuario"]}\n")
            f.write(f"contrasena: {i["contrasena"]}\n\n")

def guardarDatosV():
    with open(DATOSV, "w", encoding="utf-8") as f:
        for i in cuentasV:
            f.write(f"usuario: {i["usuario"]}\n")
            f.write(f"contrasena: {i["contrasena"]}\n\n")

def comprobarCu():
    if contraUni != "":
        return True
    else:
        return False
    
def verificarContraseñaU(passwd, passwdConf):
    global contraUni, contraUniConf
    contraUni = passwd
    contraUniConf = passwdConf

    if contraUni == "" and contraUniConf == "":
        return False
    elif contraUni == contraUniConf:
        return True
    else:
        return False
    
def confirmarContraU(contraE):
    if contraE == contraUni:
        return True
    else:
        return False
    
def incioSesionD(usuario, contrasena):
    if usuario == "" and contrasena == "":
        return False
    else:
        for i in cuentasD:
            if i["usuario"] == usuario and i["contrasena"] == contrasena:
                return True
    return False

def incioSesionV(usuario, contrasena):
    if usuario == "" and contrasena == "":
        return False
    else:
        for i in cuentasV:
            if i["usuario"] == usuario and i["contrasena"] == contrasena:
                return True
    return False

def registrarDueno(usuario, contrasena):
    dueno = {
        "usuario" : usuario,
        "contrasena" : contrasena
    }
    cuentasD.append(dueno)
    guardarDatosD()

def registrarVendedor(usuario, contrasena):
    vendedor = {
        "usuario" : usuario,
        "contrasena" : contrasena
    }
    cuentasV.append(vendedor)
    guardarDatosV()

def verificarContraseña(passwd, passwdConf):
    if passwd == "" and passwdConf == "":
        return False
    elif passwd == passwdConf:
        return True
    else:
        return False



cargarDatosD()
for pilotoz in cuentasD:
    print(pilotoz)

cargarDatosV()
for pilotoz in cuentasV:
    print(pilotoz)
#print(verificarContraseña(contraUni, contraUniConf))

comprobarCu()