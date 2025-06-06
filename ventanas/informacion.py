# ventanas/informacion.py
import tkinter as tk
from PIL import ImageTk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_QR
)
from utils.imagenes import cargar_imagen, cargar_imagen_original

class PantallaInformacion(tk.Frame):
    def __init__(self, master, continuar_callback=None):
        super().__init__(master, bg='black')
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()
        self.create_button()
        self.bind_events()

    def create_text(self):
        self.label = tk.Label(
            self,
            text="Lo primero que le recomendamos es ver\nlos tutoriales disponibles en nuestra página web.\nPuede acceder escaneando el código QR.",
            font=('Montserrat', 22, 'bold'),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            justify='center'
        )
    
        self.label.place(x=0, y=250, width=VENTANA_ANCHO, height=150)
    
        # Añadir imagen del QR usando Canvas
        qr_image = cargar_imagen(RUTA_IMAGEN_QR, 200, 200)
        if qr_image:
            self.qr_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
            self.qr_canvas.place(x=VENTANA_ANCHO//2 - 100, y=50, width=200, height=200)
            self.qr_canvas.create_image(0, 0, anchor='nw', image=qr_image)
            self.qr_canvas.image = qr_image

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
                y=410,
                width=self.button_image.width(),
                height=self.button_image.height()
            )

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())