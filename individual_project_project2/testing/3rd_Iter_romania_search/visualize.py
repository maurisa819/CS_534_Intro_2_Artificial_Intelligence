import networkx as nx
import matplotlib.pyplot as plt
from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent

def visualize_path(path):
    agent = SimpleProblemSolvingAgent()
    G = nx.Graph()
    for node, neighbors in agent.graph.items():
        for neigh, cost in neighbors.items():
            G.add_edge(node, neigh, weight=cost)
    pos = agent.locations
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_size=500)
    edge_list = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2.5)
    plt.show()

if __name__ == "__main__":
    start = input("Enter start city for visualization: ")
    goal = input("Enter goal city for visualization: ")
    agent = SimpleProblemSolvingAgent()
    path, _ = agent.astar_search(start, goal)
    visualize_path(path)
