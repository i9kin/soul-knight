# https://github.com/TheAlgorithms/Python/blob/master/graphs/bfs_shortest_path.py

def bfs_shortest_path(graph: dict, start, goal) -> str:
    explored = []
    queue = [[start]]
    if start == goal:
        return -1
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path
            explored.append(node)
    return -1

class G:
    def __init__(self, lvl):
        self.lvl = lvl
        self.build()
        self.components()

    def build(self):
        graph = {}
        for i in range(len(self.lvl)):
            for j in range(len(self.lvl[i])):
                if self.lvl[i][j] != '-':
                    graph[i * len(self.lvl[0]) + j] = []
                    if 0 <= i - 1 and 0 <= j - 1 and self.lvl[i - 1][j - 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i - 1)
                                                          * len(self.lvl[0]) + j - 1)
                    if 0 <= i - 1 and self.lvl[i - 1][j] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i - 1) * len(self.lvl[0]) + j)
                    if 0 <= i - 1 and j + 1 < len(self.lvl[i]) and self.lvl[i - 1][j + 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i - 1)
                                                          * len(self.lvl[0]) + j + 1)
                    if 0 <= j - 1 and self.lvl[i][j - 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append(i * len(self.lvl[0]) + j - 1)
                    if j + 1 < len(self.lvl[i]) and self.lvl[i][j + 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append(i * len(self.lvl[0]) + j + 1)
                    if i + 1 < len(self.lvl) and 0 <= j - 1 and self.lvl[i + 1][j - 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i + 1)
                                                          * len(self.lvl[0]) + j - 1)
                    if i + 1 < len(self.lvl) and self.lvl[i + 1][j] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i + 1) * len(self.lvl[0]) + j)
                    if i + 1 < len(self.lvl) and j + 1 < len(self.lvl[i]) and self.lvl[i + 1][j + 1] != '-':
                        graph[i * len(self.lvl[0]) + j].append((i + 1)
                                                          * len(self.lvl[0]) + j + 1)

            self.graph = graph

    def components(self):
        n = len(self.lvl[0]) * len(self.lvl) * 16 - 1
        used = [False for _ in range(n + 1)]
        colors = [-1 for _ in range(n + 1)]
        color = 0

        def dfs(v, color):
            colors[v] = color
            used[v] = True
            for u in self.graph[v]:
                if not used[u]:
                    dfs(u, color)
        color = 0
        for i in range(n):
            if colors[i] == -1 and i in self.graph:
                dfs(i, color)
                color += 1

        self.colors = colors