# Soft Potato
Open source electrochemistry simulator

It simulates current transients and cyclic voltammetry for planar diffusion. Assumes R - e -> O and Butler-Volmer kinetics. For more information visit [Soft Potato](https://oliverrdz.xyz/?page_id=143).

It requires:
+ Python 3+
+ Numpy
+ Matplotlib
+ Scipy

Tested with:
+ IDE: Spyder 3.3.6
+ OS: Manjaro Gnome

***
Log:
+ 03/Apr/2020: added a script folder with the simulation of the Randless circuit
+ 02/Apr/2020: complete restructure of the file tree plus SP written in modular form
+ 01/Apr/2020: added mod_waveforms.py
+ 06/Mar/2020: added Butler-Volmer kinetics to SP_SCV.py
+ 27/Feb/2020: added Butler-Volmer kinetics to SP_CV.py
+ 17/Feb/2020: added SP_CV.py
+ 08/Feb/2020: added SP_Cottrell.py and SP_SCV.py
