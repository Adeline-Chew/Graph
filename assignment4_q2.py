#%%
import math

class MinHeap:
    def __init__(self, roads_count, start, end):
        """Initialise Heap and do index mapping

        Args:
            vertex_index_array ([type]): [description]
        """
        self.heap = [None] * (roads_count + 1)

        self.end = end 

        self.start = start

        self.length = 0

        self.graph = [None] * roads_count

        for i in range(roads_count):
            if i == start:
                self.insert(i, 0)
            else: 
                self.insert(i, math.inf)

    def __len__(self):
        return self.length

    def insert(self, index_id, weight):
        self.length += 1 
        self.heap[self.length] = (index_id, weight)
        self.graph[index_id] = (weight, None, self.length)
        self.rise(self.length)

    def rise(self, current):
        # if my current value is less than the parent then rise 
        while current > 1 and self.heap[current][1] < self.heap[current // 2][1]:
            # Performing Swap
            self.swap(current, current // 2)
            current = current//2


    def serve(self):
        # deleting the last node and swap its item with the node 
        root = self.heap[1]

        # Swapping the root with the last node
        self.swap(1, self.length)

        # pop the last element off which is the root after swap
        
        # decrement the length by 1 
        self.length -= 1

        # sink the root 
        self.sink(1)

        return root
    
    def swap(self, i, j):
        # swapping the mapping index 
        current = self.heap[i][0] 
        new_current = self.heap[j][0]
        self.graph[current] = (self.graph[current][0], self.graph[current][1], j)
        self.graph[new_current] = (self.graph[new_current][0], self.graph[new_current][1], i)
        # swapping the heap 
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def sink(self, current):
        while 2*current <= self.length:
            child = self.smallest_child(current)
            if self.heap[current][1] > self.heap[child][1]:
                break
            self.swap(child,current)
            current = child

    def smallest_child(self, current):
        if 2 * current == self.length or self.heap[2*current] < self.heap[2*current + 1]:
            return 2 * current 
        else: 
            return 2 * current + 1

    def update(self, current, weight, indexFrom):
        # the position in my heap
        pos = self.graph[current][2]
        # change the value in the mapping index graph
        self.graph[current] = (weight, indexFrom, self.graph[current][2])
        # update the value in the heap
        self.heap[pos] = (current, weight)
        # perform rise 
        self.rise(self.graph[current][2])

class DijkstraGraph:
    def __init__(self, roads_count):
        self.count = roads_count
        self.vertices = [None] * roads_count

        for i in range(roads_count):
            self.vertices[i] = Vertex(i)

        # self.graph = [None] * roads_count

        # (distance, from which vertex, index_mapping for min_heap)
        # for i in range(1, roads_count + 1):
        #     self.graph[i-1] = (math.inf, None, i)
        
        # self.graph[start][2] = 1
        # self.graph[0][2] = start 

        # self.start = start 
        # self.end = end

    def addEdge(self, roads):
        u = roads[0]
        v = roads[1]
        w = roads[2]

        current_edge = Edge(u,v,w)

        current_vertex = self.vertices[u]
        current_vertex.add_edge(current_edge)

        current_edge = Edge(v,u,w)
        current_vertex = self.vertices[v]
        current_vertex.add_edge(current_edge)


    def cheapest_path(self, start, end):
        # Create MinHeap 
        minHeap = MinHeap(self.count, start, end)
        vertices_count = 0

        for vertex in self.vertices:
            vertex.served = False

        while vertices_count < len(self.vertices) and self.vertices[end].served == False:
            # Serve the root vertex 
            current_min = minHeap.serve()
            self.vertices[current_min[0]].served = True
            edges = self.vertices[current_min[0]].edges

            for edge in edges:
                u = edge.u
                v = edge.v
                w = edge.w 

                if (current_min[1] + w < minHeap.graph[v][0]) and self.vertices[v].served == False:
                    minHeap.update(v, current_min[1] + w, self.vertices[u].id)
            vertices_count += 1
        return minHeap.graph
        

            

    def __str__(self):
        return_string = ""
        for vertex in self.vertices:
            return_string = return_string + "Vertex" + str(vertex) + "\n"
        return return_string

class Vertex:
    def __init__(self, id):
        self.id = id
        self.served = False
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self):
        return_string = str(self.id)
        for edge in self.edges:
            return_string = return_string + "\n with edges " + str(edge)
        return return_string

class Edge: 
    def __init__(self, u, v, w):
        self.u = u
        self.v= v
        self.w = w

    def __str__(self):
        return_string = str(self.u) + ", " + str(self.v) + ", " + str(self.w)
        return return_string
    




def opt_delivery(n, roads, start, end, delivery):
    # print(n)
    # print(roads)
    # print(start)
    # print(end)
    # print(delivery)
    # Running First Dijkstra from start to end 
    # Creating a DijkstraGraph Object
    dijkstra = DijkstraGraph(n)

    # Creating all the edges
    for road in roads:
        dijkstra.addEdge(road)

    # First Dijkstra from start to end 
    start_end = dijkstra.cheapest_path(start, end)

    # Second Dijkstra from start to pickup
    pickup = delivery[0]
    start_pick = dijkstra.cheapest_path(start, pickup)

    # Third Dijkstra from pickup to delivery destination
    delivery_dest = delivery[1]
    profit = delivery[2]
    pick_delivery = dijkstra.cheapest_path(pickup, delivery_dest)

    # Fourth Dijkstra from delivery to destination
    delivery_end = dijkstra.cheapest_path(delivery_dest, end)

    start_end_cost = start_end[end][0]
    start_pick_cost = start_pick[pickup][0]
    print(start_pick_cost)
    pick_delivery_cost = pick_delivery[delivery_dest][0]
    print(pick_delivery_cost)
    delivery_end_cost = delivery_end[end][0]
    print(delivery_end_cost)

    delivery_made = start_pick_cost + pick_delivery_cost + delivery_end_cost - profit 

    output = []
    if delivery_made < start_end_cost:
        
        index = end 
        while index != delivery_dest:
            output.append(index)
            index = delivery_end[index][1]

        index = delivery_dest
        while index != pickup:
            output.append(index)
            index = pick_delivery[index][1]

        index = pickup
        while index != start:
            output.append(index)
            index = start_pick[index][1]
        output.append(index)

        output_value = delivery_made
        
    else: 

        index = end 
        while index != start: 
            output.append(index)
            index = start_end[index][1]
        output.append(index)

        output_value = start_end_cost

    # reverse my result 
    print(start_end)
    print("\n")
    print( start_pick)
    print("\n")
    print(pick_delivery)
    print("\n")
    print(delivery_end)
    return (output_value, output[::-1])

# %%
n = 15
roads = [[10, 7, 9], [7, 3, 10], [7, 13, 6], [7, 8, 0], [3, 2, 7], [7, 11, 0], [10, 0, 10], [13, 9, 10], [7, 4, 8], [3, 1, 7], [0, 6, 6], [6, 12, 6], [9, 14, 3], [1, 5, 5], [0, 3, 7], [1, 4, 0], [13, 6, 1], [9, 10, 1], [13, 3, 6], [2, 1, 2], [8, 12, 1], [2, 9, 3], [8, 6, 3], [13, 14, 7], [12, 9, 8], [7, 1, 9], [14, 1, 9], [10, 13, 8], [0, 7, 1], [11, 4, 9], [2, 6, 6], [10, 2, 10], [7, 6, 5], [6, 9, 6], [0, 14, 5], [8, 4, 3], [12, 5, 8], [8, 5, 3], [6, 10, 5], [0, 11, 0], [0, 12, 8], [9, 11, 1], [14, 2, 4], [5, 9, 0], [1, 13, 3], [12, 11, 10], [0, 13, 2], [11, 14, 10], [14, 12, 1], [10, 11, 10], [4, 13, 4], [8, 0, 0], [5, 11, 5], [0, 2, 5], [11, 8, 5], [5, 4, 6], [1, 11, 8], [1, 0, 6], [2, 7, 10], [2, 4, 3], [14, 3, 4], [10, 5, 2], [0, 5, 9], [6, 5, 6], [5, 7, 4], [12, 4, 1], [5, 13, 2], [1, 6, 0], [0, 9, 8], [10, 1, 5], [3, 10, 9], [6, 3, 2], [0, 4, 5], [10, 8, 2], [2, 8, 4], [9, 3, 2], [4, 10, 4], [4, 6, 10], [4, 14, 10], [9, 1, 6], [13, 11, 8], [2, 11, 4], [9, 8, 3], [8, 3, 4], [10, 12, 9], [9, 4, 3], [5, 3, 10], [6, 11, 6], [2, 5, 6], [14, 6, 3], [13, 8, 8], [5, 14, 3], [14, 10, 9], [12, 1, 10], [2, 12, 7], [1, 8, 5], [8, 14, 6], [2, 13, 3], [3, 12, 8], [12, 7, 6], [9, 7, 5], [3, 11, 7], [4, 3, 10], [12, 13, 5], [14, 7, 4]]
start = 4
end = 8
delivery = [0, 12, 3]
result = opt_delivery(n, roads, start, end, delivery)
print(result)
# %%
