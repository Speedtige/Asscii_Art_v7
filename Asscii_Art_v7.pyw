
# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 ASCII Art Generator - PyQt5 Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Desarrollado por:
Cristian M. Veliz Cano

Versión:
V-07

Licencia:
MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software y de los archivos de
documentación asociados, para utilizar el Software sin
restricción, incluyendo sin limitación los derechos de uso,
copia, modificación, fusión, publicación, distribución,
sublicencia y/o venta de copias del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.

Descripción:

ASCII Art Generator es una aplicación desarrollada en Python utilizando PyQt5, OpenCV y 
PIL/Pillow, diseñada para convertir imágenes tradicionales en representaciones artísticas 
mediante caracteres ASCII.

El sistema incorpora múltiples motores de generación ASCII,
permitiendo distintos estilos visuales, renderizados en color,
procesamiento monocromático y exportación de resultados tanto
en formato TXT como imagen renderizada.

Características Principales:

✔ Conversión Imagen → ASCII Art
✔ Múltiples motores de renderizado ASCII
✔ Soporte para ASCII monocromático y RGB
✔ Personalización de caracteres ASCII
✔ Exportación TXT
✔ Exportación PNG/JPG/BMP
✔ Selector de color de fondo
✔ Renderizado HTML en QTextEdit
✔ Interfaz moderna desarrollada en PyQt5
✔ Procesamiento de imágenes con OpenCV
✔ Escalado dinámico mediante slider
✔ Sistema modular de generación ASCII

Tecnologías Utilizadas:

• Python 3
• PyQt5
• OpenCV
• NumPy
• Pillow (PIL)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
##====================================================================================
##====================================================================================
import sys, os
import cv2
import tempfile
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
##====================================================================================
##====================================================================================
## Libreria --|rembg|--
import bg
import download
import parse_url
import session_base
import session_cloth
import session_factory
import session_simple
##====================================================================================
##====================================================================================
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QSlider, QMessageBox, QColorDialog, QScrollArea, QInputDialog, QLineEdit, QDialog, QShortcut,
    QPlainTextEdit)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QIcon, QImage, QTextDocument, QKeySequence

from PIL import Image
##====================================================================================
# --- Clase para manejo de rutas de recursos (Sin cambios) ---
##====================================================================================
class Path():

    # =========================
    # ✨ Debuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================
    def resource_path(relative_path):    ## Forma #1 resource_path(relative_path)
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # =========================
    # ✨ Debuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================
    def resource_path_app():    ## Forma #2 resource_path_app()

        try:
            path_app = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

        except Exception as e:
            print(e)

        except IOError as error:
            print( error )

        return path_app

##===============================================================
##===============================================================
## ASCII_CHARS = "@%#*+=-:. "                       # <--Ejemplo 01
## ASCII_CHARS = "xo,*vzmnrs. "                     # <--Ejemplo 02
## ASCII_CHARS = "+=-;:,:zcvunxr. "                 # <--Ejemplo 03
## ASCII_CHARS = "oahkbdpqwm#*+=-;:,:zcvunxr. "     # <--Ejemplo 04

# ASCII_CHARS = (                                   # <--Ejemplo 05 - Con Tupla
#     "$@B%8&WM#*oahkbdpqwmZO0QLCJ"
#     "UYXzcvunxrjft/|()1{}[]?-_+~"
#     "<>i!lI;:,\"^`'. "
# )
##====================================================================================

