# ventanas/bienvenida.py
import tkinter as tk
from PIL import ImageTk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_LOGO_KUTTERCRAFT
)
from utils.imagenes import cargar_imagen, cargar_imagen_original

class PantallaBienvenida(tk.Frame):
    def __init__(self, master, continuar_callback=None):
        super().__init__(master, bg='black')
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)
        
        self.create_text()
        self.create_button()
        self.bind_events()

    # Crea el texto de bienvenida
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

        # Añadir el logo
        Logo_Kuttercraft = cargar_imagen(RUTA_LOGO_KUTTERCRAFT, 200, 230)#268 x 308
        if Logo_Kuttercraft:
            self.qr_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
            self.qr_canvas.place(x=VENTANA_ANCHO//2 - 100, y=50, width=200, height=230)
            self.qr_canvas.create_image(0, 0, anchor='nw', image=Logo_Kuttercraft)
            self.qr_canvas.image = Logo_Kuttercraft

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
