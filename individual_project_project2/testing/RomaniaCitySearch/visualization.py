import matplotlib.pyplot as plt
import networkx as nx
from search_algorithms import romania_map, city_coordinates

def draw_path(path, title="Path Visualization"):
    G = nx.Graph()
    pos = {city: (x, -y) for city, (x, y) in city_coordinates.items()}  # Flip y-axis for correct orientation

    for city, neighbors in romania_map.items():
        for neighbor, cost in neighbors.items():
            G.add_edge(city, neighbor, weight=cost)

    plt.figure(figsize=(12, 8))
    nx.draw_networkx(G, pos, node_size=500, node_color='lightgray', font_size=10)
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)
    plt.title(title)
    plt.axis('off')
    plt.show()
