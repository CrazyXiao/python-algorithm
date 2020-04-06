"""
    并查集（union find）
    可以用数组实现的树形结构
"""
import abc
import time
import random


def uf_test_time(uf, count):
    start = time.process_time()
    uf = uf(count)
    for i in range(count):
        uf.union(int(random.random()*count), int(random.random()*count))
    for i in range(count):
        uf.is_same(int(random.random()*count), int(random.random()*count))
    elapsed = (time.process_time() - start)
    print("Time used:",elapsed)


class UnionFind(metaclass=abc.ABCMeta):
    """
        抽象类
    """
    def __init__(self, capacity):
        self.parents = list(range(capacity))

    def is_same(self, v1, v2):
        """
            查看v1 v2是否属于同一个集合
        """
        return self.find(v1) == self.find(v2)

    @abc.abstractmethod
    def find(self, v):
        """
            查找v所属集合（根节点）
        """
        raise NotImplementedError

    @abc.abstractmethod
    def union(self, v1, v2):
        """
            将v1所在集合合并到v2所在集合
        """
        raise NotImplementedError


class QuickFind(UnionFind):

    def find(self, v):
        return self.parents[v]


    def union(self, v1, v2):
        p1 = self.find(v1)
        p2 = self.find(v2)
        if p1 == p2:
            return
        for i in range(len(self.parents)):
            if self.parents[i] == p1:
                self.parents[i] =  p2


class QuickUnion(UnionFind):

    def find(self, v):
        while v != self.parents[v]:
            v = self.parents[v]
        return v


    def union(self, v1, v2):
        p1 = self.find(v1)
        p2 = self.find(v2)
        if p1 == p2:
            return
        self.parents[p1] = p2


class QuickUnionBasedOnSize(QuickUnion):
    """
        quick union基于size的优化
    """

    def __init__(self, capacity):
        super(QuickUnionBasedOnSize, self).__init__(capacity)
        self.sizes = [1 for i in range(capacity)]


    def union(self, v1, v2):
        p1 = self.find(v1)
        p2 = self.find(v2)
        if p1 == p2:
            return
        if self.sizes[p1] < self.sizes[p2]:
            self.parents[p1] = p2
            self.sizes[p2] += 1
        else:
            self.parents[p2] = p1
            self.sizes[p1] += 1

class QuickUnionBasedOnRank(QuickUnion):
    """
        quick union基于rank的优化
    """

    def __init__(self, capacity):
        super(QuickUnionBasedOnRank, self).__init__(capacity)
        self.ranks = [1 for i in range(capacity)]


    def union(self, v1, v2):
        p1 = self.find(v1)
        p2 = self.find(v2)
        if p1 == p2:
            return
        if self.ranks[p1] < self.ranks[p2]:
            self.parents[p1] = p2
        elif self.ranks[p1] > self.ranks[p2]:
            self.parents[p2] = p1
        else:
            self.parents[p1] = p2
            self.ranks[p2] += 1


class QuickUnionBasedOnRPC(QuickUnionBasedOnRank):
    """
        quick union基于rank的路径压缩
    """

    def find(self, v):
        if v != self.parents[v]:
            self.parents[v] = self.find(self.parents[v])
        return self.parents[v]


class QuickUnionBasedOnRPS(QuickUnionBasedOnRank):
    """
        quick union基于rank的路径分裂
    """

    def find(self, v):
        while v != self.parents[v]:
            p = self.parents[v]
            self.parents[v] = self.parents[p]
            v = p
        return self.parents[v]


class QuickUnionBasedOnRPH(QuickUnionBasedOnRank):
    """
        quick union基于rank的路径减半
    """

    def find(self, v):
        while v != self.parents[v]:
            p = self.parents[v]
            self.parents[v] = self.parents[p]
            v = self.parents[v]
        return self.parents[v]


if __name__ == '__main__':
    uf = QuickUnionBasedOnSize(12)
    uf.union(0 ,1)
    uf.union(3, 0)
    uf.union(0, 4)
    uf.union(2, 3)
    uf.union(2, 5)
    uf.union(6, 7)
    uf.union(8, 10)
    uf.union(9, 10)
    uf.union(9, 11)
    assert not uf.is_same(0, 6)
    assert uf.is_same(0, 5)
    uf.union(4, 6)
    assert uf.is_same(2, 7)