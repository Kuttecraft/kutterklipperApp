# ventanas/usb.py
import tkinter as tk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

import os
import subprocess

class PantallaUSB(tk.Frame):
    def __init__(self, master, respuestas, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()

        self.boton_usb = crear_boton(
            self, 
            RUTA_BOTON, 
            "Buscar Puerto USB", 
            276, 410,
            command=lambda: self.detectar_puerto_usb() # self.seleccionar_opcion("skr", "usb")
        )

        self.bind_events()

    def seleccionar_opcion(self, clave, valor):
        self.respuestas[clave] = valor
        self.continuar_callback()

    def create_text(self):
        # Crear un Canvas que abarque toda la ventana
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        # Añadir la imagen de la impresora 3D
        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        # Añadir el texto sobre la imagen
        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="Se buscará el puerto USB de la impresora.\nDebe ser la única máquina conectada.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def create_text_no_hay_usb(self):
        # Crear un Canvas que abarque toda la ventana
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        # Añadir la imagen de la impresora 3D
        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        # Añadir el texto sobre la imagen
        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="❌ No se pudo acceder al directorio.\n¿Está conectado el dispositivo USB?",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        ) 

    def detectar_puerto_usb(self):
        ruta = "/dev/serial/by-id/"
    
        try:
            # Ejecuta el comando y captura la salida
            resultado = subprocess.check_output(['ls', ruta], stderr=subprocess.STDOUT).decode().strip()
            dispositivos = resultado.split('\n') if resultado else []

            if dispositivos:
                self.boton_usb.destroy()
                print("🔌 Dispositivo(s) detectado(s):")
                for dispositivo in dispositivos:
                    print(f"- {os.path.join(ruta, dispositivo)}")

                self.boton_usb = crear_boton(
                    self, 
                    RUTA_BOTON, 
                    "Siguiente", 
                    276, 410,
                    command=lambda: self.seleccionar_opcion("USB", dispositivo)
                )
            else:
                print("⚠️ No se encontraron dispositivos USB en:", ruta)

        except subprocess.CalledProcessError:
            self.create_text.destroy()
            self.create_text_no_hay_usb()
            print("❌ No se pudo acceder al directorio. ¿Está conectado el dispositivo USB?")
        except FileNotFoundError:
            print("❌ El sistema no tiene el comando 'ls' disponible (muy raro en sistemas Linux).")

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())
