import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json")
LIMITE_RETIRO = 10000

def cargar_datos():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass  # si el archivo está dañado, se empieza con los datos por defecto
    return {
        "Gerardo": {"nip": "3333", "saldo": 0, "bloqueado": False}
    }

def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

usuarios = cargar_datos()
guardar_datos()
print("Archivo en:", ARCHIVO)
intentos = {}

ventana = tk.Tk()
ventana.title("Cajero automático")
ventana.geometry("400x500")

etiqueta = tk.Label(ventana, text="CAJERO AUTOMÁTICO", font=("Arial", 18,))
etiqueta.pack(pady=20)
# Funciones

def mostrar_registro():
    menu.pack_forget()
    entrada_nombre.delete(0, tk.END)
    entrada_nip.delete(0, tk.END)
    registro.pack(pady=10)

def regresar():
    registro.pack_forget()
    menu.pack(pady=10)

def registrar_usuario():
    nombre = entrada_nombre.get()
    nip = entrada_nip.get()

    if nombre == "":
        messagebox.showerror("Error", "El nombre no puede estar vacío")
        return

    if nombre in usuarios:
        messagebox.showerror("Error", "El usuario ya existe")
        return

    if len(nip) == 4 and nip.isdigit():
        usuarios[nombre] = {"nip": nip, "saldo": 0, "bloqueado": False}
        guardar_datos()
        messagebox.showinfo("Correcto", "Usuario registrado correctamente")
        entrada_nombre.delete(0, tk.END)
        entrada_nip.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "El NIP debe tener exactamente 4 dígitos")

def mostrar_inicio_sesion():
    menu.pack_forget()
    entrada_usuario.delete(0, tk.END)
    entrada_pin.delete(0, tk.END)
    inicio_sesion.pack(pady=10)

def regresar_inicio_sesion():
    inicio_sesion.pack_forget()
    menu.pack(pady=10)

def verificar_pin():
    nombre = entrada_usuario.get()
    pin = entrada_pin.get()


    if nombre not in usuarios:
        messagebox.showerror("Error", "El usuario no existe")
        return

    if usuarios[nombre]["bloqueado"]:
        messagebox.showerror("Error", "Cuenta bloqueada")
        return

    if nombre not in intentos:
        intentos[nombre] = 0

    if pin == usuarios[nombre]["nip"]:
        intentos[nombre] = 0
        mostrar_cajero(nombre)

    else:
        intentos[nombre] = intentos[nombre] + 1

        if intentos[nombre] >= 3:
            usuarios[nombre]["bloqueado"] = True
            guardar_datos()
            messagebox.showinfo("Error", "Cuenta bloqueada")

        else:
            messagebox.showerror("Error", "NIP incorrecto")
def mostrar_cambiar_nip():
    pantalla_cajero.pack_forget()
    entrada_nip_actual.delete(0, tk.END)
    entrada_nip_nuevo.delete(0, tk.END)
    entrada_nip_confirmar.delete(0, tk.END)
    pantalla_cambiar_nip.pack(pady=10)

def cambiar_nip():
    nombre = entrada_usuario.get().strip()
    actual = entrada_nip_actual.get()
    nuevo = entrada_nip_nuevo.get()
    confirmar = entrada_nip_confirmar.get()

    if actual != usuarios[nombre]["nip"]:
        messagebox.showerror("Error", "El NIP actual es incorrecto")
        return

    if not (len(nuevo) == 4 and nuevo.isdigit()):
        messagebox.showerror("Error", "El NIP nuevo debe tener exactamente 4 dígitos")
        return

    if nuevo == actual:
        messagebox.showerror("Error", "El NIP nuevo debe ser diferente al actual")
        return

    if nuevo != confirmar:
        messagebox.showerror("Error", "La confirmación no coincide con el NIP nuevo")
        return

    usuarios[nombre]["nip"] = nuevo
    guardar_datos()
    messagebox.showinfo("Correcto", "NIP cambiado correctamente")
    regresar_cambiar_nip()

def regresar_cambiar_nip():
    pantalla_cambiar_nip.pack_forget()
    pantalla_cajero.pack(pady=10)

