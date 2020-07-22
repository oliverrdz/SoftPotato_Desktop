# Soft Potato wiki
Open source electrochemistry simulator, now with a graphical interface!

It simulates cyclic voltammograms for planar diffusion. Assumes R - e -> O and Butler-Volmer kinetics as well as nerstian response. For more information visit [https://oliverrdz.xyz](https://oliverrdz.xyz/?page_id=143).

## Usage
Download the repository. From a terminal and within the Soft Potato directory, run:
```python
python3 SoftPotato.py
```

### Requirements
It requires:
+ Python 3+
+ PyQt5
+ Numpy
+ Matplotlib
+ [celluloid](https://github.com/jwkvam/celluloid)

```python
pip3 install numpy
pip3 install matplotlib
pip3 install pyqt5
pip3 install celluloid
```

Tested with:
+ Linux (PopOs 20.04LTS)
+ Windows 10

## Pending:
+ Build Linux, Mac and Windows binaries
+ Change to an implicit algorithm to improve stability
+ Activate non-faradaic response

## Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request.

## Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).

## Screenshots
PopOS 20.04LTS:
![Screenshot v1.0.0](https://github.com/oliverrdz/SoftPotato/blob/master/Figs/SP_v1.0.0.png?raw=true])

Windows 10:
