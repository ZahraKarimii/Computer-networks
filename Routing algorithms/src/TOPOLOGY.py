
class Topology:
    def __init__(self):
        self.routers = {}


    def add_router(self, router):
        self.routers[router.ID] = router


    def connect(self, R1, R2, cost):
        self.routers[R1].add_neighbor(R2, cost)
        self.routers[R2].add_neighbor(R1, cost)
