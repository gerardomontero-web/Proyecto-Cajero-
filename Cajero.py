import tkinter as tk
import Funciones as F
usuarios = F.cargar_datos()
intentos = {}

ventana = tk.Tk()
ventana.title("Cajero automático")
ventana.geometry("400x500")

etiqueta = tk.Label(ventana, text="CAJERO AUTOMÁTICO", font=("Arial", 18,))
etiqueta.pack(pady=20)

# ---------- Frames (pantallas) ----------

menu = tk.Frame(ventana)
menu.pack(pady=10)

registro = tk.Frame(ventana)
inicio_sesion = tk.Frame(ventana)
pantalla_cajero = tk.Frame(ventana)
pantalla_deposito = tk.Frame(ventana)
pantalla_retiro = tk.Frame(ventana)
pantalla_cambiar_nip = tk.Frame(ventana)
pantalla_eliminar = tk.Frame(ventana)

# ---------- Etiquetas y cajas de texto ----------

# Registro
tk.Label(registro, text="Nombre de usuario:").pack(pady=5)
entrada_nombre = tk.Entry(registro)
entrada_nombre.pack(pady=5)
tk.Label(registro, text="NIP de 4 dígitos:").pack(pady=5)
entrada_nip = tk.Entry(registro, show="*")
entrada_nip.pack(pady=5)

# Inicio de sesión
tk.Label(inicio_sesion, text="Nombre de usuario:").pack(pady=5)
entrada_usuario = tk.Entry(inicio_sesion)
entrada_usuario.pack(pady=5)
tk.Label(inicio_sesion, text="Ingresa tu NIP:").pack(pady=5)
entrada_pin = tk.Entry(inicio_sesion, show="*")
entrada_pin.pack(pady=5)

# Pantalla del cajero
etiqueta_bienvenida = tk.Label(pantalla_cajero, text="", font=("Arial", 20, "bold"))
etiqueta_bienvenida.pack(pady=10)

# Depósito
tk.Label(pantalla_deposito, text="¿Cuánto deseas depositar?").pack(pady=10)
entrada_deposito = tk.Entry(pantalla_deposito)
entrada_deposito.pack(pady=10)

# Retiro
tk.Label(pantalla_retiro, text="¿Cuánto deseas retirar?").pack(pady=10)
entrada_retiro = tk.Entry(pantalla_retiro)
entrada_retiro.pack(pady=10)

# Cambiar NIP
tk.Label(pantalla_cambiar_nip, text="NIP actual:").pack(pady=5)
entrada_nip_actual = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_actual.pack(pady=5)
tk.Label(pantalla_cambiar_nip, text="NIP nuevo (4 dígitos):").pack(pady=5)
entrada_nip_nuevo = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_nuevo.pack(pady=5)
tk.Label(pantalla_cambiar_nip, text="Confirma el NIP nuevo:").pack(pady=5)
entrada_nip_confirmar = tk.Entry(pantalla_cambiar_nip, show="*")
entrada_nip_confirmar.pack(pady=5)

# Eliminar cuenta
tk.Label(pantalla_eliminar, text="Ingresa tu NIP para eliminar tu cuenta:").pack(pady=10)
entrada_nip_eliminar = tk.Entry(pantalla_eliminar, show="*")
entrada_nip_eliminar.pack(pady=10)

# Menú principal
boton1 = tk.Button(menu, text="Registrar usuario",
    command=lambda: F.cambiar_pantalla(registro, pantallas, entrada_nombre, entrada_nip))
boton1.pack(pady=10)
boton2 = tk.Button(menu, text="Iniciar sesión",
    command=lambda: F.cambiar_pantalla(inicio_sesion, pantallas, entrada_usuario, entrada_pin))
boton2.pack(pady=10)
boton3 = tk.Button(menu, text="Salir", command=lambda: F.salir(ventana))
boton3.pack(pady=10)

# Registro
boton_guardar = tk.Button(registro, text="Guardar usuario",
    command=lambda: F.registrar_usuario(usuarios, entrada_nombre, entrada_nip))
boton_guardar.pack(pady=10)
boton_volver = tk.Button(registro, text="Regresar",
    command=lambda: F.cambiar_pantalla(menu, pantallas))
boton_volver.pack(pady=10)

