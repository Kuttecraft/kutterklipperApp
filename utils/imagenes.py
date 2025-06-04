import tkinter as tk
from PIL import Image, ImageTk

def cargar_imagen(ruta, ancho, alto):
    try:
        img = Image.open(ruta)
        img = img.resize((ancho, alto), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error cargando imagen {ruta}: {e}")
        return None

def cargar_imagen_original(ruta):
    try:
        return Image.open(ruta)
    except Exception as e:
        print(f"Error cargando imagen original: {e}")
        return None

def crear_boton(
    parent,
    ruta_imagen,
    texto,
    x,
    y,
    command,  # puede ser una lambda o función con argumentos
    font=('Montserrat', 16, 'bold'),
    fg='white',
    activeforeground='white',
    activebackground='white',
    borderwidth=0,
    highlightthickness=0
):
    img_orig = cargar_imagen_original(ruta_imagen)
    if img_orig:
        button_image = ImageTk.PhotoImage(img_orig)
        boton = tk.Button(
            parent,
            image=button_image,
            text=texto,
            font=font,
            fg=fg,
            activeforeground=activeforeground,
            activebackground=activebackground,
            compound='center',
            borderwidth=borderwidth,
            highlightthickness=highlightthickness,
            command=command  # ya viene como lambda o función
        )
        boton.image = button_image  # Mantener referencia
        boton.place(
            x=x,
            y=y,
            width=button_image.width(),
            height=button_image.height()
        )
        return boton
    return None
