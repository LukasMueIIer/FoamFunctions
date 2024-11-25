import classy_blocks as cb
import numpy as np
import os

def basic_line(directory,length,width=1):
    file_path = directory


    #buildup
    shapes = []

    line = cb.Box([-length/2,-width/2,-width/2],[length/2,width/2,width/2])
    line.set_patch("left","wall")
    line.set_patch("right","wall")
    shapes.append(line)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("empty","empty")
    mesh.patch_list.modify("wall","wall")
    mesh.write(file_path + "/system/blockMeshDict")