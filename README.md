# Soft Potato wiki
Open source electrochemistry simulator.

It simulates cyclic voltammograms and chronoamperograms for planar diffusion assuming Butler-Volmer kinetics. Make sure to use the slide bar at the bottom! For more information visit [https://oliverrdz.xyz/soft-potato](https://oliverrdz.xyz/soft-potato).

## Binaries
There are Windows 8.1 and Ubuntu 20.10 binaries in the [releases page](https://github.com/oliverrdz/SoftPotato/releases). Make sure to download the latest release available for your system.


## Usage
For regular use, download the binary for your system. If you want to tinker with the code, then download the repository. From a terminal and within the Soft Potato directory, run:
```python
python3 SoftPotato.py
```

### Requirements
It requires:
+ Python 3+
+ PyQt5
+ Numpy
+ Matplotlib
+ PyQTGraph

```python
pip3 install numpy
pip3 install matplotlib
pip3 install pyqt5
pip3 install pyqtgraph
```

Optional for compiling with cython, see below
+ Cython
```python
pip3 install Cython


Tested with:
+ Linux (PopOs/Ubuntu 20.10/Manjaro)
+ Windows 8.1
+ MacOS Catalina

### Compiling with Cython
The code can be made around 30% faster by cythonizing the main sp.py module.
This will particularly help speed up the calculation of finite-differences.
To compile to code install first Cython and then run the command

python3 setup.py build_ext --inplace

## Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request.

## Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).

## Screenshots
PopOS 20.10:
![Screenshot v2.0](https://github.com/oliverrdz/SoftPotato/blob/master/Figs/SP_v2.0_popOS.png?raw=true])
Windows 8.1:
![Screenshot_v2,0](https://github.com/oliverrdz/SoftPotato/blob/master/Figs/SP_v2.0_Win.png?raw=true])
