class Graph:
    def __init__(self, v_count):
        self.vertices = [None] * v_count
        for i in range(v_count):
            self.vertices[i] = Vertex(i)
            
    def add_edges(self, edges_count):
        for e in edges_count:
            u, v, r = e[0], e[1], e[2]
            cur_edge = Edge(u, v, r)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(cur_edge)
            
            
class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.discovered = False
        self.visited = False
        
    def add_edge(self, edge):
        self.edges.append(edge)
        
        
class Edge:
    def __init__(self, u, v, r):
        self.u, self.v, self.r = u, v, r
        
    # def __iter__(self):
    #   return self.u, self.v, self.r
        
        
#--------------------------------Task 1--------------------------------#

def best_trades(prices, starting_liquid, max_trades, townspeople):
    v_count = len(prices)
    route = Graph(v_count)
    edges = []
    for trade in townspeople:
        for i in range(len(trade)):
            edges.append(trade[i])
    route.add_edges(edges)
    trading = [(0, 0) for _ in range(v_count)] # (litre, value)
    trading[starting_liquid] = (1, prices[starting_liquid])
    trading_2 = [(0, 0) for _ in range(v_count)]

    current_max = prices[starting_liquid]
    for trade in range(max_trades):
        for e in edges:
            litre = trading[e[0]][0] * e[2]
            trading_val = litre * prices[e[1]]
            if trading_val > trading[e[1]][1]:
                trading_2[e[1]] = litre, trading_val
            if trading_val > current_max:
                current_max = trading_val
        trading = trading_2
        trading_2 = [(0, 0) for _ in range(v_count)]
    return max(max(trading, key=lambda x: x[1])[1], current_max)



if __name__ == "__main__":
    prices = [10, 5, 1, 0.1]
    starting_liquid = 0
    max_trades = 6
    townspeople = [[(0,1,4),(2,3,30)],[(1,2,2.5),(2,0,0.2)]]
    print(best_trades(prices, starting_liquid, max_trades, townspeople))
    max_trades = 2
    print(best_trades(prices, starting_liquid, max_trades, townspeople))





