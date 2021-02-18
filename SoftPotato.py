from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import icon_rc

import numpy as np
import webbrowser

from sp import *

# Change all plots:
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


# Default parameters
global wf_params
wf_params = [-0.5, 0.5, 1, 0.01, 2, "CV"]
mech_params = [0, 1, 1e-5, 1e-5, 0, 1e-6, 1e8, 0.5, "QR"]
Ageo = 1

# Creat objects for default simulation
#wf = Sweep()
#mech = E_mec(wf, space)

######################################################################################
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the main UI:
        uic.loadUi('main.ui', self)
        
        self.statusBar().showMessage("Ready.")
        
        # Connect File menu:
        self.fileExit.triggered.connect(QtWidgets.qApp.quit)
        self.action_tEi.triggered.connect(self.save_tEi)
        self.action_O.triggered.connect(self.save_O)
        self.action_R.triggered.connect(self.save_R)
        self.action_x.triggered.connect(self.save_x)
        self.action_Save_all.triggered.connect(self.open_saveAll)
        
        # Connect Technique menu:
        self.actionCyclic_voltammetry.triggered.connect(self.openCV)
        self.actionChronoamperometry.triggered.connect(self.openCA)
        
        # Connect Simulation menu:
        self.actionMechanism.triggered.connect(self.openEmech)
        self.actionSimulate.triggered.connect(self.simulate)
        self.actionArea.triggered.connect(self.openArea)

        # Connect Help menu:
        self.actionHelp.triggered.connect(lambda: webbrowser.open('https://oliverrdz.xyz/soft-potato'))
        self.actionAbout.triggered.connect(self.openAbout)
        
        # Connect slider for plotting:
        self.slider_plots.valueChanged[int].connect(self.changeValue)

        self.header_save = "# Data simulated with Soft Potato 2.0, for more information visit https://oliverrdz.xyz/soft-potato\n"

    def save_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save data","fileName.txt","Text Files (*.txt)", options=options)
        return fileName

    def save_tEi(self):
        header = self.header_save + "# t/s, E/V, i/A"
        fileName = self.save_dialog()
        if fileName:
            data = np.array([self.sim.t, self.sim.E, self.sim.i]).T
            np.savetxt(fileName, data, delimiter=",", header=header)


    def save_O(self):
        header = self.header_save + "# [O] / mol cm^-3"
        fileName = self.save_dialog()
        if fileName:
            data = self.sim.cO.T
            np.savetxt(fileName, data, delimiter=",", header=header)

    def save_R(self):
        header = self.header_save + "# [R] / mol cm^-3"
        fileName = self.save_dialog()
        if fileName:
            data = self.sim.cR.T
            np.savetxt(fileName, data, delimiter=",", header=header)

    def save_x(self):
        header = self.header_save + "# x / cm"
        fileName = self.save_dialog()
        if fileName:
            data = self.sim.x
            np.savetxt(fileName, data, delimiter=",", header=header)

    def open_saveAll(self, sim):
        self.saveAll = SaveAll_dialog(self.sim)
        self.saveAll.exec_()

    def openCV(self):
        self.cv = CV_dialog()
        self.cv.exec_()
        
    def openCA(self):
        self.ca = CA_dialog()
        self.ca.exec_()
        
    def openEmech(self):
        self.mech_diag = Emech_dialog()
        self.mech_diag.exec_()

    def openArea(self):
        self.area_diag = Area_dialog()
        self.area_diag.exec_()

    def openHelp(self):
        QtCore.QUrl("https://oliverrdz.xyz/soft-potato")

    def openAbout(self):
        self.about_diag = About_dialog()
        self.about_diag.exec_()
        
    def changeValue(self,value):
        sim = self.sim
        nMax = np.size(sim.t)
        n = int(value*nMax/100)
        self.plot(self.sim,n)

    def simulate(self):
        self.statusBar().showMessage("Simulating")

        # Select the technique
        global wf_params
        if wf_params[-1] == "CV":
            self.wf = Sweep(wf_params)
        else:
            self.wf = Step(wf_params)

        self.space = Equal_spc(self.wf)
        self.mech = E_mec(self.wf, self.space, mech_params)
        self.sim = Simulate(self.wf, self.space, self.mech, Ageo)
        self.sim.fd(self.progressBar)
        self.slider_plots.setEnabled(True)
        self.statusBar().showMessage("Simulation finished.")
        self.slider_plots.setValue(100)
        self.plot(self.sim,-1)
        self.progressBar.setValue(100)
        self.statusBar().showMessage("Simulation finished")

    def plot(self, sim,n):
        self.plot1.setLabel('left', 'Potential', units='V')
        self.plot1.setLabel('bottom', 'Time', units='s')
        self.plot1.plot(sim.t[0:n], sim.E[0:n], pen=pg.mkPen('k', width=3), clear=True)
        self.plot2.setLabel('left', 'Current', units='A')
        self.plot2.setLabel('bottom', 'Potential', units='V')
        self.plot2.plot(sim.E[0:n], sim.i[0:n], pen=pg.mkPen('k', width=3), clear=True)
        self.plot3.setLabel('left', 'Current', units='A')
        self.plot3.setLabel('bottom', 'Time', units='s')
        self.plot3.plot(sim.t[0:n], sim.i[0:n], pen=pg.mkPen('k', width=3), clear=True)
        self.plot4.addLegend()
        self.plot4.setLabel('left', 'Concentration', units='M')
        self.plot4.setLabel('bottom', 'Distance', units='m')
        self.plot4.plot(sim.x*1e-2, sim.cR[n,:]*1e3, pen=pg.mkPen('k', width=3), name='[R]', clear=True)
        self.plot4.plot(sim.x*1e-2, sim.cO[n,:]*1e3, pen=pg.mkPen('r', width=3), name='[O]')

