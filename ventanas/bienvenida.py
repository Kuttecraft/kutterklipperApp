# ventanas/bienvenida.py
import tkinter as tk
from PIL import ImageTk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON
)
from utils.imagenes import cargar_imagen, cargar_imagen_original

class PantallaBienvenida(tk.Frame):
    def __init__(self, master, continuar_callback=None):
        super().__init__(master, bg='black')
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.load_background()
        self.create_text()
        self.create_button()
        self.bind_events()

    def load_background(self):
        fondo = cargar_imagen(RUTA_IMAGEN_FONDO, VENTANA_ANCHO, VENTANA_ALTO)
        if fondo:
            self.bg_label = tk.Label(self, image=fondo, bg='black')
            self.bg_label.image = fondo
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_text(self):
        self.label = tk.Label(
            self,
            text="¡Te damos la bienvenida a KutterKlipper!",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            justify='center'
        )
        self.label.place(x=0, y=310, width=VENTANA_ANCHO, height=50)

    def create_button(self):
        img_orig = cargar_imagen_original(RUTA_BOTON)
        if img_orig:
            self.button_image = ImageTk.PhotoImage(img_orig)
            self.button = tk.Button(
                self,
                image=self.button_image,
                text="CONTINUAR",
                font=('Montserrat', 16, 'bold'),
                fg='white',
                activeforeground='white',
                activebackground='white',
                compound='center',
                borderwidth=0,
                highlightthickness=0,
                command=self.continuar_callback
            )
            self.button.place(
                x=275,
                y=387,
                width=self.button_image.width(),
                height=self.button_image.height()
            )

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.cerrar_callback())
