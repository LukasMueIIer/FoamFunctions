import classy_blocks as cb
import numpy as np
import os

def  classic_mesh(directory,diameter,y_wall,rad_count):    #create a classical based mesh 

    file_path = directory
    #classic chopping approach for the cylinder in freestream
    #geometry
    d = diameter #diameter cylinder
    h = 10 * diameter   #hight of simulated "channel"
    l1 = 15 * diameter  #length from inlet to center cylinder
    l2 = 20 * diameter  #length form center cylinder to outlet
    dist_extrude = 0.01 #depth in z direction
    #Subdivision and meshing
    d_2 = 4 * diameter   #radius ov the "virtual cylinder"
    if(d_2 < d):
        print("Virtual cylinder is too small, change d_2")
        exit(1)

    bl_cylinder = y_wall #height first cell of Cylinder BL
    expansion_ratio_bl_cylinder = 1.03 #expansion ratio of boundary layer
    radial_count = rad_count #8 * 15   #amount of radial sections around cylinder

    inlet_cell_count = 30       #amount of cells for inlet
    inlet_expansion_ratio = 1.05 #expansion ratio towards the inlet (larger at inlet)


    #file_path = os.path.dirname(os.path.realpath(__file__)) #to write relative to script path


    #buildup
    shapes = []
    #cyrcle containing sqare
    #A
    #some geometry calcs
    sr2 = np.sqrt(2) / 2    #for the diagonal
    r = d/2
    r2 = d_2 / 2

    #innder cylinder
    points_A = [[r,0,0],
                [r2,0,0],
                [r2 * sr2,r2*sr2,0],
                [r * sr2,r*sr2,0]]
    edges_A = [None,
            cb.Origin([0,0,0]),
            None,
            cb.Origin([0,0,0])]
    face_A = cb.Face(points_A,edges_A)
    A = cb.Extrude(face_A,dist_extrude)
    A.chop(0,start_size= bl_cylinder, c2c_expansion = expansion_ratio_bl_cylinder)
    A.chop(1,count=radial_count/8)
    A.chop(2,count=1)
    A.set_patch("top","empty_top")
    A.set_patch("bottom","empty_bottom")
    A.set_patch("left","cylinder")
    shapes.append(A)

    points_B = [[r*sr2,r*sr2,0],
                [r2 * sr2,r2*sr2,0],
                [0,r2,0],
                [0,r,0]]
    edges_B = [None,
            cb.Origin([0,0,0]),
            None,
            cb.Origin([0,0,0])]
    face_B = cb.Face(points_B,edges_B)
    B = cb.Extrude(face_B,dist_extrude)
    B.chop(0,start_size= bl_cylinder, c2c_expansion = expansion_ratio_bl_cylinder)
    B.chop(1,count=radial_count/8)
    B.chop(2,count=1)
    B.set_patch("top","empty_top")
    B.set_patch("bottom","empty_bottom")
    B.set_patch("left","cylinder")
    shapes.append(B)

    points_C = [[r2,0,0],
                [h/2,0,0],
                [h/2,sr2*r2,0],
                [sr2 * r2,sr2 * r2,0]]
    edges_C = [None,
            None,
            None,
            cb.Origin([0,0,0])]
    face_C = cb.Face(points_C,edges_C)
    C = cb.Extrude(face_C,dist_extrude)
    #try making cells quadratic
    ch = (sr2*r2) / (radial_count/8)
    c_cells_x = round((h/2 - r2)/ch)
    C.chop(0,count=c_cells_x)
    C.chop(1,count=radial_count/8)
    C.chop(2,count=1)
    C.set_patch("top","empty_top")
    C.set_patch("bottom","empty_bottom")
    shapes.append(C)

    points_D = [[sr2 * r2,sr2 * r2,0],
                [h/2,sr2*r2,0],
                [h/2,h/2,0],
                [sr2*r2,h/2,0]]
    face_D = cb.Face(points_D)
    D = cb.Extrude(face_D,dist_extrude)
    D.chop(0,count = c_cells_x)
    D.chop(1,count = c_cells_x)
    D.chop(2,count=1)
    D.set_patch("top","empty_top")
    D.set_patch("bottom","empty_bottom")
    shapes.append(D)

    points_E = [[sr2*r2,sr2*r2,0],
                [sr2*r2,h/2,0],
                [0,h/2,0],
                [0,r2,0]]
    edges_E = [None,
            None,
            None,cb.Origin([0,0,0])]
    face_E = cb.Face(points_E,edges_E)
    E = cb.Extrude(face_E,dist_extrude)
    E.chop(0,count=c_cells_x)
    E.chop(1,count=radial_count/8)
    E.chop(2,count=1)
    E.set_patch("top","empty_top")
    E.set_patch("bottom","empty_bottom")
    shapes.append(E)

    #mirror at y-axis
    for i in range(0,len(shapes)):
        shapes.append(shapes[i].copy().mirror([1,0,0]))


    #create inlet
    points_inlet_A = [[h/2,sr2*r2,0],
                    [l1,sr2*r2,0],
                    [l1,h/2,0],
                    [h/2,h/2,0]]
    face_inlet_A = cb.Face(points_inlet_A)
    inlet_A = cb.Extrude(face_inlet_A,dist_extrude)
    inlet_A.chop(0,count = inlet_cell_count, c2c_expansion = inlet_expansion_ratio)
    inlet_A.chop(1,count = c_cells_x)
    inlet_A.chop(2,count=1)
    inlet_A.set_patch("right","inlet")
    inlet_A.set_patch("top","empty_top")
    inlet_A.set_patch("bottom","empty_bottom")
    shapes.append(inlet_A)

    points_inlet_B = [[h/2,0,0],
                    [l1,0,0],
                    [l1,sr2*r2,0],
                    [h/2,sr2*r2,0]]
    face_inlet_B = cb.Face(points_inlet_B)
    inlet_B = cb.Extrude(face_inlet_B,dist_extrude)
    inlet_B.chop(0,count = inlet_cell_count, c2c_expansion = inlet_expansion_ratio)
    inlet_B.chop(1,count = radial_count/8)
    inlet_B.chop(2,count=1)
    inlet_B.set_patch("right","inlet")
    inlet_B.set_patch("top","empty_top")
    inlet_B.set_patch("bottom","empty_bottom")
    shapes.append(inlet_B)


    #crete outlet
    points_outlet_A = [[-l2,sr2*r2,0],
                    [-h/2,sr2*r2,0],
                    [-h/2,h/2,0],
                    [-l2,h/2,0]]
    face_outlet_A = cb.Face(points_outlet_A)
    outlet_A = cb.Extrude(face_outlet_A,dist_extrude)
    outlet_A.chop(0,count = 100)
    outlet_A.chop(1,count = c_cells_x)
    outlet_A.chop(2,count=1)
    outlet_A.set_patch("left","outlet")
    outlet_A.set_patch("top","empty_top")
    outlet_A.set_patch("bottom","empty_bottom")
    shapes.append(outlet_A)

    points_outlet_B = [[-l2,0,0],
                    [-h/2,0,0],
                    [-h/2,sr2*r2,0],
                    [-l2,sr2*r2,0]]
    face_outlet_B = cb.Face(points_outlet_B)
    outlet_B = cb.Extrude(face_outlet_B,dist_extrude)
    outlet_B.chop(0,count = 10)             #TODO maybe ad c2c expansion for numeric dampening
    outlet_B.chop(1,count = radial_count/8)
    outlet_B.chop(2,count=1)
    outlet_B.set_patch("left","outlet")
    outlet_B.set_patch("top","empty_top")
    outlet_B.set_patch("bottom","empty_bottom")
    shapes.append(outlet_B)




    #mirror at x-axis
    for i in range(0,len(shapes)):
        shapes.append(shapes[i].copy().mirror([0,1,0]))


    # add everything to mesh
    mesh = cb.Mesh()
    for shape in shapes:
        mesh.add(shape)
    #mesh.set_default_patch("walls", "wall") #we want far field
    mesh.set_default_patch("far_field","patch")

    #set the type of empty patches
    mesh.patch_list.modify("empty_top","empty")
    mesh.patch_list.modify("empty_bottom","empty")
    #set the type of the cylinder
    mesh.patch_list.modify("cylinder","wall")
    #debugging mode 
    #mesh.write(file_path + "/system/blockMeshDict", "debug.vtk")
    mesh.write(file_path + "/system/blockMeshDict")
