from graph import *
from union_find import *


def uf_test():
    count = 1000000
    uf_test_time(QuickUnionBasedOnSize, count)
    uf_test_time(QuickUnionBasedOnRank, count)
    uf_test_time(QuickUnionBasedOnRPS, count)
    uf_test_time(QuickUnionBasedOnRPH, count)



def graph_test():
    graph = ListGraph()
    graph.add_edge("v1", "v0")
    graph.add_edge("v1", "v2")
    graph.add_edge("v2", "v0")
    graph.add_edge("v2", "v3")
    graph.add_edge("v3", "v4")
    graph.add_edge("v0", "v4")
    print(graph, "\n-----------")
    graph.dfs("v1")


graph_test()
