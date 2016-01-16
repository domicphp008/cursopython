from cx_Freeze import setup, Executable
 
exe=Executable(
     script="PLAY.py",
     base="Win32Gui",
     )
includefiles=[('Imagens'), ('Musica'),
              ('Mapas'), ('Menus'), ('Modulos')]
includes= []
excludes=[]
packages=["sys", "xml.etree", "time", "random", "pygame"]
setup(
     version = "1.0",
     description = "Plataformer",
     author = "Pedro Forli e Ivan Veronezzi",
     name = "Cata Jóia",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )
