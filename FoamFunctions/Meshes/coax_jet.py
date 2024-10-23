import classy_blocks as cb
import numpy as np
import os

def  classic_mesh(directory,ri,ra,l,alpha,gamma,delta):    #create a classical based mesh 
    

    file_path = directory

    #buildup
    shapes = []

    points_inner = [[0,0,0],[l,0,0],[l,ri - delta + l * np.tan(alpha - gamma),0],[0,ri - delta,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner)
    
    wedge_inner.chop(0,count = 10)
    wedge_inner.chop(1,cont = 10)
    wedge_inner.chop(2,count = 1)

    shape.append(wedge_inner)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("far_field","patch")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")
