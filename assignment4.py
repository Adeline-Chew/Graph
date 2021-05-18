import math
from roads import Road


class Vertex:
    def __init__(self, id: int) -> None:
        self.id = id
        self.edges = []
        self.initialise()

    def add_edge(self, edge) -> None:
        self.edges.append(edge)

    def initialise(self):
        self.discovered = False
        self.visited = False
        self.value = math.inf
        self.position = None
        self.prev = None


class Graph:
    def __init__(self, v_count: int) -> None:
        self.vertices = [None] * v_count
        self.edges = []
        for i in range(v_count):
            self.vertices[i] = Vertex(i)

    def add_edges(self, edges_count: list, directed=True) -> None:
        edges_count.sort(key=lambda x: x[0])
        for e in edges_count:
            u, v, r = self.vertices[e[0]], self.vertices[e[1]], e[2]
            cur_edge = Edge(u, v, r)
            u.add_edge(cur_edge)
            self.edges.append(cur_edge)
        if not directed:
            for e in edges_count:
                v, u, r = self.vertices[e[0]], self.vertices[e[1]], e[2]
                cur_edge = Edge(u, v, r)
                u.add_edge(cur_edge)
                self.edges.append(cur_edge)

    def get_vertex(self, id: int) -> Vertex:
        return self.vertices[id]

    def reset_vertex(self):
        for v in self.vertices:
            v.initialise()

    def bellman_ford(self, v_count: int, source: int, max_iter: int, prices: list) -> int:
        source = self.vertices[source]
        trading = [(0, -math.inf) for _ in range(v_count)]  # (litre, value)
        trading[source.id] = (1, prices[source.id])
        trading_2 = [(0, -math.inf) for _ in range(v_count)]

        current_max = prices[source.id]
        for _ in range(max_iter):  # O(M)
            for e in self.edges:  # O(T)
                litre = trading[e.u.id][0] * e.w
                trading_val = litre * prices[e.v.id]
                if trading_val > trading_2[e.v.id][1]:
                    trading_2[e.v.id] = litre, trading_val
                elif trading_val == trading_2[e.v.id][1] and litre > trading_2[e.v.id][0]:
                    trading_2[e.v.id] = litre, trading_val
                if trading_val > current_max:
                    current_max = trading_val
            trading = trading_2
            trading_2 = [(0, -math.inf) for _ in range(v_count)]
        return current_max

    def dijkstra(self, start: int, end: int, n: int):
        start_v, end_v = self.vertices[start], self.vertices[end]
        cost = math.inf
        discovered_queue = MinHeap(n)
        discovered_queue.push(start_v) 
        start_v.value = 0

        while len(discovered_queue) > 0:
            u = discovered_queue.serve()
            u.visited = True
            if u.id == end_v.id and u.value < cost:
                cost = u.value
            for e in u.edges:
                new_cost = u.value + e.w
                if e.v.visited is True:
                    pass
                elif e.v.discovered is False:
                    e.v.prev, e.v.value = u, new_cost
                    discovered_queue.push(e.v)
                elif e.v.value > new_cost:  
                    e.v.prev, e.v.value = u, new_cost
                    discovered_queue.update(e.v, new_cost)
                e.v.discovered = True
        return cost


class Edge:
    def __init__(self, u: Vertex, v: Vertex, w) -> None:
        self.u, self.v, self.w = u, v, w