class ASCIIArtGenerator(QWidget):

    def __init__(self):
        super().__init__()

        self.image_path = None

        self.Generator_v1 = False
        self.Generator_v2 = False
        self.Generator_v3 = False
        self.Generator_v4 = False
        self.Generator_v5 = False
        self.Generator_v6 = False

        self.ASCII_CHARS = ""

        self.init_ui()
        self.apply_style()
        self.key_app_info()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def init_ui(self):

        self.setWindowTitle("ASCII Art Generator - PyQt5")

        # Icono
        icon_path = Path.resource_path("Ico\\1.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.center_on_screen()

        self.color_ascii = "#000000"
        self.pixmap = None

        # -------------------------------------------------
        # Widgets
        # -------------------------------------------------
        self.btn_open = QPushButton("Abrir Imagen")
        self.btn_open.clicked.connect(self.cuestion_choise)

        self.btn_save = QPushButton("Guardar TXT")
        self.btn_save.clicked.connect(self.save_txt)

        self.btn_clean = QPushButton("Limpiar Caja")
        self.btn_clean.clicked.connect(self.clean)

        self.btn_color = QPushButton("Definir Color")
        self.btn_color.clicked.connect(self.definir_color_Ascii)

        self.btn_save_image = QPushButton("Guardar Imagen")
        self.btn_save_image.clicked.connect(self.save_image)

        self.label_slider = QLabel("Resolución ASCII")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(300)
        self.slider.setValue(120)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #565a5e;
                height: 8px;
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #007bff;
                border: 1px solid #565a5e;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::add-page:horizontal {
                background: #565a5e;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #007bff;
                border-radius: 4px;
            }
        """)

        self.slider.valueChanged.connect(self.update_ascii)

        self.text_ascii = QTextEdit()
        self.text_ascii.setReadOnly(True)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.text_ascii)

        # Fuente monoespaciada
        font = QFont("Courier New")
        font.setPointSize(6)

        self.text_ascii.setFont(font)
        self.text_ascii.setPlaceholderText("Fabor Ingresar Nueva Imagen para Ser Tratada...")

        # -------------------------------------------------
        # Layouts
        # -------------------------------------------------
        top_layout = QHBoxLayout()

        top_layout.addWidget(self.btn_open)
        top_layout.addWidget(self.btn_save)
        top_layout.addWidget(self.btn_clean)
        top_layout.addWidget(self.btn_color)
        top_layout.addWidget(self.btn_save_image)
        top_layout.addWidget(self.label_slider)
        top_layout.addWidget(self.slider)

        main_layout = QVBoxLayout()

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.text_ascii)

        self.setLayout(main_layout)

        # Atajo Ctrl + O para inniciar el tratamiento a la Imagen con [ASCII]
        info_software = QShortcut(QKeySequence('Ctrl+O'), self)
        info_software.activated.connect(self.cuestion_choise)

        # Atajo Ctrl + I para mostrar información del software
        info_software = QShortcut(QKeySequence('Ctrl+I'), self)
        info_software.activated.connect(self.show_app_info)

        # Atajo Ctrl + K para mostrar información Sobre las Teclas de Atajo
        key_info_software = QShortcut(QKeySequence('Ctrl+K'), self)
        key_info_software.activated.connect(self.key_app_info)

        # Atajo Ctrl + Q Limpia, El Cuadro de Texto, el Resultado
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.Clean)

        # Atajo Ctrl + G para Guardar el Resultado de la Imagen con [ASCII]
        info_software = QShortcut(QKeySequence('Ctrl+G'), self)
        info_software.activated.connect(self.Choise_Save)

        # Atajo Ctrl + C para definir el Color del Tratamiento con [ASCII]
        info_software = QShortcut(QKeySequence('Ctrl+C'), self)
        info_software.activated.connect(self.definir_color_Ascii)

        # Atajo Ctrl + P para Previsualizar tanto las Imagenes, como los *.txt a Generar
        info_software = QShortcut(QKeySequence('Ctrl+P'), self)
        info_software.activated.connect(lambda: Previews_Files.file_temp_question(self))

        # Atajo Ctrl + B para Ser Tratadas las Imagenes, con BackGroud
        info_software = QShortcut(QKeySequence('Ctrl+B'), self)
        info_software.activated.connect(lambda: remove_backGroud.remover_Fondo(self))


##====================================================================================
##====================================================================================

    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    def show_app_info(self):
        dialog_i = app_info(self)
        dialog_i.exec_()

    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    def key_app_info(self):
        dialog_k = key_info(self)
        dialog_k.exec_()

##====================================================================================
##====================================================================================
	
    # =========================
    # CARACTERES ASCII 
    # =========================
    def ASCII_CHARTER(self):
    	print("Estoy en: ASCII_CHARTER...")

    	name_file, ok = ASCIIArtGenerator.show_input(self, "CARACTERES ASCII",
                        "Coloca los caracteres ASCII que deseas Utilizar:"
                    )

    	if ok and name_file:

    		self.ASCII_CHARS = f"{name_file}"
    		return "Ok"
        
    	else:

            self.ASCII_CHARS = "@%#*+=-:. "
            return "Ok"

    # =========================
    # 🎵 Centrar App
    # =========================
    def center_on_screen(self):

        screen = QApplication.primaryScreen().availableGeometry()
        w, h = 1000, 700
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2 + 10
        self.setGeometry(x, y, w, h)

    # ---------------------------------------------------------
    # Abrir Imagen
    # ---------------------------------------------------------
    def open_image(self):

        self.image_path = None
        path = ""

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:
            self.image_path = path

            if self.Generator_v2 == True:
                ASCIIArtGenerator_v2.update_ascii_v2(self)
            elif self.Generator_v3 == True:
                ASCIIArtGenerator_v3.update_ascii_v3(self)
            elif self.Generator_v4 == True:
                ASCIIArtGenerator_v4.update_ascii_v4(self)
            elif self.Generator_v5 == True:
                ASCIIArtGenerator_v5.update_ascii_v5(self)
            elif self.Generator_v6 == True:
                ASCIIArtGenerator_v6.update_ascii_v6(self)

            else:
                ASCIIArtGenerator.update_ascii(self)

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii(self):

        if not self.image_path:
            return

        if self.Generator_v2 == True:
        	ASCIIArtGenerator_v2.update_ascii_v2(self)
        elif self.Generator_v3 == True:
        	ASCIIArtGenerator_v3.update_ascii_v3(self)
        elif self.Generator_v4 == True:
        	ASCIIArtGenerator_v4.update_ascii_v4(self)
        elif self.Generator_v5 == True:
        	ASCIIArtGenerator_v5.update_ascii_v5(self)
        elif self.Generator_v6 == True:
        	ASCIIArtGenerator_v6.update_ascii_v6(self)

        else:

	        width = self.slider.value()

	        ascii_art = self.convert_to_ascii(
	            self.image_path,
	            width
	        )

	        self.text_ascii.setHtml(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii(self, path, new_width=120):
	    image = cv2.imread(path)
	    if image is None:
	        return "Error cargando imagen."

	    # BGR -> RGB
	    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	    # NumPy -> PIL
	    pil_image = Image.fromarray(image)

	    # -----------------------------------------
	    # Resize
	    # -----------------------------------------
	    width, height = pil_image.size
	    ratio = height / width
	    new_height = int(new_width * ratio * 0.55)
	    pil_image = pil_image.resize((new_width, new_height))

	    # -----------------------------------------
	    # RGB original
	    # -----------------------------------------
	    color_array = np.array(pil_image)

	    # -----------------------------------------
	    # Escala de grises
	    # -----------------------------------------
	    gray_image = pil_image.convert("L")
	    gray_array = np.array(gray_image)

	    # -----------------------------------------
	    # Mejora automática de contraste
	    # -----------------------------------------
	    gray_array = cv2.equalizeHist(gray_array)

	    # -----------------------------------------
	    # Ajustar contraste
	    # -----------------------------------------
	    gray_array = cv2.convertScaleAbs(gray_array, alpha=1.5, beta=0)

	    # -----------------------------------------
	    # HTML ASCII
	    # -----------------------------------------
	    ## background-color:black;
	    ## background-color:white;
	    ## background-color:#EAEAEA;

	    ascii_html = f"""
	    <html>
	    <body style="
	        background-color:{self.color_ascii};
	        color:white;
	        font-family:'Courier New';
	        font-size:6pt;
	        line-height:6px;
	        white-space: pre;
	    ">
	    """

	    for y in range(gray_array.shape[0]):
	        for x in range(gray_array.shape[1]):
	            pixel = gray_array[y, x]
	            r, g, b = color_array[y, x]
	            index = pixel * (len(self.ASCII_CHARS) - 1) // 255
	            char = self.ASCII_CHARS[index]
	            ascii_html += (
	                f'<span style="color:rgb({r},{g},{b});">'
	                f'{char}'
	                f'</span>'
	            )
	        ascii_html += "<br>"

	    ascii_html += "</body></html>"

	    return ascii_html

    # ---------------------------------------------------------
    # Guardar TXT
    # ---------------------------------------------------------
    def save_txt(self):

        ascii_text = self.text_ascii.toPlainText()

        if not ascii_text.strip():

            QMessageBox.warning(
                self,
                "Vacío",
                "No hay ASCII para guardar."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar ASCII",
            "ascii_art.txt",
            "Text Files (*.txt)"
        )

        if path:

            resp = ASCIIArtGenerator.show_question(self, "Pregunta", "Deseas, Ver una Vista Previa?\nAntes de ser Guardado.")
            if resp == True:

                try:

                    # Guardamos en Temporales...
                    path_txt = os.path.join(tempfile.gettempdir(), f"[ASCII-ART].txt")

                    with open(path_txt, "w", encoding="utf-8") as f:
                        f.write(ascii_text)

                    TXT_Lec.Frame_TXT_Lec(self, path_txt)

                    resp = ASCIIArtGenerator.show_question(self, "Pregunta", "Deseas, que se Guarde?")
                    if resp == True:

                        with open(path, "w", encoding="utf-8") as f:
                            f.write(ascii_text)

                        QMessageBox.information(self, "Guardado", "ASCII guardado correctamente.")

                    else:
                        pass

                except Exception as e:
                    print(e)

                finally:
                    os.remove(path_txt)

            else:

                with open(path, "w", encoding="utf-8") as f:
                    f.write(ascii_text)

                QMessageBox.information(self, "Guardado", "ASCII guardado correctamente.")

    # ---------------------------------------------------------
    # Impia la Caja de Texto y Restaura [CTRL+Q]
    # ---------------------------------------------------------
    def Clean(self):
    	ASCIIArtGenerator.clean(self)
    	ASCIIArtGenerator.clean(self)

    # ---------------------------------------------------------
    # Impia la Caja de Texto y Restaura
    # ---------------------------------------------------------
    def clean(self):

        self.image_path = None

        self.Generator_v2 = False
        self.Generator_v3 = False
        self.Generator_v4 = False
        self.Generator_v5 = False
        self.Generator_v6 = False

        self.color_ascii = "#000000"

        self.text_ascii.setText("")
        self.text_ascii.clear()
        self.slider.setValue(120)
        self.apply_style()

        self.text_ascii.setPlaceholderText("Fabor Ingresar Nueva Imagen para Ser Tratada...")

	# ---------------------------------------------------------
    # Guardar Imagen
    # ---------------------------------------------------------
    def save_image(self):

        if not self.text_ascii.toPlainText().strip():

            QMessageBox.warning(
                self,
                "Vacío",
                "No hay ASCII para exportar."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Imagen",
            "ascii_art.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )

        if not path:
            return

        # -----------------------------------------
        # Crear pixmap del tamaño del documento
        # -----------------------------------------

        document = self.text_ascii.document()

        width = int(document.size().width())
        height = int(document.size().height())

        pixmap = QPixmap(width, height)

        # Fondo negro
        ## pixmap.fill(Qt.white)

        # Fondo:
        color = QColor(self.color_ascii)   # Rojo con 50% de transparencia
        pixmap.fill(color)
        self.pixmap = pixmap

        # -----------------------------------------
        # Renderizar QTextEdit al pixmap
        # -----------------------------------------

        painter = None

        try:

            painter = QPainter(pixmap)
            document.drawContents(painter)

        finally:

            if painter:
                painter.end()

        resp = ASCIIArtGenerator.show_question(self, "Pregunta", "Deseas, Ver una Vista Previa?\nAntes de ser Guardado.")
        if resp == True:

            ASCIIArtGenerator.image_Preview(self, pixmap)
            resp = ASCIIArtGenerator.show_question(self, "Pregunta", "Deseas, que se Guarde?")

            if resp == True:

                # -----------------------------------------
                # Guardar imagen
                # -----------------------------------------

                success = pixmap.save(path)

                if success:

                    QMessageBox.information(
                        self,
                        "Guardado",
                        "Imagen exportada correctamente."
                    )

                    os.startfile(path)

                else:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "No se pudo guardar la imagen."
                    )

        else:
            # -----------------------------------------
            # Guardar imagen
            # -----------------------------------------

            success = pixmap.save(path)

            if success:

                QMessageBox.information(
                    self,
                    "Guardado",
                    "Imagen exportada correctamente."
                )

                os.startfile(path)

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo guardar la imagen."
                )

    def image_Preview(self, pixmap):

        try:

            # Como se Trae la Imagen en Pixeles, la Guardamos en Temporales...
            path_im = os.path.join(tempfile.gettempdir(), f"Image_Art [ASCII]_.png")
            pixmap.save(path_im, "PNG")

            name = "Image_Art [ASCII].png"

            #Imagen Path
            imagen_pil = Image.open(Path.resource_path(path_im))
            #Transformamos dicha Imagen para CV2
            image = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)
            #Extraemos el Nombre guardado para la Ventana Emergente de Previsualización de CV2
            x = f'Image:  {name}.-'
            #Hacemos la Ventana de CV2 Redimencionale
            cv2.namedWindow(f"{x}",cv2.WINDOW_NORMAL)
            # Para Ver la Imagen dentr de la Ventana Emergente Image de CV2
            cv2.imshow(f"{x}", image)
            #Cerramos la Ventana
            cv2.waitKey(0)

        except Exception as e:
            print(e)

        finally:
           os.remove(path_im)

    # ---------------------------------------------------------
    # Sefinir Color_Ascii
    # ---------------------------------------------------------
    def definir_color_Ascii(self):

	    color = QColorDialog.getColor()

	    if color.isValid():

	        self.color_ascii = color.name()

	        # Actualizar render automáticamente
	        self.update_ascii()

    # ---------------------------------------------------------
    # Metodo para Obtener Cualquier Tecla Pulsada dentro de la App.
    # ---------------------------------------------------------
    def keyPressEvent(self, event):

    	if event.key() == Qt.Key_Escape:
    		sys.exit()

    def cuestion_choise(self):

    	self.clean()
    	self.clean()

    	self.show_info('Respuesta', 'Empesare con el Ingreso, de los medios que Sean Seleccionados.')

    	# Crear un QMessageBox personalizado
    	msg_box = QMessageBox(self)
    	msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)


    	msg_box.setWindowTitle('--> Pregunta? <--')

        # Establecer el icono personalizado
    	self.Ico_wath = Path.resource_path('Ico\\1.png')
    	msg_box.setIconPixmap(QIcon(f'{self.Ico_wath}').pixmap(17, 17))

        # Establecer el texto del mensaje
    	msg_box.setText('Ingresar Imagenes, para su Tratamiento, [ASCII]')

        # Añadir botones personalizados
    	Opcion_01 = msg_box.addButton('   Imagen a ASCII-F01?   ', QMessageBox.YesRole)
    	Opcion_02 = msg_box.addButton('   Imagen a ASCII-F02?   ', QMessageBox.YesRole)
    	Opcion_03 = msg_box.addButton('   Imagen a ASCII-F03?   ', QMessageBox.YesRole)
    	Opcion_04 = msg_box.addButton('   Imagen a ASCII-F04?   ', QMessageBox.YesRole)
    	Opcion_05 = msg_box.addButton('   Imagen a ASCII-F05?   ', QMessageBox.YesRole)
    	Opcion_06 = msg_box.addButton('   Imagen a ASCII-F06?   ', QMessageBox.YesRole)

    	no_button = msg_box.addButton('  Ninguna Gracias  ', QMessageBox.NoRole)

        # Mostrar el mensaje y obtener la respuesta
    	reply = msg_box.exec_()

        # Manejar la respuesta
    	if msg_box.clickedButton() == Opcion_01:

            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

        # Manejar la respuesta
    	elif msg_box.clickedButton() == Opcion_02:

            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.Generator_v2 = True
            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

        # Manejar la respuesta
    	elif msg_box.clickedButton() == Opcion_03:

            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.Generator_v3 = True
            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

        # Manejar la respuesta
    	elif msg_box.clickedButton() == Opcion_04:

            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.Generator_v4 = True
            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

    	elif msg_box.clickedButton() == Opcion_05:
            
            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.Generator_v5 = True
            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

    	elif msg_box.clickedButton() == Opcion_06:
            
            try:

            	self.show_info('Aviso', 'Procede a Seleccionar Conque Caracteres-[🔥 ASCII], deseas la Imagen.\
\n✔️ Por Ejemplo:  "@%#*+=-:. "\n✔️ O bien:  "xo,*vzmnrs. "\n✔️ O bien:  "+=-;:,:zcvunxr. "\n✔️ O bien:  "oahkbdpqwm#*+=-;:,:zcvunxr. "\
\n✔️ O bien puede ser Una Tupla:  ("$@B%8&WM#*oahkbdpqwmZO0QLCJ"  "UYXzcvunxrjft/|()1{}[]?-_+~" "<>i!lI;:,\"^`. "#) ')
            	text = ASCIIArtGenerator.ASCII_CHARTER(self)
            	if text == "Ok":

            		self.Generator_v6 = True
            		self.open_image()
            		self.show_info('Respuesta', 'Procesando, Archivos Seleccionados.\nDe haberse Seleccionado, Archivos.')

            	else:
            		self.show_info('Información', 'No Ingresaste Ningun Caracter [🔥 ASCII], para Realizar el Dibujo.')
            		pass

            except Exception as e:
                print(e)

    	elif msg_box.clickedButton() == no_button:
            self.show_info('Respuesta', 'No se Selecciono ninguna Imagen para su Tratamiento [ASCII].\nVuelve a Intentarlo Despues.\nMuchas, Gracias.')

##==============================================================================================
##==============================================================================================

    def Choise_Save(self):

        # Crear un QMessageBox personalizado
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)


        msg_box.setWindowTitle('--> Pregunta? <--')

        # Establecer el icono personalizado
        self.Ico_wath = Path.resource_path('Ico\\1.png')
        msg_box.setIconPixmap(QIcon(f'{self.Ico_wath}').pixmap(17, 17))

        # Establecer el texto del mensaje
        msg_box.setText('Como deseas Guardar el Resuldo del Tratamiento, [ASCII]?')

        # Añadir botones personalizados
        Opcion_01 = msg_box.addButton('   Save File [*.TXT]?   ', QMessageBox.YesRole)
        Opcion_02 = msg_box.addButton('   Save File [*.Picture]?   ', QMessageBox.YesRole)

        no_button = msg_box.addButton('  Ninguna Gracias  ', QMessageBox.NoRole)

        # Mostrar el mensaje y obtener la respuesta
        reply = msg_box.exec_()

        # Manejar la respuesta
        if msg_box.clickedButton() == Opcion_01:

            try:
                
                self.save_txt()

            except Exception as e:
                print(e)

        # Manejar la respuesta
        elif msg_box.clickedButton() == Opcion_02:

            try:

                self.save_image()

            except Exception as e:
                print(e)

        elif msg_box.clickedButton() == no_button:
            self.show_info('Respuesta', 'No se Selecciono ninguna Imagen para su Tratamiento [ASCII].\nVuelve a Intentarlo Despues.\nMuchas, Gracias.')
            
    # =========================
    # Estilo a toda la App.
    # =========================
    def apply_style(self):

        self.setStyleSheet("""

        QDialog {
            background:#121212;
        }

        QLabel {
            color:white;
        }

        QLabel:first {
            font-size:20px;
            font-weight:bold;
            color:#00c3ff;
        }

        QTextEdit {
            background:#1e1e2f;
            color:#f1f1f1;
            border-radius:8px;
            padding:10px;
            font-size:10pt;
        }

        QPushButton {
            background:#1f1f2e;
            color:white;
            border-radius:10px;
            padding:8px;
            font-size:10px;
        }

        QPushButton:hover {
            background:#00c3ff;
            color:black;
        }

        """)

    # =========================
    # INPUT TEXT
    # =========================
    def show_input(self, titulo, texto):
        print(f"Estoy en: show_input\ncon Titulo: {titulo}\ny Texto: {texto}")

        dialog = QInputDialog(self)

        dialog.setWindowTitle(titulo)
        dialog.setLabelText(texto)

        dialog.setOkButtonText("Aceptar")
        dialog.setCancelButtonText("Cancelar")

        dialog.setStyleSheet("""
            QInputDialog {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
                font-size: 12px;
            }

            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
                min-width: 80px;
            }
        """)

        # =========================
        # ESTILO REAL DEL INPUT
        # =========================
        line_edit = dialog.findChild(QLineEdit)

        if line_edit:

            line_edit.setStyleSheet("""
                background-color: #1e1e1e;
                color: #00ff99;
                border: 1px solid #555;
                padding: 5px;
                selection-background-color: #0078d7;
                selection-color: white;
            """)

        ok = dialog.exec_()

        text = dialog.textValue()

        return text, ok

    # =========================
    # MENSAJE ERROR
    # =========================
    def show_error(self, titulo, texto):

        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)
        msg.setText(texto)

        msg.setIcon(QMessageBox.Critical)

        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
            }
        """)

        msg.exec_()

    # =========================
    # MENSAJES
    # =========================
    def show_info(self, titulo, texto):
        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)
        msg.setText(texto)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
            }
        """)

        msg.exec_()

    # =========================
    # MENSAJES
    # =========================
    def show_question(self, titulo, texto):
        msg = QMessageBox(self)

        msg.setWindowTitle(titulo)
        msg.setText(texto)

        msg.setIcon(QMessageBox.Question)

        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                padding: 6px;
            }
        """)

        respuesta = msg.exec_()

        return respuesta == QMessageBox.Yes

