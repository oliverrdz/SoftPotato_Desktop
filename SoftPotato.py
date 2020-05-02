#### Main file for Soft Potato with graphical user interface
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
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
from SP_UI import Ui_MainWindow
from about import Ui_About

import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

import waveforms as wf
import solver as sol


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.statusBar().showMessage("Ready.")
        self.bc_type = "Nernst" # By default
        self.multSR = False
        
        ## Connect GUI widgets:
        
        # Generate and plot potential waveforms:
        self.btn_genSweep.clicked.connect(self.btnGenCV)
        self.btn_plotSweep.clicked.connect(self.btnPlotEt_CV)
        self.btn_genStep.clicked.connect(self.btnGenCA)
        self.btn_plotStep.clicked.connect(self.btnPlotEt_CA)
        self.btn_genSCV.clicked.connect(self.btnGenSCV)
        self.btn_plotSCV.clicked.connect(self.btnPlotEt_SCV)
        
        # Simulate and plot solution:
        self.btnSimulate.clicked.connect(self.btnSimulate_clicked)
        self.btnPlot.clicked.connect(self.btnPlot_clicked)
        
        # Animate solution:
        self.btnAnimate.clicked.connect(self.btnAnimate_clicked)
        
        # Connect boundary conditions (radio buttons):
        self.radBtn_Nernst.toggled.connect(self.radioClicked)
        self.radBtn_BV.toggled.connect(self.radioClicked)
        self.radBtn_Irrev.toggled.connect(self.radioClicked)
        
        # Check buttons:
        self.check_SecondStep.toggled.connect(self.step2Clicked)
        self.check_Mult_sr.toggled.connect(self.mult_sr)
        
        # Menu About:
        self.actionAbout.triggered.connect(lambda: self.open_About())
        self.actionWiki.triggered.connect(lambda: self.openWiki())
        
        # Menu File:
        self.actionSave_Current.triggered.connect(lambda: self.saveCurrent())
        self.actionSave_Waveform.triggered.connect(lambda: self.saveWaveform())
        self.actionSave_O.triggered.connect(lambda: self.saveO())
        self.actionSave_R.triggered.connect(lambda: self.saveR())
        self.actionSave_x.triggered.connect(lambda: self.saveX())
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)


    def open_About(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_About()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()
        
    def openWiki(self):
        url = QtCore.QUrl("https://github.com/oliverrdz/SoftPotato/wiki")
        QtGui.QDesktopServices.openUrl(url)

    def plotFormat(self, xlab, ylab):
        plt.xlabel(xlab, fontsize = 18)
        plt.ylabel(ylab, fontsize = 18)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.grid()
        plt.tight_layout()
        
    
    def plot(self, X, Y, xlab, ylab, marker="-"):
        plt.figure()
        plt.plot(X, Y, marker)
        self.plotFormat(xlab, ylab)
    
    
    ########## Buttons to generate and plot potential waveforms:
    
    ## Cyclic voltammetry:
    def btnGenCV(self):
        self.Et_type = "CV" # For the plot simuation button to know what to plot
        self.multSR = False
        # Sweep parameters:
        Eini = float(self.box_Eini.text())
        Efin = float(self.box_Efin.text())
        dE = float(self.box_dE.text())
        ns = int(self.box_ns.text())
        tini = 0
        # Generate Et:
        self.statusBar().showMessage("Generating potential waveform for CV")
        
        # Separates list of scan rates
        if self.check_Mult_sr.isChecked():
            srList = self.box_Mult_sr.toPlainText()
            srArray = np.asarray(srList.split("\n"))
            self.sr = np.zeros(np.size(srArray))
            nt = int(abs(Efin-Eini)/dE)
            self.t = np.zeros([nt*ns, np.size(self.sr)])
            for i in range(0,np.size(srArray)):
                self.sr[i] = float(srArray[i])
                t, self.E = wf.sweep(Eini, Efin, self.sr[i], dE, ns, tini)
                self.t[:,i] = t
            self.multSR = True
            
        else:
            sr = float(self.box_sr.text())
            self.t, self.E = wf.sweep(Eini, Efin, sr, dE, ns, tini)
        
        self.btn_plotSweep.setEnabled(True)
        self.btn_plotStep.setEnabled(False)
        self.btn_plotSCV.setEnabled(False)
        self.btnSimulate.setEnabled(True)
        self.btnPlot.setEnabled(False)
        self.btnAnimate.setEnabled(False)
        self.btnSimulate.setText("Simulate CV")
        self.btnPlot.setText("Plot CV")
        self.btnAnimate.setText("Animate CV")
        self.menuSave.setTitle("Save CV")
        self.statusBar().showMessage("Potential waveform for CV generated.")
    
    def btnPlotEt_CV(self):
        self.plot(self.t, self.E, xlab="$t$ / s", ylab="$E$ / V")
        plt.show()
    
    ## Chronoamperometry:
    def btnGenCA(self):
        self.Et_type = "CA"
        Estep = float(self.box_Estep.text())
        ttot = float(self.box_ttot.text())
        dt = float(self.box_dt.text())
        tini = 0
        # Generate Et
        self.statusBar().showMessage("Generating potential waveform for CA")
        self.t, self.E = wf.step(Estep, tini, ttot, dt)
        if self.check_SecondStep.isChecked():
            Estep2 = float(self.box_Estep2.text())
            ttot2 = float(self.box_ttot2.text())
            t2, E2 = wf.step(Estep2, self.t[-1], ttot2, dt)
            self.t = np.concatenate([self.t, t2])
            self.E = np.concatenate([self.E, E2])
            
        self.btn_plotSweep.setEnabled(False)
        self.btn_plotStep.setEnabled(True)
        self.btn_plotSCV.setEnabled(False)
        self.btnSimulate.setEnabled(True)
        self.btnPlot.setEnabled(False)
        self.btnAnimate.setEnabled(False)
        self.btnSimulate.setText("Simulate CA")
        self.btnPlot.setText("Plot CA")
        self.btnAnimate.setText("Animate CA")
        self.menuSave.setTitle("Save CA")
        self.statusBar().showMessage("Potential waveform for CA generated.")
    
    def btnPlotEt_CA(self):
        self.plot(self.t, self.E, xlab="$t$ / s", ylab="$E$ / V")
        plt.show()
    
    ## Sampled current voltammetry:
    def btnGenSCV(self):
        self.Et_type = "SCV"
        Eini = float(self.box_Eini_SCV.text())
        Efin = float(self.box_Efin_SCV.text())
        dE = float(self.box_dE_SCV.text())
        ttot = float(self.box_ttot_SCV.text())
        dt = float(self.box_dt_SCV.text())
        tini = 0
        # Generate Et:
        self.statusBar().showMessage("Generating potential waveform for CA")
        nE = int(abs(Efin-Eini)/dE)
        nt = int(ttot/dt)
        E = np.linspace(Eini, Efin, nE+1)
        
        self.E = np.ones([nt,nE+1])*E.T
        self.t = np.linspace(tini, ttot, nt)
        
        self.btn_plotSweep.setEnabled(False)
        self.btn_plotStep.setEnabled(False)
        self.btn_plotSCV.setEnabled(True)
        self.btnSimulate.setEnabled(True)
        self.btnPlot.setEnabled(False)
        self.btnAnimate.setEnabled(False)
        self.btnSimulate.setText("Simulate SCV")
        self.btnPlot.setText("Plot SCV")
        self.btnAnimate.setText("Animate SCV")
        self.menuSave.setTitle("Save SCV")
        self.statusBar().showMessage(str(nE+1) + " potential waveforms for SCV generated.")
    
    def btnPlotEt_SCV(self):
        self.plot(self.t, self.E, xlab="$t$ / s", ylab="$E$ / V")
        plt.show()
    
    def radioClicked(self):
        radioBtn = self.sender()
        
        if radioBtn.isChecked():
            if radioBtn.objectName() == "radBtn_Nernst":
                self.box_ks.setEnabled(False)
                self.box_alpha.setEnabled(False)
                self.bc_type = "Nernst"
            elif radioBtn.objectName() == "radBtn_Irrev":
                self.box_ks.setEnabled(True)
                self.box_alpha.setEnabled(True)
                self.bc_type = "Irrev"
            elif radioBtn.objectName() == "radBtn_BV":
                self.box_ks.setEnabled(True)
                self.box_alpha.setEnabled(True)
                self.bc_type = "BV"
    
    def step2Clicked(self):
        if self.check_SecondStep.isChecked():
            self.box_Estep2.setEnabled(True)
            self.box_ttot2.setEnabled(True)
        else:
            self.box_Estep2.setEnabled(False)
            self.box_ttot2.setEnabled(False)
    
    
    def mult_sr(self):
        if self.check_Mult_sr.isChecked():
            self.box_sr.setEnabled(False)
            self.box_Mult_sr.setEnabled(True)
        else:
            self.box_sr.setEnabled(True)
            self.box_Mult_sr.setEnabled(False)
        
    
    
    ########## Main function to perform simulation:
    def btnSimulate_clicked(self):
        
        n = float(self.box_n.text())
        A = float(self.box_A.text())
        E0 = float(self.box_E0.text())
        COb = float(self.box_COb.text())
        CRb = float(self.box_CRb.text())
        DO = float(self.box_DO.text())
        DR = float(self.box_DR.text())
        ks = float(self.box_ks.text())
        alpha = float(self.box_alpha.text())
        Cd = float(self.box_Cd.text())
        Ru = float(self.box_Ru.text())
        
        params = [n, A, E0, COb, CRb, DO, DR, ks, alpha]
        CdRu = [Cd, Ru]
        
        
        self.progressBar.setEnabled(True)
        
        if self.Et_type == "SCV":
            nt = self.t.shape[0] # number of time elements
            nE = self.E.shape[1] # number of potential waveforms (E for SCV or scan rates for CVs)
            self.i = np.zeros([nt, nE])
            self.statusBar().showMessage("Simulating")
            for e in range(0, nE):
                self.progressBar.setValue(0)
                self.i[:,e], self.x, self.cR, self.cO = sol.main(self.t, self.E[:,e], self.bc_type, params, CdRu, self.progressBar)
                self.progressBar.setValue(100)
                self.statusBar().showMessage("Simulation " + str(e+1) + "/" + str(nE) + " finished")
            self.statusBar().showMessage("Simulation finished")
            self.btnPlot.setEnabled(True)
            self.btnAnimate.setEnabled(True)
            self.actionSave_Current.setEnabled(True)
            self.actionSave_Waveform.setEnabled(True)
            self.actionSave_O.setEnabled(False)
            self.actionSave_R.setEnabled(False)
            self.actionSave_x.setEnabled(False)
            return
        
        if self.multSR == True: # To simulate CVs with multiple scan rates
            nt = self.t.shape[0]
            nsr = np.size(self.sr)
            self.i = np.zeros([nt, nsr])
            self.statusBar().showMessage("Simulating")
            for e in range(0, nsr):
                self.progressBar.setValue(0)
                self.i[:,e], self.x, self.cR, self.cO = sol.main(self.t[:,e], self.E, self.bc_type, params, CdRu, self.progressBar)
                self.progressBar.setValue(100)
                self.statusBar().showMessage("Simulation " + str(e+1) + "/" + str(nsr) + " finished")
            self.statusBar().showMessage("Simulation finished")
            self.btnPlot.setEnabled(True)
            self.btnAnimate.setEnabled(True)
            self.actionSave_Current.setEnabled(True)
            self.actionSave_Waveform.setEnabled(True)
            self.actionSave_O.setEnabled(False)
            self.actionSave_R.setEnabled(False)
            self.actionSave_x.setEnabled(False)
            return
            
            
        self.statusBar().showMessage("Simulating.")
        self.i, self.x, self.cR, self.cO = sol.main(self.t, self.E, self.bc_type, params, CdRu, self.progressBar)
        self.statusBar().showMessage("Simulation finished")
        self.progressBar.setValue(100)
        self.btnPlot.setEnabled(True)
        self.btnAnimate.setEnabled(True)
        self.actionSave_Current.setEnabled(True)
        self.actionSave_Waveform.setEnabled(True)
        self.actionSave_O.setEnabled(True)
        self.actionSave_R.setEnabled(True)
        self.actionSave_x.setEnabled(True)
    
    
    ########## Plot solution:
    def btnPlot_clicked(self):
        if self.Et_type == "CV":
            if self.multSR == True:
                self.plot(self.E, self.i/np.sqrt(self.sr), xlab="$E$ / V", ylab="$i sr^{-1/2}$ / A s$^{1/2}$ V$^{-1/2}$")
                plt.show()
                return
            self.plot(self.E, self.i, xlab="$E$ / V", ylab="$i/$ / A")
        elif self.Et_type == "CA":
            self.plot(self.t, self.i, xlab="$t$ / s", ylab="$i$ / A", marker = "-")
        elif self.Et_type == "SCV":
            self.plot(self.E[-1,:], self.i.T/np.max(self.i.T, axis=0), xlab="$E$ / V", ylab="$i/i_{lim}$", marker = "-")
        plt.show()





############### Animate solution:
    def plotFormatAnimation(self, ax0, ax1, xlab0, ylab0, xlab1, ylab1):
        ax0.set_xlabel(xlab0, fontsize = 18)
        ax0.set_ylabel(ylab0, fontsize = 18)
        ax0.tick_params(axis="x", labelsize=14) 
        ax0.tick_params(axis="x", labelsize=14) 
        ax0.grid()
        ax1.set_xlabel(xlab1, fontsize = 18)
        ax1.set_ylabel(ylab1, fontsize = 18)
        ax1.tick_params(axis="x", labelsize=14) 
        ax1.tick_params(axis="y", labelsize=14) 
        ax1.grid()
        
    def btnAnimate_clicked(self):
        nt = np.shape(self.i)[0] # number of time elements
        if self.Et_type == "CV":
            if self.multSR == True:
                fig,ax = plt.subplots(1)
                camera = Camera(fig)
                nsr = np.shape(self.i)[1] # number of scan rates
                for e in range(0, nsr):
                    for n in range(0, nt,10): # 10 data points every snap
                        ax.plot(self.E[:n], self.i[:n,e]/(np.max(self.i[:,e])), 'k')
                        camera.snap()
                xlab0 = "$E$ / V"
                ylab0 = "$i$ / A"
                self.plotFormat(xlab0,ylab0)
                animation = camera.animate()
                plt.show()
                return
            else:
                fig, ax = plt.subplots(1,2)
                camera = Camera(fig)
                for n in range(0,nt,10): # 10 data points every snap
                    ax[0].plot(self.E[:n], self.i[:n], 'k')
                    ax[1].plot(self.x, self.cO[:,n]*1e3, 'k')
                    ax[1].plot(self.x, self.cR[:,n]*1e3, 'r')
                    camera.snap()
                xlab0 = "$E$ / V"
                ylab0 = "$i$ / A"
                xlab1 = "$x$ / cm"
                ylab1 = "C / M"          
        elif self.Et_type == "CA":
            fig, ax = plt.subplots(1,2)
            camera = Camera(fig)
            for n in range(0,nt,10): # 10 data points every snap
                ax[0].plot(self.t[:n], self.i[:n], 'k')
                ax[1].plot(self.x, self.cO[:,n]*1e3, 'k')
                ax[1].plot(self.x, self.cR[:,n]*1e3, 'r')
                camera.snap()
            xlab0 = "$t$ / s"
            ylab0 = "$i$ / A"
            xlab1 = "$x$ / cm"
            ylab1 = "C / M" 
        elif self.Et_type == "SCV":
            fig, ax = plt.subplots(1)
            camera = Camera(fig)
            nE = np.shape(self.i)[1] # number of potential elements
            for n in range(0, nE-1, 1): # 1 SCVs every snap
                    plt.plot(self.E[n,:], self.i[n,:]/(np.max(self.i[n,:], axis=0)), 'k')
                    camera.snap()
            
            xlab = "$E$ / V"
            ylab = "$i$ / A"
            self.plotFormat(xlab,ylab)
            animation = camera.animate()
            plt.show()
            return
         
        self.plotFormatAnimation(ax[0], ax[1], xlab0, ylab0, xlab1, ylab1)
        fig.tight_layout()
        animation = camera.animate()
        plt.show()
        

########## Function for the save dialog
    def saveCurrent(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save data","current.txt","Text Files (*.txt)", options=options)
        
        if fileName:
            if self.Et_type == "CV":
                if self.multSR == True:
                    header = "Cyclic voltammetry (E/V [nt,1], i/A[nt,nsr], t/A[nt, nsr]) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                    m = np.shape(self.t)[0] # number of time elements
                    nsr = np.shape(self.t)[1]
                    n = nsr*2 + 1 # number of column elements, [E,i,t]
                    data = np.zeros([m, n])
                    data[:,0] = self.E
                    data[:,1:nsr+1] = self.i
                    data[:,nsr+1:] = self.t
                    np.savetxt(fileName + ".txt", data, delimiter=",", header = header)
                    return
                header = "Cyclic voltammetry (t/s, E/V. i/A) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = np.array([self.t, self.E, self.i]).T
            elif self.Et_type == "CA":
                header = "Chronoamperometry (t/s, E/V. i/A) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = np.array([self.t, self.E, self.i]).T
            elif self.Et_type == "SCV":
                header = "Sampled current voltammetry (i/A) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = self.i
            np.savetxt(fileName + ".txt", data, delimiter=",", header = header)
    
    def saveWaveform(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save data","waveform.txt","Text Files (*.txt)", options=options)
        
        if fileName:
            if self.Et_type == "CV":
                if self.multSR == True:
                    header = "Cyclic voltammetry waveform (E/V[nt,1], t/A[nt, nsr]) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                    m = np.shape(self.t)[0] # number of time elements
                    nsr = np.shape(self.t)[1] + 1
                    #n = nsr*2 + 1 # number of column elements, [E,i,t]
                    data = np.zeros([m, nsr])
                    data[:,0] = self.E
                    data[:,1:] = self.t
                    np.savetxt(fileName + ".txt", data, delimiter=",", header = header)
                    return
                header = "Cyclic voltammetry waveform (t/s, E/V) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = np.array([self.t, self.E]).T
            elif self.Et_type == "CA":
                header = "Chronoamperometry waveform (t/s, E/V. i/A) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = np.array([self.t, self.E, self.i]).T
            elif self.Et_type == "SCV":
                header = "Sampled current voltammetry waveform (i/A) simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                data = self.i
            np.savetxt(fileName + ".txt", data, delimiter=",", header = header)

    def saveO(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save data","cO.txt","Text Files (*.txt)", options=options)
        
        if fileName:
            if self.Et_type == "CV":
                header = "[O] (mol/cm3) from cyclic voltammetry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.cO, delimiter=",", header = header)
            if self.Et_type == "CA":
                header = "[O] (mol/cm3) from chronoamperometry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.cO, delimiter=",", header = header)

    def saveR(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save data","cR.txt","Text Files (*.txt)", options=options)
        
        if fileName:
            if self.Et_type == "CV":
                header = "[R] (mol/cm3) from cyclic voltammetry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.cR, delimiter=",", header = header)
            if self.Et_type == "CA":
                header = "[R] (mol/cm3) from chronoamperometry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.cR, delimiter=",", header = header)

    def saveX(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save data","x.txt","Text Files (*.txt)", options=options)
        
        if fileName:
            if self.Et_type == "CV":
                header = "X (cm) from cyclic voltammetry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.x, delimiter=",", header = header)
            if self.Et_type == "CA":
                header = "x (cm) from chronoamperometry simulated with Soft Potato. For more info visit https://oliverrdz.xyz."
                np.savetxt(fileName + ".txt", self.x, delimiter=",", header = header)


####################################################
def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
