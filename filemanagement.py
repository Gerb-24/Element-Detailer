from PyQt6.QtWidgets import QFileDialog
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
# def save_tex(self):
#     with open("settings.txt", "w") as text:
#         save_tex_dict = {
#         'dirName':      self.dirName,
#         'topTexture':   self.topTexture,
#         'sideTexture':  self.sideTexture,
#         }
#         text.writelines(str(save_tex_dict))
#         text.close()
#
# def load_tex(self):
#     with open("settings.txt", "r") as text:
#         load_tex_dict = ast.literal_eval(text.readline())
#         self.dirName = load_tex_dict["dirName"]
#         self.topTextureLe.setText(load_tex_dict["topTexture"])
#         self.sideTextureLe.setText(load_tex_dict["sideTexture"])
