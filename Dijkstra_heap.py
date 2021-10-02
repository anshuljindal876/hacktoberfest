"""
    *******************************************************************
    * Heap-based implementation of Dijkstra's Shortest Path Algorithm *
    * By: Anshul Jindal                                               *
    *******************************************************************
"""
import math as M

"""
Name: vertex
Function: skeleton for all vertex() objects. Each has an UNIQUE key and a corresponding fval
"""
class vertex(object):
    def __init__(self, key = -1, fval = M.inf):
        self.key = int(key)
        self.fval = fval

"""
Name: edge
Function: defines an edge (a connection) of some length between two vertices (end1 and end2) which are vertex() objects
"""
class edge(object):
    def __init__(self, end1 = None, end2 = None, length = 0):
        self.end1 = end1
        self.end2 = end2
        self.len = length

    """
    INPUT: end, vertex() object
    OUTPUT: vertex() object
    Function: check if 'end' is a vertex of the edge. If yes, returns the other vertex.
    """
    def getOtherEnd(self, end):
        if self.end1.key == end.key:
            return self.end2
        if self.end2.key == end.key:
            return self.end1
        return None

    
    """
    INPUT: end, vertex() object
    OUTPUT: True/False
    Function: check if 'end' is a vertex of the edge.
    """
    def isEnd(self, end):
        if self.end1.key == end.key:
            return True
        if self.end2.key == end.key:
            return True
        return False

"""
Name: graph
Function: Min-heap to store fvals of vertices of graph
"""
class graph(object):
    def __init__(self): ##Initialize heap and size
        self.size = 0
        self.heap = []

    """
    INPUT: val, vertex() object
    OUTPUT: None
    Function: Inserts new vertex() object into heap based on its fval
    """
    def insert(self, val):
        if(self.size == 0):
            self.heap = [val]
            self.size += 1

        else:
            ## Insert object at the end leaf
            self.heap += [val]                                      
            val_index = self.size
            self.size += 1

            ## Bubble up inserted object as necessary
            while(True):
                ## Parent of a child(i) is at (i/2) or floor(i/2) depending on whether i is even or odd
                if(val_index%2 == 0):
                    parent_index = int(val_index/2) - 1
                else:
                    parent_index = M.floor(val_index/2)

                ## Check heap property
                if(self.heap[parent_index].fval < self.heap[val_index].fval or parent_index < 0):
                    return

                ## If heap property check failed, i.e., child > parent. So we swap parent with child
                self.heap[parent_index], self.heap[val_index] = self.heap[val_index], self.heap[parent_index]
                val_index = parent_index

    """
    INPUT: None
    OUTPUT: val, vertex() object
    Function: Extract min. object from the root (based on its fval) and update the heap to maintain the heap property invariant
    """
    def extractMin(self):
        if(self.size == 0):
            return None

        self.size -= 1
        val = self.heap[0]                                          ## Root value to be returned
        
        ## Steps to maintain heap property
        self.heap[0] = self.heap[self.size]                         ## Push the last leaf to top of tree, i.e., at the root
        self.heap.pop(self.size)                                    ## Delete the copy of this last leaf
        root_index = 0
        while(True):
            try: ## To check if there is a left child
                child_left_index = int(2*root_index) + 1            ## Left child of parent(i) is at 2*i
                child_left = self.heap[child_left_index].fval
                
                try: ## To check if there is a right child
                    child_right_index = int(2*root_index) + 2       ## Right child of parent(i) is at 2*i + 1
                    child_right = self.heap[child_right_index].fval

                    if(self.heap[root_index].fval <= min(child_right, child_left)): ## Heap property check
                        return val ## Check successful, heap property is maintained throughout the heap!

                    ## If heap property check fails, swap parent with min. valued child
                    if(child_left <= child_right):
                        self.heap[root_index], self.heap[child_left_index] = self.heap[child_left_index], self.heap[root_index]
                        root_index = child_left_index
                    else:
                        self.heap[root_index], self.heap[child_right_index] = self.heap[child_right_index], self.heap[root_index]
                        root_index = child_right_index
                except: ## There is only a left child
                    if(self.heap[root_index].fval <= child_left): ## Heap property check
                        return val ## Check successful, heap property is maintained throughout the heap!

                    ## If heap property check failed, i.e., child > parent. So we swap parent with left child
                    self.heap[root_index], self.heap[child_left_index] = self.heap[child_left_index], self.heap[root_index]
            except: ## No child, exit!
                return val

    # To heapify a subtree rooted with node i  
    # which is an index in arr[]. N is size of heap
    """
    INPUT: arr(list), n(int), i(int)
    OUTPUT: None
    Function: Recursively heapifies a subtree rooted at ith index in array of size n
    """
    def heapify(self, arr, n, i):       
        smallest = i # Initialize smallest as root 
        l = 2 * i + 1 # left = 2*i + 1 
        r = 2 * i + 2 # right = 2*i + 2 

        # If left child is larger than root 
        if (l > n and arr[l] < arr[smallest]): 
            smallest = l

        # If right child is larger than smallest so far 
        if (r > n and arr[r] < arr[smallest]): 
            smallest = r

        # If smallest is not root 
        if (smallest != i):
            swap = arr[i]
            arr[i] = arr[smallest]
            arr[smallest] = swap

            # Recursively heapify the affected sub-tree 
            self.heapify(arr, n, smallest)
            
    """
    INPUT: arr(list), n(int)
    OUTPUT: None
    Function: Function to build a Min-Heap from the given array arr of size n.
    Note: This does not update the current heap. It always creates a new heap from the array so prev. heap data may be lost.
          For batch insert, use insert function in a for loop.
    """
    def buildHeap(self, arr, n): 
        # Index of last non-leaf node 
        startIdx = int((n / 2)) - 1

        # Perform reverse level order traversal 
        # from last non-leaf node and heapify 
        # each node 
        for i in range(startIdx, -1, -1): 
            self.heapify(arr, n, i)

        self.heap = arr
        self.size = len(arr)

    """
    INPUT: key, val (both int)
    OUTPUT: None
    Function: Updates the fval of a vertex in self.heap having self.key = key
              The corresponding node is removed from heap, updated and then inserted into the new heap created from the remaining vertices
    """
    def setFval(self, key, val):
        if self.size == 0:
            return

        for node in self.heap:
            if(node.key == key):
                self.heap.pop(self.heap.index(node))
                self.size -= 1
                self.buildHeap(self.heap, self.size)
                self.insert(vertex(key, val))

    """
    INPUT: key(int)
    OUTPUT: fval(int)
    Function: Returns the fval of a vertex having the given key.
              As all keys are unique, the fval is correctly found.
    """
    def getFval(self, key):
        if self.size == 0:
            return None

        for node in self.heap:            
            if(node.key == key):
                return node.fval

    """
    INPUT: v(vertex() object), E(int), exp(from global)
    OUTPUT: None
    Function: Whenever a new node is explored, the fvals of the unexplored vertices connected to it are updated via dijkstra greedy score.
              For all the edges, if there is an edge having ends (v,w) such that 'v' is explored and 'w' is not explored, the fval of w = min(current fval, fval(v) + len(edge))
    """
    def updateConnectedNodes(self, v, E):
        for e in E:
            if e.isEnd(v):
                w = e.getOtherEnd(v)
                if w.key not in exp:
                    l = e.len
                    wfval = self.getFval(w.key)
                    self.setFval(w.key, min(wfval, v.fval + l))

    """
    INPUT: None
    OUTPUT: None
    Function: Prints heap data
    """
    def disp(self):
        for node in self.heap:
            print(node.key, node.fval)

