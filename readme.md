# Foam Functions
an assortment of python functions that can be used in a main script that is within a case to automate execution

## Content
### Meshes
Contains functions that create fully usable meshes for special usecases

### Tools
Contains small helper functions to aid with various tasks

### Solvers
Contains tools and classes related to running solvers




## Meshes
### Cylinder in Crossflow
Contains meshing approaches to mesh a cylinder in a crossflow

### Refinable Cylinder in Crossflow
Contains meshing approaches to mesh a cylinder in a crossflow, but uses symmetry instead of empty for front an back to allow for the non 2D refining

### coax jet
Structured Mesh for a coaxial Jet, wedge is for a cylindical case and flat for a 2d case

## Tools
### Data Readers
Functions to extract data from files that are created by OpenFoam. This data can then be used for further processing in python

### Data Processing
Functions that can manipulate and extract information from data

### general tools
Just usefull little tools that fit no specific category

### fluid calcs
Functions to perform small calculations regarding fluid mechanics. e.g. calculate the Re-Number


## Solvers
### Sim_Master
provides a class that makes executing and chaining solvers easier, runs are defined as sim_step class and then executed via the sim_master

## Installation
Navigato to this directory with the environment sources in which to install this package.
run: pip install -e .

If vs-code gets sad and says it cant import the module, but the file runs you have to add an entry to the settings.json file.
"python.analysis.extraPaths": [
        "./FoamFunctions" <- replace with directory path
]