# Soft Potato
Open source electrochemistry simulator

It simulates current transients and cyclic voltammograms for planar diffusion. Assumes R - e -> O and Butler-Volmer kinetics. For more information visit [Soft Potato](https://oliverrdz.xyz/?page_id=143) and the [SP wiki](https://github.com/oliverrdz/SoftPotato/wiki) (in process).

# Installation
Download the repository. The easiest way to access the functions from Pyhton is to put the files wafevorms.py, solver.py and plots.py on the same folder where you want to create your script. Alternatively, add the folder SoftPotato to the PYTHONPATH variable; if using [Spyder](https://www.spyder-ide.org/), this can be done by going to Tools/PYTHONPATH manager and add the folder SoftPotato, in this way, the modules can be accessed from any path.

# Usage
The general usage is as follows:
+ Import modules
+ Declare parameters
+ Create waveform
+ Solve
+ Plot

The folder Examples shows code for typical electrochemical experiments (CV, CA, SCV, etc.), while the folder Validation has scripts that compares the simulated responses with analytical solutions.

# Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request. If you write the code for a specific technique using SP and want it to be accesible for everyone, please contact me so it can be added to the repository and the SP wiki.

# Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).

# Requirements
It requires:
+ Python 3+
+ Numpy
+ Matplotlib
+ Scipy

Tested with:
+ IDE: Spyder 3.3.6
+ OS: Manjaro Gnome

# Pending
+ Add ability to simulate a reduction process
+ Add ability to have both species in solution at t = 0

# Planed improvements
+ Add double layer capacitance and solution resistance
+ Spherical and hemispherical diffusion
+ Graphical user interface

***
Log:
+ 03/Apr/2020: added a script folder with the simulation of the Randless circuit
+ 02/Apr/2020: complete restructure of the file tree plus SP written in modular form
+ 01/Apr/2020: added mod_waveforms.py
+ 06/Mar/2020: added Butler-Volmer kinetics to SP_SCV.py
+ 27/Feb/2020: added Butler-Volmer kinetics to SP_CV.py
+ 17/Feb/2020: added SP_CV.py
+ 08/Feb/2020: added SP_Cottrell.py and SP_SCV.py
