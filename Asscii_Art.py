
# -*- coding: utf-8 -*-

from PIL import Image

# Caracteres ASCII ordenados de oscuro a claro
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    """
    Redimensiona manteniendo proporción.
    """
    width, height = image.size
    ratio = height / width

    # Ajuste especial para texto terminal
    new_height = int(new_width * ratio * 0.55)

    resized = image.resize((new_width, new_height))
    return resized


def grayify(image):
    """
    Convierte imagen a escala de grises.
    """
    return image.convert("L")


def pixels_to_ascii(image):
    """
    Convierte píxeles a caracteres ASCII.
    """
    pixels = image.getdata()

    ascii_str = ""

    for pixel in pixels:

        # pixel va de 0 a 255
        index = pixel * (len(ASCII_CHARS) - 1) // 255

        ascii_str += ASCII_CHARS[index]

    return ascii_str


def image_to_ascii(path, width=100):

    try:
        image = Image.open(path)

    except Exception as e:
        print("Error al abrir imagen:", e)
        return

    # Redimensionar
    image = resize_image(image, width)

    # Escala de grises
    image = grayify(image)

    # ASCII
    ascii_data = pixels_to_ascii(image)

    # Reconstrucción por líneas
    pixel_count = len(ascii_data)

    ascii_image = ""

    for i in range(0, pixel_count, width):
        ascii_image += ascii_data[i:i+width] + "\n"

    return ascii_image


if __name__ == "__main__":

    ruta = "2.jpg"   # <-- tu imagen aquí

    resultado = image_to_ascii(ruta, width=120)

    if resultado:

        print(resultado)

        # Guardar a TXT
        with open("ascii_art.txt", "w", encoding="utf-8") as f:
            f.write(resultado)

        print("\nASCII guardado en ascii_art.txt")

"""
import ascii_magic

output = ascii_magic.from_image_file("foto.jpg", columns=120)

ascii_magic.to_terminal(output)
"""