import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class KutterKlipperInterface:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("KutterKlipper")
        
        # Configurar modo pantalla completa sin bordes ni barras
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        
        # Establecer dimensiones específicas para Raspberry Pi
        self.root.geometry("800x480")
        
        # Crear el contenedor principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # Cargar y mostrar la imagen de fondo
        self.load_background_image()
        
	# Crear el texto de bienvenida
        self.create_welcome_text()
        
        # Crear el botón transparente
        self.create_transparent_button()

    def create_welcome_text(self):
        """Crear el texto de bienvenida"""
        # Crear el texto
        self.welcome_label = tk.Label(
            self.main_frame,
            text="¡Te damos la bienvenida a KutterKlipper!",
            font=('Montserrat', 24, 'bold'),
            fg='white',
            bg='black',
            justify='center'
        )
        
        # Posicionar el texto en el centro de la ventana
        self.welcome_label.place(
            x=0,
            y=310,  # Ajusta la posición vertical según necesites
            width=800,  # Ancho completo de la ventana
            height=50  # Altura del texto
        )
        
        # Configurar el cierre de la ventana al presionar Escape
        self.root.bind('<Escape>', self.close_window)
        
    def load_background_image(self):
        image_path = "/home/kutter/animacion/init_kutterklipper/imagen/menu_inicio.png"  # corregido

        try:
            original_image = Image.open(image_path)

            # Usar dimensiones fijas (ya que las definiste como 800x480)
            window_width = 800
            window_height = 480

            background_image = ImageTk.PhotoImage(original_image.resize(
                (window_width, window_height), Image.Resampling.LANCZOS
            ))

            # Mostrar imagen con place para asegurarte de que ocupa todo
            self.background_label = tk.Label(self.main_frame, image=background_image)
            self.background_label.image = background_image
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

            
    def load_button_image(self):
        """Cargar la imagen del botón"""
        try:
            button_image_path = "/home/kutter/animacion/init_kutterklipper/imagen/boton.png"
            self.button_image = Image.open(button_image_path)
            # Mantener la imagen original para usarla en hover
            self.button_image_original = self.button_image.copy()
            
            # Convertir a PhotoImage para tkinter
            self.button_image = ImageTk.PhotoImage(self.button_image)
            return True
        except Exception as e:
            print(f"Error al cargar la imagen del botón: {e}")
            return False

    def create_transparent_button(self):
        """Crear el botón con imagen"""
        # Cargar la imagen del botón
        if not hasattr(self, 'button_image') or self.button_image is None:
            if not self.load_button_image():
                return

        # Crear el botón con la imagen
        self.button = tk.Button(
            self.main_frame,
            image=self.button_image,
            text="CONTINUAR",
            font=('Montserrat', 16, 'bold'),
	    fg='white',              # Color del texto normal
    	    activeforeground='white',  # Color del texto cuando se hace hover
    	    activebackground='white',  # Fondo cuando se hace hover
            compound='center',  # Coloca el texto sobre la imagen
            borderwidth=0,
            highlightthickness=0,
            command=self.close_window
        )
        
        # Posicionar el botón (ajusta estos valores según la posición de la caja en tu imagen)
        # Establecer el tamaño basado en la imagen del botón
        self.button.place(
            x=275,  # Ajusta según la posición deseada
            y=387,  # Ajusta según la posición deseada
            width=self.button_image.width(),
            height=self.button_image.height()
        )
        
    def close_window(self, event=None):
        self.root.quit()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KutterKlipperInterface()
    app.run()
