#Contains Functions to create Meshes to simulate simple Bypass Nozzles
import classy_blocks as cb
import numpy as np
import copy as copy

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

def squareNozzelsSponged(directory, radiusCore,radiusBypass,lengthCore,lengthBypass,lengthDomain,heightDomain,aspectRatio,y_count_core,expansionX,expansionY,lengthSponge,XCountSponge,mergeFactorSponge):
    #Geometry
    #radiusCore, absolute radius of the Core Nozzel
    #radiusBypass, absolute radius of the Bypass Nozzle
    #lengthCore, relative "extension" of the Core Nozzle after the Bypass Nozzle, must be above 0
    #lengthBypass, length of the Wall till the Bypass Nozzle ends, must be above 0
    #lenthDomain, how far the domain extends in x-Direction after the Core Nozzle Exit, above 0
    #heightDomain, how far the Domain extends in y Deriction from the Radius of the Bypass Nozzle
    #lengthSponge, length of the outlet sponge Zone in x-Direction

    #Meshing
    #aspectRatio, of the cells right at the Core nozzle exit
    #y_count_core, amount of cells in y-direction for the Core
    #xCountSponge, how many cells the XCount Sponge Zone will consist off

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
    wedge.set_patch("right","mergeCore")
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
    yCountBypass = yCount

    wedge.set_patch("right","mergeConnecting")

    shapes.append(wedge)

    #FAR Field
    points = [[0,radiusBypass,0],[lengthDomain,radiusBypass,0],[lengthDomain,radiusBypass+heightDomain,0],[0,radiusBypass+heightDomain,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xCellNozel, c2c_expansion=expansionX)
    wedge.chop(1,start_size=ySizeBypass,c2c_expansion=expansionY)

    wedge.set_patch("right","mergeFarField")

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

    #Sponge Zone 1
    points = [[lengthDomain,0,0],[lengthDomain + lengthSponge,0,0],[lengthDomain + lengthSponge, radiusCore,0],[lengthDomain, radiusCore,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    #We find the y count that gives us the lowest AR
    xDist = lengthSponge / XCountSponge
    yCount = round((radiusCore) / xDist)

    wedge.chop(0,count=XCountSponge)
    wedge.chop(1,count=y_count_core / mergeFactorSponge)

    wedge.set_patch("left","mainCore")

    shapes.append(wedge)

    #Sponge Zone 2
    points = [[lengthDomain,radiusCore,0],[lengthDomain + lengthSponge,radiusCore,0],[lengthDomain + lengthSponge, radiusBypass,0],[lengthDomain, radiusBypass,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    #We find the y count that gives us the lowest AR
    xDist = lengthSponge / XCountSponge
    yCount = round((radiusBypass - radiusCore) / xDist)
    wedge.chop(0,count=XCountSponge)
    wedge.chop(1,count=yCountBypass / mergeFactorSponge)
    wedge.set_patch("left","mainConnecting")
    shapes.append(wedge)

    #Sponge Zone 3
    points = [[lengthDomain,radiusBypass,0],[lengthDomain + lengthSponge,radiusBypass,0],[lengthDomain + lengthSponge, radiusBypass + heightDomain,0],[lengthDomain, radiusBypass + heightDomain,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    #We find the y count that gives us the lowest AR
    xDist = lengthSponge / XCountSponge
    yCount = round((heightDomain) / xDist)
    wedge.chop(0,count=XCountSponge)
    wedge.chop(1,start_size=ySizeBypass * mergeFactorSponge, c2c_expansion=expansionY)
    wedge.set_patch("left","mainFarField")
    shapes.append(wedge)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    #Merge Patches since they are non conformal
    mesh.merge_patches("mainCore","mergeCore")
    mesh.merge_patches("mainConnecting","mergeConnecting")
    mesh.merge_patches("mainFarField","mergeFarField")

    mesh.set_default_patch("farField","patch")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("nozzle","wall")
    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")

class swallowingBlocks:
    def __init__(self,id,bottomRighCorner,upperLeftCorner,ang,subsections,yCellsStart,xSizeStart,expansionPerSection,reductionPerStep):
        self.id = id
        self.deltaX = upperLeftCorner[0] - bottomRighCorner[0]
        self.deltaY = upperLeftCorner[1] - bottomRighCorner[1]
        self.bottomRightCorner = bottomRighCorner
        self.shapes = []
        self.subsections = subsections

        ySize = self.deltaY / yCellsStart
        xSize = xSizeStart

        self.slaveNames = [] #Arrays holding the patch names for later merging
        self.masterNames = []

        #assemble the blocks
        for i in range(0,subsections):

            #Corner positions
            bL = self.relativePosition(i / subsections,0)
            bR = self.relativePosition((i + 1) / subsections,0)
            tR = self.relativePosition((i + 1) / subsections,1)
            tL = self.relativePosition(i / subsections,1)

            p = [bL,bR,tR,tL]
            f = cb.Face(p)
            w = cb.Wedge(f,ang)

            w.chop(axis=0,start_size=xSize, end_size=xSize * expansionPerSection)
            xSize = expansionPerSection * xSize
            yCount = yCellsStart / (reductionPerStep ** i)
            w.chop(axis=1,count=yCount) 

            #Name Patches for merging
            if(i > 0):
                name = "slaveMerge" + str(i) + str(self.id)
                self.slaveNames.append(name)
                w.set_patch("left",name)
            if(i < subsections - 1):
                name = "masterMerge" + str(i) + str(self.id)
                self.masterNames.append(name)
                w.set_patch("right",name)

            self.shapes.append(copy.deepcopy(w))

        print("Debug")

    def appendOnMesh(self,mesh):
        #Add all to the mesh
        for shape in self.shapes:
            mesh.add(shape)
        
        return mesh

    
    def merge(self,mesh):
        for i in range(0,self.subsections - 1):
            mesh.merge_patches(self.masterNames[i],self.slaveNames[i])

        return mesh

    def relativePosition(self,xRel,yRel):
        x = self.bottomRightCorner[0] + xRel * self.deltaX
        y = self.bottomRightCorner[1] + yRel * self.deltaY
        return [x,y,0]
    
    def slaveUpperPatches(self):
        #turb the upper Patches into slaves for merging (ufff)
        self.upperNames = []
        for i in range(0,self.subsections):
            name = "slaveMergeUpper" + str(i) + str(self.id)
            self.upperNames.append(name)
            self.shapes[i].set_patch("back",name)
    
    def masterLowerPatches(self):
        #turb the upper Patches into slaves for merging (ufff)
        self.lowerNames = []
        for i in range(0,self.subsections):
            name = "masterMergeLower" + str(i) + str(self.id)
            self.lowerNames.append(name)
            self.shapes[i].set_patch("front",name)

    def mergeAsMaster(self,otherBlock,mesh):
        for i in range(0,self.subsections):
            mesh.merge_patches(self.lowerNames[i],otherBlock.upperNames[i])
        
        return mesh
    
    def slaveFront(self):
        #turns the Front into a slave patch for merging
        self.frontName = "slaveFront" + str(self.id)
        self.shapes[0].set_patch("left",self.frontName)
    

class swallowingBlocksExpanding:
    def __init__(self,id,bottomRighCorner,upperLeftCorner,ang,subsections,yStartSize,yExpansionRatio,xStartSize,expansionPerSection,reductionPerStep,mantelIsWall = False):
        self.id = id
        self.deltaX = upperLeftCorner[0] - bottomRighCorner[0]
        self.deltaY = upperLeftCorner[1] - bottomRighCorner[1]
        self.bottomRightCorner = bottomRighCorner
        self.shapes = []
        self.subsections = subsections

        xSize = xStartSize

        self.slaveNames = [] #Arrays holding the patch names for later merging
        self.masterNames = []

        #assemble the blocks
        for i in range(0,subsections):

            #Corner positions
            bL = self.relativePosition(i / subsections,0)
            bR = self.relativePosition((i + 1) / subsections,0)
            tR = self.relativePosition((i + 1) / subsections,1)
            tL = self.relativePosition(i / subsections,1)

            p = [bL,bR,tR,tL]
            f = cb.Face(p)
            w = cb.Wedge(f,ang)

            w.chop(axis=0,start_size=xSize, end_size=xSize * expansionPerSection)
            xSize = expansionPerSection * xSize
            w.chop(axis=1,start_size=yStartSize,c2c_expansion=yExpansionRatio) 

            #Name Patches for merging
            if(i > 0):
                name = "slaveMerge" + str(i) + str(self.id)
                self.slaveNames.append(name)
                w.set_patch("left",name)
            if(i < subsections - 1):
                name = "masterMerge" + str(i) + str(self.id)
                self.masterNames.append(name)
                w.set_patch("right",name)

            self.shapes.append(copy.deepcopy(w))

            #old System that made severly non orthogonal Faces

            #new system .. sucks kinda
            factorSize = 0
            for i in range(0,reductionPerStep):
                factorSize = factorSize + yExpansionRatio ** i

            yStartSize = yStartSize * factorSize
            yExpansionRatio = yExpansionRatio ** reductionPerStep

            #new system .. sucks kinda
            factorSize = 0

            for i in range(0,reductionPerStep):
                factorSize = factorSize + yExpansionRatio ** i

            #yStartSize = yStartSize * factorSize
            #yExpansionRatio = yExpansionRatio ** reductionPerStep

        print("Debug")

    def appendOnMesh(self,mesh):
        #Add all to the mesh
        for shape in self.shapes:
            mesh.add(shape)
        
        return mesh

    def merge(self,mesh):
        for i in range(0,self.subsections - 1):
            mesh.merge_patches(self.masterNames[i],self.slaveNames[i])

        return mesh

    def relativePosition(self,xRel,yRel):
        x = self.bottomRightCorner[0] + xRel * self.deltaX
        y = self.bottomRightCorner[1] + yRel * self.deltaY
        return [x,y,0]
    
    def slaveUpperPatches(self):
        #turb the upper Patches into slaves for merging (ufff)
        self.upperNames = []
        for i in range(0,self.subsections):
            name = "slaveMergeUpper" + str(i) + str(self.id)
            self.upperNames.append(name)
            self.shapes[i].set_patch("back",name)
    
    def masterLowerPatches(self):
        #turb the upper Patches into slaves for merging (ufff)
        self.lowerNames = []
        for i in range(0,self.subsections):
            name = "masterMergeLower" + str(i) + str(self.id)
            self.lowerNames.append(name)
            self.shapes[i].set_patch("front",name)

    def mergeAsMaster(self,otherBlock,mesh):
        for i in range(0,self.subsections):
            mesh.merge_patches(self.lowerNames[i],otherBlock.upperNames[i])
        
        return mesh
    
    def slaveFront(self):
        #turns the Front into a slave patch for merging
        self.frontName = "slaveFront" + str(self.id)
        self.shapes[0].set_patch("left",self.frontName)

    def setPatches(self,pathIdentifier,pathName):
        for shape in self.shapes:
            shape.set_patch(pathIdentifier,pathName)
    


def playground(file_path):

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    sCore = swallowingBlocks(0,[0,0,0],[10,1,0],ang,3,12,2,2,2)



    mesh = cb.Mesh()

    mesh = sCore.appendOnMesh(mesh)

    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("farField","patch")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")


def cascadedBypass(file_path,radiusCore,radiusBypass,lengthCore,lengthBypass,lengthHD,heightHD,aspectRatio,y_count_core,lengthSponge,
                   heightSponge, sectionsSponge,expansionPerSection,reductionPerStep = 2,yExpansion = 1, xExpansionInlet = 1, mantelIsWall = False):
    
    #Geometry
    #radiusCore, absolute radius of the Core Nozzel
    #radiusBypass, absolute radius of the Bypass Nozzle
    #lengthCore, relative "extension" of the Core Nozzle after the Bypass Nozzle, must be above 0
    #lengthBypass, length of the Wall till the Bypass Nozzle ends, must be above 0
    #lenthDomain, how far the domain extends in x-Direction after the Core Nozzle Exit, above 0
    #heightDomain, how far the Domain extends in y Deriction from the Radius of the Bypass Nozzle
    #lengthSponge, length of the outlet sponge Zone in x-Direction
    #Meshing
    #aspectRatio, of the cells right at the Core nozzle exit
    #y_count_core, amount of cells in y-direction for the Core
    #xCountSponge, how many cells the XCount Sponge Zone will consist off
    #Calculate the Cell sizes
    xCellNozel = aspectRatio * radiusCore / y_count_core
    yCellNozle = radiusCore / y_count_core

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #Block Core Nozzle
    points = [[0,0,0],[lengthHD,0,0],[lengthHD,radiusCore,0],[0,radiusCore,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.set_patch("left","core")
    wedge.set_patch("right","mergeCore")
    wedge.chop(0,start_size=xCellNozel)
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
    points = [[0,radiusCore,0],[lengthHD,radiusCore,0],[lengthHD,radiusBypass,0],[0,radiusBypass,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCount)

    wedge.set_patch("right","mergeConnecting")

    yCountBypass = yCount
    shapes.append(wedge)

    #The Songe Zone for the Core
    spongeCore = swallowingBlocks(0,[lengthHD,0,0],[lengthHD + lengthSponge,radiusCore,0],ang,sectionsSponge,y_count_core,xCellNozel,expansionPerSection,reductionPerStep)

    #The Sponge Zone for the Bypass
    spongeBypass = swallowingBlocks(1,[lengthHD,radiusCore,0],[lengthHD + lengthSponge,radiusBypass,0],ang,sectionsSponge,yCount,xCellNozel,expansionPerSection,reductionPerStep)

    #The Bypass Flow
    points = [[-lengthCore,radiusBypass,0], [0,radiusBypass,0],[0,radiusBypass+heightHD,0],[-lengthCore,radiusBypass+heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    yCountBP = round((heightHD) / ySizeBypass)

    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCountBP)

    shapes.append(wedge)

    points = [[0,radiusBypass,0],[lengthHD,radiusBypass,0],[lengthHD,radiusBypass + heightHD,0],[0,radiusBypass + heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.set_patch("right","mergeBypass")
    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCountBP)

    #The True Y Size we ended up with. needed for the outer sponges
    ySizeBP = (heightHD) / yCountBP

    shapes.append(wedge)

    spongeOuterBypass = swallowingBlocks(2,[lengthHD,radiusBypass,0],[lengthHD + lengthSponge,radiusBypass + heightHD,0],ang,sectionsSponge,yCountBP,xCellNozel,expansionPerSection,reductionPerStep)

    #The inlet sponge
    points = [[-lengthCore - lengthBypass,radiusBypass,0],[ -lengthCore, radiusBypass,0],[-lengthCore, radiusBypass + heightHD,0],[-lengthCore -lengthBypass, radiusBypass + heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,end_size=xSizeBypass, c2c_expansion= 1/xExpansionInlet)
    wedge.chop(1,count=yCountBP)

    wedge.set_patch("front","nozzle")

    shapes.append(wedge)

    #The Inlet Double sponge
    spongeDouble = swallowingBlocksExpanding(3,[lengthHD,radiusBypass + heightHD,0],[lengthHD + lengthSponge,radiusBypass + heightHD + heightSponge,0],ang,sectionsSponge,ySizeBP,yExpansion,xCellNozel,expansionPerSection,reductionPerStep)
    spongeDouble.setPatches("back","mantel")

    #The Manual Bock At the inlet with constant x Still
    points = [[-lengthCore,radiusBypass+heightHD,0],[0,radiusBypass+heightHD,0],[0,radiusBypass+heightHD+heightSponge,0],[-lengthCore,radiusBypass+heightHD+heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xSizeBypass)
    wedge.chop(1,start_size=ySizeBP, c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    points = [[0,radiusBypass + heightHD,0],[lengthHD,radiusBypass + heightHD,0],[lengthHD,radiusBypass + heightHD + heightSponge,0],[0,radiusBypass + heightHD + heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,start_size=ySizeBP, c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    #DOUBLE GRADED INLET BLOCK
    points = [[-lengthCore - lengthBypass,radiusBypass + heightHD,0],[-lengthCore,radiusBypass + heightHD,0],[-lengthCore,radiusBypass + heightHD + heightSponge,0],[-lengthCore - lengthBypass,radiusBypass + heightHD + heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,end_size=xSizeBypass, c2c_expansion= 1/xExpansionInlet)
    wedge.chop(1,count=ySizeBP,c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    #Append the sponges
    mesh = spongeCore.appendOnMesh(mesh)
    mesh = spongeBypass.appendOnMesh(mesh)
    mesh = spongeOuterBypass.appendOnMesh(mesh)
    mesh = spongeDouble.appendOnMesh(mesh)

    #Merge the Meshes
    mesh = spongeCore.merge(mesh)
    mesh = spongeBypass.merge(mesh)
    mesh = spongeOuterBypass.merge(mesh)
    mesh = spongeDouble.merge(mesh)

    spongeCore.slaveUpperPatches()
    spongeBypass.masterLowerPatches()
    mesh = spongeBypass.mergeAsMaster(spongeCore,mesh)

    spongeBypass.slaveUpperPatches()
    spongeOuterBypass.masterLowerPatches()
    mesh = spongeOuterBypass.mergeAsMaster(spongeBypass,mesh)

    spongeOuterBypass.slaveUpperPatches()
    spongeDouble.masterLowerPatches()
    mesh = spongeDouble.mergeAsMaster(spongeOuterBypass,mesh)

    #Manually Merge the Fronts
    spongeCore.slaveFront()
    spongeBypass.slaveFront()
    spongeOuterBypass.slaveFront()

    mesh.merge_patches("mergeCore",spongeCore.frontName)
    mesh.merge_patches("mergeConnecting",spongeBypass.frontName)
    mesh.merge_patches("mergeBypass",spongeOuterBypass.frontName)


    #set the type of empty patches


    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("nozzle","wall")

    if(mantelIsWall):
        mesh.patch_list.modify("mantel","wall")

    #debugging mode 

    mesh.set_default_patch("farField","patch")

    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")

def centerFocused(file_path,radiusCore,radiusBypass,lengthCore,lengthBypass,lengthHD,heightHD,aspectRatio,y_count_core,
                   heightSponge,transitionLength,transitionStretching,endSpongeLength,yExpansion = 1, xExpansionInlet = 1, mantelIsWall = False):
    
    #Geometry
    #radiusCore, absolute radius of the Core Nozzel
    #radiusBypass, absolute radius of the Bypass Nozzle
    #lengthCore, relative "extension" of the Core Nozzle after the Bypass Nozzle, must be above 0
    #lengthBypass, length of the Wall till the Bypass Nozzle ends, must be above 0
    #lenthDomain, how far the domain extends in x-Direction after the Core Nozzle Exit, above 0
    #heightDomain, how far the Domain extends in y Deriction from the Radius of the Bypass Nozzle
    #lengthSponge, length of the outlet sponge Zone in x-Direction
    #Meshing
    #aspectRatio, of the cells right at the Core nozzle exit
    #y_count_core, amount of cells in y-direction for the Core
    #xCountSponge, how many cells the XCount Sponge Zone will consist off
    #Calculate the Cell sizes
    xCellNozel = aspectRatio * radiusCore / y_count_core
    yCellNozle = radiusCore / y_count_core

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #Block Core Nozzle
    points = [[0,0,0],[lengthHD,0,0],[lengthHD,radiusCore,0],[0,radiusCore,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.set_patch("left","core")
    wedge.chop(0,start_size=xCellNozel)
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
    points = [[0,radiusCore,0],[lengthHD,radiusCore,0],[lengthHD,radiusBypass,0],[0,radiusBypass,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCount)


    yCountBypass = yCount
    shapes.append(wedge)

    
    #The Bypass Flow
    points = [[-lengthCore,radiusBypass,0], [0,radiusBypass,0],[0,radiusBypass+heightHD,0],[-lengthCore,radiusBypass+heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    yCountBP = round((heightHD) / ySizeBypass)

    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCountBP)

    shapes.append(wedge)

    points = [[0,radiusBypass,0],[lengthHD,radiusBypass,0],[lengthHD,radiusBypass + heightHD,0],[0,radiusBypass + heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,count=yCountBP)

    #The True Y Size we ended up with. needed for the outer sponges
    ySizeBP = (heightHD) / yCountBP

    shapes.append(wedge)

    #The inlet sponge
    points = [[-lengthCore - lengthBypass,radiusBypass,0],[ -lengthCore, radiusBypass,0],[-lengthCore, radiusBypass + heightHD,0],[-lengthCore -lengthBypass, radiusBypass + heightHD,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,end_size=xSizeBypass, c2c_expansion= 1/xExpansionInlet)
    wedge.chop(1,count=yCountBP)

    wedge.set_patch("front","nozzle")

    shapes.append(wedge)


    #The Manual Bock At the inlet with constant x Still
    points = [[-lengthCore,radiusBypass+heightHD,0],[0,radiusBypass+heightHD,0],[0,radiusBypass+heightHD+heightSponge,0],[-lengthCore,radiusBypass+heightHD+heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,start_size=xSizeBypass)
    wedge.chop(1,start_size=ySizeBP, c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    points = [[0,radiusBypass + heightHD,0],[lengthHD,radiusBypass + heightHD,0],[lengthHD,radiusBypass + heightHD + heightSponge,0],[0,radiusBypass + heightHD + heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)
    wedge.chop(0,start_size=xCellNozel)
    wedge.chop(1,start_size=ySizeBP, c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    #DOUBLE GRADED INLET BLOCK
    points = [[-lengthCore - lengthBypass,radiusBypass + heightHD,0],[-lengthCore,radiusBypass + heightHD,0],[-lengthCore,radiusBypass + heightHD + heightSponge,0],[-lengthCore - lengthBypass,radiusBypass + heightHD + heightSponge,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,ang)

    wedge.chop(0,end_size=xSizeBypass, c2c_expansion= 1/xExpansionInlet)
    wedge.chop(1,count=ySizeBP,c2c_expansion=yExpansion)

    wedge.set_patch("back","mantel")

    shapes.append(wedge)

    #Creting the transition region where cells are stretched
    points = [[lengthHD,0,0],[lengthHD + transitionLength,0,0],[lengthHD + transitionLength,radiusCore,0],[lengthHD,radiusCore,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size=xCellNozel,end_size=xCellNozel * transitionStretching)
    w.chop(1,count=y_count_core)

    shapes.append(w)

    points=[[lengthHD,radiusCore,0],[lengthHD+transitionLength,radiusCore,0],[lengthHD+transitionLength,radiusBypass,0],[lengthHD,radiusBypass,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size=xCellNozel,end_size=xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass)

    shapes.append(w)

    points = [[lengthHD,radiusBypass,0],[lengthHD + transitionLength,radiusBypass,0],[lengthHD + transitionLength,radiusBypass + heightHD,0],[lengthHD,radiusBypass+heightHD,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size=xCellNozel,end_size=xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass)

    shapes.append(w)

    points = [[lengthHD,radiusBypass + heightHD,0],[lengthHD + transitionLength,radiusBypass + heightHD,0],[lengthHD + transitionLength,radiusBypass + heightHD + heightSponge,0],[lengthHD,radiusBypass + heightHD + heightSponge,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.set_patch("back","mantel")

    w.chop(0,start_size=xCellNozel,end_size=xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass,c2c_expansion=yExpansion)

    shapes.append(w)

    #creating the end sponge
    points = [[lengthHD + transitionLength,0,0],[lengthHD + transitionLength + endSpongeLength,0,0],[lengthHD + transitionLength + endSpongeLength,radiusCore,0],[lengthHD + transitionLength,radiusCore,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size=xCellNozel * transitionStretching)
    w.chop(1,count=y_count_core)

    shapes.append(w)

    points=[[lengthHD + transitionLength,radiusCore,0],[lengthHD+transitionLength+endSpongeLength,radiusCore,0],[lengthHD+transitionLength+endSpongeLength,radiusBypass,0],[lengthHD+transitionLength,radiusBypass,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size=xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass)

    shapes.append(w)

    points = [[lengthHD + transitionLength,radiusBypass,0],[lengthHD + transitionLength+endSpongeLength,radiusBypass,0],[lengthHD + transitionLength+endSpongeLength,radiusBypass + heightHD,0],[lengthHD+transitionLength,radiusBypass+heightHD,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.chop(0,start_size = xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass)

    shapes.append(w)

    points = [[lengthHD+transitionLength,radiusBypass + heightHD,0],[lengthHD + transitionLength + endSpongeLength,radiusBypass + heightHD,0],[lengthHD + transitionLength + endSpongeLength,radiusBypass + heightHD + heightSponge,0],[lengthHD + transitionLength,radiusBypass + heightHD + heightSponge,0]]
    f = cb.Face(points)
    w = cb.Wedge(f,ang)

    w.set_patch("back","mantel")

    w.chop(0,start_size=xCellNozel * transitionStretching)
    w.chop(1,start_size=ySizeBypass,c2c_expansion=yExpansion)

    shapes.append(w)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)


    #set the type of empty patches


    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("nozzle","wall")

    if(mantelIsWall):
        mesh.patch_list.modify("mantel","wall")

    #debugging mode 

    mesh.set_default_patch("farField","patch")

    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")