class MinHeap:

    def __init__(self, max_count: int) -> None:
        self.count = 0
        self.the_array = [None for _ in range(max_count + 1)]

    def __len__(self):
        return self.count

    def rise(self, k) -> int:
        while k > 1 and self.the_array[k].value < self.the_array[k // 2].value:
            self.the_array[k // 2], self.the_array[k] = self.the_array[k], self.the_array[k // 2]
            self.the_array[k].position = k
            self.the_array[k // 2].position = k // 2
            k = k // 2
        return k

    def push(self, elem) -> None:
        self.count += 1
        self.the_array[self.count] = elem
        self.the_array[self.count].position = self.count
        self.rise(self.count)

    def sink(self, pos: int) -> None:
        left, right = 2 * pos, 2 * pos + 1
        if left < self.count:
            small_child = left
            if right < self.count and self.the_array[right].value < self.the_array[left].value:
                small_child = right
            if self.the_array[small_child].value < self.the_array[pos].value:
                self.the_array[small_child], self.the_array[pos] = self.the_array[pos], self.the_array[
                    small_child]  # swap
                self.the_array[small_child].position = small_child
                self.the_array[pos].position = pos
                self.sink(small_child)

    def serve(self) :  # O(log n)
        elem = self.the_array[1]
        self.the_array[1] = self.the_array[self.count]
        self.the_array[self.count] = None
        self.count -= 1
        self.sink(1)
        return elem

    def update(self, key: Vertex, value: int) -> None:
        self.the_array[key.position].value = value
        self.rise(key.position)


# --------------------------------Task 1--------------------------------#

def best_trades(prices, starting_liquid, max_trades, townspeople):
    v_count = len(prices)
    edges = []
    for trade in townspeople:
        for i in range(len(trade)):
            edges.append(trade[i])
    routes = Graph(v_count)
    routes.add_edges(edges, True)
    return round(routes.bellman_ford(v_count, starting_liquid, max_trades, prices)) #TODO remove round


def path_tracing(end, res): # O(V)
    while end.prev is not None:
        res.append(end.prev.id)
        end = end.prev
    res.reverse()
    return res


def opt_delivery(n, roads, start, end, delivery):
    route = Graph(n)
    route.add_edges(roads, False)

    # path includes delivery
    d_cost = route.dijkstra(start, delivery[0], n)
    d_path = path_tracing(route.get_vertex(delivery[0]), [])
    route.reset_vertex()
    d_cost += route.dijkstra(delivery[0], delivery[1], n) - delivery[2]
    d_path += path_tracing(route.get_vertex(delivery[1]), [])
    route.reset_vertex()
    if delivery[1] != end:
        d_cost += route.dijkstra(delivery[1], end, n)
        d_path += path_tracing(route.get_vertex(end), [end])
        route.reset_vertex()
    else:
        d_path.append(end)

    # path without delivery
    cost = route.dijkstra(start, end, n)
    path = path_tracing(route.get_vertex(end), [end])

    if cost < d_cost:
        return cost, path
    return d_cost, d_path


if __name__ == "__main__":
    # prices = [10, 5, 1, 0.1]
    # starting_liquid = 0
    # max_trades = 6
    # townspeople = [[(0, 1, 4), (2, 3, 30)], [(1, 2, 2.5), (2, 0, 0.2)]]
    # print(best_trades(prices, starting_liquid, max_trades, townspeople))
    # max_trades = 2
    # print(best_trades(prices, starting_liquid, max_trades, townspeople))
    # max_trades = 7
    # print(best_trades(prices, starting_liquid, max_trades, townspeople))
    # max_trades = 9
    # print(best_trades(prices, starting_liquid, max_trades, townspeople))
    # prices = [20]
    # starting_liquid = 0
    # max_trades = 10
    # townspeople = [[(0, 0, 1), (0, 0, 0.5)], [(0, 0, 1)]]
    # result = best_trades(prices, starting_liquid, max_trades, townspeople)
    # expected = 20
    # print(result == expected)
    #
    # # Test with trading all the time
    # townspeople = [[(0, 0, 2), (0, 0, 0.5)], [(0, 0, 1)]]
    # result = best_trades(prices, starting_liquid, max_trades, townspeople)
    # expected = 20 * 2 ** 10
    # print(result == expected)
    #
    # prices = [10, 10, 10, 10, 10]
    # starting_liquid = 1
    # max_trades = 10
    # townspeople = [[(1, 4, 3), (1, 2, 10), (4, 0, 10), (2, 3, 2)]]
    # result = best_trades(prices, starting_liquid, max_trades, townspeople)
    # expected = 300
    # print(result == expected)
    #
    # prices = [1, 3, 2, 5, 4]
    # starting_liquid = 2
    # max_trades = 3
    # townspeople = [[(1, 4, 3), (1, 2, 10), (4, 0, 10), (2, 3, 2)]]
    # result = best_trades(prices, starting_liquid, max_trades, townspeople)
    # expected = 10
    # print(result == expected)
    #
    # n = 4
    # roads = [(0, 1, 3), (0, 2, 5), (2, 3, 7), (1, 3, 20)]
    # start = 0
    # end = 1
    # delivery = (2, 3, 100)
    # print(opt_delivery(n, roads, start, end, delivery))

    # expected = (-684, [94, 88, 65, 23, 75, 19, 75, 23, 65, 88, 94, 28, 97])
    n = 100
    # start = 94
    # end = 97
    # delivery = (19, 94, 745)
    roads = Road().roads
    # print(opt_delivery(n, roads, start, end, delivery))

    r = Road()
    failed = 0
    for s in range(len(r.setup)):
        setp = r.setup[s]
        if opt_delivery(100 , roads , setp[0] , setp[1] , setp[2])[0] != r.answer[s][0][0] :
            print("Ans = " + str(opt_delivery(100 , roads , setp[0] , setp[1] , setp[2])))
            print("Expected = " + str(r.answer[s][0]))
            failed += 1
    print("Failed = " + str(failed))
    print("Total = " + str(len(r.setup)))

    