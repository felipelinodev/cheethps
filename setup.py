import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "darkdetect", "packaging"],
    "includes": ["customtkinter", "PIL"],
    "include_files": [
        "funcoes_app.py",
        "core.py",
        "tema.json",
        "dados.json", 
        "icone.ico",  
        "icone.png",  
        "logotipo.png" 

    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="cheethps",
    version="1.0",
    description="Gerenciador de Automação com Foco no Adobe Photoshop",
    options={"build_exe": build_exe_options},
    executables=[Executable("cheethps.py", base=base)]
)
