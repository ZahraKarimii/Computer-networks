from ROUTER import Router
from TOPOLOGY import Topology
from SIMULATOR import Simulator
import matplotlib.pyplot as plt
import math


def display_topology_gui(topology):
    routers = list(topology.routers.keys())
    n = len(routers)
    if n == 0:
        return
    
    angle_step = 2 * math.pi / n
    positions = {}

    for i, r in enumerate(routers):
        angle = i * angle_step
        x = math.cos(angle)
        y = math.sin(angle)
        positions[r] = (x, y)

    plt.figure("Network Topology", figsize=(6, 6))

    drawn = set()
    for r in topology.routers.values():
        x1, y1 = positions[r.ID]
        for nbr, cost in r.neighbors.items():
            edge = tuple(sorted([r.ID, nbr]))
            if edge in drawn:
                continue
            drawn.add(edge)

            x2, y2 = positions[nbr]

            plt.plot([x1, x2], [y1, y2], "k-")

            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            plt.text(mx, my, str(cost), color="red", fontsize=18,
                     horizontalalignment="center", verticalalignment="center")

    for r, (x, y) in positions.items():
        plt.scatter(x, y, s=800)
        plt.text(x, y, r, color="white", fontsize=12,
                 horizontalalignment="center", verticalalignment="center")

    plt.axis("off")
    plt.title("Network Topology Graph")
    plt.show(block = False)


def main():
    topology = Topology()

    n = int(input("Number of router : "))
    for i in range(1, n + 1):
        router = Router(f"R{i}")
        topology.add_router(router)
    print("\nGraph nodes :")
    print(", ".join(topology.routers.keys()))
    print("\nInter cost by this format : R1 R2 cost")
    print("For the end write [done]")

    while True:
        try:
            line =  input().strip()
        except EOFError:
            break 
        if line.lower() == "done":
            break
        if not line:
            continue
    
        r1, r2, cost = line.split()
        cost = int(cost)
        if r1 not in topology.routers or r2 not in topology.routers:
            print("Invalid router")
            continue

        topology.connect(r1, r2, cost)

    display_topology_gui(topology)

    sim = Simulator(topology)
    sim.flood_LSA()
    sim.build_routing_tables()

    for r in topology.routers.values():
        print(f"\nRouting Table {r.ID}:")
        print("Destination  ||  Next hop ")
        for dest, (next_hop, cost) in r.routing_table.items():
            print(f"    {dest}       ->    {next_hop}      cost = {cost}")
        print("**************************************")

    while True:
        print("\n Send packet")
        src = input("Source router : ")
        if src == 'A':
            break
        dst = input("Destination router : ")

        if src in topology.routers and dst in topology.routers:
            sim.send_packet(src, dst)
        else:
            print("Router invalid")
    
if __name__ == "__main__":
    main()
