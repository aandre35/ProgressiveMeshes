from utils.obj import parse_obj
from mesh import Mesh
from mesh_bis import Mesh_Bis
import numpy as np
import os

# Parse the obj file (bunny.obj)
vertices, faces, lines = parse_obj()

# Create the initial mesh
mesh = Mesh_Bis(vertices, faces)
nb_faces_init = mesh.get_nb_faces()
compression_rate = 0.1
#print(mesh_init.get_nb_edges())

# Test 
#print(mesh.priority_queue[0:10])

# Counter
cpt = 0
################### Compression ###################
while cpt < 1000 and mesh.get_nb_faces() > nb_faces_init * compression_rate:
    
    # Display the iteration number
    print("\nIteration Edge Collapse {}".format(cpt+1))

    # Edge collapse
    mesh.edge_collapse()

    # cpt incrementation
    cpt += 1

lines_after_compression = mesh.write_obj()

cpt2 = 0
lines = []
while cpt2 < cpt:

    print("\nIteration VSplit {}".format(cpt2+1))
    
    lines = np.append(lines, mesh.vsplit())

    cpt2 += 1

# Create the new obj file
path = "data/obj_final.obja"
os.remove(path)
new_obj = open(path, "a")
new_obj.writelines(lines_after_compression)
new_obj.writelines(lines)
new_obj.close()
