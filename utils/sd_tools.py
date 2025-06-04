# utiles/sd_tools.py
import os
import shutil
import subprocess
import sys

archivo_firmware = "/home/kutter/firmware.bin"
sd_device = "/dev/mmcblk1p1"
sd_mount_point = "/media/sdcard"

def montar_sd():
    print("[INFO] Intentando montar la SD...")
    os.makedirs(sd_mount_point, exist_ok=True)
    subprocess.run(["sudo", "mount", sd_device, sd_mount_point], check=True)
    print("[OK] SD montada en", sd_mount_point)

def copiar_firmware():
    destino = os.path.join(sd_mount_point, "firmware.bin")
    if not os.path.exists(archivo_firmware):
        raise FileNotFoundError(f"[ERROR] El archivo de firmware no existe: {archivo_firmware}")
    shutil.copy(archivo_firmware, destino)
    print(f"[OK] Archivo copiado a {destino}")

def desmontar_sd():
    print("[INFO] Desmontando la SD...")
    subprocess.run(["sudo", "umount", sd_mount_point], check=True)
    print("[OK] SD desmontada correctamente.")

def proceso_sd_completo():
    if not os.path.ismount(sd_mount_point):
        montar_sd()
    else:
        print(f"[INFO] La SD ya está montada en {sd_mount_point}")
    copiar_firmware()
    desmontar_sd()
