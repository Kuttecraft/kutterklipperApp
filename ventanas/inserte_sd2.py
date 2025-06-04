# ventanas/inserte_sd2.py
import tkinter as tk
import os
import shutil
import subprocess
import sys
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaInserteSD2(tk.Frame):
    def __init__(self, master, respuestas=None, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        # Ruta del archivo a copiar
        self.archivo_firmware = "/home/kutter/firmware.bin"  # Cambiar si es necesario

        # Dispositivo y punto de montaje
        self.sd_device = "/dev/mmcblk1p1"
        self.sd_mount_point = "/media/sdcard"

        self.texto_sd = self.create_text()
        self.boton_sd = crear_boton(
            self, 
            RUTA_BOTON, 
            "Continuar", 
            276, 410,
            command=lambda: self.montar_sd()
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
        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        # Añadir el texto sobre la imagen
        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="Inserte una tarjeta SD vacía en el KutterKlipper.\n"
            "Esta tarjeta se usará para grabar el archivo de actualización\n"
            "Una vez insertada, presione el botón 'Continuar'",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def create_text_sd_montada(self):
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
            text="Se detecto y monto la SD\nSe procedera a copiar el archivo \"firmware.bin\"",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas
    
    def create_text_sd_montada_error(self):
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
            text="No se detecto la SD\nReinserte la SD y presione continuar",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def create_text_sd_copiado(self):
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
            text="Se copio el archivo \"firmware.bin\" a la SD",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def create_text_sd_error(self):
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
            text="Error al copiar el archivo \"firmware.bin\" a la SD\nSe tendra que installar manualmente el firmware",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas
    
    def create_text_sd_desmontada(self):
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
            text="La tarjeta SD se expulso correctamente\nProceda a insertar la tarjeta SD en la electronica\nPara su instalacion en la impresora 3D",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())

    def montar_sd(self):
        print("[INFO] Intentando montar la SD...")
        self.texto_sd.destroy()

        try:
            os.makedirs(self.sd_mount_point, exist_ok=True)

            # Verificar si la SD ya está montada
            resultado = subprocess.run(
                ["mountpoint", "-q", self.sd_mount_point]
            )

            if resultado.returncode != 0:
                # Solo intentar montar si no está montada
                subprocess.run(["sudo", "mount", self.sd_device, self.sd_mount_point], check=True)
            else:
                print("[INFO] La SD ya estaba montada.")

            self.boton_sd.destroy()
            self.texto_sd = self.create_text_sd_montada()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.copiar_firmware()
            )

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Fallo al montar la SD: {e}")
            self.texto_sd = self.create_text_sd_montada_error()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.montar_sd()
            )

        except Exception as e:
            print(f"[ERROR] Error inesperado al montar la SD: {e}")
            self.texto_sd = self.create_text_sd_montada_error()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.montar_sd()
            )
    def copiar_firmware(self):
        destino = os.path.join(self.sd_mount_point, "firmware.bin")
        self.boton_sd.destroy()
        self.texto_sd.destroy()

        try:
            if not os.path.exists(self.archivo_firmware):
                print(f"[ERROR] El archivo de firmware no existe: {self.archivo_firmware}")
                
            # Copiar el archivo
            subprocess.run(["sudo", "cp", self.archivo_firmware, destino], check=True)
            print(f"[OK] Archivo copiado a {destino}")

            

            self.texto_sd = self.create_text_sd_copiado()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.desmontar_sd()
            )

        except PermissionError:
            self.texto_sd = self.create_text_sd_error()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.continuar_callback()
            )
            print("[ERROR] Permiso denegado al copiar el archivo.")
            
        except shutil.SameFileError:
            print("[ERROR] El archivo de origen y destino son iguales.")
            self.texto_sd = self.create_text_sd_error()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.continuar_callback()
            )
            
        except Exception as e:
            print(f"[ERROR] Error inesperado al copiar el archivo: {e}")    
            self.texto_sd = self.create_text_sd_error()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.continuar_callback()
            )

    def desmontar_sd(self):
        print("[INFO] Desmontando la SD...")
        try:
            subprocess.run(["sudo", "umount", self.sd_mount_point], check=True)
            print("[OK] SD desmontada correctamente.")

            self.texto_sd.destroy()
            self.boton_sd.destroy()

            self.texto_sd = self.create_text_sd_desmontada()
            self.boton_sd = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=lambda: self.continuar_callback()
            )
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Fallo al desmontar la SD: {e}")
        except Exception as e:
            print(f"[ERROR] Error inesperado al desmontar la SD: {e}")