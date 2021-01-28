from utils.obj import parse_obj
from mesh import Mesh
import numpy as np
import os

# Parse the obj file (bunny.obj)
vertices, faces, lines = parse_obj()

# Create the initial mesh
mesh_init = Mesh(vertices, faces)
#print(mesh_init.get_nb_edges())

# Copy of the initial mesh
mesh = mesh_init.copy()

# Test 
#print(mesh.priority_queue[0:10])

# Counter
cpt = 1
################### Compression ###################
while cpt < 200:#mesh.get_nb_vertices() > 100:
    # Display the iteration number
    print("\n\nIteration number {}\n".format(cpt))

    # Edge collapses
    new_lines = mesh.edge_collapse()
    lines = np.append(lines, new_lines)

    # cpt incrementation
    cpt += 1
    


################### Decompression ###################

# Create the new obj file
path = "data/new_obj.obja"
os.remove(path)
new_obj = open(path, "a")
new_obj.writelines(lines)
new_obj.close()