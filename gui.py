import sys
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon
from main import detailMultipleElements, ElementToDetail
from filemanagement import load_file


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle("Element Detailer")
        self.setWindowIcon(QIcon('appicon.ico'))
        self.setFixedSize(self.size())

        # core variables
        self.fileName = ""
        self.elementToDetailList = []

        # saving variables
        self.dirName = ""
        self.texvar = {}
        self.texvarInverse = {}

        self.prototypeVMF = ""
        self.method = ""
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
                    ]

        with open("cssfiles/removestyle.css", "r") as f:
            removeStyle = f.read()

        for elem in self.data:
            elem["rmv"].setStyleSheet(removeStyle)

        self.setMethod("side")


        self.fileNameBtn.clicked.connect(lambda: load_file(self, type="fileName"))
        self.prototypeBtn.clicked.connect(lambda: load_file(self, type="prototype"))
        self.loadTexVarBtn.clicked.connect(lambda: load_file(self, type="texvar") )

        self.sideBtn.clicked.connect(lambda: self.setMethod("side"))
        self.topBtn.clicked.connect(lambda: self.setMethod("top"))

        self.addBtn.clicked.connect( self.addToList )


        self.textureLe.textChanged.connect(lambda: self.setTexture(self.textureLe.text()))

        self.compileBtn.clicked.connect( self.compile )

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
            background-color: #3498db;
            border-radius: 5px;
        }
        '''

        if method == "side":
            self.topBtn.setStyleSheet(offStyle)
            self.sideBtn.setStyleSheet(onStyle)
        elif method == "top":
            self.sideBtn.setStyleSheet(offStyle)
            self.topBtn.setStyleSheet(onStyle)

    def addToList( self ):
        try:
            try:
                actual_texture = self.texvar[self.texture]
            except Exception:
                actual_texture = self.texture
            element = ElementToDetail(self.prototypeVMF, actual_texture, method=self.method)
            self.elementToDetailList.append(element)
            self.rerenderList()

            # clear variables
            self.prototypeVMF = ""
            self.texture = ""
            self.method = ""
            self.prototypeLe.setText("")
            self.textureLe.setText("")
        except Exception:
            print(traceback.format_exc())

    def compile( self ):
        try:
            detailMultipleElements(self.fileName, self.elementToDetailList)
            self.compileBtn.setText("Done")
        except Exception:
            print(traceback.format_exc())

    def createItem( self, index, element ):
        prt, mtd, tex, rmv = self.data[index].values()
        prt.setEnabled(True)
        mtd.setEnabled(True)
        tex.setEnabled(True)
        rmv.setEnabled(True)
        prt.setText(element.prototypeName)
        mtd.setText(element.method)
        try:
            tex.setText(self.texvarInverse[element.texture])
        except Exception:
            tex.setText(element.texture)
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




if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(open('cssfiles/stylesheet.css').read())

    window = MyApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(' Closing Window ... ')
