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
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton


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
    def __init__(self, master, respuestas, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()
        self.create_console_output()
        self.bind_events()

        # Redirigir stdout y stderr a la consola gráfica
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = TextRedirector(self.console_text)
        sys.stderr = TextRedirector(self.console_text)

        print(
            "Inserte una tarjeta SD vacía en el KutterKlipper.\n"
            "Esta tarjeta se usará para grabar el archivo de actualización\n"
            "\"firmware.bin\" para poder grabarlo después en la impresora.\n"
            "Una vez insertada, presione el botón 'Continuar' en la pantalla."
            )

        # Crear el botón después de que todo esté inicializado
        self.boton_sd_info = crear_boton(
            self, 
            RUTA_BOTON, 
            "CONTINUAR", 
            276, 410,
            command=self.continuar
        )

    def continuar(self):
        # Primero restaurar la salida estándar
        if hasattr(self, 'original_stdout'):
            sys.stdout = self.original_stdout
            del self.original_stdout
        
        if hasattr(self, 'original_stderr'):
            sys.stderr = self.original_stderr
            del self.original_stderr
        
        # Luego destruir los widgets
        if hasattr(self, 'console_text'):
            self.console_text.destroy()
            del self.console_text
        
        if hasattr(self, 'main_canvas'):
            self.main_canvas.destroy()
            del self.main_canvas
        
        # Finalmente destruir la pantalla
        self.destroy()
        
        # Continuar a la siguiente pantalla
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
            VENTANA_ANCHO // 2,  # Posición X centrada
            350,  # Posición Y
            text="Inserte el SD Card de la impresora",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )

    def create_console_output(self):
        self.console_text = tk.Text(
            self,
            bg='black',
            fg='white',
            font=('Courier', 11),
            width=100,   # 800 / 8 = 100 caracteres aprox
            height=6    # 200 / 16 px = 12 líneas aprox
        )
        self.console_text.place(x=100, y=VENTANA_ALTO - 200, width=600, height=100)
        self.console_text.config(state='disabled')
        
    def bind_events(self):
        self.bind_all('<Escape>', self.limpiar_y_salir)

    def limpiar_redireccion(self):
        if hasattr(self, 'original_stdout'):
            sys.stdout = self.original_stdout
            del self.original_stdout
        
        if hasattr(self, 'original_stderr'):
            sys.stderr = self.original_stderr
            del self.original_stderr

    def limpiar_widgets(self):
        # Destruir el widget de texto
        if hasattr(self, 'console_text'):
            self.console_text.destroy()
            del self.console_text
        
        # Destruir el canvas
        if hasattr(self, 'main_canvas'):
            self.main_canvas.destroy()
            del self.main_canvas

    def limpiar_y_salir(self, event=None):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        self.destroy()
        self.master.quit()
