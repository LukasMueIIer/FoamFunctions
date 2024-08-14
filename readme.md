# Foam Functions
an assortment of python functions that can be used in a main script that is within a case to automate execution

## Content
### Meshes
Contains functions that create fully usable meshes for special usecases

### Tools
Contains small helper functions to aid with various tasks




## Meshes
### Cylinder in Crossflow
Contains meshing approaches to mesh a cylinder in a crossflow

## Tools
### Data Readers
Functions to extract data from files that are created by OpenFoam. This data can then be used for further processing in python

### Data Processing
Functions that can manipulate and extract information from data


## Installation
Navigato to this directory with the environment sources in which to install this package.
run: pip install -e .

If vs-code gets sad and says it cant import the module, but the file runs you have to add an entry to the settings.json file.
"python.analysis.extraPaths": [
        "./FoamFunctions" <- replace with directory path
]