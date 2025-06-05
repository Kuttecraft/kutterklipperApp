# ventanas/final.py
import tkinter as tk
from PIL import ImageTk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaFinal(tk.Frame):
    def __init__(self, master, respuestas=None, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()
        self.imprimir_respuestas()
        crear_boton(
            self, 
            RUTA_BOTON, 
            "Salir", 
            276, 410,
            command=self.master.quit
        )
        self.bind_events()

    def imprimir_respuestas(self):
        print(self.respuestas)

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
            text="Perfecto, ya se creó un archivo printer.cfg\ncon los valores de la impresora.Ahora solo queda\nreiniciar el firmware para poder probar la máquina.",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        ) 

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())