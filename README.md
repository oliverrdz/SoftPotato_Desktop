# Soft Potato wiki
Open source electrochemistry simulator, now with a graphical interface!

It simulates cyclic voltammograms for planar diffusion. Assumes R - e -> O and Butler-Volmer kinetics. For more information visit [https://oliverrdz.xyz/soft-potato](https://oliverrdz.xyz/soft-potato).

## Binaries
There are Windows 8.1 and Ubuntu 20.10 binaries in the [releases page](https://github.com/oliverrdz/SoftPotato/releases/tag/v2.0).


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

Tested with:
+ Linux (PopOs/Ubuntu 20.10)
+ Windows 8.1

## Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request.

## Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).

## Screenshots
PopOS 20.04LTS:
![Screenshot v2.0](https://github.com/oliverrdz/SoftPotato/blob/master/Figs/SP_v2.0.png?raw=true])
