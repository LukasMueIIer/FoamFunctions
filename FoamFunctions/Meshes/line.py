import classy_blocks as cb
import numpy as np
import os

def basic_line(directory,length,chop_count,width=1):
    file_path = directory


    #buildup
    shapes = []

    line = cb.Box([0,-width/2,-width/2],[length,width/2,width/2])
    

    line.set_patch("left","wall")
    line.set_patch("right","wall")
    line.chop(axis=0,count = chop_count)
    line.chop(axis=1,count=1)
    line.chop(axis=2,count=1)

    shapes.append(line)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("empty","empty")
    mesh.patch_list.modify("wall","wall")
    mesh.write(file_path + "/system/blockMeshDict")

def dampened_line(directory,length,chop_count,width=1,damp_zone = 0.5,c2c=10):
    file_path = directory

    size = (length/2 * (1 + damp_zone)) - (length/2 * (1 - damp_zone)) 
    size = size / chop_count

    #buildup
    shapes = []

    #damp zone 1
    line1 = cb.Box([0,-width/2,-width/2],[length/2 * (1 - damp_zone),width/2,width/2])
    
    line1.set_patch("left","wall")
    line1.chop(axis=0, end_size= size,start_size= c2c * size)
    line1.chop(axis=1,count=1)
    line1.chop(axis=2,count=1)

    shapes.append(line1)

    #center zone
    line2 = cb.Box([length/2 * (1 - damp_zone),-width/2,-width/2],[length/2 * (1 + damp_zone),width/2,width/2])
    
    line2.chop(axis=0,count = chop_count)
    line2.chop(axis=1,count=1)
    line2.chop(axis=2,count=1)

    shapes.append(line2)

    #damp zone 2
    line3 = cb.Box([length/2 * (1 + damp_zone),-width/2,-width/2],[length,width/2,width/2])
    
    line3.set_patch("right","wall")
    line3.chop(axis=0,end_size= c2c * size , start_size= size)
    line3.chop(axis=1,count=1)
    line3.chop(axis=2,count=1)

    shapes.append(line3)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("empty","empty")
    mesh.patch_list.modify("wall","wall")
    mesh.write(file_path + "/system/blockMeshDict")