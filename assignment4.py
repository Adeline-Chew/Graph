import math


class Graph:
    def __init__(self, v_count):
        self.vertices = [None] * v_count
        for i in range(v_count):
            self.vertices[i] = Vertex(i)

    def add_edges(self, edges_count, directed=True):
        for e in edges_count:
            u, v, r = self.vertices[e[0]], self.vertices[e[1]], e[2]
            cur_edge = Edge(u, v, r)
            u.add_edge(cur_edge)
        if not directed:
            for e in edges_count:
                v, u, r = self.vertices[e[0]], self.vertices[e[1]], e[2]
                cur_edge = Edge(u, v, r)
                u.add_edge(cur_edge)

    def get_vertex(self, id: int):
        return self.vertices[id]


class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.discovered = False
        self.visited = False
        self.position = None
        self.prev = None

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:
    def __init__(self, u: Vertex, v: Vertex, w):
        self.u, self.v, self.w = u, v, w


class MinHeap:

    def __init__(self, max_count):
        self.count = 0
        self.the_array = [[] for _ in range(max_count + 1)]

    def __len__(self):
        return self.count

    def rise(self, k, elem) -> int:
        while k > 1 and elem[1] < self.the_array[k // 2][1]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        return k

    def push(self, elem):
        self.count += 1
        k = self.rise(self.count, elem)
        elem[0].position = k
        self.the_array[k] = elem

    def sink(self, pos):
        left, right = 2 * pos + 1, 2 * pos + 2
        if left < self.count:
            small_child = left
            if right < self.count and self.the_array[right][1] < self.the_array[left][1]:
                small_child = right
            if self.the_array[small_child][1] < self.the_array[pos][1]:
                self.the_array[small_child], self.the_array[pos] = self.the_array[pos], self.the_array[
                    small_child]  # swap
                self.the_array[small_child][0].position = small_child
                self.the_array[pos][0].position = pos
                self.sink(small_child)

    def serve(self):  # O(log n)
        elem = self.the_array[1]
        self.the_array[1] = []
        self.the_array[1] = self.the_array[self.count]
        self.count -= 1
        self.sink(1)
        return elem

    def update(self, key, value):  # O(1)
        self.the_array[key.position][1] = value


# --------------------------------Task 1--------------------------------#

def best_trades(prices, starting_liquid, max_trades, townspeople):
    v_count = len(prices)
    route = Graph(v_count)
    edges = []
    for trade in townspeople:
        for i in range(len(trade)):
            edges.append(trade[i])
    route.add_edges(edges, True)
    trading = [(0, 0) for _ in range(v_count)]  # (litre, value)
    trading[starting_liquid] = (1, prices[starting_liquid])
    trading_2 = [(0, 0) for _ in range(v_count)]

    current_max = prices[starting_liquid]
    for trade in range(max_trades):  # O(M)
        for e in edges:  # O(T)
            litre = trading[e[0]][0] * e[2]
            trading_val = litre * prices[e[1]]
            if trading_val > trading[e[1]][1]:
                trading_2[e[1]] = litre, trading_val
            if trading_val > current_max:
                current_max = trading_val
        trading = trading_2
        trading_2 = [(0, 0) for _ in range(v_count)]
    return current_max


def opt_delivery(n, roads, start, end, delivery):
    res = [end]
    route = Graph(n * 2)
    route.add_edges(roads, False)
    # preprocess another graph
    roads2 = []
    cost = 0
    for u, v, p in roads:
        roads2.append((u + n, v + n, p))
        if u == delivery[0] and v == delivery[1]:
            cost = p
    roads2 += [(delivery[0], delivery[1] + n, -delivery[2] + cost)]
    route.add_edges(roads2, False)

    cost, vertex = dijkstra(route.get_vertex(start), route.get_vertex(end), n)
    while vertex.prev is not None:
        ver_id = vertex.prev.id if vertex.prev.id < n else vertex.prev.id - n
        res.append(ver_id)
        vertex = vertex.prev
    res.reverse()
    return cost, res


def dijkstra(start, end, n):
    vertex = end
    cost = math.inf
    discovered_queue = MinHeap(n * 2)
    discovered_queue.push([start, 0, None])  # (vertex, cost)

    while len(discovered_queue) > 0:
        item = discovered_queue.serve()
        u, curr_cost = item[0], item[1]
        u.visited = True
        if (u.id == end.id or u.id == end.id + n) and curr_cost < cost:
            cost, vertex = curr_cost, u
        for e in u.edges:
            if e.v.visited is True:
                pass
            elif e.v.discovered is False:
                discovered_queue.push([e.v, curr_cost + e.w, u])
                e.v.prev = u
            elif e.v.distance > u.distance + e.w:
                discovered_queue.update(e.v, curr_cost + e.w)
                e.v.prev = u
                e.v.discovered = True
    return cost, vertex


if __name__ == "__main__":
    prices = [10, 5, 1, 0.1]
    starting_liquid = 0
    max_trades = 6
    townspeople = [[(0, 1, 4), (2, 3, 30)], [(1, 2, 2.5), (2, 0, 0.2)]]
    print(best_trades(prices, starting_liquid, max_trades, townspeople))
    max_trades = 2
    print(best_trades(prices, starting_liquid, max_trades, townspeople))
    max_trades = 7
    print(best_trades(prices, starting_liquid, max_trades, townspeople))
    max_trades = 9
    print(best_trades(prices, starting_liquid, max_trades, townspeople))
    prices = [20]
    starting_liquid = 0
    max_trades = 10
    townspeople = [[(0, 0, 1), (0, 0, 0.5)], [(0, 0, 1)]]
    result = best_trades(prices, starting_liquid, max_trades, townspeople)
    expected = 20
    print(result == expected)

    # Test with trading all the time
    townspeople = [[(0, 0, 2), (0, 0, 0.5)], [(0, 0, 1)]]
    result = best_trades(prices, starting_liquid, max_trades, townspeople)
    expected = 20 * 2 ** 10
    print(result == expected)

    prices = [10, 10, 10, 10, 10]
    starting_liquid = 1
    max_trades = 10
    townspeople = [[(1, 4, 3), (1, 2, 10), (4, 0, 10), (2, 3, 2)]]
    result = best_trades(prices, starting_liquid, max_trades, townspeople)
    expected = 300
    print(result == expected)

    prices = [1, 3, 2, 5, 4]
    starting_liquid = 2
    max_trades = 3
    townspeople = [[(1, 4, 3), (1, 2, 10), (4, 0, 10), (2, 3, 2)]]
    result = best_trades(prices, starting_liquid, max_trades, townspeople)
    expected = 10
    print(result == expected)

    n = 4
    roads = [(0, 1, 3), (0, 2, 5), (2, 3, 7), (1, 3, 20)]
    start = 0
    end = 1
    delivery = (2, 3, 100)
    print(opt_delivery(n, roads, start, end, delivery))
