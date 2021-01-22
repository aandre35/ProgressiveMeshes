def parse_obj(file="data/bunny.obj"):
    f = open(file, "r")
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

def rewrite_obj(file, existing_lines, new_lines):
    g = open(file, "w")
    g.writelines(existing_lines)
    g.write("\n")
    g.writelines(new_lines)
    g.close()