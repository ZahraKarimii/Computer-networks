
from DIJKSTRA import dijkstra

class Simulator:
    def __init__(self, topology):
        self.topology = topology



    def flood_LSA(self):
        queue = []

        for router in self.topology.routers.values():
            LSA = router.generate_LSA()
            router.install_LSA(LSA)
            queue.append((router.ID, LSA))

        while queue:
            sender_ID, LSA = queue.pop(0)
            sender = self.topology.routers[sender_ID]

            for nbr_ID in sender.neighbors:
                nbr = self.topology.routers[nbr_ID]
                if nbr.install_LSA(LSA):
                    queue.append((nbr_ID, LSA))



    def build_routing_tables(self):
        for router in self.topology.routers.values():
            graph = {}
            for LSA in router.LSDB.values():
                graph[LSA.origin_ID] = LSA.neighbors

            dist, parent = dijkstra(graph, router.ID) 

            router.routing_table = {}
            for dest in dist:
                if dest == router.ID or parent[dest] is None:
                    continue

                hop = dest
                while parent[hop] != router.ID:
                    hop = parent[hop]

                router.routing_table[dest] = (hop, dist[dest])



    def send_packet(self, src, dst):
        current = src
        path = [current]

        while current != dst:
            router = self.topology.routers[current]
            if dst not in router.routing_table:
                print("Packet dropped")
                return
            current = router.routing_table[dst][0]
            path.append(current)

        print("Packet path : ", " → ".join(path))