def mostrar_cajero(nombre):
    inicio_sesion.pack_forget()
    etiqueta_bienvenida.config(text=f"Bienvenido {nombre}")
    pantalla_cajero.pack(pady=10)

def cerrar_sesion():
    pantalla_cajero.pack_forget()
    entrada_usuario.delete(0, tk.END)
    entrada_pin.delete(0, tk.END)
    menu.pack(pady=10)

def ver_saldo():
    nombre = entrada_usuario.get()
    saldo = usuarios[nombre]["saldo"]

    messagebox.showinfo("Saldo actual", f"Tu saldo es de ${saldo}")

def mostrar_deposito():
    pantalla_cajero.pack_forget()
    entrada_deposito.delete(0, tk.END)
    pantalla_deposito.pack(pady=10)

def depositar():
    nombre = entrada_usuario.get()
    deposito = float(entrada_deposito.get())

    if deposito > 0:
        usuarios[nombre]["saldo"] = usuarios[nombre]["saldo"] + deposito
        guardar_datos()
        messagebox.showinfo("Correcto", "Depósito realizado")
        entrada_deposito.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Cantidad inválida")

def regresar_deposito():
    pantalla_deposito.pack_forget()
    pantalla_cajero.pack(pady=10)

def mostrar_retiro():
    pantalla_cajero.pack_forget()
    pantalla_retiro.pack(pady=10)

def retirado_hoy(nombre):
    usuario = usuarios[nombre]
    hoy = date.today().isoformat()

    if usuario.get("fecha_retiro") != hoy:
        usuario["fecha_retiro"] = hoy
        usuario["retirado_hoy"] = 0

    return usuario["retirado_hoy"]

