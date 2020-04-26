#### main file
'''
    Copyright (C) 2020 Oliver Rodriguez
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
#### @author oliverrdz
#### https://oliverrdz.xyz

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import mainWindow
import sol_fd as sol
import waveforms as wf
import numpy as np
import matplotlib.pyplot as plt

        # Connect all buttons:
        #self.btnSimulate.clicked.connect(self.clickSimulate)
        #self.btnPlot.clicked.connect(self.clickPlot)
        
        # Connect boundary conditions (radio buttons):
        #self.Nernst.toggled.connect(self.radioClicked)
        #self.Irrev.toggled.connect(self.radioClicked)
        #self.BV.toggled.connect(self.radioClicked)
        
        # Connect menu:
        #self.actionCV.triggered.connect(lambda: self.resetCV())

class App(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.bc_type = "Nernst" # By default, in case user does not select boundary condition

    def plot(self, X, Y, marker = "-", xlab = "$E$ / V", ylab = "$i$ / A"):
        plt.figure()
        plt.plot(X, Y, marker)
        plt.xlabel(xlab, fontsize = 18)
        plt.ylabel(ylab, fontsize = 18)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.grid()
        plt.tight_layout()

    
    def clickSimulate(self):
        # Sweep parameters:
        self.Eini = float(self.box_Eini.text())
        self.Efin = float(self.box_Efin.text())
        self.sr = float(self.box_sr.text())
        self.dE = float(self.box_dE.text())
        self.ns = int(self.box_ns.text())
        self.tini = 0
        
        # Electrochemsitry parameters:
        self.n = float(self.box_n.text())
        self.A = float(self.box_A.text())
        self.E0 = float(self.box_E0.text())
        self.COb = float(self.box_COb.text())
        self.CRb = float(self.box_CRb.text())
        self.DO = float(self.box_DO.text())
        self.DR = float(self.box_DR.text())
        self.ks = float(self.box_ks.text())
        self.alpha = float(self.box_alpha.text())
        self.Cd = float(self.box_Cd.text())
        self.Ru = float(self.box_Ru.text())
        
        params = [self.n, self.A, self.E0, self.COb, self.CRb, self.DO, self.DR, self.ks, self.alpha]
        CdRu = [self.Cd, self.Ru]
        
        self.t, self.E = wf.sweep(self.Eini, self.Efin, self.sr, self.dE, self.ns, self.tini)
        
        self.btnPlot.setEnabled(False) # In case the user wants to simulate again
        self.progressBar.setEnabled(True)
        self.i, self.x, self.cR, self.cO = sol.main(self.t, self.E, self.bc_type, params, CdRu, self.progressBar)
        self.progressBar.setValue(100)
        self.btnPlot.setEnabled(True)
        
    def radioClicked(self):
        radioBtn = self.sender()
        
        if radioBtn.isChecked():
            if radioBtn.objectName() == "Nernst":
                self.box_ks.setEnabled(False)
                self.box_alpha.setEnabled(False)
                self.bc_type = "Nernst"
            elif radioBtn.objectName() == "Irrev":
                self.box_ks.setEnabled(True)
                self.box_alpha.setEnabled(True)
                self.bc_type = "Irrev"
            elif radioBtn.objectName() == "BV":
                self.box_ks.setEnabled(True)
                self.box_alpha.setEnabled(True)
                self.bc_type = "BV"
    
    def clickPlot(self):
        print("Plotting")
        self.plot(self.E, self.i)
        plt.show()
        
    def resetCV(self):
        _translate = QtCore.QCoreApplication.translate
        self.box_Eini.setText(_translate("MainWindow", "-0.5"))
        self.box_Efin.setText(_translate("MainWindow", "0.5"))
        self.box_sr.setText(_translate("MainWindow", "1"))
        self.box_dE.setText(_translate("MainWindow", "0.01"))
        self.box_ns.setText(_translate("MainWindow", "2"))
        self.box_n.setText(_translate("MainWindow", "1"))
        self.box_A.setText(_translate("MainWindow", "1"))
        self.box_E0.setText(_translate("MainWindow", "0"))
        self.box_COb.setText(_translate("MainWindow", "0"))
        self.box_DO.setText(_translate("MainWindow", "1e-5"))
        self.box_DR.setText(_translate("MainWindow", "1e-5"))
        self.box_ks.setText(_translate("MainWindow", "1e-3"))
        self.box_alpha.setText(_translate("MainWindow", "0.5"))
        self.box_CRb.setText(_translate("MainWindow", "5e-6"))
        self.box_Cd.setText(_translate("MainWindow", "0"))
        self.box_Ru.setText(_translate("MainWindow", "0"))

        self.Nernst.setChecked(True)
        self.btnPlot.setEnabled(False)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 0)

def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    