######################################################################################

class CV_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(CV_dialog, self).__init__()
        uic.loadUi('CV.ui', self)
        
        # Connect buttons
        self.btn_ok.clicked.connect(self.fun_ok)
        self.btn_cancel.clicked.connect(self.fun_cancel)
        self.btn_plot.clicked.connect(self.fun_plot)
        
        # Recover the last used values
        # if a different technique was used previously, it will raise an error
        global wf_params
        #print(wf_params)
        if wf_params[-1] != "CV":
            wf_params = [-0.5, 0.5, 1, 0.01, 2, "CV"]
        else:
            self.txt_Eini.setText(str(wf_params[0]))
            self.txt_Efin.setText(str(wf_params[1]))
            self.txt_sr.setText(str(wf_params[2]))
            self.txt_dE.setText(str(wf_params[3]))
            self.txt_ns.setText(str(wf_params[4]))

            
    def get_values(self):
        self.Eini = float(self.txt_Eini.text())
        self.Efin = float(self.txt_Efin.text())
        self.sr = float(self.txt_sr.text())
        self.dE = float(self.txt_dE.text())
        self.ns = int(self.txt_ns.text())
        return [self.Eini, self.Efin, self.sr, self.dE, self.ns, "CV"]
    
    def fun_ok(self):
        global wf_params
        wf_params = self.get_values()
        self.reject()

    def fun_cancel(self):
        self.reject()
    
    def fun_plot(self):
        # Plot can be saved because window is a dialog
        params = self.get_values()
        self.wf = Sweep(params)
        self.cv_plot.setLabel('left', 'Potential', units='V')
        self.cv_plot.setLabel('bottom', 'Time', units='s')
        self.cv_plot.plot(self.wf.t, self.wf.E, pen=pg.mkPen('k', width=3), clear=True)
        

######################################################################################

class Area_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Area_dialog, self).__init__()
        uic.loadUi("Area.ui", self)

        # Connect buttons
        self.btn_OK.clicked.connect(self.fun_ok)
        self.btn_Cancel.clicked.connect(self.fun_cancel)

        # Recover last used value
        global Ageo
        self.txt_Ageo.setText(str(Ageo))

    def get_values(self):
        self.Ageo = float(self.txt_Ageo.text())
        return self.Ageo

    def fun_ok(self):
        global Ageo
        Ageo = self.get_values()
        self.reject()

    def fun_cancel(self):
        self.reject()
        
        


######################################################################################

class CA_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(CA_dialog, self).__init__()
        uic.loadUi('CA.ui', self)
        
        # Connect buttons
        self.btn_ok.clicked.connect(self.fun_ok)
        self.btn_cancel.clicked.connect(self.fun_cancel)
        self.btn_plot.clicked.connect(self.fun_plot)
        
        # Recover the last used values
        global wf_params
        if wf_params[-1] != "CA":
            wf_params = [1, 1, 0.01, "CA"]
        else:
            self.txt_Es.setText(str(wf_params[0]))
            self.txt_ttot.setText(str(wf_params[1]))
            self.txt_dt.setText(str(wf_params[2]))
            
    def get_values(self):
        self.Es = float(self.txt_Es.text())
        self.ttot = float(self.txt_ttot.text())
        self.dt = float(self.txt_dt.text())
        return [self.Es, self.ttot, self.dt, "CA"]
    
    def fun_ok(self):
        global wf_params
        wf_params = self.get_values()
        self.reject()
    
    def fun_cancel(self):
        self.reject()
        
    def fun_plot(self):
        ############ Plot can't be saved because window is a dialog
        params = self.get_values()
        self.wf = Step(params)
        self.cv_plot.setLabel('left', 'Potential', units='V')
        self.cv_plot.setLabel('bottom', 'Time', units='s')
        self.cv_plot.plot(self.wf.t, self.wf.E, pen=pg.mkPen('k', width=3), clear=True)



