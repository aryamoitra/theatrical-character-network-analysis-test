import matplotlib.pyplot as plt
import networkx as nx
import os
from typing import Dict, List

# Construct, save (as a PNG), and display the network
def create_network(filename: str, frequency_dict: Dict[str, Dict[str, int]], volume_dict: Dict[str, int], removed_characters: List[str]=[]):
    G = nx.Graph()
    counter=0
    for speaker, responses in frequency_dict.items():
        print(f"\n\n{counter}\n{speaker}\n{responses}\n\n")
        G.add_node(speaker)
        for respondent, frequency in responses.items():
            print(f"Processing response from {speaker} to {respondent}")
            if G.has_edge(speaker, respondent):
                G[speaker][respondent]["weight"] += frequency
            else:
                G.add_edge(speaker, respondent, weight=frequency)
            print(f"{speaker}-{respondent}: {G[speaker][respondent]["weight"]}")
        print("\n--")
        counter += 1    
    pos = nx.spring_layout(G, iterations=10000)
    node_sizes = [volume*10 for character, volume in volume_dict.items() if character not in removed_characters]
    for speaker, respondent in G.edges():
        G[speaker][respondent]["weight"] /= 10
        print(f"{speaker}-{respondent} weigth = {G[speaker][respondent]["weight"]}")
    plt.figure(figsize=(9, 5))
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="blue", alpha=0.4)
    nx.draw_networkx_edges(G, pos, edge_color="blue", alpha=0.65)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", verticalalignment="bottom")
    while True:
        try:
            plt.savefig(f"Output/{filename}.png", format="png")
            break
        except FileNotFoundError:
            os.mkdir("Output")
    print(f"{filename}.png has been successfully created!")
    plt.show()
