from utils.obj import parse_obj
from mesh import Mesh

# Parse the obj file (bunny.obj)
vertices, faces, lines = parse_obj()

# Create the initial mesh
mesh_init = Mesh(vertices, faces)
#print(mesh_init.get_nb_edges())

# Create the new obj file
new_obj = open("data/new_obj.obj", "a")
new_obj.writelines(lines)

# Edge collapses
mesh = mesh_init.copy()
while 1:
    
    #
    vertex_ind, face_ind = mesh.edge_collapse()
    mesh.delete_vertex()







# Close file
new_obj.close()