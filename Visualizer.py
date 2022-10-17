
from itertools import cycle
from matplotlib import pyplot as plt
import igraph as ig
import os

from sympy import false


for i in range(1, 21):
    nb_vertices = 0
    nb_edges = 0
    v = 0
    iedges = []
    with open(f'.\examples01-20\graph\ex{i:02}-graph.txt', "r") as f:
        for line in f:
            line = line.strip()
            if(line == ""):
                continue
            if(line[0] == "#"):
                continue
            line = line.split(" ")
            if(len(line) != 2):
                nb_vertices = int(line[0]) if nb_vertices == 0 else nb_vertices
                nb_edges = int(line[0]) if(
                    nb_vertices != 0 and v == 1) else nb_edges
                v += 1
                continue
            iedges.append((int(line[0])-1, int(line[1])-1))
    start = []
    end = []
    goal = False
    with open(f'.\examples01-20\scen\ex{i:02}-scen.txt', "r") as f:
        for line in f:
            line = line.strip()
            if(line == ""):
                continue
            if(line[0] == "#"):
                continue
            if(line == "GOAL:"):
                goal = True
                continue
            line = line.split(" ")
            if(len(line) == 2 and goal == False):
                start.append(int(line[1]))
                continue
            if(len(line) == 2 and goal == True):
                end.append(int(line[1]))
                
    ver = [*range(1, nb_vertices+1)]
    g = ig.Graph(iedges, directed=False, vertex_attrs={"class": "A"  if index_s in start else "B" for index_s in ver})
    results = []
    fig, ax = plt.subplots(figsize=(20, 20))
    if i < 13:
        ig.plot(g, target=ax, vertex_size=0.1, vertex_label=range(1, nb_vertices+1),
            vertex_color=["steelblue" if index_s in start else "red" for index_s in ver],)
    else:
        ig.plot(g, target=ax, vertex_size=0.3,
            vertex_color=["steelblue" if index_s in start else "red" for index_s in ver],)
    # print(iedges)
    fig.savefig(f'examples01-20/imgs/{i:02}.png')
    g.save(f'examples01-20/gmls/{i:02}.gml')
    # plt.show()
input("Press Enter to continue...")
