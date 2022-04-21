from PyQt6.QtWidgets import QFileDialog
from main import ElementToDetail
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
            with open(filepath, "r") as f:
                data = json.loads(f.read())
            new_data = {elem["var"]: elem["tex"] for elem in data }
            new_data_inv = {elem["tex"]: elem["var"] for elem in data }
            self.texvar = new_data
            self.texvarInverse = new_data_inv
            self.loadTexVarBtn.setText("Texture Variables Loaded")
            self.loadTexVarBtn.setStyleSheet( open('cssfiles/loadedstyle.css', 'r').read() )

# def save_vmf_dir(self, filepath):
#     dirName = os.path.dirname(filepath)
#     self.dirName = dirName
#     with open("settings.txt", "w") as text:
#         save_tex_dict = {
#         'dirName':      self.dirName,
#         'topTexture':   self.topTexture,
#         'sideTexture':  self.sideTexture,
#         }
#         text.writelines(str(save_tex_dict))
#         text.close()
#
def save_settings(self):
    elementToDetailListSerialized = [ element.serialize() for element in self.elementToDetailList ]
    save_data = {
    'dirName':                          self.dirName,
    'texvar':                           self.texvar,
    'elementToDetailListSerialized':    elementToDetailListSerialized
    }
    json_data = json.dumps( save_data, indent=2 )
    with open("settings.json", "w") as f:
        f.write(json_data)


def load_settings(self):
    with open("settings.json", "r") as f:
        load_data = json.loads(f.read())
    self.dirName = load_data["dirName"]
    self.texvar = load_data["texvar"]
    self.texvarInverse = { element[1]: element[0] for element in load_data["texvar"].items()}
    if self.texvar != {}:
        self.loadTexVarBtn.setText("Texture Variables Loaded")
        self.loadTexVarBtn.setStyleSheet( open('cssfiles/loadedstyle.css', 'r').read() )
    elementToDetailListSerialized = load_data["elementToDetailListSerialized"]
    self.elementToDetailList = [ ElementToDetail(*serializedElement) for serializedElement in elementToDetailListSerialized ]
