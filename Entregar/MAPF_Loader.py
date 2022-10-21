from datetime import datetime, timedelta
import time

initial = time.time()
from sys import argv
from minizinc import Instance, Model, Solver, Status

import igraph as ig


chuffed = Solver.lookup("chuffed")
gecode = Solver.lookup("gecode")


if(len(argv) != 3):
    print("Usage: python3 MAPF_Loader.py <graphfile> <scenfile>")
    exit(1)

graphfile = argv[1]
scenfile = argv[2]
# if(graphfile[-5:] != ".data"):
#     print("Graph file must be in data format")
#     exit(1)
# if(scenfile[-5:] != ".data"):
#     print("Scenario file must be in data format")
#     exit(1)

# Load graph
edges = []
iedges = []
nb_vertices = 0
nb_edges = 0
v = 0


with open(graphfile, "r") as f:
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
        if((line[0], line[1]) not in edges):
            edges.append((int(line[0]), int(line[1])))
            iedges.append((int(line[0])-1, int(line[1])-1))
        if((line[1], line[0]) not in edges):
            edges.append((int(line[1]), int(line[0])))

# print(iedges)
# Load scenarios
agents = {}
nb_agents = 0
half_line = 0

with open(scenfile, "r") as f:
    for line in f:
        line = line.strip()
        if(line == ""):
            continue
        if(line[0] == "#"):
            continue
        line = line.split(" ")
        if(len(line) == 1):
            nb_agents = int(line[0]) if nb_agents == 0 else nb_agents
            continue
        if(line[0] not in agents and len(line) == 2):
            agents[line[0]] = (int(line[1]), None)
            continue
        if(line[0] in agents and len(line) == 2):
            agents[line[0]] = (agents[line[0]][0], int(line[1]))


# Convert agents to minizinc format
agents_array = []
start = []
end = []
for agent in agents:
    agents_array.append([agents[agent][0], agents[agent][1]])
    start.append(agents[agent][0])
    end.append(agents[agent][1])

# print(agents_array)

formated_scen = 'input = ['
for agent in agents:
    formated_scen += '|{}, {}'.format(agents[agent][0], agents[agent][1])
formated_scen += '|];\n'


# Sort edges by first vertex
formated_edges = 'edges = '
edges.sort()
edges_array = []

for edge in edges:
    while len(edges_array) < edge[0]:
        edges_array.append({edge[0]})
   
    edges_array[edge[0]-1].add(edge[1])

formated_edges += str(edges_array)
formated_edges += ';\n'

_input = formated_edges + formated_scen + 'V = ' + \
    str(nb_vertices) + ';\n' + 'A = ' + str(nb_agents) + \
    ';\n' + 'E = ' + str(nb_edges) + ';\n'

#print(_input)


g = ig.Graph(iedges, n=nb_vertices, directed=False)
results = []
for a in agents_array:
    #print(g.get_shortest_paths(a[0], to=a[1], output="epath"))
    results.append(len(g.get_shortest_paths(a[0]-1, to=a[1]-1, output="epath")[0]))


def fgecode(gecode, engine, time_value, nb_vertices, nb_agents, nb_edges, edges_array, agents_array):
    global maxTime
    instance = Instance(gecode, engine)
    instance["V"] = nb_vertices
    instance["A"] = nb_agents
    instance["E"] = nb_edges
    instance["edges"] = edges_array
    instance["input"] = agents_array
    #print(maxTime)
    while True:
        with instance.branch() as child:
            child["maxTime"] = maxTime
            result = child.solve(timeout=time_value)
            #print(result.status)
            if result.status == Status.SATISFIED:
                #print("Solution found")
                #print(result)
                #print("MaxTime: ", child["maxTime"])
                break
            elif result.status == Status.UNKNOWN:
                break
            else:
                maxTime += 1
    return result

def fchuffed(chuffed, engine, time_value, nb_vertices, nb_agents, nb_edges, edges_array, agents_array):
    global maxTime
    instance = Instance(chuffed, engine)
    instance["V"] = nb_vertices
    instance["A"] = nb_agents
    instance["E"] = nb_edges
    instance["edges"] = edges_array
    instance["input"] = agents_array
    #print(maxTime)
    while True:
        with instance.branch() as child:
            child["maxTime"] = maxTime
            result = child.solve(timeout=time_value)
            #print(result.status)
            if result.status == Status.SATISFIED:
                #print("Solution found")
                #print(result)
                #print("MaxTime: ", child["maxTime"])
                break
            elif result.status == Status.UNKNOWN:
                break
            else:
                maxTime += 1
    return result




engine = Model("./solver5.mzn")
# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
chuffed = Solver.lookup("chuffed")


time_value = timedelta(milliseconds=(2000+nb_agents*10+nb_vertices*10+nb_edges*10+max(results)*100))
maxTime = max(results)
gecode_in_use = True
print(500+nb_agents*10+nb_vertices*10+nb_edges*10+max(results)*100)
print(time_value)
while True:
    try:
        if(gecode_in_use):
            result = fgecode(gecode, engine, time_value, nb_vertices, nb_agents, nb_edges, edges_array, agents_array)
            if(result.status == Status.SATISFIED):
                print("SATISFIED")
                print(result)
                break
            elif(result.status == Status.UNKNOWN):
                print("switching to Chuffed")
                gecode_in_use = False
        else:
            result = fchuffed(chuffed, engine, time_value, nb_vertices, nb_agents, nb_edges, edges_array, agents_array)
            if(result.status == Status.SATISFIED):
                print("SATISFIED")
                print(result)
                break
            elif(result.status == Status.UNKNOWN):
                print("switching to Gecode")
                gecode_in_use = True
    except Exception as e:
        print(e)
        break

end = time.time()
print("Total Time", end- initial)
#print("\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\n\n")
# python .\MAPF_Loader.py .\examples01-20\graph\ex01-graph.txt .\examples01-20\scen\ex01-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex02-graph.txt .\examples01-20\scen\ex02-scen.txt >> "time_only_2.txt" ; python .\MAPF_Loader.py .\examples01-20\graph\ex03-graph.txt .\examples01-20\scen\ex03-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex04-graph.txt .\examples01-20\scen\ex04-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex05-graph.txt .\examples01-20\scen\ex05-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex06-graph.txt .\examples01-20\scen\ex06-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex07-graph.txt .\examples01-20\scen\ex07-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex08-graph.txt .\examples01-20\scen\ex08-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex10-graph.txt .\examples01-20\scen\ex10-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex13-graph.txt .\examples01-20\scen\ex13-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex14-graph.txt .\examples01-20\scen\ex14-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex15-graph.txt .\examples01-20\scen\ex15-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex16-graph.txt .\examples01-20\scen\ex16-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex17-graph.txt .\examples01-20\scen\ex17-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex18-graph.txt .\examples01-20\scen\ex18-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex19-graph.txt .\examples01-20\scen\ex19-scen.txt >> "time_only_2.txt" ;python .\MAPF_Loader.py .\examples01-20\graph\ex20-graph.txt .\examples01-20\scen\ex20-scen.txt >> "time_only_2.txt" ;


