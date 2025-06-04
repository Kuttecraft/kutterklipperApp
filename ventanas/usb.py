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

        self.main_canvas = None
        self.boton_usb = None

        self.int_texto = self.create_text()

        self.boton_usb = crear_boton(
            self, 
            RUTA_BOTON, 
            "Buscar Puerto USB", 
            276, 410,
            command=lambda: self.detectar_puerto_usb()
        )

        self.bind_events()

    def limpiar_canvas(self):
        try:
            self.main_canvas.destroy()
        except AttributeError:
            pass
        self.main_canvas = None

    def limpiar_boton_usb(self):
        try:
            self.boton_usb.destroy()
        except AttributeError:
            pass
        self.boton_usb = None

    def seleccionar_opcion(self, clave, valor):
        self.respuestas[clave] = valor
        self.continuar_callback()

    def create_text(self):
        self.limpiar_canvas()
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="Se buscará el puerto USB de la impresora.\nDebe ser la única máquina conectada.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def create_text_no_hay_usb(self):
        self.limpiar_canvas()
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="No se pudo acceder al directorio.\n¿Está conectado el dispositivo USB?",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def create_text_hay_usb(self):
        self.limpiar_canvas()
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="¡Perfecto!\nSe ha detectado USB",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        ) 

    def detectar_puerto_usb(self):
        ruta = "/dev/serial/by-id/"
    
        try:
            resultado = subprocess.check_output(['ls', ruta], stderr=subprocess.STDOUT).decode().strip()
            dispositivos = resultado.split('\n') if resultado else []

            if dispositivos:
                print("🔌 Dispositivo(s) detectado(s):")
                for dispositivo in dispositivos:
                    print(f"- {os.path.join(ruta, dispositivo)}")
                
                self.limpiar_boton_usb()
                self.int_texto.destroy()

                self.create_text_hay_usb()

                self.boton_usb = crear_boton(
                    self, 
                    RUTA_BOTON, 
                    "Siguiente", 
                    276, 410,
                    command=lambda: self.seleccionar_opcion("USB", os.path.join(ruta, dispositivo))
                )
            else:
                print("⚠️ No se encontraron dispositivos USB en:", ruta)

        except subprocess.CalledProcessError:
            self.int_texto.destroy()
            self.limpiar_boton_usb()
            self.create_text_no_hay_usb()

            self.boton_usb = crear_boton(
                self, 
                RUTA_BOTON, 
                "Buscar Puerto USB", 
                276, 410,
                command=lambda: self.detectar_puerto_usb()
            )
            print("No se pudo acceder al directorio. ¿Está conectado el dispositivo USB?")

        except FileNotFoundError:
            print("❌ El sistema no tiene el comando 'ls' disponible (muy raro en sistemas Linux).")

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())
