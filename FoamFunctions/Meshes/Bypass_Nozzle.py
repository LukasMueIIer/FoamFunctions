#Contains Functions to create Meshes to simulate simple Bypass Nozzles

def squareNozzels(radiusCore,radiusBypass,lengthCore,lengthBypass,lengthDomain,heightDomain,expansionX,expansionY):
    #Geometry
    #radiusCore, absolute radius of the Core Nozzel
    #radiusBypass, absolute radius of the Bypass Nozzle
    #lengthCore, relative "extension" of the Core Nozzle after the Bypass Nozzle, must be above 0
    #lengthBypass, length of the Wall till the Bypass Nozzle ends, must be above 0
    #lenthDomain, how far the domain extends in x-Direction after the Core Nozzle Exit, above 0
    #heightDomain, how far the Domain extends in y Deriction from the Radius of the Bypass Nozzle
