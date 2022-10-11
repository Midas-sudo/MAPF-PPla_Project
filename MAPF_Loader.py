import sys
from minizinc import Instance, Model, Solver, Status

import igraph as ig


if(len(sys.argv) != 3):
    print("Usage: python3 MAPF_Loader.py <graphfile> <scenfile>")
    exit(1)

graphfile = sys.argv[1]
scenfile = sys.argv[2]
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
            iedges.append((int(line[0]), int(line[1])))
        if((line[1], line[0]) not in edges):
            edges.append((int(line[1]), int(line[0])))

#print(iedges)
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
start =[]
end=[]
for agent in agents:
    agents_array.append([agents[agent][0], agents[agent][1]])
    start.append(agents[agent][0])
    end.append(agents[agent][1])

#print(agents_array)

formated_scen = 'input = ['
for agent in agents:
    formated_scen += '|{}, {}'.format(agents[agent][0], agents[agent][1])
formated_scen += '|];\n'

# Sort edges by first vertex
formated_edges = 'edges = '
edges.sort()
edges_array = [];

for edge in edges:
    if len(edges_array) < edge[0]:
        edges_array.append({edge[0]})
    edges_array[edge[0]-1].add(edge[1])
     
formated_edges += str(edges_array)
formated_edges += ';\n'

_input = formated_edges + formated_scen + 'V = ' + str(nb_vertices) + ';\n' + 'A = ' + str(nb_agents) + ';\n' + 'E = ' + str(nb_edges) + ';\n'

print(_input)

g = ig.Graph(nb_edges, edges=iedges, directed=False)
results = []
for a in agents_array:
    #print(g.get_shortest_paths(a[0], to=a[1], output="epath"))
    results.append(len(g.get_shortest_paths(a[0], to=a[1], output="epath")[0]))
#print("Lower Limit: ", max(results))
#print("Upper Limit: ", sum(results)) 

print("Lower Limit: ", max(results))

# Load n-Queens model from file
engine = Model("./solver2.mzn")
# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, engine)
# Assign 4 to n
instance["V"] = nb_vertices
instance["A"] = nb_agents
instance["E"] = nb_edges
instance["edges"] = edges_array
instance["input"] = agents_array
maxTime = max(results)
result = False

while True:
     with instance.branch() as child:
        maxTime += 1
        child["maxTime"] = maxTime
        result = child.solve()
        print(result.status)
        if result.status == Status.SATISFIED:
            #print("Solution found")
            print(result)
            #print("MaxTime: ", child["maxTime"])  
            break
print("MaxTime: ", maxTime)
print("Lower Limit: ", max(results))
