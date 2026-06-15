
from LSA import LSA

class Router:
    def __init__(self, router_ID):
        self.ID = router_ID
        self.neighbors = {}          
        self.LSDB = {}               
        self.routing_table = {}      

    def add_neighbor(self, neighbor_ID, cost):
        self.neighbors[neighbor_ID] = cost

    def generate_LSA(self):
        seq = self.LSDB[self.ID].seq_num + 1 if self.ID in self.LSDB else 1
        return LSA(self.ID, seq, list(self.neighbors.items()))

    def install_LSA(self, LSA):
        if (LSA.origin_ID not in self.LSDB or
            LSA.seq_num > self.LSDB[LSA.origin_ID].seq_num):
            self.LSDB[LSA.origin_ID] = LSA
            return True
        return False
