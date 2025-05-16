# utils/imagenes.py
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