"""
INPUT: H, V, E, source
OUTPUT: nodes, a list of vertex() objects
Function: Core function for implementing Dijkstra's Shortest Path Algorithm
          on a graph(V, E) where V has all the vertices and E has all the edges.
          H is a min-heap, having the fvals of the vertices as its keys.
          Heap implementation allows for saving time.
"""       
def dijkstra(H, V, E, source):
    global exp
    exp, nodes = [], []
    H.setFval(source, 0)
    arr = [(i+1) for i in range(H.size)]
    while(set(exp) != set(arr)):
        node = H.extractMin()
        exp.append(node.key)
        nodes.append(node)
        H.updateConnectedNodes(node, E)
    return nodes

"""
INPUT: path(string)
OUTPUT: H, V, E
Function: Function for reading input file containing test cases.
          Generates appropriate heap H and lists V and E that map the entire graph.
File format: 1. A graph having N vertices is numbered from 1-N.
             2. The graph must be undirected.
             3. There are N no. of lines where first character of the i'th line is 'i' and following are details of its connectivity
             4. Sample line:
                 3 4,50 8,78 10,61 19,48
             5. In the above sample, (3,4), (3,8), (3,10) and (3,19) are all the edges from vertex with label 3
                 (50, 78, 61, 48) are their respective edge lengths/weights.
"""  
def readGraph(path):
    file = open(path)                                           ## Open the file from input path
    data = file.readlines()
    H = graph()
    V, E, arr = [], [], []
    for line in data:                                           ## number of lines = number of nodes
        items = line.split()                                    ## Separate the string to individual characters
        u = int(items.pop(0))
        arr.append(u)
        end1 = vertex(u)
        V.append(end1)
        for item in items:
            item = item.split(',')
            l, v = int(item.pop()), int(item.pop())
            if v not in arr:
                end2 = vertex(v)
                e = edge(end1, end2, l)
                E.append(e)
    H.buildHeap(V, len(V))
    return H, V, E

if __name__ == '__main__':
    path = "dijkstraTest2.txt"
    H, V, E = readGraph(path)
    source = 1                                                  ## Source Vertex (to be changed according to necessity)
    arr = dijkstra(H, V, E, source)
    
    for i in arr:
        print(i.key, i.fval)
