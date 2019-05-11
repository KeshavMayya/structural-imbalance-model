
import networkx as nx
import random
G = nx.complete_graph(4)
G.add_edges_from([(u, v, {'sign': 2*random.randint(0, 1)-1}) for u, v in G.edges])
nx.relabel_nodes(G, {0: 'Alice', 1: 'Bob', 2: 'Eve', 3: 'Wally'}, copy=False)

print('Friendly relationships: ', [(x, y) for (x, y, sign) in G.edges(data='sign') if (sign == 1)])
print('Hostile relationships: ', [(x, y) for (x, y, sign) in G.edges(data='sign') if (sign == -1)])



from helpers.solvers import default_solver
my_solver, my_token = default_solver()



# Select a D-Wave system and handle mapping from problem graph to sampler graph
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite


sampler = EmbeddingComposite(DWaveSampler(solver="", token="")) #Make sure to add your API token and solver



# Return a good partition (minimal structural imbalance) and its frustrated edges  
import dwave_networkx as dnx
imbalance, bicoloring = dnx.structural_imbalance(G, sampler)

# Mark the returned frustrated edges and node set (color) on the graph 
for edge in G.edges:
    G.edges[edge]['frustrated'] = edge in imbalance
for node in G.nodes:
    G.nodes[node]['color'] = bicoloring[node]

# Print the relationships for the returned partition
print('Yellow set: ', [person for (person, color) in bicoloring.items() if (color == 0)])
print('Blue set: ', [person for (person, color) in bicoloring.items() if (color == 1)])
print('\nFrustrated relationships: ', list(imbalance.keys()))


from helpers.draw import draw
draw(G, with_labels=True);





# Load data from the Stanford Militants Mapping Project into NetworkX graph G
from helpers.loader import global_signed_social_network
G = global_signed_social_network()




# Select the Syria subregion by creating subgraph S from the full data set G
syria_groups = set()
for v, data in G.nodes(data=True):
    if 'map' not in data:
        continue
    if data['map'] in {'Syria', 'Aleppo'}:
        syria_groups.add(v)
S = G.subgraph(syria_groups)

# Filter by year
year = 2013
filtered_edges = ((u, v) for u, v, a in S.edges(data=True) if a['event_year'] <= year)
S = S.edge_subgraph(filtered_edges)


# See data associated with nodes (first two nodes only for brevity)
list(S.nodes(data=True))[:2]



# See data associated with edges (first two)
list(S.edges(data=True))[:2]




position = draw(S)




# Return a good partition of the Syrian 2013 network and its frustrated edges 
imbalance, bicoloring = dnx.structural_imbalance(S, sampler)
# Annotate the network with the returned frustrated edges and node sets
for edge in S.edges:
    S.edges[edge]['frustrated'] = edge in imbalance
for node in S.nodes:
    S.nodes[node]['color'] = bicoloring[node]



# Nodes now have a group bicoloring
list(S.nodes(data=True))[:2]


# In[ ]:


# Edges now have a marking indicating whether they are frustrated or not
list(S.edges(data=True))[:2]


# Redraw the network with the previous node positioning: nodes are now bicolored and dashed lines indicate frustrated edges.


draw(S, position);


# Redraw the network with a new positioning that separates the two sets.
# Frustrated edges now stand out
draw(S);


#Solving the entire dataset

imbalance, bicoloring = dnx.structural_imbalance(G, sampler)
for edge in G.edges:
    G.edges[edge]['frustrated'] = edge in imbalance
for node in G.nodes:
    G.nodes[node]['color'] = bicoloring[node]
draw(G);

