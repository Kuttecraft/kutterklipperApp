# ventanas/varillas.py
import tkinter as tk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaVarillas(tk.Frame):
    def __init__(self, master, respuestas=None, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()

        crear_boton(
            self, 
            RUTA_BOTON, 
            "8mm", 
            108, 410, 
            command=lambda: self.seleccionar_opcion("Varilla", "8")
        )

        crear_boton(
            self,
            RUTA_BOTON,
            "4mm",
            442, 410,
            command=lambda: self.seleccionar_opcion("Varilla", "4")
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
        impresora_3d = cargar_imagen("./recursos/varilla.png", 736, 260)
        if impresora_3d:
            self.main_canvas.create_image(32, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        # Añadir el texto sobre la imagen
        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="¿Que tipo de varillas tienes\n8mm: 4 líneas | 4mm: 2 líneas?",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())
