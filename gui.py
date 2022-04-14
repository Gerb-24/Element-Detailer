import sys
import traceback
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QIcon
from main import detailMultipleElements, ElementToDetail
from filemanagement import load_vmf


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


        self.prototypeVMF = ""
        self.method = ""
        self.texture = ""

        self.setMethod("side")


        self.fileNameBtn.clicked.connect(lambda: load_vmf(self, type="fileName"))
        self.prototypeBtn.clicked.connect(lambda: load_vmf(self, type="prototype"))

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
            element = ElementToDetail(self.prototypeVMF, self.texture, method=self.method)
            self.elementToDetailList.append(element)
            self.elementList.addItem(element.asString())

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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(open('stylesheet.css').read())

    window = MyApp()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print(' Closing Window ... ')