##====================================================================================
##====================================================================================

class app_info(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #-> Forma Uno (1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        #-> Forma Dos (2)
        #self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Información del Software")
        self.setFixedSize(520, 420)
        self.setModal(True)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- Título ---
        title = QLabel("Información del Software")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00A3FF;
            }
        """)
        layout.addWidget(title)

        # --- Texto informativo ---
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 ASCII Art Generator
Versión: V-7

Desarrollado por:
Cristian M. Veliz Cano

Descripción:

ASCII Art Generator es una herramienta visual desarrollada
en Python con PyQt5 que permite transformar imágenes
tradicionales en arte ASCII mediante distintos métodos
de renderizado y procesamiento gráfico.

El sistema incorpora múltiples motores ASCII capaces de
generar representaciones monocromáticas y en color,
permitiendo personalizar caracteres, resolución visual
y estilos de salida.

La aplicación fue diseñada con un enfoque artístico,
experimental y modular, ofreciendo una experiencia
ligera, visual y altamente configurable.

Características Principales:

✔ Conversión de imágenes a ASCII Art
✔ Renderizado ASCII en color RGB
✔ Conversión ASCII monocromática
✔ Múltiples motores de generación
✔ Personalización de caracteres ASCII
✔ Exportación TXT
✔ Exportación como imagen
✔ Selector dinámico de color de fondo
✔ Escalado visual mediante slider
✔ Interfaz moderna desarrollada en PyQt5

Tecnologías Utilizadas:

• Python 3
• PyQt5
• OpenCV
• NumPy
• Pillow (PIL)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Atajos Disponibles:
Ctrl + K  → Atajos de teclado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Licencia:
MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software y de los archivos de
documentación asociados, para utilizar el Software sin
restricción, incluyendo sin limitación los derechos de uso,
copia, modificación, fusión, publicación, distribución,
sublicencia y/o venta de copias del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.      → Cerrar aplicación 

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #F1F1F1;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 8px;
                font-size: 10.5pt;
            }
        """)
        layout.addWidget(info_text)

        # --- Botón cerrar ---
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        layout.addWidget(close_button)

