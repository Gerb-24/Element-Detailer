import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon
from compile import detailMultipleElements
from filemanagement import load_file, save_settings, load_settings, new_file, save_elementToDetailList
import json
from copy import deepcopy


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle("Element Detailer")
        self.setWindowIcon(QIcon('ui_images/appicon.ico'))
        self.setFixedSize(self.size())

        self.prototypePath = "./prototypes"
        # self.prototypePath = os.path.join(os.getcwd(), "prototypes")
        self.edPath = ""

        # core variables
        self.fileName = ""
        self.elementToDetailList = []


        # saving variables
        self.dirName = ""
        self.textureVariableFileName = ""


        self.prototypeVMF = ""
        self.method = ""
        self.methodBtnDict = {
            "top":              self.topBtn,
            "side":             self.sideBtn,
            "bigside":          self.bigsideBtn,
            "corner":           self.cornerBtn,
        }
        self.texture = ""

        self.data = [
                        {
                            "prt": self.prototypeLe_1,
                            "mtd": self.methodLe_1,
                            "tex": self.textureLe_1,
                            "rmv": self.removeBtn_1,
                        },


                        {
                            "prt": self.prototypeLe_2,
                            "mtd": self.methodLe_2,
                            "tex": self.textureLe_2,
                            "rmv": self.removeBtn_2,
                        },


                        {
                            "prt": self.prototypeLe_3,
                            "mtd": self.methodLe_3,
                            "tex": self.textureLe_3,
                            "rmv": self.removeBtn_3,
                        },


                        {
                            "prt": self.prototypeLe_4,
                            "mtd": self.methodLe_4,
                            "tex": self.textureLe_4,
                            "rmv": self.removeBtn_4,
                        },


                        {
                            "prt": self.prototypeLe_5,
                            "mtd": self.methodLe_5,
                            "tex": self.textureLe_5,
                            "rmv": self.removeBtn_5,
                        },


                        {
                            "prt": self.prototypeLe_6,
                            "mtd": self.methodLe_6,
                            "tex": self.textureLe_6,
                            "rmv": self.removeBtn_6,
                        },


                        {
                            "prt": self.prototypeLe_7,
                            "mtd": self.methodLe_7,
                            "tex": self.textureLe_7,
                            "rmv": self.removeBtn_7,
                        },

                        {
                            "prt": self.prototypeLe_8,
                            "mtd": self.methodLe_8,
                            "tex": self.textureLe_8,
                            "rmv": self.removeBtn_8,
                        },

                        {
                            "prt": self.prototypeLe_9,
                            "mtd": self.methodLe_9,
                            "tex": self.textureLe_9,
                            "rmv": self.removeBtn_9,
                        },

                        {
                            "prt": self.prototypeLe_10,
                            "mtd": self.methodLe_10,
                            "tex": self.textureLe_10,
                            "rmv": self.removeBtn_10,
                        },

                        {
                            "prt": self.prototypeLe_11,
                            "mtd": self.methodLe_11,
                            "tex": self.textureLe_11,
                            "rmv": self.removeBtn_11,
                        },

                        {
                            "prt": self.prototypeLe_12,
                            "mtd": self.methodLe_12,
                            "tex": self.textureLe_12,
                            "rmv": self.removeBtn_12,
                        },

                        {
                            "prt": self.prototypeLe_13,
                            "mtd": self.methodLe_13,
                            "tex": self.textureLe_13,
                            "rmv": self.removeBtn_13,
                        },
                    ]

        with open("cssfiles/removestyle.css", "r") as f:
            removeStyle = f.read()

        for elem in self.data:
            elem["rmv"].setStyleSheet(removeStyle)

        self.setMethod("side")


        self.fileNameBtn.clicked.connect(lambda: load_file(self, type="fileName", relpath=self.dirName, filetype="VMF(*.vmf)"))
        self.prototypeBtn.clicked.connect(lambda: load_file(self, type="prototype", relpath=self.dirName, filetype="VMF(*.vmf)"))
        self.loadTexVarBtn.clicked.connect(lambda: load_file(self, type="texvar", relpath=self.dirName, filetype="JSON(*.json)") )
        self.edPathBtn.clicked.connect(lambda: load_file(self, type="edPath", relpath=self.prototypePath, filetype="ED(*.ed)") )
        self.settingsBtn.clicked.connect(lambda: save_settings(self))
        self.queueBtn.clicked.connect(lambda: save_elementToDetailList(self))
        self.newPrototypeBtn.clicked.connect(lambda: new_file(self))

        self.sideBtn.clicked.connect(lambda: self.setMethod("side"))
        self.topBtn.clicked.connect(lambda: self.setMethod("top"))
        self.cornerBtn.clicked.connect(lambda: self.setMethod("corner"))
        self.bigsideBtn.clicked.connect(lambda: self.setMethod("bigside"))

        self.addBtn.clicked.connect( self.addToList )


        self.textureLe.textChanged.connect(lambda: self.setTexture(self.textureLe.text()))

        self.compileBtn.clicked.connect( self.compile )

        load_settings( self )
        self.rerenderList()
        self.fileNameLe.setText(os.path.basename(self.fileName))
        self.edPathLe.setText(self.edPath)

    def setTexture( self, texture ):
        self.texture = texture

    def setMethod( self, method ):
        self.method = method
        offStyle = '''
        QPushButton {
            background-color: #34495e;
            border-radius: 5px;
        }
        QPushButton::hover {
            background-color: #7f8c8d;
            border-radius: 5px;
        }
        '''
        onStyle = '''
        QPushButton {
            background-color: #f1c40f;
            border-radius: 5px;
            color: #34495e;
        }
        '''
        methodStyleDict = {
            "top":              offStyle,
            "side":             offStyle,
            "corner":           offStyle,
            "bigside":          offStyle,
        }

        methodStyleDict[method] = onStyle
        for key in self.methodBtnDict:
            self.methodBtnDict[key].setStyleSheet(methodStyleDict[key])


    def addToList( self ):
        try:

            element = {
                "prt": self.prototypeVMF,
                "tex": self.texture,
                "mtd": self.method,
            }
            # element = ElementToDetail(self.prototypeVMF, actual_texture, method=self.method)
            self.elementToDetailList.append(element)
            self.rerenderList()

            # clear variables
            self.prototypeVMF = ""
            self.texture = ""
            self.prototypeLe.setText("")
            self.textureLe.setText("")
        except Exception:
            print(traceback.format_exc())

    def compile( self ):
        try:
            # First we will need to change the texture variable into the actual texture
            preElementToDetailList = deepcopy(self.elementToDetailList)
            with open(self.textureVariableFileName, "r") as f:
                textureVariables = json.loads(f.read())
            textureVariablesDict = { elem["var"]: elem["tex"] for elem in textureVariables }
            for elem in preElementToDetailList:
                texture = elem["tex"]
                try:
                    actual_texture = textureVariablesDict[elem["tex"]]
                except Exception:
                    actual_texture = elem["tex"]
                elem["tex"] = actual_texture

            actualPreElementToDetailList = preElementToDetailList.copy()
            for elem in actualPreElementToDetailList:
                elem["prt"] = os.path.join( self.prototypePath, elem["prt"] )
            detailMultipleElements(self.fileName, preElementToDetailList)
            self.compileBtn.setText("Done")
        except Exception:
            print(traceback.format_exc())

    def createItem( self, index, element ):
        prt, mtd, tex, rmv = self.data[index].values()
        prt.setEnabled(True)
        mtd.setEnabled(True)
        tex.setEnabled(True)
        rmv.setEnabled(True)
        prt.setText(os.path.basename(element["prt"]))
        mtd.setText(element["mtd"])
        tex.setText(element["tex"])
        rmv.setText("remove")
        rmv.clicked.connect(lambda: self.removeItem(index))

    def removeItem( self, index ):
            try:
                self.elementToDetailList.pop(index)
                self.rerenderList()
            except Exception:
                print(traceback.format_exc())

    def rerenderList( self ):
        # Clear List
        for elem in self.data:
            for item in elem.values():
                item.setEnabled(False)
            elem["rmv"].setText("")
            # We only want to connect one signal
            try:
                elem["rmv"].clicked.disconnect()
            except Exception:
                pass

        # Rerender
        for index, element in enumerate(self.elementToDetailList):
            self.createItem( index, element )

        if len(self.data) == len(self.elementToDetailList):
            self.addBtn.setEnabled(False)
        else:
            self.addBtn.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(open('cssfiles/stylesheet.css').read())

    window = MyApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(' Closing Window ... ')
