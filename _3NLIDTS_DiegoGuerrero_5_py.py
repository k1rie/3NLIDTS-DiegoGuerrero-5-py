#Formulario de registro con validación (versión mejorada con IA)
import os
import re
import tkinter as tk
from tkinter import messagebox

# Carpeta Documentos del usuario actual (ya no depende de desde dónde se ejecute el script)
CARPETA_DESTINO = os.path.join(os.path.expanduser("~"), "Documents", "Programacion Avanzada")
ARCHIVO_DESTINO = os.path.join(CARPETA_DESTINO, "Datos3N_11Oct26_IA.txt")

# Reglas de validación en un solo lugar
EDAD_MINIMA, EDAD_MAXIMA = 1, 120
ESTATURA_MINIMA, ESTATURA_MAXIMA = 50, 250   # centímetros
# Letras (incluye acentos y ñ) separadas por un solo espacio, apóstrofo o guion
PATRON_TEXTO = re.compile(r"[^\W\d_]+(?:[ '\-][^\W\d_]+)*")
PATRON_TELEFONO = re.compile(r"[0-9]{10}")
PATRON_ESTATURA = re.compile(r"[0-9]{2,3}(?:[.,][0-9]{1,2})?")
COLOR_OK = "white"
COLOR_ERROR = "#FFB3B3"

# Cada validador solo revisa el dato y devuelve el mensaje de error (o None). No abre ventanas.
def validar_texto(valor, campo):
    valor = valor.strip()
    if not valor:
        return campo + ": campo obligatorio."
    if not PATRON_TEXTO.fullmatch(valor):
        return campo + ": solo letras, espacios, apóstrofo o guion."
    return None

def validar_telefono(valor):
    if not PATRON_TELEFONO.fullmatch(valor.strip()):
        return "Teléfono: exactamente 10 dígitos."
    return None

def validar_edad(valor):
    valor = valor.strip()
    if not re.fullmatch(r"[0-9]{1,3}", valor) or not (EDAD_MINIMA <= int(valor) <= EDAD_MAXIMA):
        return "Edad: número entero entre %d y %d." % (EDAD_MINIMA, EDAD_MAXIMA)
    return None

def validar_estatura(valor):
    valor = valor.strip()
    if not PATRON_ESTATURA.fullmatch(valor) or not (ESTATURA_MINIMA <= float(valor.replace(",", ".")) <= ESTATURA_MAXIMA):
        return "Estatura: centímetros entre %d y %d (ej. 167 o 167.5)." % (ESTATURA_MINIMA, ESTATURA_MAXIMA)
    return None

def validar_genero(genero_id):
    if genero_id not in (1, 2, 3):
        return "Género: seleccione una opción."
    return None

def solo_digitos(texto_nuevo, maximo):
    # Teléfono y edad solo aceptan dígitos al escribir
    return texto_nuevo == "" or (texto_nuevo.isascii() and texto_nuevo.isdigit() and len(texto_nuevo) <= int(maximo))

def marcar(entrada, error):
    entrada.config(bg=COLOR_ERROR if error else COLOR_OK)
    return error

def borrar():
    for entrada in (tbNombre, tbApellidos, tbEdad, tbEstatura, tbTelefono):
        entrada.delete(0, tk.END)
        entrada.config(bg=COLOR_OK)
    rbSeleccionGenero.set(0)
    tbNombre.focus_set()

def guardar():
    # Se revisan todos los campos para marcar en rojo cada uno que falle
    errores = [marcar(entrada, validar()) for entrada, validar in VALIDADORES]
    errores.append(validar_genero(rbSeleccionGenero.get()))
    errores = [error for error in errores if error]
    if errores:
        messagebox.showwarning("Datos incompletos",
                               "Corrija los siguientes datos antes de guardar:\n\n" + "\n".join("- " + e for e in errores))
        return

    nombres = tbNombre.get().strip()
    apellidos = tbApellidos.get().strip()
    edad = tbEdad.get().strip()
    estatura = tbEstatura.get().strip()
    tel = tbTelefono.get().strip()
    genero = {1: "Masculino", 2: "Femenino", 3: "No Definido"}[rbSeleccionGenero.get()]
    datos = "\n".join([
        "Nombre : " + nombres,
        "Apellidos : " + apellidos,
        "Edad : " + edad,
        "Telefono : " + tel,
        "Estatura : " + estatura,
        "Genero : " + genero,
    ])
    try:
        os.makedirs(CARPETA_DESTINO, exist_ok=True)
        with open(ARCHIVO_DESTINO, "a", encoding="utf-8") as archivo:
            archivo.write(datos + "\n\n")
    except OSError as error:
        messagebox.showerror("Error al guardar", "No se pudo escribir el archivo:\n" + str(error))
        return
    messagebox.showinfo("Informacion", "Datos guardados correctamente \n" + datos)
    borrar()


