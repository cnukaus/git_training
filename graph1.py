class graph:
    
    #https://www.educative.io/edpresso/how-to-implement-a-graph-in-python


    def __init__(self):
        self.graph=[]
        self.vertices_no=0
        self.vertices=[]

    def add_vertex(self,v,verbose=False):
        '''
        final result is 2d array of 0s
        '''
        if v in self.vertices:
            if verbose:
                print("Vertex ", v, " already exists")
        else:
            self.vertices_no = self.vertices_no + 1
            self.vertices.append(v)
            if self.vertices_no > 1:
                for vertex in self.graph:
                    vertex.append(0)
            # above to extend, below to insert 1 new vertex        
            temp = []
            for i in range(self.vertices_no):
                temp.append(0)
            self.graph.append(temp)


    # modify edge value, between vertex v1 and v2, add e
    def add_edge(self,v1, v2, e,verbose=False):
        # Check if vertex v1 is a valid vertex
        if v1 not in self.vertices:
            if verbose:
                print("Vertex ", v1, " does not exist.")
        # Check if vertex v1 is a valid vertex
        elif v2 not in self.vertices:
            if verbose:
                print("Vertex ", v2, " does not exist.")
        # Since this code is not restricted to a directed or 
        # an undirected graph, an edge between v1 v2 does not
        # imply that an edge exists between v2 and v1
        else:
            index1 = self.vertices.index(v1)
            index2 = self.vertices.index(v2)
            self.graph[index1][index2] += e

    # Print the graph
    def print_graph(self,min_weight=1):
        for i in range(self.vertices_no):
            for j in range(self.vertices_no):
                if self.graph[i][j] >= min_weight:
                    print(self.vertices[i], " -> ", self.vertices[j], \
                    " edge weight: ", self.graph[i][j])