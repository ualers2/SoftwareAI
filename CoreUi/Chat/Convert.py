
########################################################################
# IMPORT Libs 
import subprocess
import os
import shutil
########################################################################



def convert_and_move_src():
    comand = [
        "Custom_Widgets", "--convert-ui", "ui", "--qt-library", "PySide2"
    ]
    subprocess.run(comand, shell=True)
    src_list = os.listdir("src")
    for src_ in src_list:    
        shutil.copy(f"src\{src_}", f"src_")

    shutil.rmtree("src")
convert_and_move_src()
