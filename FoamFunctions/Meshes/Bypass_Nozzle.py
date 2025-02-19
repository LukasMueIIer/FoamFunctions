#Contains Functions to create Meshes to simulate simple Bypass Nozzles
import classy_blocks as cb
import numpy as np

def squareNozzels(directory, radiusCore,radiusBypass,lengthCore,lengthBypass,lengthDomain,heightDomain,aspectRatio,y_count_core,expansionX,expansionY):
    #Geometry
    #radiusCore, absolute radius of the Core Nozzel
    #radiusBypass, absolute radius of the Bypass Nozzle
    #lengthCore, relative "extension" of the Core Nozzle after the Bypass Nozzle, must be above 0
    #lengthBypass, length of the Wall till the Bypass Nozzle ends, must be above 0
    #lenthDomain, how far the domain extends in x-Direction after the Core Nozzle Exit, above 0
    #heightDomain, how far the Domain extends in y Deriction from the Radius of the Bypass Nozzle

    #Meshing
    #aspectRatio, of the cells right at the Core nozzle exit
    #y_count_core, amount of cells in y-direction for the Core
    
    #Calculate the Cell sizes
    xCellNozel = aspectRatio * radiusCore / y_count_core
    yCellNozle = radiusCore / y_count_core

    file_path = directory
    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #Block Core Nozzle
    points = [[0,0,0],[lengthDomain,0,0],[lengthDomain,radiusCore,0],[0,radiusCore,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.set_patch("left","core")
    wedge.chop(0,start_size=xCellNozel, c2c_expansion=expansionX)
    wedge.chop(1,count = y_count_core)

    shapes.append(wedge)

    #Block Bypass
    points = [[-lengthCore,radiusCore,0],[0,radiusCore,0],[0,radiusBypass,0],[-lengthCore,radiusBypass,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.set_patch("left","bypass")
    wedge.set_patch("front","nozzle")

    #calculate the chopping that is closest to the core one
    yCount = round((radiusBypass - radiusCore) / yCellNozle)
    xCount = round(lengthCore / xCellNozel)

    wedge.chop(0,count=xCount)
    wedge.chop(1,count=yCount)

    #calculate true size for later use
    ySizeBypass = (radiusBypass - radiusCore) / yCount
    xSizeBypass = lengthCore / xCount

    shapes.append(wedge)

    #Connecting Block
    points = [[0,radiusCore,0],[lengthDomain,radiusCore,0],[lengthDomain,radiusBypass,0],[0,radiusBypass,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xCellNozel, c2c_expansion=expansionX)
    wedge.chop(1,count=yCount)

    shapes.append(wedge)

    #FAR Field
    points = [[0,radiusBypass,0],[lengthDomain,radiusBypass,0],[lengthDomain,radiusBypass+heightDomain,0],[0,radiusBypass+heightDomain,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xCellNozel, c2c_expansion=expansionX)
    wedge.chop(1,start_size=ySizeBypass,c2c_expansion=expansionY)

    shapes.append(wedge)

    #Filler Block Between Farfield and Sponge
    points = [[- lengthCore,radiusBypass,0],[0,radiusBypass,0],[0,radiusBypass+heightDomain,0],[- lengthCore, radiusBypass+heightDomain,0]]

    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    wedge.chop(0,count=xCount)
    wedge.chop(1,start_size=ySizeBypass,c2c_expansion=expansionY)
    shapes.append(wedge)

    #Inlet Sponge
    points = [[-lengthCore -lengthBypass,radiusBypass,0], [-lengthCore,radiusBypass,0],[-lengthCore,radiusBypass+heightDomain,0],[-lengthCore -lengthBypass,radiusBypass+heightDomain,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,end_size=xSizeBypass,c2c_expansion= 1/expansionX)
    wedge.chop(1,start_size=ySizeBypass,c2c_expansion=expansionY)

    wedge.set_patch("front","nozzle")

    shapes.append(wedge)


    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("farField","patch")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("nozzle","wall")
    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")