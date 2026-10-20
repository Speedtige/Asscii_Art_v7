import hashlib
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Type
import download
import onnxruntime as ort

from session_base import BaseSession
from session_cloth import ClothSession
from session_simple import SimpleSession

import os, sys

class Path():

    ##(Dir. Raiz.)
    ## Solamente para obtener el Directorio donde se encuentra Ejecutandose la app.
    def resource_path_app():    ## Forma #2

        try:
            path_app = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

        except Exception as e:
            print(e)

        except IOError as error:
            print( error )

        return path_app

    ##==============================================================
    ##==============================================================

    def resource_path(relative_path):    ## Forma #1
        """Get absolute path to resource, works for dev and for pyinstaller"""

        try:
            #PyInstaller Create a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


def new_session(model_name: str) -> BaseSession:
    session_class: Type[BaseSession]

    if model_name == "u2netp":
        md5 = "8e83ca70e441ab06c318d82300c84806"
        url = "https://drive.google.com/uc?id=1tNuFmLv0TSNDjYIkjEdeH1IWKQdUA4HR"
        session_class = SimpleSession
    elif model_name == "u2net":
        md5 = "60024c5c889badc19c04ad937298a77b"
        url = "https://drive.google.com/uc?id=1tCU5MM1LhRgGou5OpmpjBQbSrYIUoYab"
        session_class = SimpleSession
    elif model_name == "u2net_human_seg":
        md5 = "c09ddc2e0104f800e3e1bb4652583d1f"
        url = "https://drive.google.com/uc?id=1ZfqwVxu-1XWC1xU1GHIP-FM_Knd_AX5j"
        session_class = SimpleSession
    elif model_name == "u2net_cloth_seg":
        md5 = "2434d1f3cb744e0e49386c906e5a08bb"
        url = "https://drive.google.com/uc?id=15rKbQSXQzrKCQurUjZFg8HqzZad8bcyz"
        session_class = ClothSession
    else:
        assert AssertionError(
            "Choose between u2net, u2netp, u2net_human_seg or u2net_cloth_seg"
        )

    bundle_dir = Path.resource_path_app()
    path = os.path.join(bundle_dir, ".u2net", "u2net.onnx")

    sess_opts = ort.SessionOptions()

    if "OMP_NUM_THREADS" in os.environ:
        sess_opts.inter_op_num_threads = int(os.environ["OMP_NUM_THREADS"])

    return session_class(
        model_name,
        ort.InferenceSession(
            str(path), providers=ort.get_available_providers(), sess_options=sess_opts
        ),
    )
