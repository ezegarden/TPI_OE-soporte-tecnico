import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# ==========================
# BASE DE DATOS SIMULADA
# ==========================

usuarios = [
    {"legajo": "1001", "nombre": "Ana García", "sector": "Administración"},
    {"legajo": "1002", "nombre": "Carlos Ruiz", "sector": "Sistemas"},
    {"legajo": "1003", "nombre": "Laura Méndez", "sector": "Contabilidad"},
    {"legajo": "1004", "nombre": "Martín López", "sector": "RRHH"},
]

categorias = {
    "1": {
        "nombre": "PC no enciende",
        "solucion": "Verificá el cable de alimentación y el tomacorriente."
    },
    "2": {
        "nombre": "Sin acceso a internet",
        "solucion": "Reiniciá el router y verificá la conexión."
    },
    "3": {
        "nombre": "Olvidé mi contraseña",
        "solucion": "Tu contraseña fue restablecida a Temp1234!"
    },
    "4": {
        "nombre": "Impresora no imprime",
        "solucion": "Verificá conexión y cola de impresión."
    },
    "5": {
        "nombre": "Error en ERP",
        "solucion": None
    },
    "6": {
        "nombre": "Otro problema",
        "solucion": None
    }
}

tickets = []

# ==========================
# ESTADO DEL BOT
# ==========================

estado = {
    "paso": "IDENTIFICACION",
    "intentos": 0,
    "usuario": None,
    "categoria": None,
    "ticket": None
}

# ==========================
# FUNCIONES
# ==========================

def generar_ticket():
    return "TKT-" + datetime.now().strftime("%H%M%S")

def escribir_bot(texto):
    chat.insert(tk.END, f"🤖 TechBot: {texto}\n\n")
    chat.see(tk.END)

def escribir_usuario(texto):
    chat.insert(tk.END, f"👤 Usuario: {texto}\n")
    chat.see(tk.END)

def mostrar_categorias():

    texto = """
Seleccioná una categoría:

1 - PC no enciende
2 - Sin acceso a internet
3 - Olvidé mi contraseña
4 - Impresora no imprime
5 - Error en ERP
6 - Otro problema
"""

    escribir_bot(texto)

def escalar_ticket():

    ticket = generar_ticket()

    tickets.append({
        "id": ticket,
        "estado": "ESCALADO"
    })

    estado["ticket"] = ticket
    estado["paso"] = "FIN"

    escribir_bot(
        f"No encontré solución automática.\n"
        f"Ticket generado: {ticket}\n"
        f"Derivado a soporte técnico nivel 2."
    )

def procesar(mensaje):

    mensaje = mensaje.strip()

    # =====================
    # IDENTIFICACION
    # =====================

    if estado["paso"] == "IDENTIFICACION":

        usuario = None

        for u in usuarios:
            if mensaje == u["legajo"] or mensaje.lower() == u["nombre"].lower():
                usuario = u
                break

        if usuario:

            estado["usuario"] = usuario
            estado["paso"] = "CLASIFICACION"

            escribir_bot(
                f"Bienvenido {usuario['nombre']} "
                f"({usuario['sector']})"
            )

            mostrar_categorias()

        else:

            estado["intentos"] += 1

            if estado["intentos"] >= 3:

                estado["paso"] = "FIN"

                escribir_bot(
                    "Acceso bloqueado.\n"
                    "Superaste los 3 intentos."
                )

            else:

                escribir_bot(
                    f"Usuario no encontrado.\n"
                    f"Intento {estado['intentos']}/3"
                )

    # =====================
    # CLASIFICACION
    # =====================

    elif estado["paso"] == "CLASIFICACION":

        if mensaje not in categorias:

            escribir_bot("Ingresá una opción válida.")

            return

        categoria = categorias[mensaje]

        estado["categoria"] = categoria

        if categoria["solucion"]:

            estado["paso"] = "SOLUCION"

            escribir_bot(
                f"Problema: {categoria['nombre']}\n\n"
                f"Solución:\n{categoria['solucion']}"
            )

            escribir_bot(
                "¿Se resolvió?\n"
                "Escribí SI o NO"
            )

        else:

            escalar_ticket()

    # =====================
    # SOLUCION
    # =====================

    elif estado["paso"] == "SOLUCION":

        respuesta = mensaje.upper()

        if respuesta == "SI":

            ticket = generar_ticket()

            tickets.append({
                "id": ticket,
                "estado": "RESUELTO"
            })

            estado["ticket"] = ticket
            estado["paso"] = "FIN"

            escribir_bot(
                f"Perfecto.\n"
                f"Ticket {ticket} registrado como RESUELTO."
            )

        elif respuesta == "NO":

            escalar_ticket()

        else:

            escribir_bot("Respondé únicamente SI o NO.")

    # =====================
    # FIN
    # =====================

    elif estado["paso"] == "FIN":

        escribir_bot(
            "El proceso ya finalizó.\n"
            "Reiniciá la aplicación para comenzar nuevamente."
        )

# ==========================
# EVENTO BOTON
# ==========================

def enviar():

    mensaje = entrada.get()

    if mensaje == "":
        return

    escribir_usuario(mensaje)

    entrada.delete(0, tk.END)

    procesar(mensaje)

# ==========================
# INTERFAZ
# ==========================

ventana = tk.Tk()
ventana.title("TechBot - Soporte Técnico")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="TechBot - Soporte Técnico Nivel 1",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=10)

chat = scrolledtext.ScrolledText(
    ventana,
    width=90,
    height=25,
    font=("Consolas", 10)
)
chat.pack(padx=10, pady=10)

entrada = tk.Entry(
    ventana,
    width=70,
    font=("Arial", 12)
)
entrada.pack(side=tk.LEFT, padx=10, pady=10)

boton = tk.Button(
    ventana,
    text="Enviar",
    command=enviar
)
boton.pack(side=tk.LEFT)

escribir_bot(
    "Hola. Soy TechBot.\n\n"
    "Ingresá tu legajo o nombre completo."
)

ventana.mainloop()