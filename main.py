from utils.obj import parse_obj
from mesh import Mesh
from mesh_bis import Mesh_Bis
import numpy as np
import os

# Parse the obj file (bunny.obj)
vertices, faces, lines = parse_obj()

# Create the initial mesh
mesh = Mesh_Bis(vertices, faces)
nb_vertices_init = mesh.get_nb_vertices()
compression_rate = 0.5
#print(mesh_init.get_nb_edges())

# Test 
#print(mesh.priority_queue[0:10])

# Counter
cpt = 1
################### Compression ###################
while cpt < 1000 and mesh.get_nb_vertices() > nb_vertices_init * (1 - compression_rate):
    # Display the iteration number
    print("\n\nIteration {}\n".format(cpt))

    # Edge collapses
    mesh.edge_collapse()

    # cpt incrementation
    cpt += 1
    


################### Decompression ###################

# Create the new obj file
path = "data/obj_final.obja"
os.remove(path)
new_obj = open(path, "a")
new_obj.writelines(mesh.write_obj())
new_obj.close()