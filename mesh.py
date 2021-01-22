from utils.obj import rewrite_obj
class Mesh:

    def __init__(self, vertices, faces, lines):
        self.vertices = vertices
        self.faces = faces


    @property
    def edges(self):
        edges = []
        for i in range(len(self.faces)):
            #Veiller à toujours mettre les arêtes dans l'ordre de sommet croissant
            e1 = [min(self.faces[i][0], self.faces[i][1]), max(self.faces[i][0], self.faces[i][1])]
            if e1 not in edges:
                edges.append(e1)
            e2 = [min(self.faces[i][1], self.faces[i][2]), max(self.faces[i][1], self.faces[i][2])]
            if e2 not in edges:
                edges.append(e2)
            e3 = [min(self.faces[i][0], self.faces[i][2]), max(self.faces[i][0], self.faces[i][2])]
            if e3 not in edges:
                edges.append(e3)
        return edges

    def get_nb_edges(self):
        return len(self.edges)

    def get_nb_faces(self):
        return len(self.faces)
    
    def get_nb_vertices(self):
        return len(self.vertices)

    def translate_vertex(self, ind_vertex, translate):
        self.vertices[ind_vertex] += translate

    def delete_face(self, face_ind):
        del self.faces[face_ind]
        
    def energy(self):
        return E_dist + E_Rep + E_spring
        
    def edge_collapse(self):

        # Calculate energy
        E = self.energy()

        edge_ind = 

        return vertex_ind, face_ind
    