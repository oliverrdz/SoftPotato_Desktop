# Version 1.1

Soft potato going back to the roots. I am rewriting the main code to make it easier to maintain. I am now trying to use the OOP paradigm. I am also writing Soft Potato in a modular way so it can be used as a script. The GUI would just be a complement.

### Requirements
It requires:
+ Python 3+
+ Numpy
+ Matplotlib

```python
pip3 install numpy
pip3 install matplotlib
```

Tested with:
+ Linux (PopOs 20.04LTS)

## Pending:
+ Validation of cyclic voltammetry

## Log:
+ 22/Oct/2020
  + Created CV and waveform scripts for the documentation
  + Removed extra time point in wf.Construct()
  + Created Randles-Sevick script to test CV
  + Positive or negative sweep
  + Both O and R present at t = 0

## Contributing
To report bugs, make suggestions or comments or collaborations, please contact me on [Twitter](https://twitter.com/ol1v3r) or create a pull request.

## Credits
The simulator is based on the "Modelling in Electrochemistry" lectures given by [Dr. Guy Denuault](https://www.southampton.ac.uk/chemistry/about/staff/gd.page).
