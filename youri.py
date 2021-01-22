import numpy as np
levels = 16
profondeur_max = 1

class Arbre:
    def __init__(self, profondeur=0, taille=2.0, centre=[0,0,0]):
        self.branches = [None] * 8
        self.profondeur = profondeur
        self.taille = taille
        self.centre = centre
        self.faces = []
        self.empty = False

    def count(self):
        sum_f = 0
        if self.branches == [None] * 8:
            if self.empty:
                return 0
            return 1
        else:
            for f in self.branches:
                sum_f += f.count()
            return sum_f

    def subdiviser(self, vertices, faces, profondeur_max):
        nouvelle_taille = self.taille/2
        centres = [[1,1,1], [1,1,-1], [1,-1,1], [1,-1,-1], [-1,1,1], [-1,1,-1], [-1,-1,1], [-1,-1,-1]]
        centres = np.multiply(centres, nouvelle_taille/2)
        centres = np.add(centres,self.centre)
        cubes_non_vides = [0]*8
        vertices_in = []
        for counter, centre in enumerate(centres):
            for counter_vertex, vertex in enumerate(vertices):
                if (np.abs(vertex[0] - centre[0]) < nouvelle_taille/2 and np.abs(vertex[1] - centre[1]) < nouvelle_taille/2 and np.abs(vertex[2] - centre[2]) < nouvelle_taille/2):
                    vertices_in.append((counter_vertex+1, vertex))
                    cubes_non_vides[counter] = 1
                    
        #### DEF VARIABLES
        
        if np.sum(cubes_non_vides) >= 5 and self.profondeur < profondeur_max:
            for counter, centre in enumerate(centres):
                nouvelle_branche = Arbre(self.profondeur+1, nouvelle_taille, centre)
                nouvelle_branche.subdiviser(vertices, faces, profondeur_max)
                self.branches[counter] = nouvelle_branche
        else:
            new_bunny = open("assets/new_bunny.obj", "a")
            new_bunny.write("v {} {} {}\n".format(self.centre[0], self.centre[1], self.centre[2]))
            new_bunny.close()
            bunny_cassed = open("assets/bunny_cassed.obj", "a")
            bunny_correction = open("assets/bunny_correction.txt", "a")
            if np.sum(cubes_non_vides) > 0:
                bunny_correction.write("ev {} {} {} {}\n".format(str(vertices_in[0][0]), (vertices_in[0][1][0]), (vertices_in[0][1][1]), vertices_in[0][1][2]))
                if len(vertices_in) > 1:
                    for face in faces:
                        for i in range(0,3):
                            if face[i] in vertices_in[1:][0]:
                                face[i] = vertices_in[0][0]

            else:
                self.empty = True
            for vertex in vertices_in:
                None
                # bunny_correction.write("ev {} {} {} {}\n".format(str(vertex[0]), (vertex[1][0]), (vertex[1][1]), vertex[1][2]))
                # bunny_cassed.write("ev {} {} {} {}\n".format(str(vertex[0]), (self.centre[0]), (self.centre[1]), self.centre[2]))
            bunny_cassed.close()
            bunny_correction.close()
            
    def visuel(self):
        print("\t" * self.profondeur + ":---\\")
        if self.branches != [None] * 8:
            for bra in self.branches:
                bra.visuel()
                
def parse_obj(file="assets/bunny_striped.obj"):
    f = open("assets/bunny_striped.obj", "r")
    lines = f.readlines()
    cmds = [x.strip("\n") for x in lines]
    f.close()
    vertices = [x for x in cmds if x.startswith("v")]
    faces = [x for x in cmds if x.startswith("f")]
    faces = [x.split(" ")[1:4] for x in faces]
    faces = [[int(y) for y in x] for x in faces]
    vertices = [tuple(x.split(" ")[1:4]) for x in vertices]
    vertices = [[float(y) for y in x] for x in vertices]
    return vertices, faces, lines

def quantify(vertices,levels):
    quantifications = [x * 1.0/levels for x in range(-levels,levels+1)]
    print(quantifications)
    def quantifyer(x,quantifications=quantifications):
        return min(quantifications, key=lambda i:abs(i-x))
    vertices_quant = []
    new_operations = []
    for counter, current_vertex in enumerate(vertices):
        new_vertex = [0,0,0]
        new_vertex[0] = quantifyer(current_vertex[0])
        new_vertex[1] = quantifyer(current_vertex[1])
        new_vertex[2] = quantifyer(current_vertex[2])
        if new_vertex in vertices_quant:
            new_operations.append("")
        new_operations.append("ev {} {} {} {}\n".format(str(counter+1), (new_vertex[0]), (new_vertex[1]), new_vertex[2]))
        vertices_quant.append(new_vertex)
    return vertices_quant, new_operations

def rewrite_obj(file,existing_lines, new_lines):
    g = open(file, "w")
    g.writelines(existing_lines)
    g.write("\n")
    g.writelines(new_lines)
    g.close()

def create_octree(vertices, faces, profondeur_max):
    octree = Arbre()
    octree.subdiviser(vertices, faces, profondeur_max)
    return octree.count()
    # octree.visuel()



vertices, faces, lines = parse_obj()
# vertices_quant, new_operations = quantify(vertices, levels)

bunny_correction = open("assets/bunny_correction.txt", "w")
bunny_correction.write("")
bunny_correction.close()

ensemble_faces = []
enlever_faces = []
for counter_face, face in enumerate(faces):
    if face in ensemble_faces:
        enlever_faces.append('df ' + str(counter_face + 1))
        print(face)
    else:
        ensemble_faces.append(face)


rewrite_obj("assets/bunny_cassed.obj", lines, [])
feuilles = create_octree(vertices, faces, profondeur_max)
octet_feuilles_new = feuilles * (1 + 3 * 0.5)
octet_feuilles_old = len(vertices) * (1 + 3 * 0.5)
octet_faces = (len(faces) - len(enlever_faces)) * 4
s_old = octet_feuilles_old + octet_faces
s_new = octet_feuilles_new + octet_faces
bunny_correction = open("assets/bunny_correction.txt", "r")
li = bunny_correction.readlines()
bunny_cassed = open("assets/bunny_cassed.obj", "a")
bunny_cassed.writelines(li)

print(s_old)
print((1 - s_new/s_old) * 100, "%")