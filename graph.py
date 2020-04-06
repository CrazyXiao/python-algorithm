"""
    图
"""

import abc
import heapq
from union_find import QuickUnionBasedOnRPH

class Graph(metaclass=abc.ABCMeta):
    # 顶点集合
    vertexs = {}
    # 边集合
    edges = set()
    def add_vertex(self, v):
        """ 添加顶点 """
        raise NotImplementedError

    @abc.abstractmethod
    def add_edge(self, _from, _to, weight=None):
        """ 添加边 """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_edge(self,  _from, _to):
        """ 删除边 """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_vertex(self, vertex):
        """ 删除顶点 """
        raise NotImplementedError

    def vertex_size(self):
        return len(self.vertexs)

    def edge_size(self):
        return len(self.edges)

    @abc.abstractmethod
    def bfs(self, begin):
        """
            广度优先搜索
        """
        raise NotImplementedError

    @abc.abstractmethod
    def dfs(self, begin):
        """
            深度优先搜索
        """
        raise NotImplementedError

    def khan(self):
        """
            拓扑排序
        """
        pass

    def mst(self):
        """
            最小生成树
        """
        pass

class Vertex():
    """
        顶点
    """
    def __init__(self, v):
        self.value = v
        self.out_edges = set()
        self.in_edges = set()

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return "%s" % (self.value)

class Edge:
    """
        边
    """
    def __init__(self, _from, _to, weight=0):
        self._from = _from
        self._to = _to
        self.weight = weight

    def __eq__(self, other):
        return self._from == other._from and self._to == other._to

    def __hash__(self):
        return hash(self._from)*8+hash(self._to)

    def __str__(self):
        return "%s -> %s, %s" % (self._from, self._to, self.weight)

    def __lt__(self, other):
        return self.weight < other.weight



