import tkinter as tk
from ventanas.bienvenida import PantallaBienvenida
from ventanas.informacion import PantallaInformacion
from ventanas.confirmacion_entrar_asistente import PantallaConfirmacionEntrarAsistente
from ventanas.electronica import PantallaElectronica
from ventanas.final import PantallaFinal
from ventanas.arduino import PantallaArduino
from ventanas.skr import PantallaSkr
from ventanas.extrusor import PantallaExtrusor
from ventanas.tipo_maquina import PantallaTipoMaquina
from ventanas.varillas import PantallaVarillas
from ventanas.motor import PantallaMotor
from ventanas.usb import PantallaUSB
from ventanas.inserte_sd2 import PantallaInserteSD2
from constantes import VENTANA_ANCHO, VENTANA_ALTO

class KutterKlipperInterface:
    def __init__(self, printer_1_data="printer_1_data"):
        self.printer_1_data = printer_1_data  # 👉 Guardás el valor recibido
        self.root = tk.Tk()
        self.root.configure(bg='black')  # 👈 fondo negro base
        self.root.title("KutterKlipper")
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}")

        self.current_screen = None
        self.respuestas = {}  # Inicializar el diccionario de respuestas
        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        #print("printer_1_data", self.printer_1_data)
        self.limpiar_pantalla()
        self.current_screen = PantallaBienvenida(
            self.root,
            continuar_callback=self.mostrar_informacion
        )

    def mostrar_informacion(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaInformacion(
            self.root,
            continuar_callback=self.mostrar_confirmacion_entrar_asistente
        )

    def mostrar_confirmacion_entrar_asistente(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaConfirmacionEntrarAsistente(
            self.root,
            continuar_callback=self.mostrar_electronica
        )


    def mostrar_electronica(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaElectronica(
            self.root,
            respuestas=self.respuestas,
            continuar_32bits=self.mostrar_skr,
            continuar_8bits=self.mostrar_arduino  # Nuevo método que defines tú
        )

    def mostrar_arduino(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaArduino(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_usb
        )

    def mostrar_skr(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaSkr(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_inserte_sd2
        )

    def mostrar_inserte_sd2(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaInserteSD2(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_usb
        )
    
    def mostrar_usb(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaUSB(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_tipo_maquina
        )

    def mostrar_tipo_maquina(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaTipoMaquina(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_extrusor
        )

    def mostrar_extrusor(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaExtrusor(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_varillas
        )

    def mostrar_varillas(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaVarillas(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_motor
        )

    def mostrar_motor(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaMotor(
            self.root,
            respuestas=self.respuestas,
            continuar_callback=self.mostrar_final
        )
        
    def mostrar_final(self):
        self.limpiar_pantalla()
        self.current_screen = PantallaFinal(
            self.root,
            respuestas=self.respuestas,
            printer_1_data=self.printer_1_data,
            continuar_callback=self.quit
        )


    def quit(self):
        self.root.quit()


    def limpiar_pantalla(self):
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None

    def run(self):
        self.root.mainloop()
