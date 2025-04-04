import classy_blocks as cb
import numpy as np
import os

def  wedge_mesh(directory,ri,ra,l,alpha,gamma,delta,x_count,buffer_count,exp_inner,exp_outer):    #create a classical based mesh 
    
    file_path = directory

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #size_buffer = ((ri + l * np.tan(np.deg2rad(alpha))) - (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))))/ (buffer_count)
    size_buffer = delta / (buffer_count)
    size_buffer = size_buffer * (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))) / (ri - delta)
    points_inner = [[0,0,0],[l,0,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[0,ri - delta,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner,angle=ang)
    
    wedge_inner.set_patch("left","inlet_inner")
    wedge_inner.set_patch("right","outlet")

    wedge_inner.chop(0,count = x_count)
    wedge_inner.chop(1,end_size = size_buffer,c2c_expansion = 1/exp_inner)

    shapes.append(wedge_inner)


    points_buffer_inner = [[0,ri - delta,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[0,ri,0]]
    face_buffer_inner = cb.Face(points_buffer_inner)
    wedge_buffer_inner = cb.Wedge(face_buffer_inner,angle=ang)

    wedge_buffer_inner.set_patch("left","inlet_inner")
    wedge_buffer_inner.set_patch("right","outlet")
    wedge_buffer_inner.chop(0,count = x_count)
    wedge_buffer_inner.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_inner)

    points_buffer_outer = [[0,ri,0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[0,ri+delta,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.set_patch("left","inlet_outer")
    wedge_buffer_outer.set_patch("right","outlet")
    wedge_buffer_outer.chop(0,count = x_count)
    wedge_buffer_outer.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_outer)

    points_outer = [[0,ri+delta,0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[l,ra,0],[0,ra,0]]
    face_outer = cb.Face(points_outer)
    wedge_outer = cb.Wedge(face_outer,angle=ang)

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


def  wedge_mesh_piped(directory,ri,ra,l,l_pipe,alpha,gamma,delta,x_count,buffer_count,exp_inner,exp_outer,exp_pipe):    #create a classical based mesh 
    
    file_path = directory

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #size_buffer = ((ri + l * np.tan(np.deg2rad(alpha))) - (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))))/ (buffer_count)
    size_buffer = delta / (buffer_count)
    #size_buffer = size_buffer * (ri - delta + l * np.tan(np.deg2rad(alpha - gamma))) / (ri - delta)
    points_inner = [[0,0,0],[l,0,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[0,ri - delta,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner,angle=ang)
    
    wedge_inner.set_patch("left","inlet_inner")
    wedge_inner.set_patch("right","outlet")

    wedge_inner.chop(0,count = x_count)
    wedge_inner.chop(1,end_size = size_buffer,c2c_expansion = 1/exp_inner, take = "min")

    shapes.append(wedge_inner)


    points_buffer_inner = [[0,ri - delta,0],[l,ri - delta + l * np.tan(np.deg2rad(alpha - gamma)),0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[0,ri,0]]
    face_buffer_inner = cb.Face(points_buffer_inner)
    wedge_buffer_inner = cb.Wedge(face_buffer_inner,angle=ang)

    wedge_buffer_inner.set_patch("left","inlet_inner")
    wedge_buffer_inner.set_patch("right","outlet")
    wedge_buffer_inner.chop(0,count = x_count)
    wedge_buffer_inner.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_inner)

    points_buffer_outer = [[0,ri,0],[l,ri + l * np.tan(np.deg2rad(alpha)),0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[0,ri+delta,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.set_patch("right","outlet")
    wedge_buffer_outer.chop(0,count = x_count)
    wedge_buffer_outer.chop(1,count = buffer_count)
    shapes.append(wedge_buffer_outer)


    points_outer = [[0,ri+delta,0],[l,ri + delta + l * np.tan(np.deg2rad(alpha + gamma)),0],[l,ra,0],[0,ra,0]]
    face_outer = cb.Face(points_outer)
    wedge_outer = cb.Wedge(face_outer,angle=ang)

    wedge_outer.set_patch("right","outlet")
    wedge_outer.chop(0,count = x_count)
    wedge_outer.chop(1,start_size = size_buffer, c2c_expansion = exp_outer,take = "max",preserve="start_size")
    shapes.append(wedge_outer)


    points_pipe_buffer = [[-1 * l_pipe,ri,0],[0,ri,0],[0,ri+delta,0],[-1 * l_pipe,ri+delta,0]]
    face_pipe_buffer = cb.Face(points_pipe_buffer)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)

    wedge_pipe_buffer.set_patch("left","inlet_outer")
    wedge_pipe_buffer.set_patch("front","pipe")
    wedge_pipe_buffer.chop(0,end_size = l/x_count, c2c_expansion = 1 / exp_pipe)
    wedge_pipe_buffer.chop(1,count = buffer_count)
    shapes.append(wedge_pipe_buffer)

    points_pipe_outer = [[-1 * l_pipe,ri + delta,0],[0, ri + delta,0],[0,ra,0],[-1 * l_pipe,ra,0]]
    face_pipe_outer = cb.Face(points_pipe_outer)
    wedge_pipe_outer = cb.Wedge(face_pipe_outer)

    wedge_pipe_outer.set_patch("left","inlet_outer")
    wedge_pipe_outer.chop(0,end_size = l/x_count, c2c_expansion = 1 / exp_pipe)
    wedge_pipe_outer.chop(1,start_size = size_buffer, c2c_expansion = exp_outer,take="min",preserve="start_size")
    shapes.append(wedge_pipe_outer)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("upper","patch")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("pipe","wall")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")


def optimized_wedge_piped(directory,ri,ra,l,l_pipe,alpha,x_count,core_y_refine,exp_ratio_y,exp_ratio_x_pipe):
    #ri is the pipe diameter
    #ra is the diameted of the domain
    #l is length of the domain
    #l_pipe is length of the pipe
    #alpha is expected spread angle
    #x_count is the chopping count of the jet domain in x-direction
    #core y_refinement dictates the core chopping count multiplyer total count is 15 * core_y_refine, only integers allowed

    file_path = directory
    #buildup
    shapes = []
    ang = np.deg2rad(2)

    #Create the mesh for the Jet Part
    #calculate predicted endpoints
    ri_1 = ri  + l * np.tan(np.deg2rad(alpha))

    def create_core_block(ri_0,x1,ri_1,y_rel_in,y_rel_a,refine_factor):
        #creates the subblocks to get the optimized chopping
        y_inner_0 =  y_rel_in * ri_0
        y_inner_1 =  y_rel_in * ri_1
        y_outer_0 =  y_rel_a * ri_0
        y_outer_1 =  y_rel_a * ri_1

        points = [[0,y_inner_0,0],[l,y_inner_1,0],[l,y_outer_1,0],[0,y_outer_0,0]]
        face = cb.Face(points)
        wedge = cb.Wedge(face,angle=ang)

        wedge.set_patch("left","inlet_inner")
        wedge.set_patch("right","outlet")
        wedge.chop(0,count = x_count)
        wedge.chop(1,count = core_y_refine - 1)
        shapes.append(wedge)
        return [(y_outer_0 - y_inner_0),(y_outer_1 - y_inner_1)]

    chop_points = [0, 5.26013094e-02, 1.15722881e-01, 1.91468768e-01,
               2.82363834e-01, 3.91437913e-01, 4.82332978e-01, 5.58078865e-01,
               6.48973930e-01, 7.24719816e-01, 7.87841388e-01, 8.40442697e-01,
               9.03564268e-01, 9.56165577e-01, 1.00000000e+00]

    last_cell_size = 0
    last_cell_size_rear = 0
    for i in range(0,14):
        last_cell_size,last_cell_size_rear = (create_core_block(ri,l,ri_1,chop_points[i],chop_points[i+1],core_y_refine))
        last_cell_size = last_cell_size / core_y_refine
        last_cell_size_rear = last_cell_size_rear / core_y_refine

    #Outer Block 
    #calculate the required length on the outlet to get nice cells
    factor_sum_er = (ra - ri) /last_cell_size
    l2 = factor_sum_er * last_cell_size_rear
    points = [[0,ri,0],[l,ri_1,0],[l,ra + 0 * l * np.tan(np.deg2rad(alpha)),0],[0,ra,0]]
    face = cb.Face(points)
    wedge = cb.Wedge(face,angle=ang)
    wedge.set_patch("right","outlet")
    wedge.chop(0,count = x_count)
    wedge.chop(1,start_size=last_cell_size,c2c_expansion=exp_ratio_y,take="min",preserve="end_size")
    shapes.append(wedge)

    points_pipe_buffer = [[-1 * l_pipe,ri,0],[0,ri,0],[0,ra,0],[-1 * l_pipe,ra,0]]
    face_pipe_buffer = cb.Face(points_pipe_buffer)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)
    #wedge_pipe_buffer.set_patch("left","inlet_outer")
    wedge_pipe_buffer.set_patch("front","pipe")
    wedge_pipe_buffer.chop(0,end_size = l/x_count, c2c_expansion = 1 / exp_ratio_x_pipe)
    wedge_pipe_buffer.chop(1,start_size=last_cell_size,c2c_expansion=exp_ratio_y)
    shapes.append(wedge_pipe_buffer)


    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)
    mesh.set_default_patch("inlet_outer","patch")
    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("pipe","wall")
    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")


def piped_double_stacked_wedge_mesh(directory,ri,ra,l,l_pipe,spread_angle,x_count,y_count,exp_Inlet,exp_Farfield,x_decay):    #create a classical based mesh 
    
    file_path = directory

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    x_size = l / (x_count)
    y_size = ri / y_count
    
    points_inner = [[0,0,0],[l,0,0],[l,ri,0],[0,ri,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner,angle=ang)
    
    wedge_inner.set_patch("left","inlet_inner")
    wedge_inner.set_patch("right","outlet")

    wedge_inner.chop(0,start_size=x_size,c2c_expansion= x_decay)
    wedge_inner.chop(1,count=y_count)

    shapes.append(wedge_inner)


    #the high deff area surrounding the pipe part, it extends up 1/4 the pipe length (approximatley)
    #calc the approximation distance
    x_target = 0.25 * l_pipe
    y_target = l * np.tan(np.deg2rad(spread_angle))

    x_size = l / (x_count)
    y_size = ri / y_count

    x_ext_count = np.rint(x_target / x_size)
    y_ext_count = np.rint(y_target / y_size)

    x_ext = -1 * x_ext_count * x_size
    y_ext = y_ext_count * y_size

    points_buffer_inner = [[0,ri,0],[l,ri ,0],[l,ri + y_ext ,0],[0,ri + y_ext,0]]
    face_buffer_inner = cb.Face(points_buffer_inner)
    wedge_buffer_inner = cb.Wedge(face_buffer_inner,angle=ang)

    wedge_buffer_inner.set_patch("right","outlet")
    wedge_buffer_inner.chop(0, start_size=x_size, c2c_expansion=x_decay)
    wedge_buffer_inner.chop(1,count = y_ext_count)
    shapes.append(wedge_buffer_inner)


    #Cut it in two, for the patches
    points_buffer_inner = [[x_ext,ri,0],[0,ri ,0],[0,ri + y_ext ,0],[x_ext,ri + y_ext,0]]
    face_pipe_buffer = cb.Face(points_buffer_inner)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)

    wedge_pipe_buffer.set_patch("front","pipe")
    wedge_pipe_buffer.chop(0,count=x_ext_count)
    wedge_pipe_buffer.chop(1,count=y_ext_count)
    shapes.append(wedge_pipe_buffer)


    #Circular part, that goes up towards the far field
    points_buffer_outer = [[0,ri + y_ext,0],[l,ri + y_ext,0],[l,ra,0],[0,ra,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.set_patch("right","outlet")
    wedge_buffer_outer.chop(0,start_size=x_size, c2c_expansion=x_decay)
    wedge_buffer_outer.chop(1,start_size=y_size,c2c_expansion=exp_Farfield)
    shapes.append(wedge_buffer_outer)


    points_buffer_outer = [[x_ext,ri + y_ext,0],[0,ri + y_ext,0],[0,ra,0],[x_ext,ra,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.chop(0,count=x_ext_count)
    wedge_buffer_outer.chop(1,start_size=y_size,c2c_expansion=exp_Farfield)
    shapes.append(wedge_buffer_outer)


    #Part at the "Inlet where the mesh gets lees defined" in only x_direction
    points_pipe_buffer = [[-1 * l_pipe,ri,0],[x_ext,ri,0],[x_ext,ri + y_ext,0],[-1 * l_pipe,ri + y_ext,0]]
    face_pipe_buffer = cb.Face(points_pipe_buffer)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)

    wedge_pipe_buffer.set_patch("left","inlet_outer")
    wedge_pipe_buffer.set_patch("front","pipe")
    wedge_pipe_buffer.chop(0,end_size = x_size, c2c_expansion = 1 / exp_Inlet)
    wedge_pipe_buffer.chop(1,start_size=y_size)
    shapes.append(wedge_pipe_buffer)

    #Part at the "Inlet where the mesh gets lees defined" in both directions
    points_pipe_outer = [[-1 * l_pipe,ri + y_ext,0],[x_ext, ri + y_ext,0],[x_ext,ra,0],[-1 * l_pipe,ra,0]]
    face_pipe_outer = cb.Face(points_pipe_outer)
    wedge_pipe_outer = cb.Wedge(face_pipe_outer)

    wedge_pipe_outer.set_patch("left","inlet_outer")
    wedge_pipe_outer.chop(0,end_size = x_size, c2c_expansion = 1 / exp_Inlet)
    wedge_pipe_outer.chop(1,start_size = y_size, c2c_expansion = exp_Farfield)
    shapes.append(wedge_pipe_outer)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("upper","patch")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")
    mesh.patch_list.modify("pipe","wall")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")

def piped_double_stacked_wedge_mesh_walled(directory,ri,ra,l,l_pipe,spread_angle,x_count,y_count,exp_Inlet,exp_Farfield,x_decay):    #create a classical based mesh 
    
    file_path = directory

    #buildup
    shapes = []
    ang = np.deg2rad(2)

    x_size = l / (x_count)
    y_size = ri / y_count
    
    points_inner = [[0,0,0],[l,0,0],[l,ri,0],[0,ri,0]]
    face_inner = cb.Face(points_inner)
    wedge_inner = cb.Wedge(face_inner,angle=ang)
    
    wedge_inner.set_patch("left","inlet_inner")
    wedge_inner.set_patch("right","outlet")

    wedge_inner.chop(0,start_size=x_size,c2c_expansion= x_decay)
    wedge_inner.chop(1,count=y_count)

    shapes.append(wedge_inner)


    #the high deff area surrounding the pipe part, it extends up 1/4 the pipe length (approximatley)
    #calc the approximation distance
    x_target = 0.25 * l_pipe
    y_target = l * np.tan(np.deg2rad(spread_angle))

    x_size = l / (x_count)
    y_size = ri / y_count

    x_ext_count = np.rint(x_target / x_size)
    y_ext_count = np.rint(y_target / y_size)

    x_ext = -1 * x_ext_count * x_size
    y_ext = y_ext_count * y_size

    points_buffer_inner = [[0,ri,0],[l,ri ,0],[l,ri + y_ext ,0],[0,ri + y_ext,0]]
    face_buffer_inner = cb.Face(points_buffer_inner)
    wedge_buffer_inner = cb.Wedge(face_buffer_inner,angle=ang)

    wedge_buffer_inner.set_patch("right","outlet")
    wedge_buffer_inner.chop(0, start_size=x_size, c2c_expansion=x_decay)
    wedge_buffer_inner.chop(1,count = y_ext_count)
    shapes.append(wedge_buffer_inner)


    #Cut it in two, for the patches
    points_buffer_inner = [[x_ext,ri,0],[0,ri ,0],[0,ri + y_ext ,0],[x_ext,ri + y_ext,0]]
    face_pipe_buffer = cb.Face(points_buffer_inner)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)

    wedge_pipe_buffer.chop(0,count=x_ext_count)
    wedge_pipe_buffer.chop(1,count=y_ext_count)
    shapes.append(wedge_pipe_buffer)


    #Circular part, that goes up towards the far field
    points_buffer_outer = [[0,ri + y_ext,0],[l,ri + y_ext,0],[l,ra,0],[0,ra,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.set_patch("right","outlet")
    wedge_buffer_outer.chop(0,start_size=x_size, c2c_expansion=x_decay)
    wedge_buffer_outer.chop(1,start_size=y_size,c2c_expansion=exp_Farfield)
    shapes.append(wedge_buffer_outer)


    points_buffer_outer = [[x_ext,ri + y_ext,0],[0,ri + y_ext,0],[0,ra,0],[x_ext,ra,0]]
    face_buffer_outer = cb.Face(points_buffer_outer)
    wedge_buffer_outer = cb.Wedge(face_buffer_outer,angle=ang)

    wedge_buffer_outer.chop(0,count=x_ext_count)
    wedge_buffer_outer.chop(1,start_size=y_size,c2c_expansion=exp_Farfield)
    shapes.append(wedge_buffer_outer)


    #Part at the "Inlet where the mesh gets lees defined" in only x_direction
    points_pipe_buffer = [[-1 * l_pipe,ri,0],[x_ext,ri,0],[x_ext,ri + y_ext,0],[-1 * l_pipe,ri + y_ext,0]]
    face_pipe_buffer = cb.Face(points_pipe_buffer)
    wedge_pipe_buffer = cb.Wedge(face_pipe_buffer)

    wedge_pipe_buffer.set_patch("left","inlet_outer")
    wedge_pipe_buffer.chop(0,end_size = x_size, c2c_expansion = 1 / exp_Inlet)
    wedge_pipe_buffer.chop(1,start_size=y_size)
    shapes.append(wedge_pipe_buffer)

    #Part at the "Inlet where the mesh gets lees defined" in both directions
    points_pipe_outer = [[-1 * l_pipe,ri + y_ext,0],[x_ext, ri + y_ext,0],[x_ext,ra,0],[-1 * l_pipe,ra,0]]
    face_pipe_outer = cb.Face(points_pipe_outer)
    wedge_pipe_outer = cb.Wedge(face_pipe_outer)

    wedge_pipe_outer.set_patch("left","inlet_outer")
    wedge_pipe_outer.chop(0,end_size = x_size, c2c_expansion = 1 / exp_Inlet)
    wedge_pipe_outer.chop(1,start_size = y_size, c2c_expansion = exp_Farfield)
    shapes.append(wedge_pipe_outer)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)

    mesh.set_default_patch("pipe","wall")

    #set the type of empty patches
    mesh.patch_list.modify("wedge_back","wedge")
    mesh.patch_list.modify("wedge_front","wedge")

    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")

def full_rotational_mesh(directory,ri,ra,l,l_pipe,spread_angle,x_count,y_count,exp_Inlet,exp_Farfield,x_decay,createMantel = False, mantelIsWall = False):
    file_path = directory
    #buildup
    shapes = []
   
    x_size = l / (x_count)
    y_size = ri / y_count

    x_target = 0.25 * l_pipe
    y_target = l * np.tan(np.deg2rad(spread_angle))
    x_size = l / (x_count)
    y_size = ri / y_count
    x_ext_count = np.rint(x_target / x_size)
    y_ext_count = np.rint(y_target / y_size)
    x_ext = -1 * x_ext_count * x_size
    y_ext = y_ext_count * y_size

    #Inner Cylinder
    inlet_inner = [0,0,0]
    outlet_inner = [l,0,0]
    radius_inner = [0,ri,0]

    inner_cylinder = cb.Cylinder(inlet_inner,outlet_inner,radius_inner)

    inner_cylinder.chop_axial(start_size = x_size,c2c_expansion = x_decay)
    inner_cylinder.chop_radial(start_size = y_size)
    inner_cylinder.chop_tangential(start_size = y_size)
    
    inner_cylinder.set_start_patch("inlet")

    cb.SemiCylinder

    shapes.append(inner_cylinder)

    #High Def surrounding inner and pipe

    hd_outflow = cb.ExtrudedRing.expand(inner_cylinder,y_ext)
    hd_outflow.chop_radial(start_size = y_size)
    shapes.append(hd_outflow)

    hd_pipe = cb.ExtrudedRing.chain(hd_outflow,-1 * x_ext,start_face=True)
    hd_pipe.chop_axial(start_size = x_size)
    hd_pipe.set_inner_patch("pipe")
    shapes.append(hd_pipe)

    #Surrounding ring
    
    outflow_ring = cb.ExtrudedRing.expand(hd_outflow,ra - ri - y_ext)

    #outflow_ring.chop_axial(start_size = x_size,c2c_expansion = x_decay)
    outflow_ring.chop_radial(start_size = y_size, c2c_expansion = exp_Farfield)
    #outflow_ring.chop_tangential(start_size = y_size)
    if(createMantel):
        outflow_ring.set_outer_patch("mantel")

    shapes.append(outflow_ring)

    pip_hd_mantel = cb.ExtrudedRing.chain(outflow_ring, -1 * x_ext, start_face=True)
    pip_hd_mantel.chop_axial(start_size = x_size)
    if(createMantel):
        pip_hd_mantel.set_outer_patch("mantel")
    shapes.append(pip_hd_mantel)

    pipe_buffer = cb.ExtrudedRing.chain(hd_pipe,l_pipe + x_ext)
    pipe_buffer.chop_axial(start_size = x_size, c2c_expansion = exp_Inlet)
    pipe_buffer.set_inner_patch("pipe")
    shapes.append(pipe_buffer)

    Inflow_Buffer = cb.ExtrudedRing.chain(pip_hd_mantel,l_pipe + x_ext)
    Inflow_Buffer.chop_axial(start_size = x_size, c2c_expansion = exp_Inlet)
    if(createMantel):
        Inflow_Buffer.set_outer_patch("mantel")
    shapes.append(Inflow_Buffer)

    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)
    mesh.set_default_patch("FarField","patch")
    #set the type of empty patches

    mesh.patch_list.modify("pipe","wall")

    if(mantelIsWall and createMantel):
        mesh.patch_list.modify("mantel","wall")

    #debugging mode 
    mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    #mesh.write(file_path + "/system/blockMeshDict")