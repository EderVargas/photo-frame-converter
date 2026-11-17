# Conversor de imágenes WhatsApp para marcos digitales

Surgió de un problema muy concreto: tengo un marco digital de esos genéricos que funciona perfectamente con fotos tomadas desde el celular, pero en cuanto le metía imágenes descargadas de WhatsApp, simplemente no las leía. Los videos sí. Solo las fotos eran el problema.

Después de investigar un poco, la conclusión fue que esos marcos tienen soporte muy limitado para ciertos formatos, y WhatsApp modifica el documento de forma que el marco no lo reconoce. Como posibles opciones:

- Guarda las imágenes como JPEG "progresivo" en lugar de JPEG baseline
- Puede incluir perfiles de color ICC modernos que el firmware del marco no entiende
- Metadatos EXIF más complejos de lo que el hardware espera
- A veces imágenes WEBP disfrazadas de JPG
- Resoluciones que simplemente no soporta

La solución fue escribir este script en Python que limpia todo eso y genera imágenes simples, sin adornos, que el marco pueda leer sin problema.

## Qué hace

Toma una carpeta con imágenes (JPG, JPEG, PNG o WEBP), las convierte a JPEG baseline estándar y las guarda en otra carpeta lista para copiar a una USB.

Lo que hace con cada imagen:

- La convierte a RGB puro, sin perfiles de color raros
- La redimensiona si supera los 1280x720, manteniendo la proporción
- La guarda con `progressive=False`, que es básicamente lo que resuelve todo
- Elimina los metadatos problemáticos desde la raíz

Al final muestra un resumen: cuántas se convirtieron, cuántas fallaron y dónde quedaron guardadas.

## Uso

```bash
pip install pillow
```

O, con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

El script recibe dos argumentos, ambos opcionales y en este orden:

| Argumento | Qué es | Si no lo pasás |
| --- | --- | --- |
| `entrada` | Carpeta con las imágenes originales | `imagenes` |
| `salida` | Carpeta donde quedan los JPEG | `convertidas` |

Solo procesa `.jpg`, `.jpeg`, `.png` y `.webp`. Videos y cualquier otro archivo se saltan. Cada imagen sale como `.jpg` con el mismo nombre, aunque el original fuera PNG o WEBP. La carpeta de salida se crea si no existe.

### Sin parámetros

```bash
python convertir.py
```

Lee `./imagenes` y escribe en `./convertidas`.

Si `imagenes` no existe, termina con error y no crea nada:

```text
[ERROR] La carpeta de entrada no existe: imagenes
```

Si la carpeta existe pero no hay imágenes de esos formatos:

```text
No se encontraron imágenes en: imagenes
```

Si hay imágenes, imprime una línea por archivo y un resumen al final:

```text
Procesando 2 imagen(es) desde 'imagenes'...

  [OK] foto.png
  [OK] vacaciones.webp

--- Resumen ---
  Total encontradas : 2
  Convertidas       : 2
  Errores           : 0
  Guardadas en      : C:\...\fotosParaFrame\convertidas
```

En `convertidas` quedan `foto.jpg` y `vacaciones.jpg`.

### Solo la carpeta de entrada

```bash
python convertir.py D:\whatsapp
```

Lee `D:\whatsapp` y escribe en `./convertidas`, el valor por defecto de la salida. El resto del comportamiento es el mismo: error si esa carpeta no existe, aviso si no hay imágenes, y resumen si las hay.

### Entrada y salida

```bash
python convertir.py D:\whatsapp E:\USB
```

Lee `D:\whatsapp` y escribe en `E:\USB`. Sirve para dejar los JPEG directo en la memoria que va al marco. `E:\USB` se crea si no existe; si `D:\whatsapp` no existe, el script termina con el mismo error de carpeta inexistente.

## Por qué `progressive=False`

Los marcos digitales genéricos suelen tener firmware muy limitado. El JPEG baseline es el formato de siempre, el que todos entienden desde hace décadas. El JPEG progresivo es más moderno y se carga de forma incremental, lo cual es útil para web, pero muchos dispositivos de hardware limitado directamente no lo soportan.

Pillow lo resuelve con un parámetro al guardar:

```python
img.save("foto.jpg", format="JPEG", progressive=False)
```

## Resultado

Las imágenes quedan listas para copiar a una USB formateada en FAT32. El marco las lee sin problemas.

## Tecnologías

- Python 3
- Pillow (PIL)