class ListGraph(Graph):

    def __str__(self):
        return "\n".join([str(edge) for edge in self.edges])

    def add_vertex(self, v):
        vertex = self.vertexs.get(v)
        if not vertex:
            vertex = Vertex(v)
            self.vertexs[v] = vertex

    def _remove_edge(self, edge):
        if edge in self.edges:
            edge._from.out_edges.remove(edge)
            edge._to.in_edges.remove(edge)
            self.edges.remove(edge)

    def remove_edge(self, _from, _to):
        _from_vertex = self.vertexs.get(_from)
        _to_vertex = self.vertexs.get(_to)
        if not _from_vertex or not _to_vertex:
            return
        edge = Edge(_from_vertex, _to_vertex)
        self._remove_edge(edge)


    def add_edge(self, _from, _to, weight=0):
        _from_vertex = self.vertexs.get(_from)
        _to_vertex = self.vertexs.get(_to)
        if not _from_vertex:
            _from_vertex = Vertex(_from)
            self.vertexs[_from] = _from_vertex
        if not _to_vertex:
            _to_vertex = Vertex(_to)
            self.vertexs[_to] = _to_vertex

        edge = Edge(_from_vertex, _to_vertex, weight)

        if edge in _from_vertex.out_edges:
            _from_vertex.out_edges.remove(edge)
        if edge in _to_vertex.in_edges:
            _to_vertex.in_edges.remove(edge)
        _from_vertex.out_edges.add(edge)
        _to_vertex.in_edges.add(edge)
        self.edges.add(edge)

    def remove_vertex(self, v):
        if v not in self.vertexs:
            return
        vertex = self.vertexs[v]
        del self.vertexs[v]

        for edge in list(vertex.out_edges):
            self._remove_edge(edge)
        for edge in list(vertex.in_edges):
            self._remove_edge(edge)

    def bfs(self, begin):
        begin_vertex = self.vertexs.get(begin)
        if not begin_vertex:
            return
        visited_vertex = set()
        queue = []
        visited_vertex.add(begin_vertex)
        queue.append(begin_vertex)

        while queue:
            vertex = queue.pop(0)
            print(vertex)
            for edge in vertex.out_edges:
                if edge._to in visited_vertex:
                    continue
                visited_vertex.add(edge._to)
                queue.append(edge._to)


    def _dfs(self, vertex, visited_vertex):
        print(vertex)
        visited_vertex.add(vertex)
        for edge in vertex.out_edges:
            if edge._to in visited_vertex:
                continue
            self._dfs(edge._to, visited_vertex)


    def dfs(self, begin):
        begin_vertex = self.vertexs.get(begin)
        if not begin_vertex:
            return
        visited_vertex = set()
        self._dfs(begin_vertex, visited_vertex)

    def dfs2(self, begin):
        """
            非递归的深度优先搜索
        """
        begin_vertex = self.vertexs.get(begin)
        if not begin_vertex:
            return
        visited_vertex = set()
        stack = []
        stack.append(begin_vertex)
        visited_vertex.add(begin_vertex)
        print(begin_vertex)
        while stack:
            vertex = stack.pop()
            for edge in vertex.out_edges:
                if edge._to in visited_vertex:
                    continue
                visited_vertex.add(edge._to)
                print(edge._to)
                stack.append(edge._from)
                stack.append(edge._to)


    def khan(self):
        res = []
        queue = []
        ins = {}
        for v in self.vertexs:
            vertex = self.vertexs[v]
            if len(vertex.in_edges) == 0:
                queue.append(vertex)
            else:
                ins[vertex] = len(vertex.in_edges)
        while queue:
            vertex = queue.pop(0)
            res.append(vertex.value)
            for edge in vertex.out_edges:
                if edge._to not in ins:
                    continue
                ins[edge._to] -= 1
                if ins[edge._to] == 0:
                    queue.append(edge._to)
        return res

    def prim(self):
        """
            prim 算法
        """
        res = []
        vertexs = list(self.vertexs.values())
        added_vertexs = set()
        if not vertexs:
            return
        vertex = vertexs[0]
        added_vertexs.add(vertex)
        heap = list(vertex.out_edges)
        heapq.heapify(heap) # 批量建堆
        while heap and len(res) < len(self.vertexs)-1:
            edge = heapq.heappop(heap)
            if edge._to in added_vertexs:
                continue
            res.append({"from": edge._from.value, "to": edge._to.value, "weight": edge.weight})
            added_vertexs.add(edge._to)
            for _edge in edge._to.out_edges:
                heapq.heappush(heap, _edge)
        return res

    def kruskal(self):
        """
            kruskal 算法
            通过并查集判断是否形成环
        """
        res = []
        heap = list(self.edges)
        uf = QuickUnionBasedOnRPH(self.vertex_size()) # O(V)
        uf_map = {self.vertexs[v]: index for v, index in zip(self.vertexs, uf.parents)}
        heapq.heapify(heap) # 批量建堆 O(E)
        # O(Elog(E))
        while heap and len(res) < len(self.vertexs)-1:
            edge = heapq.heappop(heap)
            if uf.is_same(uf_map[edge._from], uf_map[edge._to]):
                continue
            res.append({"from": edge._from.value, "to": edge._to.value, "weight": edge.weight})
            uf.union(uf_map[edge._from], uf_map[edge._to])
        return res

    def mst(self):
        # return self.kruskal()
        return self.prim()


    def add_undirect_edge(self, v1, v2, weight=0):
        self.add_edge(v1, v2, weight)
        self.add_edge(v2, v1, weight)


def graph_test():
    graph = ListGraph()
    graph.add_edge("v1", "v0")
    graph.add_edge("v1", "v2")
    graph.add_edge("v2", "v0")
    graph.add_edge("v2", "v3")
    graph.add_edge("v3", "v4")
    graph.add_edge("v0", "v4")
    print(graph, "\n-----------")
    graph.dfs2("v1")


def topo_test():
    graph = ListGraph()
    input_list = [
        (0,2), (1,0), (2,5), (2,6), (3,1), (3,5), (3,7), (5,7),  (6,4), (7,6)
    ]
    for v1, v2 in input_list:
        graph.add_edge(v1, v2)
    print(graph.khan())


def test_mst():
    graph = ListGraph()
    graph.add_undirect_edge("A", "B", 17)
    graph.add_undirect_edge("A", "F", 1)
    graph.add_undirect_edge("A", "E", 16)
    graph.add_undirect_edge("B", "C", 6)
    graph.add_undirect_edge("B", "D", 5)
    graph.add_undirect_edge("B", "F", 11)
    graph.add_undirect_edge("C", "D", 10)
    graph.add_undirect_edge("D", "E", 4)
    graph.add_undirect_edge("D", "F", 14)
    graph.add_undirect_edge("E", "F", 33)
    res = graph.mst()
    print(res)

if __name__ == '__main__':
    test_mst()
