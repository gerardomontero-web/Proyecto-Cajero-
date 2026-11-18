import json
import os
import math
from datetime import date
from tkinter import messagebox, END

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json")
LIMITE_RETIRO = 10000

# ---------- Datos ----------

def cargar_datos():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"Gerardo": {"nip": "3333", "saldo": 0, "bloqueado": False}}

def guardar_datos(usuarios):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def retirado_hoy(usuarios, nombre):
    usuario = usuarios[nombre]
    hoy = date.today().isoformat()
    if usuario.get("fecha_retiro") != hoy:
        usuario["fecha_retiro"] = hoy
        usuario["retirado_hoy"] = 0
    return usuario["retirado_hoy"]

# ---------- Pantallas ----------

def cambiar_pantalla(destino, pantallas, *entradas):
    for p in pantallas:
        p.pack_forget()
    for e in entradas:
        e.delete(0, END)
    destino.pack(pady=10)

def salir(ventana):
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
        ventana.destroy()

# ---------- Cuentas ----------

def registrar_usuario(usuarios, entrada_nombre, entrada_nip):
    nombre = entrada_nombre.get().strip()
    nip = entrada_nip.get()

    if nombre == "":
        messagebox.showerror("Error", "El nombre no puede estar vacío")
        return
    if nombre in usuarios:
        messagebox.showerror("Error", "El usuario ya existe")
        return
    if not (len(nip) == 4 and nip.isdigit()):
        messagebox.showerror("Error", "El NIP debe tener exactamente 4 dígitos")
        return

    usuarios[nombre] = {"nip": nip, "saldo": 0, "bloqueado": False}
    guardar_datos(usuarios)
    messagebox.showinfo("Correcto", "Usuario registrado correctamente")
    entrada_nombre.delete(0, END)
    entrada_nip.delete(0, END)

def verificar_pin(usuarios, intentos, entrada_usuario, entrada_pin,
                  etiqueta_bienvenida, pantalla_cajero, pantallas):
    nombre = entrada_usuario.get().strip()
    pin = entrada_pin.get()

    if nombre not in usuarios:
        messagebox.showerror("Error", "El usuario no existe")
        return
    if usuarios[nombre]["bloqueado"]:
        messagebox.showerror("Error", "Cuenta bloqueada")
        return

    intentos.setdefault(nombre, 0)

    if pin == usuarios[nombre]["nip"]:
        intentos[nombre] = 0
        etiqueta_bienvenida.config(text=f"Bienvenido {nombre}")
        cambiar_pantalla(pantalla_cajero, pantallas)
    else:
        intentos[nombre] += 1
        if intentos[nombre] >= 3:
            usuarios[nombre]["bloqueado"] = True
            guardar_datos(usuarios)
            messagebox.showerror("Error", "Cuenta bloqueada")
        else:
            messagebox.showerror("Error", "NIP incorrecto")

def cambiar_nip(usuarios, nombre, e_actual, e_nuevo, e_confirmar,
                pantalla_cajero, pantallas):
    actual, nuevo, confirmar = e_actual.get(), e_nuevo.get(), e_confirmar.get()

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
    guardar_datos(usuarios)
    messagebox.showinfo("Correcto", "NIP cambiado correctamente")
    cambiar_pantalla(pantalla_cajero, pantallas)

def eliminar_cuenta(usuarios, intentos, nombre, entrada_nip_eliminar,
                    entrada_usuario, entrada_pin, menu, pantallas):
    if entrada_nip_eliminar.get() != usuarios[nombre]["nip"]:
        messagebox.showerror("Error", "NIP incorrecto")
        return
    if not messagebox.askyesno(
        "Eliminar cuenta",
        "¿Seguro que quieres eliminar tu cuenta?\nEsta acción no se puede deshacer."
    ):
        return

    del usuarios[nombre]
    intentos.pop(nombre, None)
    guardar_datos(usuarios)
    messagebox.showinfo("Cuenta eliminada", "Tu cuenta fue eliminada correctamente")
    cambiar_pantalla(menu, pantallas, entrada_usuario, entrada_pin)

# ---------- Dinero ----------

def ver_saldo(usuarios, nombre):
    saldo = usuarios[nombre]["saldo"]
    messagebox.showinfo("Saldo actual", f"Tu saldo es de ${saldo:,.2f}")

def depositar(usuarios, nombre, entrada_deposito):
    try:
        deposito = float(entrada_deposito.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa una cantidad válida")
        return
    if not math.isfinite(deposito) or deposito <= 0:
        messagebox.showerror("Error", "Cantidad inválida")
        return

    usuarios[nombre]["saldo"] += deposito
    guardar_datos(usuarios)
    messagebox.showinfo("Correcto", "Depósito realizado")
    entrada_deposito.delete(0, END)

def retirar(usuarios, nombre, entrada_retiro):
    try:
        retiro = float(entrada_retiro.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa una cantidad válida")
        return
    if not math.isfinite(retiro) or retiro <= 0:
        messagebox.showerror("Error", "Cantidad inválida")
        return

    saldo = usuarios[nombre]["saldo"]
    ya_retirado = retirado_hoy(usuarios, nombre)
    disponible = LIMITE_RETIRO - ya_retirado

    if retiro > disponible:
        messagebox.showerror(
            "Límite diario",
            f"Hoy has retirado ${ya_retirado:,.2f}.\n"
            f"Solo te quedan ${disponible:,.2f} de tu límite diario de ${LIMITE_RETIRO:,.2f}."
        )
    elif retiro > saldo:
        messagebox.showerror("Error", "Saldo insuficiente")
    else:
        usuarios[nombre]["saldo"] = saldo - retiro
        usuarios[nombre]["retirado_hoy"] = ya_retirado + retiro
        guardar_datos(usuarios)
        messagebox.showinfo("Correcto", "Retiro realizado")
        entrada_retiro.delete(0, END)