######################################################################################
class Emech_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Emech_dialog, self).__init__()
        uic.loadUi('Emech.ui', self)
        
        # Connect radio buttons
        self.rBtn_QR.toggled.connect(self.rBtn_kinetics)
        self.rBtn_OR.toggled.connect(self.rBtn_kinetics)
        self.rBtn_RO.toggled.connect(self.rBtn_kinetics)
        
        # Connect buttons
        self.btn_ok.clicked.connect(self.fun_ok)
        self.btn_cancel.clicked.connect(self.fun_cancel)
        
        # Recover the last used values
        global mech_params
        try:
            self.txt_n.setText(str(int(mech_params[1])))
        except:
            self.txt_n.setText('1')
        try:
            self.txt_E0.setText(str(mech_params[0]))
        except:
            self.txt_E0.setText('0')
        try:
            self.txt_cO.setText(str(mech_params[4]))
        except:
            self.txt_cO.setText('0')
        try:
            self.txt_cR.setText(str(mech_params[5]))
        except:
            self.txt_cR.setText('1e-6')
        try:
            self.txt_DO.setText(str(mech_params[2]))
        except:
            self.txt_DO.setText('1e-5')
        try:
            self.txt_DR.setText(str(mech_params[3]))
        except:
            self.txt_DR.setText('1e-5')
        try:
            self.txt_ks.setText(str(mech_params[6]))
        except:
            self.txt_ks.setText('1e8')
        try:
            self.txt_alpha.setText(str(mech_params[7]))
        except:
            self.txt_alpha.setText('0.5')
            
        # Find which kinetics is active and select its radio button:
        #global mech_params
        self.BV = mech_params[-1]
        print(self.BV)
        if self.BV == 'OR':
            self.rBtn_RO.setChecked(False)
            self.rBtn_OR.setChecked(True)
            self.rBtn_QR.setChecked(False)
        elif self.BV == 'RO':
            self.rBtn_RO.setChecked(True)
            self.rBtn_OR.setChecked(False)
            self.rBtn_QR.setChecked(False)
        else:
            self.rBtn_RO.setChecked(False)
            self.rBtn_OR.setChecked(False)
            self.rBtn_QR.setChecked(True)
        
        
    def rBtn_kinetics(self):
        rBtn = self.sender()
        
        if rBtn.isChecked():
            if rBtn.objectName() == 'rBtn_OR':
                self.BV = 'OR'
            elif rBtn.objectName() == 'rBtn_RO':
                self.BV = 'RO'
            else:
                self.BV = 'QR'
        
    def fun_ok(self):
        #params = self.get_values()
        #self.rBtn_kinetics()
        global mech_params
        mech_params = self.get_values()
        self.reject()
        
    def fun_cancel(self):
        self.reject()
        
    def get_values(self):
        self.n = float(self.txt_n.text())
        self.E0 = float(self.txt_E0.text())
        self.cOb = float(self.txt_cO.text())
        self.cRb = float(self.txt_cR.text())
        self.DO = float(self.txt_DO.text())
        self.DR = float(self.txt_DR.text())
        self.ks = float(self.txt_ks.text())
        self.alpha = float(self.txt_alpha.text())
        self.rBtn_kinetics()
        return [self.E0, self.n, self.DO, self.DR, self.cOb, self.cRb, self.ks, self.alpha, self.BV]
        


class About_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(About_dialog, self).__init__()
        uic.loadUi("About.ui", self)

        self.btn_webpage.clicked.connect(lambda: webbrowser.open('https://oliverrdz.xyz/soft-potato'))
        


class SaveAll_dialog(QtWidgets.QDialog):
    def __init__(self, sim):
        super(SaveAll_dialog, self).__init__()
        uic.loadUi("Save_all.ui", self)

        self.btn_Save.clicked.connect(self.save)
        self.btn_Cancel.clicked.connect(self.cancel)

        self.sim = sim

    def save(self):

        self.btn_Save.setEnabled(True)
        pathName = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.header_save = "# Data simulated with Soft Potato 2.0, for more information visit https://oliverrdz.xyz/soft-potato\n"

        # If the user selects a folder, saves and exits:
        if pathName:
            fileName = pathName + "/" + self.txt_fileName.text()
            
            header = self.header_save + "# t/s, E/V, i/A"
            data = np.array([self.sim.t, self.sim.E, self.sim.i]).T
            np.savetxt(fileName + "_tEi.txt", data, delimiter=",", header=header)

            header = self.header_save + "# [O] / mol cm^-3"
            data = self.sim.cO.T
            np.savetxt(fileName + "_[O].txt", data, delimiter=",", header=header)

            header = self.header_save + "# [R] / mol cm^-3"
            data = self.sim.cR.T
            np.savetxt(fileName + "_[R].txt", data, delimiter=",", header=header)

            header = self.header_save + "# x / cm"
            data = self.sim.x
            np.savetxt(fileName + "_x.txt", data, delimiter=",", header=header)

            self.reject()



    def cancel(self):
        self.reject()
        
######################################################################################
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.simulate()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
