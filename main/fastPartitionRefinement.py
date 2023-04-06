from graph import *
from coloring import *
from partition_refinement import *
from DDL import *

graph_list = []
queue = [0]
def setup():
    global graph_list
    graph_path = 'Benchmark_instances/CrefBenchmark1.grl'
    graph_list = get_graph_list(graph_path)
    combined_vertices = []
    for graph in graph_list:
        initialize(graph)
        for v in graph.vertices:
            combined_vertices.append(v)
    max_degree = len(combined_vertices)//len(graph_list)
    return combined_vertices, max_degree

def initialize(graph):
    for vertice in graph.vertices:
        vertice.set_color(0)

disjoint_graph, max_degree = setup()
new_colr = 0

def partition():
    partition = {}
    for vertex in disjoint_graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = [vertex]
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

def partition_graph(graph):
    partition = {}
    for vertex in graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = [vertex]
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

def new_color():
    return new_colr+1
def find_Nx(Ci, i):
    Nx = []
    for vertex in list(Ci.values()):
        for v in vertex:
            if len(v.neighbours) == i:
                Nx.append(v)
    return Nx


def refine(C, x): # x - degree, aka delta function; C - partition by colors
    global new_colr

    L = set()  # store unique colors
    A = {}  # states with color i in Ci
    queue = [0]


    # Split color classes

    while queue:
        print('degree: ', x)

        Nx = find_Nx(C, x)


        if len(Nx) == 0:
            return C, False

        print('NX', Nx)
        print('queue', queue)


        # Compute L and A
        # Works correctly!
        for key, value in C.items():
            A[key] = 0
            for q1 in Nx:
                if q1 in C[key]:
                    L.add(key)
                    A[key] += 1


        print('l',L)
        print('A', A)
        print('C', C)
        # split color class into 2 new classes
        for i in L:
            print('len:', len(C[i]))
            print('color', i)
            if A[i] < len(C[i]):
                new_colr = new_color()
                C[new_colr] = []
                print('new', new_colr)
                for q in C[i]:
                    if q in Nx:
                        C[i].remove(q)
                        C[new_colr].append(q)
                print(len(C[i]), len(C[new_colr]))
                if len(C[new_colr]) == 0:
                    del C[new_colr]
                    continue

                if i in queue:
                    queue.append(new_colr)
                else:
                    queue.append(min(i, new_colr))
        t = queue.pop(0)  # next color to refine
        print('t', t)
        print('qq', queue)


        # Update colors of states
        for key, value in C.items():
            for v in value:
                v.set_color(key)
    C = partition()
    print(C)

    return C, True

# loops through all degree 0<i<=maxdegree
def refines(C):
    for i in range(1, max_degree+1):
        new_partition, check = refine(C, i)
        # check whether the partition is stable such that degree existed in Nx
        # if C == new_partition and check == True:
        #     print(C)
        #     return C
        # else:
        C = new_partition
    print(C)
    return C

#ToDo: split the graph and define isomorphisms
# def split(partition):
#     for i in range(len(graph_list)):
#         name = "graph_"+str(i)
#         globals()[name] = {}
#         for key, value in partition.items():
#             for val in value:
#                 if val in graph_list[i].vertices():
#                     globals()[name][key] = [val]
#         print(graph_1)

def split():
    for i in range(len(graph_list)):
        print(f'[{i}', end='')
        for j in range(i + 1, len(graph_list)):
            if partition_graph(graph_list[i]) == partition_graph(graph_list[j]):
                print(j, end=' ')
        print(']')


C = partition()
refines(C)
split()