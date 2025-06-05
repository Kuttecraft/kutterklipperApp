import tkinter as tk
import subprocess
import os
import time
import threading

from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, crear_boton


class PantallaArduino(tk.Frame):
    def __init__(self, master, respuestas, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.port = None

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
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="Conecte su impresora por cable USB\nSe va a cargar el nuevo firmware.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def no_se_encontro_puerto(self):
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="No se encontró el Arduino.\nVerifique que esté bien conectado.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def se_encontro_puerto(self):
        self.main_canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        impresora_3d = cargar_imagen(RUTA_IMAGEN_IMPRESORA_3D, 640, 329)
        if impresora_3d:
            self.main_canvas.create_image(80, 8, anchor='nw', image=impresora_3d)
            self.main_canvas.image = impresora_3d

        self.main_canvas.create_text(
            VENTANA_ANCHO // 2, 350,
            text="Arduino detectado.\nSe va a cargar el nuevo firmware.",
            font=('Montserrat', 22, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        )
        return self.main_canvas

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())

    def menu_get_arduino_port(self):
        self.port = self.get_arduino_port()

        self.texto_arduino.destroy()
        self.boton_arduino.destroy()

        if not self.port:
            self.texto_arduino = self.no_se_encontro_puerto()
            self.boton_arduino = crear_boton(
                self,
                RUTA_BOTON,
                "Continuar",
                276, 410,
                command=self.menu_get_arduino_port
            )
        else:
            print("✅ Arduino detectado en:", self.port)
            self.texto_arduino = self.se_encontro_puerto()
            self.boton_arduino = crear_boton(
                self,
                RUTA_BOTON,
                "Cargar firmware",
                276, 410,
                command=self.menu_flash_firmware
            )

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

    def menu_flash_firmware(self):
        self.texto_arduino.destroy()
        self.boton_arduino.destroy()

        self.loading_label = tk.Label(
            self, text="Cargando firmware", font=('Montserrat', 20),
            fg=COLOR_TEXTO, bg=COLOR_FONDO
        )
        self.loading_label.place(x=VENTANA_ANCHO // 2 - 100, y=350)

        self.dots = ""
        self.animar = True  # ← bandera para controlar la animación
        self.animate_loading()

        thread = threading.Thread(target=self.proceso_firmware)
        thread.start()

    def animate_loading(self):
        if not getattr(self, "animar", False):
            return  # salir si ya no debe animar

        self.dots = "." if self.dots == "..." else self.dots + "."
        self.loading_label.config(text=f"Cargando firmware{self.dots}")
        self.after(500, self.animate_loading)

    def proceso_firmware(self):
        self.stop_klipper_services()
        time.sleep(1)
        self.flash_firmware()
        time.sleep(1)
        self.start_klipper_services()
        self.after(0, self.proceso_terminado)

    def proceso_terminado(self):
        self.animar = False  # ← detener la animación antes de destruir el label
        self.loading_label.destroy()

        final_label = tk.Label(
            self, text="✅ Firmware cargado con éxito",
            font=('Montserrat', 20), fg=COLOR_TEXTO, bg=COLOR_FONDO
        )
        final_label.place(x=VENTANA_ANCHO // 2 - 180, y=350)

        crear_boton(
            self,
            RUTA_BOTON,
            "Continuar",
            276, 410,
            command=self.continuar_callback
        )

    def stop_klipper_services(self):
        for i in range(1, 5):
            service = f"klipper-{i}.service"
            print(f"🛑 Deteniendo {service}...")
            subprocess.run(["sudo", "systemctl", "stop", service])

    def flash_firmware(self):
        cmd = [
            "sudo", "avrdude",
            "-p", "atmega2560",
            "-c", "wiring",
            "-P", self.port,
            "-b", "115200",
            "-D",
            "-U", "flash:w:out/klipper.elf.hex"
        ]
        print("🚀 Flasheando firmware...")
        subprocess.run(cmd)

    def start_klipper_services(self):
        for i in range(1, 5):
            service = f"klipper-{i}.service"
            print(f"✅ Iniciando {service}...")
            subprocess.run(["sudo", "systemctl", "start", service])


'''


# Paso 1: Encontrar el puerto del Arduino


# Paso 2: Detener servicios Klipper


# Paso 3: Flashear firmware


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