import classy_blocks as cb
import numpy as np
import os

def  straightPipeMultiSnappedRegions(directory,radius,dY,yStart,expRatio,lengths,walled = True):    #create a classical based mesh 
    #A straight pipe with given radius
    #uniform blocking uses the "size" dY
    #order is allwas -> expanding, contracting, uniform , expanding, contracting, uniform
    #if walled = True add a outsideWall patch

    file_path = directory

    indicator = 0  #0, expaning; 1, contracting; 2, uniform

    y = yStart

    shapes = []
    first = True

    def calc_expansion(d0,exr,l):
        #Calculates the effective expansion ratio 
        target = l / d0
        n = 0
        res = 0
        while(res < target):
            n = n + 1
            res = (exr ** n  - 1) / (exr - 1)
        
        #now find the expansion ratio via the disection method

    for i in range(0,len(lengths)):
        if(lengths[i] > 0):
            if(indicator = 0):
