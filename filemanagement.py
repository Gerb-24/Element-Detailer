from PyQt6.QtWidgets import QFileDialog
from classes import ElementToDetail
import ast
import os
import json

def load_file(self, type="fileName", relpath="", filetype="TXT(*.txt)"):
    filepath, _ = QFileDialog.getOpenFileName(self, "Load File", relpath, filetype)
    if filepath == "":
        return
    else:
        if type == "fileName":
            self.fileName = filepath
            self.fileNameLe.setText(os.path.basename(filepath))
        elif type == "prototype":
            self.prototypeVMF = os.path.relpath(filepath, start=self.prototypePath)
            self.prototypeLe.setText(os.path.basename(filepath))
        elif type == "edPath":
            self.edPath = os.path.relpath(filepath, start=self.prototypePath)
            self.edPathLe.setText(self.edPath)
            load_elementToDetailList( self )
            self.rerenderList()
        elif type == "texvar":
            self.textureVariableFileName = filepath
            self.loadTexVarBtn.setText("Texture Variables Loaded")
            self.loadTexVarBtn.setStyleSheet( open('cssfiles/loadedstyle.css', 'r').read() )


def save_settings(self):
    save_data = {
    'fileName':                 self.fileName,
    'textureVariableFileName':  self.textureVariableFileName,
    'edPath':                   self.edPath
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
    self.edPath = load_data["edPath"]
    if self.edPath != "":
        with open( os.path.join(self.prototypePath, self.edPath ), 'r' ) as f:
            ed_load_data = json.loads(f.read())
        self.elementToDetailList = ed_load_data["elementToDetailList"]

def load_elementToDetailList(self):
    with open( os.path.join(self.prototypePath, self.edPath ), 'r' ) as f:
        ed_load_data = json.loads(f.read())
    self.elementToDetailList = ed_load_data["elementToDetailList"]

def save_elementToDetailList(self):
    save_data = {
    'elementToDetailList':      self.elementToDetailList
    }
    json_data = json.dumps( save_data, indent=2 )
    print( self.prototypePath, self.edPath  )
    with open( os.path.join(self.prototypePath, self.edPath ), 'w' ) as f:
        f.write(json_data)

def new_file(self):
    filepath, _ = QFileDialog.getSaveFileName(self, "Save File", self.prototypePath, "VMF(*.vmf)")
    if filepath == "":
        return
    prototype_filepath = f'prototypes/core/{ self.method }_prototype.vmf'
    with open(prototype_filepath, 'r') as f:
        prototype_text = f.read()
    with open(filepath, 'w') as f:
        f.write(prototype_text)
    self.prototypeVMF = os.path.relpath( filepath, start=self.prototypePath )
    self.prototypeLe.setText(os.path.basename(filepath))
