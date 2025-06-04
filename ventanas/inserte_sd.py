# ventanas/inserte_sd.py
import tkinter as tk
from PIL import ImageTk
import sys
import io

from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original


class TextRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', message)
        self.text_widget.see('end')  # Auto-scroll
        self.text_widget.config(state='disabled')

    def flush(self):
        pass


class PantallaInserteSD(tk.Frame):
    def __init__(self, master, continuar_callback=None):
        super().__init__(master, bg='black')
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()
        self.create_button_aceptar()
        self.create_button_omitir()
        self.create_console_output()
        self.bind_events()

        # Redirigir stdout y stderr a la consola gráfica
        sys.stdout = TextRedirector(self.console_text)
        sys.stderr = TextRedirector(self.console_text)

        print("Esperando confirmación de tarjeta SD insertada.")

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
            VENTANA_ANCHO // 2,  # Posición X centrada
            350,  # Posición Y
            text="Inserte el SD Card de la impresora",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def create_button_aceptar(self):
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
                x=442,
                y=410,
                width=self.button_image.width(),
                height=self.button_image.height()
            )

    def create_button_omitir(self):
        img_orig = cargar_imagen_original(RUTA_BOTON)
        if img_orig:
            self.button_image_omitir = ImageTk.PhotoImage(img_orig)
            self.button_omitir = tk.Button(
                self,
                image=self.button_image_omitir,
                text="OMITIR",
                font=('Montserrat', 16, 'bold'),
                fg='white',
                activeforeground='white',
                activebackground='white',
                compound='center',
                borderwidth=0,
                highlightthickness=0,
                command=self.master.quit
            )
            self.button_omitir.image = self.button_image_omitir  # Mantener referencia a la imagen
            self.button_omitir.place(
                x=108,
                y=410,
                width=self.button_image_omitir.width(),
                height=self.button_image_omitir.height()
            )

    def create_console_output(self):
        self.console_text = tk.Text(
            self,
            bg='black',
            fg='white',
            font=('Courier', 11),
            width=100,   # 800 / 8 = 100 caracteres aprox
            height=12    # 200 / 16 px = 12 líneas aprox
        )
        self.console_text.place(x=0, y=VENTANA_ALTO - 300, width=800, height=200)
        self.console_text.config(state='disabled')

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())
