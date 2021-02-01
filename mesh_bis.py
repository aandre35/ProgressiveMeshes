from utils.obj import rewrite_obj
import numpy as np
import time

class Mesh_Bis(object):


    def __init__(self, vertices, faces):
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
        self.vs_list = []
        self.vt_list = []
        self.new_vs_list = []
        self.faces_list = []
        self.faces_vt_list = []


    def get_nb_vertices(self):
        return len(self.vertices)
    
    def get_nb_faces(self):
        return len(self.faces)


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
        return edges


    def get_length_edges(self):
        #print("\nDébut du calcul de la longueur des edges")
        #t1 = time.time()
        length = []
        for i in range(len(self.edges)):
            pt1 = np.array(self.vertices[self.edges[i][0]])
            pt2 = np.array(self.vertices[self.edges[i][1]])
            length.append(np.linalg.norm(pt2-pt1))
        #print("fin du calcul de la longueur des edges en {:.2f} secondes".format(time.time() - t1))
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


    def energy(self, i):
        return self.corner_energy(i) + self.length_energy(i)

        
    def corner_energy(self, i):
        found_faces = self.e2f(i)
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


    def e2f(self, i):
        """e2f : return indices of faces containing an edge"""
        found_faces = []
        e = self.edges[i]
        for k in range(len(self.faces)):
            if e[0] in self.faces[k,:] and e[1] in self.faces[k,:]:
                found_faces.append(k)
        return found_faces

    def v2f(self, i):
        """v2f : return indices of faces containing a vertex"""
        found_faces = []
        for k in range(len(self.faces)):
            if i in self.faces[k,:]:
                found_faces.append(k)
        return found_faces

    def v2e(self, i):
        """v2e : return indices of edges containing a vertex"""
        found_edges = []
        for k in range(len(self.edges)):
            if i in self.edges[k]:
                found_edges.append(k)
        return found_edges
    
    def edge_collapse(self):

        # Calculer les edges, les longueurs des edges et la priority queue
        self.edges = self.get_edges()
        self.length_edges = self.get_length_edges()
        self.priority = self.get_priority_queue()

        # Affichage console
        print("Nombre de vertices : {}".format(self.get_nb_vertices()))
        print("Nombre de faces : {}".format(self.get_nb_faces()))
        print("Nombre d'edges : {}".format(len(self.edges)))

        # Récupérer le premier edge de la priority queue
        edge_ind = self.priority[0]
        #print(self.priority[0:10])

        # Récupérer les indices des vertices de l'edge
        vertices_ind = self.edges[edge_ind]
        vs_ind = vertices_ind[0]
        vt_ind = vertices_ind[1]

        # Créer le nouveau point vs
        vs = np.copy(self.vertices[vs_ind])
        vt = self.vertices[vt_ind]
        alpha = 0.5
        new_vs = alpha * vs + (1 - alpha) * vt

        # Mettre à jour les vertices et les faces
        faces_ind_to_del = self.e2f(edge_ind)
        faces_del = []
        for i in faces_ind_to_del:
            faces_del.append([self.vertices[self.faces[i][0]], self.vertices[self.faces[i][1]], self.vertices[self.faces[i][2]]])

        faces_vt_ind = self.v2f(vt_ind)
        faces_vt = []
        for i in faces_vt_ind:
            if i not in faces_ind_to_del:
                faces_vt.append([self.vertices[self.faces[i][0]], self.vertices[self.faces[i][1]], self.vertices[self.faces[i][2]]])
        

        self.update_vertices(vs_ind, vt_ind, new_vs)
        self.update_faces(faces_ind_to_del, vs_ind, vt_ind)

        # Affichage
        #print("vs : ", vs)
        #print("vt : ", vt)
        #print("new_vs : ", new_vs)
        #print("faces_del : ", faces_del)
        #print("faces_vt : ", faces_vt)

        # Stocker les informations
        self.vs_list.append(vs)
        self.vt_list.append(vt)
        self.new_vs_list.append(new_vs)
        self.faces_list.append(faces_del)
        self.faces_vt_list.append(faces_vt)


    def update_vertices(self, ind_to_keep, ind_to_del, new_vertice):
        self.vertices[ind_to_keep] = new_vertice
        self.vertices = np.delete(self.vertices, ind_to_del, 0)


    def update_faces(self, faces_ind_to_del, vs_ind, vt_ind):
        self.faces = np.delete(self.faces, faces_ind_to_del, 0)
        for i in range(len(self.faces)):
            for j in range(3):
                if self.faces[i][j] == vt_ind:
                    self.faces[i][j] = vs_ind
                elif self.faces[i][j] > vt_ind:
                    self.faces[i][j] -= 1

    
    def vsplit(self):

        # Affichage console
        print("Nombre de vertices : {}".format(self.get_nb_vertices()))
        print("Nombre de faces : {}".format(self.get_nb_faces()))
        print("Nombre d'edges : {}".format(len(self.get_edges())))

        # Initialisation et récupération des données
        lines = []
        faces_del = self.faces_list[-1]
        faces_vt = self.faces_vt_list[-1]
        vs = self.vs_list[-1]
        vt = self.vt_list[-1]
        new_vs = self.new_vs_list[-1]

        # Affichage
        print("faces_to_del : ", faces_del)
        print("faces_vt : ", faces_vt)
        print("vs : ", vs)
        print("vt : ", vt)
        print("new_vs : ", new_vs)

        self.faces_list = np.delete(self.faces_list, -1, 0)
        self.faces_vt_list = np.delete(self.faces_vt_list, -1, 0)
        self.vs_list = np.delete(self.vs_list, -1, 0)
        self.vt_list = np.delete(self.vt_list, -1, 0)
        self.new_vs_list = np.delete(self.new_vs_list, -1, 0)

        # Ajouter le vertex vt
        vt_ind = len(self.vertices)
        self.vertices = np.append(self.vertices, [vt], axis=0) 
        print("vt_ind : ", vt_ind)
        lines = np.append(lines, "\nv {} {} {}".format(vt[0], vt[1], vt[2]))

        # Ajouter les faces contenant l'edge (vs, vt)
        for i in range(len(faces_del)):
            face = faces_del[i]
            v_ind = []
            for j in range(3):
                v = face[j]
                #print("v2ind(v) : ", self.v2ind(v))
                #print("vertex : ", self.vertices[self.v2ind(v)])
                v_ind.append(self.v2ind(v))
            self.faces = np.append(self.faces, [v_ind], axis=0)
            lines = np.append(lines, "\nf {} {} {}".format(v_ind[0] + 1, v_ind[1] + 1, v_ind[2] + 1))

        # Déplacer le vertex vs
        vs_ind = self.v2ind(new_vs)
        print("vs_ind : ", vs_ind)
        #print("vs_before : ", self.vertices[vs_ind])
        self.vertices[vs_ind][:] = vs
        #print("vs_after : ", self.vertices[vs_ind])
        lines = np.append(lines, "\nev {} {} {} {}".format(vs_ind + 1, vs[0], vs[1], vs[2]))

        # Editer les faces contenant initialement vt
        for i in range(len(faces_vt)):
            face = faces_vt[i]
            face_v_ind = []
            v_ind = 0
            for j in range(3):
                v = face[j]
                #print("v : ", v)
                #print("vt : ", vt)
                if abs(v[0] - vt[0]) < 1e-5 and abs(v[1] - vt[1]) < 1e-5 and abs(v[2] - vt[2]) < 1e-5:
                    #print("1")
                    face_v_ind.append(vs_ind)
                    v_ind = j
                else:
                    #print("2")
                    face_v_ind.append(self.v2ind(v))
                #print("face_v_ind : ", face_v_ind)
            #print("face_v_ind : ", face_v_ind)
            
            face_ind = self.f2ind(face_v_ind)
            #print("face_ind : ", face_ind)
            #print("v_ind : ", v_ind)
            self.faces[face_ind][v_ind] = vt_ind
            lines = np.append(lines, "\nefv {} {} {}".format(face_ind + 1, v_ind + 1, vt_ind + 1))

        return lines


    def v2ind(self, v):
        for i in range(len(self.vertices)):
            vert = self.vertices[i]
            if abs(vert[0] - v[0]) < 1e-5 and abs(vert[1] - v[1]) < 1e-5 and abs(vert[2] - v[2]) < 1e-5:
                return i

    def f2ind(self, f):
        for i in range(len(self.faces)):
            face = self.faces[i]
            #print(face, f)
            if (face[0] == f[0] and face[1] == f[1] and face[2] == f[2]):
                return i


    def write_obj(self):
        lines = []
        for i in range(len(self.vertices)):
            lines = np.append(lines, "v {} {} {}\n".format(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2]))
        for i in range(len(self.faces)):
            lines = np.append(lines, "f {} {} {}\n".format(self.faces[i][0]+1, self.faces[i][1]+1, self.faces[i][2]+1))
        return lines