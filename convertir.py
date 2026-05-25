"""
Conversor de imágenes WhatsApp → marcos digitales

El problema: los marcos digitales genéricos no leen las fotos de WhatsApp.
La causa es una combinación de cosas: JPEG progresivo, perfiles ICC, metadatos
EXIF complejos, resoluciones altas. Este script limpia todo eso y genera
imágenes simples que el marco pueda leer sin problema.
"""

import os
import sys
import argparse
from PIL import Image, UnidentifiedImageError

MAX_SIZE = (1280, 720)
EXTENSIONES = (".jpg", ".jpeg", ".png", ".webp")


def convertir_imagen(ruta_entrada: str, ruta_salida: str) -> None:
    with Image.open(ruta_entrada) as img:
        # Crear una imagen nueva y pegarle el contenido convertido a RGB.
        # Así nos deshacemos del perfil ICC y cualquier metadato que cause problemas.
        img_limpia = Image.new("RGB", img.size)
        img_limpia.paste(img.convert("RGB"))

        # Redimensionar solo si pasa del máximo, manteniendo la proporción.
        img_limpia.thumbnail(MAX_SIZE, Image.LANCZOS)

        img_limpia.save(
            ruta_salida,
            format="JPEG",
            quality=95,
            optimize=False,
            progressive=False,
        )


def procesar_carpeta(carpeta_entrada: str, carpeta_salida: str) -> None:
    if not os.path.isdir(carpeta_entrada):
        print(f"[ERROR] La carpeta de entrada no existe: {carpeta_entrada}")
        sys.exit(1)

    os.makedirs(carpeta_salida, exist_ok=True)

    archivos = [
        f for f in os.listdir(carpeta_entrada)
        if f.lower().endswith(EXTENSIONES)
    ]

    if not archivos:
        print(f"No se encontraron imágenes en: {carpeta_entrada}")
        return

    total = len(archivos)
    convertidas = 0
    errores = 0

    print(f"\nProcesando {total} imagen(es) desde '{carpeta_entrada}'...\n")

    for archivo in archivos:
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        nombre = os.path.splitext(archivo)[0]
        ruta_salida = os.path.join(carpeta_salida, f"{nombre}.jpg")

        try:
            convertir_imagen(ruta_entrada, ruta_salida)
            print(f"  [OK] {archivo}")
            convertidas += 1

        except UnidentifiedImageError:
            print(f"  [ERROR] {archivo} — imagen corrupta o formato no reconocido")
            errores += 1

        except Exception as e:
            print(f"  [ERROR] {archivo} — {e}")
            errores += 1

    print(f"\n--- Resumen ---")
    print(f"  Total encontradas : {total}")
    print(f"  Convertidas       : {convertidas}")
    print(f"  Errores           : {errores}")
    print(f"  Guardadas en      : {os.path.abspath(carpeta_salida)}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convierte imágenes de WhatsApp a JPEG baseline para marcos digitales."
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        default="imagenes",
        help="Carpeta con las imágenes originales (default: imagenes)",
    )
    parser.add_argument(
        "salida",
        nargs="?",
        default="convertidas",
        help="Carpeta de destino (default: convertidas)",
    )
    args = parser.parse_args()

    procesar_carpeta(args.entrada, args.salida)


if __name__ == "__main__":
    main()
