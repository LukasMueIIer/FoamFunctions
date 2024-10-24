import classy_blocks as cb
import numpy as np
import os

def  wedge_mesh(directory,ri,ra,l,alpha,gamma,delta,x_count,buffer_count,exp_inner,exp_outer):    #create a classical based mesh 
    

    file_path = directory

    #buildup
    shapes = []

    #size_buffer = ((ri + l * np.tan(np.deg2rad(alpha))) - (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))))/ (buffer_count)
    size_buffer = delta / (buffer_count)
    size_buffer = size_buffer * (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))) / (ri - delta)
    points_inner = [[0,0,0],[l,0,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[0,ri - delta,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner)
    
    wedge_inner.set_patch("left","inlet_inner")
    wedge_inner.set_patch("right","outlet")

    wedge_inner.chop(0,count = x_count)
    wedge_inner.chop(1,end_size = size_buffer,c2c_expansion = 1/exp_inner)

    shapes.append(wedge_inner)


    points_buffer_inner = [[0,ri - delta,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[0,ri,0]]
    face_buffer_inner = cb.Face(points_buffer_inner)
    wedge_buffer_inner = cb.Wedge(face_buffer_inner)

    wedge_buffer_inner.set_patch("left","inlet_inner")
    wedge_buffer_inner.set_patch("right","outlet")
    wedge_buffer_inner.chop(0,count = x_count)
    wedge_buffer_inner.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_inner)

    points_buffer_outer = [[0,ri,0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[0,ri+delta,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer)

    wedge_buffer_outer.set_patch("left","inlet_outer")
    wedge_buffer_outer.set_patch("right","outlet")
    wedge_buffer_outer.chop(0,count = x_count)
    wedge_buffer_outer.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_outer)

    points_outer = [[0,ri+delta,0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[l,ra,0],[0,ra,0]]
    face_outer = cb.Face(points_outer)
    wedge_outer = cb.Wedge(face_outer)

    wedge_outer.set_patch("left","inlet_outer")
    wedge_outer.set_patch("right","outlet")
    wedge_outer.chop(0,count = x_count)
    wedge_outer.chop(1,start_size = size_buffer, c2c_expansion = exp_outer)
    shapes.append(wedge_outer)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("upper","patch")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")
