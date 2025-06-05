# ventanas/arduino.py
import tkinter as tk
import subprocess
import os
import time
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaArduino(tk.Frame):
    def __init__(self, master, respuestas, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.texto_arduino = self.create_text()

        self.boton_arduino = crear_boton(
            self, 
            RUTA_BOTON, 
            "Continuar", 
            276, 410,
            command=self.menu_get_arduino_port
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
            text="Conecte su impresora por cable USB\nSe va a cargar el nuevo firmware.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def no_se_encontro_puerto(self):
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
            text="No se encontró el Arduino.\nVerifique que esté bien conectado.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())

    def menu_get_arduino_port(self):
        port = self.get_arduino_port()

        self.texto_arduino.destroy()
        self.boton_arduino.destroy()

        if not port:
            self.texto_arduino = self.no_se_encontro_puerto()
            self.boton_arduino = crear_boton(
                self, 
                RUTA_BOTON, 
                "Continuar", 
                276, 410,
                command=self.menu_get_arduino_port
            )
        else:
            print("✅ Arduino detectado en:", port)

    def get_arduino_port(self):
        try:
            output = subprocess.check_output(['ls', '-l', '/dev/serial/by-id/']).decode()
            for line in output.splitlines():
                if 'Arduino' in line:
                    parts = line.split('->')
                    if len(parts) == 2:
                        return os.path.realpath('/dev/serial/by-id/' + line.split()[-1])
        except Exception as e:
            print("Error detectando el puerto del Arduino:", e)
        return None


'''


# Paso 1: Encontrar el puerto del Arduino


# Paso 2: Detener servicios Klipper
def stop_klipper_services():
    for i in range(1, 5):
        service = f"klipper-{i}.service"
        print(f"🛑 Deteniendo {service}...")
        subprocess.run(["sudo", "systemctl", "stop", service])

# Paso 3: Flashear firmware
def flash_firmware(port):
    cmd = [
        "sudo", "avrdude",
        "-p", "atmega2560",
        "-c", "wiring",
        "-P", port,
        "-b", "115200",
        "-D",
        "-U", "flash:w:out/klipper.elf.hex"
    ]
    print("🚀 Flasheando firmware...")
    subprocess.run(cmd)

# Paso 4: Iniciar servicios Klipper
def start_klipper_services():
    for i in range(1, 5):
        service = f"klipper-{i}.service"
        print(f"✅ Iniciando {service}...")
        subprocess.run(["sudo", "systemctl", "start", service])

# Programa principal
if __name__ == "__main__":
    print("🔍 Buscando Arduino...")
    port = get_arduino_port()
    if not port:
        print("❌ No se encontró el Arduino.")
        exit(1)

    print(f"✅ Arduino detectado en: {port}")
    stop_klipper_services()
    time.sleep(1)  # Pausa breve

    flash_firmware(port)
    time.sleep(1)  # Esperar para asegurar escritura completa

    start_klipper_services()
    print("🎉 ¡Proceso completo!")

'''