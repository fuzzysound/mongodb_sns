import networkx as nx
import matplotlib.pyplot as plt


g = nx.DiGraph()
g.add_edge('a', 'b', weight=1)
g.add_edge('b', 'c', weight=2)
g.add_edge('c', 'a', weight=3)
g.add_edge('c', 'd', weight=2)
g.add_edge('e', 'f', weight=1)
pr1 = nx.pagerank_numpy(g)
print(pr1)

g = nx.MultiDiGraph()
g.add_edge('a', 'b')
g.add_edge('b', 'c')
g.add_edge('b', 'c')
g.add_edge('c', 'a')
g.add_edge('c', 'a')
g.add_edge('c', 'a')
g.add_edge('c', 'd')
g.add_edge('c', 'd')
g.add_edge('e', 'f')
pr2 = nx.pagerank_scipy(g)
nx.draw(g)
plt.show()
print(pr2)