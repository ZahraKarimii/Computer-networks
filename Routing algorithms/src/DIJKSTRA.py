
import heapq

def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    parent = {v: None for v in graph}
    dist[start] = 0

    pq = [(0, start)]
    while pq:
        cost, u = heapq.heappop(pq)
        if cost > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent
