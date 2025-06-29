# ventanas/final.py
import tkinter as tk
import time
import re
import subprocess
from PIL import ImageTk
from constantes import (
    VENTANA_ANCHO, VENTANA_ALTO,
    FUENTE_TITULO, COLOR_TEXTO, COLOR_FONDO,
    RUTA_IMAGEN_FONDO, RUTA_BOTON, RUTA_IMAGEN_IMPRESORA_3D
)
from utils.imagenes import cargar_imagen, cargar_imagen_original, crear_boton

class PantallaFinal(tk.Frame):
    def __init__(self, master, respuestas=None, printer_1_data=None, continuar_callback=None):
        super().__init__(master, bg='black')
        self.respuestas = respuestas
        self.printer_1_data = printer_1_data
        self.pack(fill='both', expand=True)
        self.continuar_callback = continuar_callback or (lambda: None)

        self.create_text()

        crear_boton(
            self, 
            RUTA_BOTON, 
            "Salir", 
            276, 410,
            command=self.salir
        )
        self.bind_events()

        self.ruta_nuevo_archivo = f"/home/kutter/{self.printer_1_data}/config/printer.cfg"

        #respuestas = {'Tipo': '32_Bits', 'skr': 'skr1_4_turbo', 'USB': '/dev/serial/by-id/usb-Klipper_lpc1768_0D70000163102CAFA106FB5AC42000F5-if00', 'tipo_maquina': 'pk3++', 'EXT': 'BMG', 'Varilla': '4mm', 'motor': 'con'}
        #adelante se estable el valor de las cariables para el final guardarlas en el archivo real y teminar creando al printer.cfg
        
        if(respuestas["Tipo"] == "32_Bits"):
            if(respuestas["skr"] == "skr2_0"):
                self.ruta_archivo = "/home/kutter/kutterklipperApp/config_printer/printer_SKR2.cfg"
            else:
                self.ruta_archivo = "/home/kutter/kutterklipperApp/config_printer/printer_SKR1_4.cfg"

            if(respuestas["motor"] == "sin"):
                self.guiro_motor_x = ""
                self.guiro_motor_y = ""
                self.guiro_motor_z = ""
            else:
                self.guiro_motor_x = "!"
                self.guiro_motor_y = ""
                self.guiro_motor_z = ""

        if(respuestas["Tipo"] == "8_Bits"):
            self.ruta_archivo = "/home/kutter/kutterklipperApp/config_printer/printer_ramps.cfg"

            if(respuestas["motor"] == "sin"):
                self.guiro_motor_x = ""
                self.guiro_motor_y = "!"
                self.guiro_motor_z = "!"
            else:
                self.guiro_motor_x = "!"
                self.guiro_motor_y = ""
                self.guiro_motor_z = ""
            
        if(respuestas["tipo_maquina"] == "pk3"):
            self.medida_eje_x = "230"
            self.medida_eje_y = "210"
            self.medida_eje_z = "210"

        elif(respuestas["tipo_maquina"] == "pk3++"):
            self.medida_eje_x = "230"
            self.medida_eje_y = "310"
            self.medida_eje_z = "210"

        elif(respuestas["tipo_maquina"] == "pk3ext"):
            self.medida_eje_x = "230"
            self.medida_eje_y = "310"
            self.medida_eje_z = "410"


        if(respuestas["EXT"] == "BMG"):
            self.valor_extruder = "#BMG EXTRUDER\nmicrosteps: 16\ngear_ratio: 3:1\nrotation_distance: 23.132\nfull_steps_per_rotation: 200\nmax_extrude_cross_section: 50"
            self.offset_x = "54"
            self.offset_y = "-36"
            self.retract_length_ = "0.8"

            if(respuestas["tipo_maquina"] == "pk3"):
                self.home_xy_position = "61,141"
                self.mesh_min = "54,10"
                self.mesh_max = "124,174"

            elif(respuestas["tipo_maquina"] == "pk3++"):
                self.home_xy_position = "61,191"
                self.mesh_min = "54,10"
                self.mesh_max = "224,274"

            elif(respuestas["tipo_maquina"] == "pk3ext"):
                self.home_xy_position = "61,191"
                self.mesh_min = "54,10"
                self.mesh_max = "224,274"
        else:
            self.valor_extruder = "microsteps: 16\nrotation_distance: 30"
            self.offset_x = "54"
            self.offset_y = "-36"
            self.retract_length_ = "6"

            if(respuestas["tipo_maquina"] == "pk3"):
                self.home_xy_position = "61,141"
                self.mesh_min = "54,10"
                self.mesh_max = "124,174"

            elif(respuestas["tipo_maquina"] == "pk3++"):
                self.home_xy_position = "61,191"
                self.mesh_min = "54,10"
                self.mesh_max = "224,274"

            elif(respuestas["tipo_maquina"] == "pk3ext"):
                self.home_xy_position = "61,191"
                self.mesh_min = "54,10"
                self.mesh_max = "224,274"

        self.valores = {
            "usb_impresora": respuestas["USB"],
            "carpeta_impresora": self.printer_1_data,
            "direcion_motor_x": self.guiro_motor_x,
            "medida_eje_x": self.medida_eje_x,
            "direcion_motor_y": self.guiro_motor_y,
            "medida_eje_y": self.medida_eje_y,
            "direcion_motor_z": self.guiro_motor_z,
            "valor_paso_motor_z": respuestas["Varilla"],
            "medida_eje_z": self.medida_eje_z,
            "valor_extruder": self.valor_extruder,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "home_xy_position": self.home_xy_position,
            "mesh_min": self.mesh_min,
            "mesh_max": self.mesh_max,
            "retract_length": self.retract_length_,
            "sensor_de_filamento": ""
        }

        with open(self.ruta_archivo, "r", encoding="utf-8") as file:
            self.contenido = file.read()

        self.nuevo_contenido = re.sub(r"<(.*?)>", self.reemplazar, self.contenido)

        try:
            subprocess.run(["sudo", "rm", self.ruta_nuevo_archivo], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Fallo al eliminar: {e}")
        except Exception as e:
            print(f"[ERROR] Error inesperado al eliminar: {e}")
            

        with open(self.ruta_nuevo_archivo, "w", encoding="utf-8") as file:
            file.write(self.nuevo_contenido)
            #print("[INFO] Archivo creado correctamente", self.nuevo_contenido)
            #solo una nota

    def reemplazar(self, match):
        clave = match.group(1)
        return self.valores.get(clave, match.group(0))
        

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
            text="Perfecto, ya se creó un archivo printer.cfg\ncon los valores de la impresora.Ahora solo queda\nreiniciar el firmware para poder probar la máquina.",
            font=('Montserrat', 18, 'bold'),
            fill=COLOR_TEXTO,
            justify='center'
        ) 

    def bind_events(self):
        self.bind_all('<Escape>', lambda e: self.master.quit())



    def stop_klipper_services(self):
        for i in range(1, 5):
            service = f"klipper-{i}.service"
            print(f"🛑 Deteniendo {service}...")
            subprocess.run(["sudo", "systemctl", "stop", service])

    def start_klipper_services(self):
        for i in range(1, 5):
            service = f"klipper-{i}.service"
            print(f"✅ Iniciando {service}...")
            subprocess.run(["sudo", "systemctl", "start", service])

    def salir(self):
        #self.stop_klipper_services()
        #time.sleep(1)
        #self.start_klipper_services()
        #time.sleep(1)
        self.master.quit()
        