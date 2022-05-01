from PyQt6.QtWidgets import QFileDialog
from classes import ElementToDetail
import ast
import os
import json

def load_file(self, type="fileName"):
    filetype = "JSON(*.json)" if (type == "texvar") else "VMF(*.vmf)"
    filepath, _ = QFileDialog.getOpenFileName(self, "Load File", self.dirName, filetype)
    if filepath == "":
        return
    else:
        if type == "fileName":
            self.fileName = filepath
            self.fileNameLe.setText(os.path.basename(filepath))
        elif type == "prototype":
            self.prototypeVMF = filepath
            self.prototypeLe.setText(os.path.basename(filepath))
        elif type == "texvar":
            self.textureVariableFileName = filepath
            self.loadTexVarBtn.setText("Texture Variables Loaded")
            self.loadTexVarBtn.setStyleSheet( open('cssfiles/loadedstyle.css', 'r').read() )


def save_settings(self):
    save_data = {
    'fileName':                 self.fileName,
    'textureVariableFileName':  self.textureVariableFileName,
    'elementToDetailList':      self.elementToDetailList
    }
    json_data = json.dumps( save_data, indent=2 )
    with open("settings.json", "w") as f:
        f.write(json_data)


def load_settings(self):
    with open("settings.json", "r") as f:
        load_data = json.loads(f.read())
    self.fileName = load_data["fileName"]
    self.textureVariableFileName = load_data["textureVariableFileName"]
    if self.textureVariableFileName != "":
        self.loadTexVarBtn.setText("Texture Variables Loaded")
        self.loadTexVarBtn.setStyleSheet( open('cssfiles/loadedstyle.css', 'r').read() )
    self.elementToDetailList = load_data["elementToDetailList"]

def new_file(self):
    filepath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "VMF(*.vmf)")
    if filepath == "":
        return
    prototype_filepath = f'prototypes/{ self.method }_prototype.vmf'
    with open(prototype_filepath, 'r') as f:
        prototype_text = f.read()
    with open(filepath, 'w') as f:
        f.write(prototype_text)
    self.prototypeVMF = filepath
    self.prototypeLe.setText(os.path.basename(filepath))
