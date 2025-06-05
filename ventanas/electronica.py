# ventanas/electronica.py
import tkinter as tk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaElectronica(tk.Frame):
    def __init__(self, master, respuestas=None, continuar_32bits=None, continuar_8bits=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas or {}
        self.pack(fill='both', expand=True)
        self.continuar_32bits = continuar_32bits
        self.continuar_8bits = continuar_8bits

        self.create_text()

        crear_boton(
            self,
            RUTA_BOTON,
            "8 Bits (Arduino)",
            108, 410,
            command=lambda: self.seleccionar_opcion("Tipo", "8_Bits")
        )

        crear_boton(
            self,
            RUTA_BOTON,
            "32 Bits (SKR)",
            442, 410,
            command=lambda: self.seleccionar_opcion("Tipo", "32_Bits")
        )

        self.bind_events()

    def seleccionar_opcion(self, clave, valor):
        self.respuestas[clave] = valor
        if valor == "32_Bits" and self.continuar_32bits:
            self.continuar_32bits()
        elif valor == "8_Bits" and self.continuar_8bits:
            self.continuar_8bits()


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
            text="¿Que tipo de electronica tiene tu impresora?",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())