def retirar():
    nombre = entrada_usuario.get().strip()

    try:
        retiro = float(entrada_retiro.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa una cantidad válida")
        return

    saldo = usuarios[nombre]["saldo"]
    ya_retirado = retirado_hoy(nombre)
    disponible = LIMITE_RETIRO - ya_retirado

    if retiro <= 0:
        messagebox.showerror("Error", "Cantidad inválida")

    elif retiro > disponible:
        messagebox.showerror(
            "Límite diario",
            f"Hoy has llegado al limite de retiro de ${ya_retirado:,.2f}.\n"
            "Vuelva mañana"
        )

    elif retiro > saldo:
        messagebox.showerror("Error", "Saldo insuficiente")

    else:
        usuarios[nombre]["saldo"] = saldo - retiro
        usuarios[nombre]["retirado_hoy"] = ya_retirado + retiro
        guardar_datos()
        messagebox.showinfo("Correcto", "Retiro realizado")
        entrada_retiro.delete(0, tk.END)

def regresar_retiro():
    pantalla_retiro.pack_forget()
    entrada_retiro.delete(0, tk.END)
    pantalla_cajero.pack(pady=10)

# Menú principal

menu = tk.Frame(ventana)
menu.pack(pady=10)

boton1 = tk.Button(menu, text="Registrar usuario", command = mostrar_registro)
boton1.pack(pady=10)

boton2 = tk.Button(menu, text="Iniciar sesión", command = mostrar_inicio_sesion)
boton2.pack(pady=10)

boton3 = tk.Button(menu, text="Salir", command = ventana.destroy)
boton3.pack(pady=10)

# Pantalla de registro

registro = tk.Frame(ventana)

etiqueta_nombre = tk.Label(registro, text="Nombre de usuario:")
etiqueta_nombre.pack(pady=5)

entrada_nombre = tk.Entry(registro)
entrada_nombre.pack(pady=5)

etiqueta_nip = tk.Label(registro, text="NIP de 4 dígitos:")
etiqueta_nip.pack(pady=5)

entrada_nip = tk.Entry(registro)
entrada_nip.pack(pady=5)

boton_guardar = tk.Button(registro, text="Guardar usuario", command=registrar_usuario)
boton_guardar.pack(pady=10)

boton_volver = tk.Button(registro, text="Regresar", command=regresar)
boton_volver.pack(pady=10)

inicio_sesion = tk.Frame(ventana)

etiqueta_usuario = tk.Label(inicio_sesion, text="Nombre de usuario:")
etiqueta_usuario.pack(pady=5)

entrada_usuario = tk.Entry(inicio_sesion)
entrada_usuario.pack(pady=5)

etiqueta_pin = tk.Label(inicio_sesion, text = "Ingresa tu NIP:")
etiqueta_pin.pack(pady=5)

entrada_pin = tk.Entry(inicio_sesion, show = "*")
entrada_pin.pack(pady=5)

boton_ingresar = tk.Button(inicio_sesion, text="Ingresar", command = verificar_pin)
boton_ingresar.pack(pady=10)

boton_regresar = tk.Button(inicio_sesion, text="Regresar", command=regresar_inicio_sesion)
boton_regresar.pack(pady=10)

# Pantalla del cajero

pantalla_cajero = tk.Frame(ventana)

etiqueta_bienvenida = tk.Label(pantalla_cajero, text="", font=("Arial", 20, "bold"))
etiqueta_bienvenida.pack(pady=10)

boton_saldo = tk.Button(pantalla_cajero, text="Ver saldo", command = ver_saldo)
boton_saldo.pack(pady=10)

boton_depositar = tk.Button(pantalla_cajero, text="Depositar", command = mostrar_deposito)
boton_depositar.pack(pady=10)

boton_retirar = tk.Button(pantalla_cajero, text="Retirar", command = mostrar_retiro)
boton_retirar.pack(pady=10)

boton_cambiar_nip = tk.Button(pantalla_cajero, text="Cambiar NIP", command=mostrar_cambiar_nip)
boton_cambiar_nip.pack(pady=10)

boton_cerrar = tk.Button(pantalla_cajero, text="Cerrar sesión", command = cerrar_sesion)
boton_cerrar.pack(pady=10)

# Pantalla de depósito

pantalla_deposito = tk.Frame(ventana)

etiqueta_deposito = tk.Label(pantalla_deposito, text="¿Cuánto deseas depositar?")
etiqueta_deposito.pack(pady=10)

entrada_deposito = tk.Entry(pantalla_deposito)
entrada_deposito.pack(pady=10)

boton_confirmar = tk.Button(pantalla_deposito, text="Confirmar depósito", command=depositar)
boton_confirmar.pack(pady=10)

boton_regresar_deposito = tk.Button(pantalla_deposito, text="Regresar", command=regresar_deposito)
boton_regresar_deposito.pack(pady=10)

# Pantalla de retiro

pantalla_retiro = tk.Frame(ventana)

etiqueta_retiro = tk.Label(pantalla_retiro, text="¿Cuánto deseas retirar?")
etiqueta_retiro.pack(pady=10)

entrada_retiro = tk.Entry(pantalla_retiro)
entrada_retiro.pack(pady=10)

boton_confirmar_retiro = tk.Button(pantalla_retiro, text="Confirmar retiro", command=retirar)
boton_confirmar_retiro.pack(pady=10)

boton_regresar_retiro = tk.Button(pantalla_retiro, text="Regresar", command=regresar_retiro)
boton_regresar_retiro.pack(pady=10)

# Pantalla de cambio de NIP

pantalla_cambiar_nip = tk.Frame(ventana)

etiqueta_nip_actual = tk.Label(pantalla_cambiar_nip, text="NIP actual:")
etiqueta_nip_actual.pack(pady=5)

entrada_nip_actual = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_actual.pack(pady=5)

etiqueta_nip_nuevo = tk.Label(pantalla_cambiar_nip, text="NIP nuevo (4 dígitos):")
etiqueta_nip_nuevo.pack(pady=5)

entrada_nip_nuevo = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_nuevo.pack(pady=5)

etiqueta_nip_confirmar = tk.Label(pantalla_cambiar_nip, text="Confirma el NIP nuevo:")
etiqueta_nip_confirmar.pack(pady=5)

entrada_nip_confirmar = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_confirmar.pack(pady=5)

boton_guardar_nip = tk.Button(pantalla_cambiar_nip, text="Guardar NIP", command=cambiar_nip)
boton_guardar_nip.pack(pady=10)

boton_regresar_nip = tk.Button(pantalla_cambiar_nip, text="Regresar", command=regresar_cambiar_nip)
boton_regresar_nip.pack(pady=10)

ventana.mainloop()