ventana = tk.Tk()
ventana.configure(bg="pink")
ventana.geometry("350x550")
ventana.resizable(False, False)
ventana.title("Actividad 05.1 - Validación de Formulario Vr. 002 (IA) - Diego Enrique González Guerrero")
rbSeleccionGenero = tk.IntVar()
vcmd_edad = (ventana.register(solo_digitos), "%P", "3")
vcmd_telefono = (ventana.register(solo_digitos), "%P", "10")
tk.Label(ventana, text="Nombre : " , font=("Segoe UI",14,"bold")).pack(padx=10, pady=8)
tbNombre = tk.Entry(ventana, width=35,justify="center")
tbNombre.pack()
tk.Label(ventana, text="Apellidos : " , font=("Segoe UI",14,"bold")).pack(padx=10, pady=8)
tbApellidos = tk.Entry(ventana, width=35,justify="center")
tbApellidos.pack()
tk.Label(ventana, text="Edad : " , font=("Segoe UI",14,"bold")).pack(padx=10, pady=8)
tbEdad = tk.Entry(ventana, width=10,justify="center", validate="key", validatecommand=vcmd_edad)
tbEdad.pack()
tk.Label(ventana, text="Estatura : " , font=("Segoe UI",14,"bold")).pack(padx=10, pady=8)
tbEstatura = tk.Entry(ventana, width=15,justify="center")
tbEstatura.pack()
tk.Label(ventana, text="Telefono : " , font=("Segoe UI",14,"bold")).pack(padx=10, pady=8)
tbTelefono = tk.Entry(ventana, width=35,justify="center", validate="key", validatecommand=vcmd_telefono)
tbTelefono.pack()
gb = tk.LabelFrame(ventana, text="Selecione un Genero : ", padx=10, pady=8)
gb.pack(padx=10, pady=8)
rbMasculino = tk.Radiobutton(gb, text="Masculino", value=1,variable=rbSeleccionGenero)
rbMasculino.grid(column=1,row=1)
rbFemenino = tk.Radiobutton(gb, text="Femenino", value=2,variable=rbSeleccionGenero)
rbFemenino.grid(column=2,row=1)
rbNoDefinido = tk.Radiobutton(gb, text="No Definido", value=3,variable=rbSeleccionGenero)
rbNoDefinido.grid(column=3,row=1)
gb2 = tk.LabelFrame(ventana, text="")
gb2.pack(padx=10, pady=8)
btnBorrar = tk.Button(gb2, text="Borrar", width=10 , padx=10, pady=8, command=borrar)
btnBorrar.grid(column=2, row=1)
btnGuardar = tk.Button(gb2, text="Guardar", width=10,padx=10, pady=8, command= guardar)
btnGuardar.grid(column=1, row=1)

# Cada campo se valida al perder el foco (se marca en rojo) y de nuevo al pulsar Guardar
VALIDADORES = [
    (tbNombre, lambda: validar_texto(tbNombre.get(), "Nombre")),
    (tbApellidos, lambda: validar_texto(tbApellidos.get(), "Apellidos")),
    (tbTelefono, lambda: validar_telefono(tbTelefono.get())),
    (tbEdad, lambda: validar_edad(tbEdad.get())),
    (tbEstatura, lambda: validar_estatura(tbEstatura.get())),
]
for entrada, validar in VALIDADORES:
    entrada.bind("<FocusOut>", lambda evento, e=entrada, v=validar: marcar(e, v()))
ventana.mainloop()
