"""
AutoTroisBras
Manu Cheremeh, Version 1.0, July 2022
@author = Manu Cheremeh
version = 1.0
"""
import os
import sys

from PySide2 import QtGui, QtCore, QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as apiUI


def get_main_window():
    """Get the maya window pointer to parent the main window inside maya"""
    ptr = omui.MQtUtil.mainWindow()
    maya_window = wrapInstance(int(ptr), QtWidgets.QWidget)
    return maya_window


class Main(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # self.main_controller = MainController()

        self.setObjectName('auto_trois_bras')

        self.setWindowTitle('Auto Trois Bras')
        self.setGeometry(500, 500, 450, 300)

    def build(self):
        pass

    def connect(self):
        pass

    def action(self):
        pass


if __name__ == '__main__':
    main_window = get_main_window()
    tool = Main(main_window)
    tool.show()

    # stylesheet
    # with open(os.path.dirname(__file__) + "/resources/stylesheet/style.css", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)
    # sys.exit(app.exec_())
