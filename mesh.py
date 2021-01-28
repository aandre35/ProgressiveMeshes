from utils.obj import rewrite_obj
import numpy as np
import time

class Mesh(object):


    def __init__(self, vertices, faces, edges=[], priority_queue=[], length_edges=[]):
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
        
        if np.any(edges):
            self.edges = edges
        else:
            self.edges = self.get_edges()
        
        if np.any(length_edges):
            self.length_edges = length_edges
        else:
            self.length_edges = self.get_length_edges()

        if np.any(priority_queue):
            self.priority_queue = priority_queue
        else:
            self.priority_queue = self.get_priority_queue()


    def get_edges(self):
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
        edges = np.array(edges)
        print("Nombre d'edges : {}".format(edges.shape[0]))
        return edges


    def get_length_edges(self):
        print("\nDébut du calcul de la longueur des edges")
        t1 = time.time()
        length = []
        for i in range(len(self.edges)):
            pt1 = np.array(self.vertices[self.edges[i][0]])
            pt2 = np.array(self.vertices[self.edges[i][1]])
            length.append(np.linalg.norm(pt2-pt1))
        print("fin du calcul de la longueur des edges en {:.2f} secondes".format(time.time() - t1))
        return length
        

    def get_max_length_edges(self):
        return np.max(self.length_edges)


    def get_priority_queue(self):
        print("\nDébut du calcul de la priority queue")
        t1 = time.time()
        energies = []
        for i in range(len(self.edges)):
            e_i = self.energy(i)
            energies = np.append(energies, e_i)
        priority_queue = sorted(range(len(energies)), key= lambda k: energies[k])
        print("fin du calcul de la priority queue en {:.2f} secondes".format(time.time() - t1))
        return priority_queue


    def get_nb_edges(self):
        return len(self.edges)


    def get_nb_faces(self):
        return len(self.faces)
  
    
    def get_nb_vertices(self):
        return len(self.vertices)
 
        
    #def energy(self):
    #    return E_dist + E_spring + E_scalar + E_disc
    def energy(self, i):
        return self.corner_energy(i) + self.length_energy(i)

        
    def corner_energy(self, i):
        found_faces = self.find_faces(i)
        if len(found_faces) == 2:
            face1 = self.faces[found_faces[0]]
            face2 = self.faces[found_faces[1]]
            pts1 = np.array([self.vertices[face1[0]], self.vertices[face1[1]], self.vertices[face1[2]]])
            pts2 = np.array([self.vertices[face2[0]], self.vertices[face2[1]], self.vertices[face2[2]]])
            normal1 = np.cross(pts1[1] - pts1[0], pts1[2] - pts1[0])
            normal2 = np.cross(pts2[1] - pts2[0], pts2[2] - pts2[0])
            normal1 /= np.linalg.norm(normal1)
            normal2 /= np.linalg.norm(normal2)

            prod_scal = np.vdot(normal1, normal2)
            
            return 1 - prod_scal
        else:
            return 10000

         
    def length_energy(self, i):
        return self.length_edges[i] / self.get_max_length_edges()


    def find_faces(self, i):
        found_faces = []
        e = self.edges[i]
        for k in range(len(self.faces)):
            if e[0] in self.faces[k,:] and e[1] in self.faces[k,:]:
                found_faces.append(k)
        return found_faces

    def find_faces_v(self, i):
        found_faces = []
        for k in range(len(self.faces)):
            if i in self.faces[k,:]:
                found_faces.append(k)
        return found_faces
    
    def edge_collapse(self):

        new_lines = []

        # Trouver l'edge qui minimise l'energie
        edge_ind = self.priority_queue[0]
        vertex_ind = self.edges[edge_ind]

        faces_ind = self.find_faces(edge_ind)
        
        # Delete the edge
        self.edges = np.delete(self.edges, edge_ind, 0)

        #Delete the faces
        self.faces = np.delete(self.faces, faces_ind, 0)
        new_lines = np.append(new_lines, "\ndf {}".format(faces_ind[0]+1))
        new_lines = np.append(new_lines, "\ndf {}".format(faces_ind[1]+1))
        
        #Compute the new vertex 
        # (Vs, Vt) -> Vs
        vs = self.vertices[vertex_ind[0]]
        vt = self.vertices[vertex_ind[1]]

        alpha = 0.5
        new_vs = (1 - alpha) * vs + alpha * vt
        self.vertices[vertex_ind[0]] = new_vs
        new_lines = np.append(new_lines, "\nev {} {} {} {}".format(vertex_ind[0]+1, new_vs[0], new_vs[1], new_vs[2]))
        #self.vertices = np.delete(self.vertices, vertex_ind[1])
        
        # Update faces
        faces_lines = self.update_faces(vertex_ind[1], vertex_ind[0])
        new_lines = np.append(new_lines, faces_lines)
        
        # Update Edges
        self.edges = self.get_edges()
        
        #Update Priority Queue
        #self.update_priority(edge_ind, vertex_ind[0])
        self.length_edges = self.get_length_edges()
        self.priority_queue = self.get_priority_queue()
        #Update Length
        #self.update_length_edges()
        
        print(new_lines)

        return new_lines

    
    def find_edges(self, vs_ind):
        found_edges = []
        for k in range(len(self.edges)):
            if vs_ind in self.edges[k]:
                found_edges.append(k)
        return found_edges

    
    def update_priority(self, edge_ind, vs_ind):
        self.priority_queue = self.priority_queue[1:-1]
        for i in range(len(self.priority_queue)):
            if self.priority_queue[i] > edge_ind:
                self.priority_queue[i] -= 1
    
        new_edges = self.find_edges(vs_ind)
        print(new_edges)

    def update_length_edges(self):
        return


    def update_faces(self, vt_ind, vs_ind):
        faces_lines = []
        faces_ind_v = self.find_faces_v(vt_ind)
        for i in faces_ind_v:
            for k in range(3):
                if self.faces[i][k] == vt_ind:
                    self.faces[i][k] = vs_ind
                    faces_lines = np.append(faces_lines, "\nefv {} {} {}".format(i+1, k+1, vs_ind+1))
        return faces_lines

    def copy(self):
        return Mesh(self.vertices, self.faces, self.edges, self.priority_queue, self.length_edges)