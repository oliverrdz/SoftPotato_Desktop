# Soft Potato
Open source electrochemistry simulator, now with a graphical interface!

It simulates cyclic voltammograms for planar diffusion. Assumes R - e -> O and Butler-Volmer kinetics as well as nerstian response. For more information visit [https://oliverrdz.xyz](https://oliverrdz.xyz/?page_id=143).

# Usage
Download the repository. From a terminal and within the SP directory, run:
```python
python3 SP.py 
```

# Requirements
It requires:
+ Python 3+
+ PyQt5
+ Numpy
+ Matplotlib

Tested with:
+ OS: Debian 10, XFCE

# Pending:
+ Desing GUI for chronoamperometry and sampled current voltammetry
+ Change to an implicit algorithm to improve stability
+ Activate non-faradaic response

# Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request.

# Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).

# Screenshot, v0.2.0

![Screenshot v0.2.0](https://github.com/oliverrdz/SoftPotato/blob/master/Figs/screenshot_v0-2-0.png?raw=true])