# Inicio de sesión
boton_ingresar = tk.Button(inicio_sesion, text="Ingresar",
    command=lambda: F.verificar_pin(usuarios, intentos, entrada_usuario, entrada_pin,
                                    etiqueta_bienvenida, pantalla_cajero, pantallas))
boton_ingresar.pack(pady=10)
boton_regresar = tk.Button(inicio_sesion, text="Regresar",
    command=lambda: F.cambiar_pantalla(menu, pantallas))
boton_regresar.pack(pady=10)

# Pantalla del cajero
boton_saldo = tk.Button(pantalla_cajero, text="Ver saldo",
    command=lambda: F.ver_saldo(usuarios, entrada_usuario.get().strip()))
boton_saldo.pack(pady=10)

boton_depositar = tk.Button(pantalla_cajero, text="Depositar",
    command=lambda: F.cambiar_pantalla(pantalla_deposito, pantallas, entrada_deposito))
boton_depositar.pack(pady=10)

boton_retirar = tk.Button(pantalla_cajero, text="Retirar",
    command=lambda: F.cambiar_pantalla(pantalla_retiro, pantallas, entrada_retiro))
boton_retirar.pack(pady=10)

boton_cambiar_nip = tk.Button(pantalla_cajero, text="Cambiar NIP",
    command=lambda: F.cambiar_pantalla(pantalla_cambiar_nip, pantallas,
                                        entrada_nip_actual, entrada_nip_nuevo, entrada_nip_confirmar))
boton_cambiar_nip.pack(pady=10)
boton_eliminar = tk.Button(pantalla_cajero, text="Eliminar cuenta",
    command=lambda: F.cambiar_pantalla(pantalla_eliminar, pantallas, entrada_nip_eliminar))
boton_eliminar.pack(pady=10)
boton_cerrar = tk.Button(pantalla_cajero, text="Cerrar sesión",
    command=lambda: F.cambiar_pantalla(menu, pantallas, entrada_usuario, entrada_pin))
boton_cerrar.pack(pady=10)

# Depósito
boton_confirmar = tk.Button(pantalla_deposito, text="Confirmar depósito",
    command=lambda: F.depositar(usuarios, entrada_usuario.get().strip(), entrada_deposito))
boton_confirmar.pack(pady=10)

boton_regresar_deposito = tk.Button(pantalla_deposito, text="Regresar",
    command=lambda: F.cambiar_pantalla(pantalla_cajero, pantallas))
boton_regresar_deposito.pack(pady=10)

# Retiro
boton_confirmar_retiro = tk.Button(pantalla_retiro, text="Confirmar retiro",
    command=lambda: F.retirar(usuarios, entrada_usuario.get().strip(), entrada_retiro))
boton_confirmar_retiro.pack(pady=10)

boton_regresar_retiro = tk.Button(pantalla_retiro, text="Regresar",
    command=lambda: F.cambiar_pantalla(pantalla_cajero, pantallas))
boton_regresar_retiro.pack(pady=10)

# Cambiar NIP
boton_guardar_nip = tk.Button(pantalla_cambiar_nip, text="Guardar NIP",
    command=lambda: F.cambiar_nip(usuarios, entrada_usuario.get().strip(),
                                  entrada_nip_actual, entrada_nip_nuevo, entrada_nip_confirmar,
                                  pantalla_cajero, pantallas))
boton_guardar_nip.pack(pady=10)

boton_regresar_nip = tk.Button(pantalla_cambiar_nip, text="Regresar",
    command=lambda: F.cambiar_pantalla(pantalla_cajero, pantallas))
boton_regresar_nip.pack(pady=10)

# Eliminar cuenta
boton_confirmar_eliminar = tk.Button(pantalla_eliminar, text="Eliminar cuenta",
    command=lambda: F.eliminar_cuenta(usuarios, intentos, entrada_usuario.get().strip(),
                                      entrada_nip_eliminar, entrada_usuario, entrada_pin,
                                      menu, pantallas))
boton_regresar_nip.pack(pady=10)

boton_regresar_eliminar = tk.Button(pantalla_eliminar, text="Regresar",
    command=lambda: F.cambiar_pantalla(pantalla_cajero, pantallas))
boton_regresar_eliminar.pack(pady=10)

pantallas = [menu, registro, inicio_sesion, pantalla_cajero,
             pantalla_deposito, pantalla_retiro,
             pantalla_cambiar_nip, pantalla_eliminar]

ventana.mainloop()
