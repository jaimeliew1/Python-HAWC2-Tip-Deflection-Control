Python-HAWC2 Tip Deflection Control
===================================

An example of individual pitch control (IPC) for a wind turbine. The IPC is
implemented using my Python-HAWC2 Interface project. The IPC algorithm is
written in python and can be found as the update() function in Example.py.

 

Requirements
============

This repository is written for Windows.

[HAWC2](http://www.hawc2.dk/)should be installed and the executable HAWC2mb.exe
should either be in the PATH directory, or in the same folder as this
repository.

The Python module uses numpy, threading and os.

TCPServer.dll should be placed in the control folder of the turbine model
directory. The DLL is available on the [HAWC2
website](http://www.hawc2.dk/download/dlls) in the MATLAB control download zip
file. It is also provided in this repository.

IPC Background
==============

To do: write implementation notes.

 