##====================================================================================
##====================================================================================

class key_info(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        #-> Forma Uno (1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        #-> Forma Dos (2)
        #self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("Atajo de Teclas")
        self.setFixedSize(520, 420)
        self.setModal(True)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- Título ---
        title = QLabel("Atajo de Teclas")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: #00A3FF;
            }
        """)
        layout.addWidget(title)

        # --- Texto informativo ---
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText("""
Atajos de Teclado Disponibles:

• [CTRL + I]  → Abrir información del software
• [CTRL + K]  → Ver lista de atajos
• [CTRL + Q]  → Limpiar contenido / resultados
• [CTRL + O]  → Para indicar Imagen a ser tratada con [ASCII]
• [CTRL + G]  → Para Guardar Image_Art [ASCII] y\\o  [ASCII-ART].txt
• [CTRL + C]  → Para definir el Color de Fondo en la Imagen
• [CTRL + P]  → Nos muestra una Previsualización, en [*.txt | o | *.png]
• [CTRL + B]  → Remove BackGround [Quita el Fondo a las Imagenes] 
• [ESC]       → Cerrar aplicación

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Licencia:

MIT License

Software Open-Source orientado al aprendizaje,
experimentación y desarrollo didáctico.

Se permite:
✔ Uso libre
✔ Modificación
✔ Distribución
✔ Aprendizaje
✔ Mejora del código

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #F1F1F1;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                padding: 8px;
                font-size: 10.5pt;
            }
        """)
        layout.addWidget(info_text)

        # --- Botón cerrar ---
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(32)
        layout.addWidget(close_button)

##====================================================================================
##====================================================================================

class ASCIIArtGenerator_v2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii_v2(self):

        if not self.image_path:
            return

        width = self.slider.value()

        ascii_art = ASCIIArtGenerator_v2.convert_to_ascii_v2(self, 
            self.image_path,
            width
        )

        self.text_ascii.setHtml(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii_v2(self, path, new_width=120):
	    image = cv2.imread(path)
	    if image is None:
	        return "Error cargando imagen."

	    # BGR -> RGB
	    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	    # NumPy -> PIL
	    pil_image = Image.fromarray(image)

	    # -----------------------------------------
	    # Resize
	    # -----------------------------------------
	    width, height = pil_image.size
	    ratio = height / width
	    new_height = int(new_width * ratio * 0.55)
	    pil_image = pil_image.resize((new_width, new_height))

	    # -----------------------------------------
	    # RGB original
	    # -----------------------------------------
	    color_array = np.array(pil_image)

	    # -----------------------------------------
	    # Escala de grises
	    # -----------------------------------------
	    gray_image = pil_image.convert("L")
	    gray_array = np.array(gray_image)

	    # -----------------------------------------
	    # Mejora automática de contraste
	    # -----------------------------------------
	    gray_array = cv2.equalizeHist(gray_array)

	    # -----------------------------------------
	    # Ajustar contraste
	    # -----------------------------------------
	    gray_array = cv2.convertScaleAbs(gray_array, alpha=1.5, beta=0)

	    # -----------------------------------------
	    # HTML ASCII
	    # -----------------------------------------
	    ## background-color:black;
	    ## background-color:white;
	    ## background-color:#EAEAEA;

	    ascii_html = f"""
	    <html>
	    <body style="
	        background-color:{self.color_ascii};
	        color:white;
	        font-family:'Courier New';
	        font-size:6pt;
	        line-height:6px;
	        white-space: pre;
	    ">
	    """

	    for y in range(gray_array.shape[0]):
	        for x in range(gray_array.shape[1]):
	            pixel = gray_array[y, x]
	            r, g, b = color_array[y, x]
	            index = pixel * (len(self.ASCII_CHARS) - 1) // 255
	            char = self.ASCII_CHARS[index]
	            ascii_html += (
	                f'<span style="color:rgb({r},{g},{b});">'
	                f'{char}'
	                f'</span>'
	            )
	        ascii_html += "<br>"

	    ascii_html += "</body></html>"

	    return ascii_html

##====================================================================================
##====================================================================================

class ASCIIArtGenerator_v3(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii_v3(self):

        if not self.image_path:
            return

        width = self.slider.value()

        ascii_art = ASCIIArtGenerator_v3.convert_to_ascii_v3(self, 
            self.image_path,
            width
        )

        self.text_ascii.setHtml(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii_v3(self, path, new_width=120):

	    image = cv2.imread(path)

	    if image is None:
	        return "Error cargando imagen."

	    # BGR -> RGB
	    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	    # NumPy -> PIL
	    pil_image = Image.fromarray(image)

	    # -----------------------------------------
	    # Resize
	    # -----------------------------------------

	    width, height = pil_image.size

	    ratio = height / width

	    new_height = int(new_width * ratio * 0.55)

	    pil_image = pil_image.resize(
	        (new_width, new_height)
	    )

	    # -----------------------------------------
	    # RGB original
	    # -----------------------------------------
	    color_array = np.array(pil_image)

	    # -----------------------------------------
	    # Escala de grises
	    # -----------------------------------------
	    gray_image = pil_image.convert("L")
	    gray_array = np.array(gray_image)

		# -----------------------------------------
		# Mejora automática de contraste
		# -----------------------------------------
	    gray_array = cv2.equalizeHist(gray_array)

	    # -----------------------------------------
	    # HTML ASCII
	    # -----------------------------------------
	    ## background-color:black;
	    ## background-color:white;
	    ## background-color:#EAEAEA;

	    ascii_html = f"""
	    <html>
	    <body style="
	    	background-color:{self.color_ascii};
	        color:white;
	        font-family:'Courier New';
	        font-size:6pt;
	        line-height:6px;
	        white-space: pre;
	    ">
	    """

	    for y in range(gray_array.shape[0]):

	        for x in range(gray_array.shape[1]):

	            pixel = gray_array[y, x]
	            r, g, b = color_array[y, x]
	            index = pixel * (len(self.ASCII_CHARS) - 1) // 255
	            char = self.ASCII_CHARS[index]

	            ascii_html += (
	                f'<span style="color:rgb({r},{g},{b});">'
	                f'{char}'
	                f'</span>'
	            )

	        ascii_html += "<br>"

	    ascii_html += "</body></html>"

	    return ascii_html

##====================================================================================
##====================================================================================

class ASCIIArtGenerator_v4(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii_v4(self):

        if not self.image_path:
            return

        width = self.slider.value()

        ascii_art = ASCIIArtGenerator_v4.convert_to_ascii_v4(self, 
            self.image_path,
            width
        )

        self.text_ascii.setHtml(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii_v4(self, path, new_width=120):

	    image = cv2.imread(path)

	    if image is None:
	        return "Error cargando imagen."

	    # BGR -> RGB
	    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	    # NumPy -> PIL
	    pil_image = Image.fromarray(image)

	    # -----------------------------------------
	    # Resize
	    # -----------------------------------------

	    width, height = pil_image.size
	    ratio = height / width
	    new_height = int(new_width * ratio * 0.55)

	    pil_image = pil_image.resize(
	        (new_width, new_height)
	    )

	    # -----------------------------------------
	    # RGB original
	    # -----------------------------------------
	    color_array = np.array(pil_image)

	    # -----------------------------------------
	    # Escala de grises
	    # -----------------------------------------
	    gray_image = pil_image.convert("L")
	    gray_array = np.array(gray_image)

		# -----------------------------------------
		# Mejora automática de contraste
		# -----------------------------------------
	    gray_array = cv2.equalizeHist(gray_array)

	    # -----------------------------------------
	    # HTML ASCII
	    # -----------------------------------------
	    ## background-color:black;
	    ## background-color:white;
	    ## background-color:#EAEAEA;

	    ascii_html = f"""
	    <html>
	    <body style="
	        background-color:{self.color_ascii};
	        color:white;
	        font-family:'Courier New';
	        font-size:6pt;
	        line-height:6px;
	        white-space: pre;
	    ">
	    """

	    for y in range(gray_array.shape[0]):

	        for x in range(gray_array.shape[1]):

	            pixel = gray_array[y, x]
	            r, g, b = color_array[y, x]
	            index = pixel * (len(self.ASCII_CHARS) - 1) // 255
	            char = self.ASCII_CHARS[index]

	            ascii_html += (
	                f'<span style="color:rgb({r},{g},{b});">'
	                f'{char}'
	                f'</span>'
	            )

	        ascii_html += "<br>"

	    ascii_html += "</body></html>"

	    return ascii_html

##====================================================================================
##====================================================================================

class ASCIIArtGenerator_v5(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii_v5(self):

        if not self.image_path:
            return

        width = self.slider.value()

        ascii_art = ASCIIArtGenerator_v5.convert_to_ascii_v5(self, 
            self.image_path,
            width
        )

        self.text_ascii.setPlainText(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii_v5(self, path, new_width=120):

        # ---------------------------------------------
        # OpenCV carga imagen
        # ---------------------------------------------
        image = cv2.imread(path)

        if image is None:
            return "Error cargando imagen."

        # ---------------------------------------------
        # BGR -> RGB
        # ---------------------------------------------
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # ---------------------------------------------
        # NumPy array -> PIL
        # ---------------------------------------------
        pil_image = Image.fromarray(image)

        # ---------------------------------------------
        # Resize
        # ---------------------------------------------

        width, height = pil_image.size
        ratio = height / width
        new_height = int(new_width * ratio * 0.55)

        pil_image = pil_image.resize(
            (new_width, new_height)
        )

        # ---------------------------------------------
        # Escala de grises
        # ---------------------------------------------
        pil_image = pil_image.convert("L")

        # ---------------------------------------------
        # PIL -> NumPy
        # ---------------------------------------------
        image_array = np.array(pil_image)

        # ---------------------------------------------
        # Generar ASCII
        # ---------------------------------------------
        ascii_image = ""

        for row in image_array:

            for pixel in row:

                index = pixel * (len(self.ASCII_CHARS) - 1) // 255
                ascii_image += self.ASCII_CHARS[index]

            ascii_image += "\n"

        return ascii_image

##====================================================================================
##====================================================================================

class ASCIIArtGenerator_v6(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
    def resize_image_v6(self, image, new_width=100):
	    """
	    Redimensiona manteniendo proporción.
	    """
	    width, height = image.size
	    ratio = height / width

	    # Ajuste especial para texto terminal
	    new_height = int(new_width * ratio * 0.55)
	    resized = image.resize((new_width, new_height))

	    return resized


    def grayify_v6(self, image):
	    """
	    Convierte imagen a escala de grises.
	    """
	    return image.convert("L")


    def pixels_to_ascii_v6(self, image):
	    """
	    Convierte píxeles a caracteres ASCII.
	    """
	    pixels = image.getdata()

	    ascii_str = ""

	    for pixel in pixels:

	        # pixel va de 0 a 255
	        index = pixel * (len(self.ASCII_CHARS) - 1) // 255
	        ascii_str += self.ASCII_CHARS[index]

	    return ascii_str

    # ---------------------------------------------------------
    # Actualizar ASCII
    # ---------------------------------------------------------

    def update_ascii_v6(self):

        if not self.image_path:
            return

        width = self.slider.value()

        ascii_art = ASCIIArtGenerator_v6.convert_to_ascii_v6(self, 
            self.image_path,
            width
        )

        self.text_ascii.setPlainText(ascii_art)
        print(ascii_art)

    # ---------------------------------------------------------
    # Conversión principal
    # ---------------------------------------------------------

    def convert_to_ascii_v6(self, path, width=120):

	    try:
	        image = Image.open(path)

	    except Exception as e:
	        print("Error al abrir imagen:", e)
	        return

	    # Redimensionar
	    image = ASCIIArtGenerator_v6.resize_image_v6(self, image, width)

	    # Escala de grises
	    image = ASCIIArtGenerator_v6.grayify_v6(self, image)

	    # ASCII
	    ascii_data = ASCIIArtGenerator_v6.pixels_to_ascii_v6(self, image)

	    # Reconstrucción por líneas
	    pixel_count = len(ascii_data)

	    ascii_image = ""

	    for i in range(0, pixel_count, width):
	        ascii_image += ascii_data[i:i+width] + "\n"

	    return ascii_image

##====================================================================================
##====================================================================================

class Previews_Files(ASCIIArtGenerator):

    def __init__(self, parent=None):
        super().__init__(parent)

    def file_temp_question(self):

        # Crear un QMessageBox personalizado
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #00c3ff;
                color: black;
            }
        """)


        msg_box.setWindowTitle('--> Pregunta? <--')

        # Establecer el icono personalizado
        self.Ico_wath = Path.resource_path('Ico\\1.png')
        msg_box.setIconPixmap(QIcon(f'{self.Ico_wath}').pixmap(17, 17))

        # Establecer el texto del mensaje
        msg_box.setText('Deseas ver Una Previsualización?')

        # Añadir botones personalizados
        Opcion_01 = msg_box.addButton('   Previsualizar en: [*.TXT]?   ', QMessageBox.YesRole)
        Opcion_02 = msg_box.addButton('   Previsualizar en: [*.Picture]?   ', QMessageBox.YesRole)

        no_button = msg_box.addButton('  Ninguna Gracias  ', QMessageBox.NoRole)

        # Mostrar el mensaje y obtener la respuesta
        reply = msg_box.exec_()

        # Manejar la respuesta
        if msg_box.clickedButton() == Opcion_01:

            try:
                
                Previews_Files.file_temp_txt(self)

            except Exception as e:
                print(e)

        # Manejar la respuesta
        elif msg_box.clickedButton() == Opcion_02:

            try:

                Previews_Files.file_temp_img(self)

            except Exception as e:
                print(e)

        elif msg_box.clickedButton() == no_button:
            self.show_info('Respuesta', 'No se Selecciono ninguna Imagen para su Tratamiento [ASCII].\nVuelve a Intentarlo Despues.\nMuchas, Gracias.')
            

    def file_temp_txt(self):

        if not self.text_ascii.toPlainText().strip():

            QMessageBox.warning(
                self,
                "Vacío",
                "No hay ASCII para exportar."
            )

        ascii_text = self.text_ascii.toPlainText()

        try:

            # Guardamos en Temporales...
            path_txt = os.path.join(tempfile.gettempdir(), f"[ASCII-ART].txt")

            with open(path_txt, "w", encoding="utf-8") as f:
                f.write(ascii_text)

            TXT_Lec.Frame_TXT_Lec(self, path_txt)

        except Exception as e:
            print(e)

        finally:
            os.remove(path_txt)

    def file_temp_img(self):

        if not self.text_ascii.toPlainText().strip():

            QMessageBox.warning(
                self,
                "Vacío",
                "No hay ASCII para exportar."
            )

            return

        # Guardamos en Temporales...
        path_txt = os.path.join(tempfile.gettempdir(), f"[ASCII-ART].txt")

        # -----------------------------------------
        # Crear pixmap del tamaño del documento
        # -----------------------------------------

        document = self.text_ascii.document()

        width = int(document.size().width())
        height = int(document.size().height())

        pixmap = QPixmap(width, height)

        # Fondo negro
        ## pixmap.fill(Qt.white)

        # Fondo:
        color = QColor(self.color_ascii)   # Rojo con 50% de transparencia
        pixmap.fill(color)

        # -----------------------------------------
        # Renderizar QTextEdit al pixmap
        # -----------------------------------------

        painter = None

        try:

            painter = QPainter(pixmap)
            document.drawContents(painter)

        finally:

            if painter:
                painter.end()
        
        ASCIIArtGenerator.image_Preview(self, pixmap)

