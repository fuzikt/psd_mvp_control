# PSD pump and MVP valve controller 
Python application to control Hamilton PSD/4, PSD/6 pumps and MVP/4 valves.

## Features
- easy to  integrate independent hw_classes for PSD pump and MVP valve
- see control_demo.py for details of integration
- multiple addressable devices per COM port
- Qt5 based GUI
- loop support in gui built programs

## Requirements / dependencies
- Python 3
- PyQt5
- PySerial

## Builts
PyInstaller made builds with all dependencies are available for Windows and Linux systems.

## Install from sources
Make sure all dependencies are installed.

Alternatively, create a conda environment with the dependencies.

Download the sources from Github.
```
git clone 
cd 
```
To run the GUI use:
```
main_app.py
```

To run the demo script:
```
control_demo.py
```

## Screenshots
Main Application
![Alt text](/screenshots/main.png?raw=true "Main app")
Add devices
![Alt text](/screenshots/main.png?raw=true "Add devices")
Add program steps 1
![Alt text](/screenshots/main.png?raw=true "Add program steps 1")
Add program steps 2
![Alt text](/screenshots/main.png?raw=true "Add program steps 2")

# Supported devices
PSD/4 - STD, SF, HLF, HVT, HLF/HVT (Standard, Smooth Flow, High-Lift Force, HiValve Torque, High-Lift Force / HiValve Torque)
PSD/6 - STD, SF, HLF, HVT, HLF/HVT (Standard, Smooth Flow, High-Lift Force, HiValve Torque, High-Lift Force / HiValve Torque)
MVP/4

## Files description
main_app.py
- main GUI program to control the devices.

control_demo.py
- demo script to control devices without GUI.

hw_classes/mvp_valve.py
- class to control MVP valves through serial communication.
- usage shown in control_demo.py

hw_classes/psd_pump.py
- class to control PSD/4, PSD/8 pumps through serial communication
- usage shown in control_demo.py

hw_classes/serial_com.py
- class for COM serial communication
- used by psd_pump.py and mvp_valve.py