##====================================================================================
##====================================================================================

class TXT_Lec(ASCIIArtGenerator):

    def __init__(self, parent=None):
        super().__init__(parent)

    def Frame_TXT_Lec(self, output_path):

        dialog = QDialog(self)
        dialog.setWindowTitle("Contenido del Archivo")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.center_on_screen()

        layout = QVBoxLayout()
        dialog.setLayout(layout)

        fpath, fname = os.path.split(output_path)
        label = QLabel(f'Nombre del Texto: -> {fname}')
        layout.addWidget(label)

        # Create Font Size, Font Bold, Font Wieight, Font PonintSize
        self.font_txt = QtGui.QFont("Courier New")
        self.font_txt.setPointSize(6)
        self.font_txt.setBold(True)
        self.font_txt.setWeight(50)

        self.editor = QPlainTextEdit()
        self.editor.setFont(self.font_txt)
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0 )

        layout.addWidget(self.editor)

        try:

            try:

                with open(output_path, 'r') as f:
                    text = f.read()

                    print(text)
                    self.editor.setPlainText(text)

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)

            try:

                with open(output_path, 'r', encoding="utf-8") as f:
                    text = f.read()

                    print(text)
                    self.editor.setPlainText(text)

            except Exception as e:
                print(e)

        dialog.exec_()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = self.width(), self.height()
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, 300, 200)

##====================================================================================
##====================================================================================

class remove_backGroud(ASCIIArtGenerator):

    def __init__(self, parent=None):
        super().__init__(parent)

    def remover_Fondo(self):

        self.show_info('Aviso', 'Fabor de Uvicar la Imagen a Ser Tratada, con Remove BoacGround.\nMuchas, Gracias.')
        in_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not in_path:
            self.show_info('Aviso', 'No, se selecciono ninguna Imagen para Ser Tratada.\nNo se Hara Nada...')
            return

        self.show_info('Aviso', 'Fabor de Uvicar Un Directorio de Salida para la Imagen Tratada, con Remove BoacGround.\nMuchas, Gracias.')
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Imagen",
            "ascii_art.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )

        if not output_path:
            self.show_info('Aviso', 'No, se Selecciono, ningun Directorio para Guardar la Imagen Ya Tratada.\nNo se Hara Nada...')
            return

        try:


            input = Image.open(in_path)
            output = bg.remove(input)
            output.save(output_path, "PNG", optimize = True, quality = 150)

            self.show_info('Aviso', f'Se Informa que la Imagen Tratada, con Remove BoacGround.\
\nA sido Guardada Exitosamente en el directorio:\n{output_path}.\nMuchas, Gracias.')

            os.startfile(output_path)

        except Exception as e:
            print(e)

            #self.texto_lbl(msn)  
            PDFCreator.show_error(self, "Error...",
                f'Ha Ocurrido un Error, el Error es:\n'
                f'{e}\n\n'
                f'Procede a Intentarlo Nuevamente\n\n'
                f'Muchas Gracias...'
            )

##====================================================================================
##                                  MAIN
##====================================================================================


if __name__ == "__main__":

	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	window = ASCIIArtGenerator()
	window.show()

	sys.exit(app.exec_())

##====================================================================================
##====================================================================================