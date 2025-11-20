# Отчет по лабораторной работе 10

# Графы

**Дата:** 2025-11-20
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы

Изучить основные понятия теории графов и алгоритмы работы с ними. Освоить представления графов в памяти и основные алгоритмы обхода. Получить практические навыки реализации алгоритмов на графах и анализа их сложности.

## Практическая часть

### Выполненные задачи

- [ ] Реализовать различные представления графов (матрица смежности, список смежности).
- [ ] Реализовать алгоритмы обхода графов (BFS, DFS).
- [ ] Реализовать алгоритмы поиска кратчайших путей и компонент связности.
- [ ] Провести сравнительный анализ эффективности разных представлений графов.
- [ ] Решить практические задачи на графах.

### Ключевые фрагменты кода

```PYTHON
# graph_representation.py

class AdjacencyМatrix:
    """
    Класс сущности матрицы смежности для представления графа.
    Attributes:
        matrix (list of list of int): Матрица смежности графа.
        directed (bool): Флаг, указывающий, является ли граф ориентированным.
    Память: O(V^2)
    """

    def __init__(self, directed=False):
        self.matrix = list()
        self.directed = directed

    def add_vertex(self):
        """
        Добавляет вершину в граф, расширяя матрицу смежности.
        """
        size = len(self.matrix)
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * (size + 1))
    # Время: O(V)

    def remove_vertex(self, index):
        """
        Удаляет вершину из графа, сужая матрицу смежности.
        Args:
            index (int): Индекс вершины для удаления.
        """
        if index < 0 or index >= len(self.matrix):
            raise IndexError("Vertex index out of range")
        self.matrix.pop(index)
        for row in self.matrix:
            row.pop(index)
    # Время: O(V^2)

    def add_edge(self, u, v, weight=1):
        """
        Добавляет ребро между вершинами u и v с заданным весом.
        Args:
            u (int): Индекс начальной вершины.
            v (int): Индекс конечной вершины.
            weight (int): Вес ребра (по умолчанию 1).
        """
        if u < 0 or u >= len(self.matrix) or v < 0 or v >= len(self.matrix):
            raise IndexError("Vertex index out of range")
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight
    # Время: O(1)

    def remove_edge(self, u, v):
        """
        Удаляет ребро между вершинами u и v.
        Args:
            u (int): Индекс начальной вершины.
            v (int): Индекс конечной вершины.
        """
        if u < 0 or u >= len(self.matrix) or v < 0 or v >= len(self.matrix):
            raise IndexError("Vertex index out of range")
        self.matrix[u][v] = 0
        if not self.directed:
            self.matrix[v][u] = 0
    # Время: O(1)

    def list_to_matrix(self, adj_list):
        """
        Преобразует список смежности в матрицу смежности.
        Args:
            adj_list (AdjacencyList): Граф, представленный списком смежности.
        """
        size = len(adj_list.adj_list)
        self.matrix = [[0] * size for _ in range(size)]
        for u in adj_list.adj_list:
            for idx, v in enumerate(adj_list.adj_list[u]):
                weight = adj_list.weight_list[u][idx]
                self.matrix[u][v] = weight
    # Время: O(V^2)

    def print_matrix(self):
        """
        Печатает матрицу смежности графа.
        """
        for row in self.matrix:
            print(row)


class AdjacencyList:
    """
    Класс сущности списка смежности для представления графа.
    Attributes:
        adj_list (dict): Словарь, где ключи - вершины,
        а значения - списки смежных вершин.
        directed (bool): Флаг, указывающий, является ли граф ориентированным.
    Память: O(V + E)
    """

    def __init__(self, directed=False):
        self.adj_list = dict()
        self.weight_list = dict()
        self.directed = directed

    def add_vertex(self, vertex):
        """
        Добавляет вершину в граф.
        Args:
            vertex (int): Вершина для добавления.
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.weight_list[vertex] = []
    # Время: O(1)

    def remove_vertex(self, vertex):
        """
        Удаляет вершину из графа.
        Args:
            vertex (int): Вершина для удаления.
        """
        if vertex in self.adj_list:
            self.adj_list.pop(vertex)
            self.weight_list.pop(vertex)
            for v in self.adj_list:
                if vertex in self.adj_list[v]:
                    self.adj_list[v].remove(vertex)
                    self.weight_list[v].pop(self.adj_list[v].index(vertex))
    # Время: O(V + E)

    def add_edge(self, u, v, weight=1):
        """
        Добавляет ребро между вершинами u и v с заданным весом.
        Args:
            u (int): Индекс начальной вершины.
            v (int): Индекс конечной вершины.
            weight (int): Вес ребра (по умолчанию 1).
        """
        if u not in self.adj_list:
            raise KeyError(f"Vertex {u} does not exist")
        if v not in self.adj_list:
            raise KeyError(f"Vertex {v} does not exist")
        self.adj_list[u].append(v)
        self.weight_list[u].append(weight)
        if not self.directed:
            self.adj_list[v].append(u)
            self.weight_list[v].append(weight)
    # Время: O(1)

    def remove_edge(self, u, v):
        """
        Удаляет ребро между вершинами u и v.
        Args:
            u (int): Индекс начальной вершины.
            v (int): Индекс конечной вершины.
        """
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)
            self.weight_list[u].pop(self.adj_list[u].index(v))
            if not self.directed:
                self.adj_list[v].remove(u)
                self.weight_list[v].pop(self.adj_list[v].index(u))
    # Время: O(E)

    def matrix_to_list(self, adj_matrix):
        """
        Преобразует матрицу смежности в список смежности.
        Args:
            adj_matrix (AdjacencyМatrix): Граф, 
            представленный матрицей смежности.
        """
        size = len(adj_matrix.matrix)
        self.adj_list = {i: [] for i in range(size)}
        self.weight_list = {i: [] for i in range(size)}
        for u in range(size):
            for v in range(size):
                if adj_matrix.matrix[u][v] != 0:
                    self.adj_list[u].append(v)
                    self.weight_list[u].append(adj_matrix.matrix[u][v])
    # Время: O(V^2)

    def print_list(self):
        """
        Печатает список смежности графа.
        """
        for vertex in self.adj_list:
            print(f"{vertex}: {self.adj_list[vertex]}")

```

```PYTHON
# graph_traversal.py


# Поиск в ширину (BFS): находит кратчайшие
# пути в невзвешенном графе, сложность O(V + E)


def bfs(graph, start):
    """
    Выполняет поиск в ширину (BFS) на графе, представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф, представленный матрицей смежности.
        start (int): Начальная вершина для обхода.
    Returns:
        list: Порядок посещения вершин.
    """
    visited = set()
    queue = [start]
    order = []

    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            neighbors = [
                idx for idx, val in enumerate(graph.matrix[vertex]) if val != 0
            ]
            queue.extend(neighbors)

    return order
# Время: O(V + E)

# Поиск в глубину (DFS): обход с возвратом, сложность O(V + E)


def dfs_recursive(graph, vertex, visited=None, order=None):
    """
    Выполняет рекурсивный поиск в глубину (DFS) 
    на графе, представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф, представленный матрицей смежности.
        vertex (int): Текущая вершина для обхода.
        visited (set): Множество посещенных вершин.
        order (list): Порядок посещения вершин.
    Returns:
        list: Порядок посещения вершин.
    """
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(vertex)
    order.append(vertex)

    neighbors = [
        idx for idx, val in enumerate(graph.matrix[vertex]) if val != 0
    ]
    for neighbor in neighbors:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order
# Время: O(V + E)


def dfs_iterative(graph, start):
    """
    Выполняет итеративный поиск в глубину (DFS) 
    на графе, представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф, представленный матрицей смежности.
        start (int): Начальная вершина для обхода.
    Returns:
        list: Порядок посещения вершин.
    """
    visited = set()
    stack = [start]
    order = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            neighbors = [
                idx for idx, val in enumerate(graph.matrix[vertex]) if val != 0
            ]
            stack.extend(reversed(neighbors))

    return order
# Время: O(V + E)

```

```PYTHON
# shortest_path.py

# from src.modules.graph_traversal import dfs_recursive # tests
from modules.graph_traversal import dfs_recursive
import heapq
from collections import deque
# Топологическая сортировка: для ориентированных ациклических графов (DAG)


def topological_sort(graph):
    """
    Выполняет топологическую сортировку на
    ориентированном ациклическом графе (DAG),
    представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф, представленный матрицей смежности.
    Returns:
        list: Топологически отсортированный порядок вершин.
    """

    in_degree = [0] * len(graph.matrix)
    for u in range(len(graph.matrix)):
        for v in range(len(graph.matrix)):
            if graph.matrix[u][v] == 1:
                in_degree[v] += 1

    queue = deque([i for i in range(len(graph.matrix)) if in_degree[i] == 0])
    topo_order = []

    while queue:
        vertex = queue.popleft()
        topo_order.append(vertex)

        for neighbor in range(len(graph.matrix)):
            if graph.matrix[vertex][neighbor] == 1:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    if len(topo_order) != len(graph.matrix):
        raise ValueError("Graph is not a DAG; topological sort not possible.")

    return topo_order
# Время: O(V + E)


# Поиск компонент связности


def connected_components(graph):
    """
    Находит все компоненты связности в неориентированном графе,
    представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф, представленный матрицей смежности.
    Returns:
        list of list: Список компонент связности, каждая из
        которых представлена списком вершин.
    """
    visited = set()
    components = []

    while len(visited) < len(graph.matrix):
        for i in range(len(graph.matrix)):
            if i not in visited:
                component = dfs_recursive(graph, i)
                for i in component:
                    visited.add(i)
                components.append(component)

    return components
# Время: O(V + E)

# Алгоритм Дейкстры для взвешенных графов


def dijkstra(graph, start):
    """
    Выполняет алгоритм Дейкстры для поиска
    кратчайших путей от стартовой вершины
    до всех остальных вершин в взвешенном графе,
    представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Взвешенный граф,
        представленный матрицей смежности.
        start (int): Начальная вершина.
    Returns:
        dict: Словарь с кратчайшими расстояниями от
        стартовой вершины до каждой вершины.
    """

    distances = {i: float('inf') for i in range(len(graph.matrix))}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor in range(len(graph.matrix)):
            weight = graph.matrix[current_vertex][neighbor]
            if weight > 0:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances
# Время: O((V + E) log V)


def find_shortest_path_in_maze(graph, start, end):
    """
    Находит кратчайший путь в лабиринте,
    представленном матрицей смежности.
    Args:
        graph (AdjacencyМatrix): Граф-лабиринт,
        представленный матрицей смежности.
        start (int): Начальная вершина.
        end (int): Конечная вершина.
    Returns:
        list: Список вершин, представляющих кратчайший путь
        от стартовой до конечной вершины.
    """
    distances = {i: float('inf') for i in range(len(graph.matrix))}
    previous = {i: None for i in range(len(graph.matrix))}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor in range(len(graph.matrix)):
            weight = graph.matrix[current_vertex][neighbor]
            if weight > 0:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    if distances[end] == float('inf'):
        return []  # Путь не найден

    return path

```

```PYTHON
# perfomance_analysis.py

from modules.graph_representation import AdjacencyМatrix
from modules.graph_representation import AdjacencyList
import timeit
import matplotlib.pyplot as plt
# Сравнение add Vertex(matrix, list), Remove Vertex(matrix, list)


def measure_time_matrix(size):
    """
    Измеряет время добавления и удаления вершин
    в графе, представленном матрицей смежности.
    Args:
        size (int): Количество вершин для добавления и удаления.
    Returns:
        tuple: Время добавления и удаления вершин в миллисекундах."""
    matrix = AdjacencyМatrix()

    start = timeit.default_timer()
    for _ in range(size):
        matrix.add_vertex()
    end = timeit.default_timer()
    matrix_add = (end - start) * 1000

    start = timeit.default_timer()
    for _ in range(size):
        matrix.remove_vertex(0)
    end = timeit.default_timer()
    matrix_remove = (end - start) * 1000

    return (matrix_add, matrix_remove)


def measure_time_list(size):
    """
    Измеряет время добавления и удаления вершин
    в графе, представленном списком смежности.
    Args:
        size (int): Количество вершин для добавления и удаления.
    Returns:
        tuple: Время добавления и удаления вершин в миллисекундах.
    """
    lst = AdjacencyList()

    start = timeit.default_timer()
    for i in range(size):
        lst.add_vertex(i)
    end = timeit.default_timer()
    list_add = (end - start) * 1000

    start = timeit.default_timer()
    for _ in range(size):
        lst.remove_vertex(0)
    end = timeit.default_timer()
    list_remove = (end - start) * 1000

    return (list_add, list_remove)


def Visualisation(sizes):
    """
    Визуализирует результаты измерений
    времени добавления и удаления вершин
    для матрицы и списка смежности.
    Args:
        sizes (list): Список размеров графов для измерений.
    """

    matrix_add_times = []
    list_add_times = []
    matrix_remove_times = []
    list_remove_times = []

    for size in sizes:
        result = measure_time_matrix(size)
        matrix_add_times.append(result[0])
        matrix_remove_times.append(result[1])

        result = measure_time_list(size)
        list_add_times.append(result[0])
        list_remove_times.append(result[1])

    plt.plot(sizes, matrix_add_times, label='Matrix Add Vertex')
    plt.plot(sizes, list_add_times, label='List Add Vertex')
    plt.title('Add Vertex Performance')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.savefig('./report/add_vertex_performance.png')
    plt.show()

    plt.plot(sizes, matrix_remove_times, label='Matrix Remove Vertex')
    plt.plot(sizes, list_remove_times, label='List Remove Vertex')
    plt.title('Remove Vertex Performance')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.savefig('./report/remove_vertex_performance.png')
    plt.show()

```

```PYTHON
# main.py

from modules.graph_representation import AdjacencyМatrix, AdjacencyList
from modules.graph_traversal import bfs, dfs_recursive, dfs_iterative
from modules.shortest_path import (
    topological_sort, connected_components, dijkstra,
    find_shortest_path_in_maze)
from modules.perfomance_analysis import Visualisation

matrix = AdjacencyМatrix(directed=False)
for _ in range(0, 6):
    matrix.add_vertex()

matrix.add_edge(2, 3)
matrix.add_edge(3, 1)
matrix.add_edge(4, 0)
matrix.add_edge(4, 1)
matrix.add_edge(5, 0, 99)
matrix.add_edge(5, 2)

# print("Topological Sort:", topological_sort(matrix))
print("BFS from vertex 5:", bfs(matrix, 5))
print("DFS Recursive from vertex 5:", dfs_recursive(matrix, 5))
print("DFS Iterative from vertex 5:", dfs_iterative(matrix, 5))

for i in connected_components(matrix):
    print("Connected Component:", i)

ways = dijkstra(matrix, 5)
for i in range(len(ways)):
    print(f"Shortest path from 5 to {i}: {ways[i]}")

Visualisation([100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
              600, 650, 700, 750, 800, 850, 900, 950, 1000])

print("\nGraph Representation:\n")
print("Adjacency Matrix:")
matrix.print_matrix()
print("\nAdjacency List:")
lst = AdjacencyList()
lst.matrix_to_list(matrix)

lst.print_list()

print("Maze-task")
maze = AdjacencyМatrix(directed=False)
# 0 - road, 1 - wall
#  [s, 1, 0, 0, 0, e],
#  [0, 1, 0, 1, 1, 0],
#   [0, 0, 0, 0, 1, 0],
#   [0, 1, 1, 0, 1, 0],
#  [0, 0, 0, 0, 0, 0],
#

for _ in range(30):
    maze.add_vertex()

edges = [
    (0, 6), (6, 12), (12, 18), (18, 24), (24, 25),
    (12, 13), (13, 14), (25, 26), (14, 8), (14, 15),
    (8, 2), (2, 3), (3, 4), (4, 5), (26, 27), (27, 28),
    (28, 29), (14, 20), (5, 11), (11, 17), (17, 23), (23, 29)
]
for u, v in edges:
    maze.add_edge(u, v)

path = find_shortest_path_in_maze(maze, 0, 5)
print("Shortest path in maze from S(0) to E(5):", path)

# Характеристики вычислительной машины
pc_info = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
"""
print(pc_info)

```

<image src="./report/add_vertex_performance.png" style="display:block; margin: auto;">
<image src="./report/remove_vertex_performance.png" style="display:block; margin: auto;">


```bash

BFS from vertex 5: [5, 0, 2, 4, 3, 1]
DFS Recursive from vertex 5: [5, 0, 4, 1, 3, 2]
DFS Iterative from vertex 5: [5, 0, 4, 1, 3, 2]
Connected Component: [0, 4, 1, 3, 2, 5]
Shortest path from 5 to 0: 5
Shortest path from 5 to 1: 3
Shortest path from 5 to 2: 1
Shortest path from 5 to 3: 2
Shortest path from 5 to 4: 4
Shortest path from 5 to 5: 0

Graph Representation:

Adjacency Matrix:
[0, 0, 0, 0, 1, 99]
[0, 0, 0, 1, 1, 0]
[0, 0, 0, 1, 0, 1]
[0, 1, 1, 0, 0, 0]
[1, 1, 0, 0, 0, 0]
[99, 0, 1, 0, 0, 0]

Adjacency List:
0: [4, 5]
1: [3, 4]
2: [3, 5]
3: [1, 2]
4: [0, 1]
5: [0, 2]
Maze-task
Shortest path in maze from S(0) to E(5): [0, 6, 12, 13, 14, 8, 2, 3, 4, 5]


Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12

```

| Операция / Характеристика     | Матрица смежности                         | Список смежности                          |
|------------------------------|--------------------------------------------|--------------------------------------------|
| **Память**                   | O(V²)                                      | O(V + E)                                   |
| **Добавление вершины**       | O(V) — нужно расширять каждую строку       | O(1) — просто создаётся новый список       |
| **Удаление вершины**         | O(V²) — удаление строки и столбца          | O(V + E) — проход по спискам               |
| **Добавление ребра**         | O(1) — просто записываем вес               | O(1) — добавляем элемент в список          |
| **Удаление ребра**           | O(1) — ставим 0                             | O(E) — поиск и удаление из списка          |
| **Проверка существования ребра** | O(1) — matrix[u][v]                        | O(deg(u)) — поиск в списке                |
| **Обход соседей вершины**    | O(V) — нужно пройти всю строку             | O(deg(u)) — только реальные соседи         |
| **Поддержка взвешенных рёбер** | Да (вес в ячейке)                          | Да (вес параллельным списком)              |
| **Лучше подходит для…**      | Плотных графов, V большое, E ≈ V²          | Разреженных графов, E << V²               |
| **Хуже подходит для…**       | Разреженных графов (растёт память)         | Графов, где важны быстрые проверки ребра  |
| **Конвертация список → матрица** | O(V²)                                    | —                                          |
| **Конвертация матрица → список** | O(V²)                                   | —                                          |



| Задача                                | Какой алгоритм применять                            | Почему                                                                                                                    |
| ------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Найти кратчайший путь в лабиринте** | BFS (если все рёбра = 1), Дейкстра (если есть веса) | Лабиринт = невзвешенный граф, поэтому BFS даёт кратчайший путь по количеству шагов; в случае разных стоимостей — Дейкстра |
| **Определить связность сети**         | BFS / DFS / Поиск компонент связности               | DFS/BFS позволяют определить доступные вершины; для всей сети — проходим все компоненты                                   |
| **Топологическая сортировка**         | DFS-based topo sort                  | Работает только для DAG; используется порядок зависимостей                                                                |


# Ответы на контрольные вопросы

## 1. Разница между матрицей смежности и списком смежности

| Критерий | Матрица смежности | Список смежности |
|---------|--------------------|------------------|
| **Память** | O(V²) | O(V + E) |
| **Проверка наличия ребра u→v** | O(1) | O(deg(u)) |
| **Добавление ребра** | O(1) | O(1) |
| **Удаление ребра** | O(1) | O(deg(u)) |
| **Добавление вершины** | Очень дорого — пересоздание матрицы | O(1) |
| **Оптимально для** | Плотных графов | Разреженных графов |
| **Недостатки** | Высокое потребление памяти | Медленнее проверка наличия ребра |
| **Преимущества** | Быстрые операции проверки | Экономия памяти |

---

## 2. Алгоритм поиска в ширину (BFS) и его применение

Поиск в ширину (BFS) — это алгоритм обхода графа, который исследует вершины слоями: сначала посещает всех соседей стартовой вершины, затем соседей этих соседей и так далее. Он использует очередь, что гарантирует, что вершины посещаются в порядке возрастания расстояния от источника.

BFS применяется для:
- нахождения кратчайшего пути в невзвешенных графах;
- проверки связности графа;
- поиска компонент связности;
- задач на минимальное количество шагов (лабиринты, сетевые маршруты);
- проверки на двудольность графа.

---

## 3. Отличия DFS от BFS и дополнительные задачи, решаемые DFS

Поиск в глубину (DFS) обходит граф, углубляясь по одному пути до конца, а затем делает откат назад. Он использует стек (неявный — в рекурсии или явный — вручную).

Отличия:
- **BFS** идёт слоями и находит кратчайшие пути в невзвешенных графах.
- **DFS** идёт вглубь, не гарантируя минимального пути, но лучше подходит для анализа структуры графа.

Задачи, решаемые DFS:
- проверка графа на наличие циклов;
- топологическая сортировка (DFS-версия);
- поиск мостов и точек сочленения;
- поиск компонент сильной связности;
- нахождение всех путей между вершинами (в небольших графах).

---

## 4. Алгоритм Дейкстры: принцип работы и ограничения

Алгоритм Дейкстры ищет кратчайшие пути во взвешенном графе без отрицательных рёбер. Он поддерживает массив расстояний и структуру данных (обычно очередь с приоритетами), которая всегда выбирает вершину с минимальной текущей оценкой расстояния. После выбора вершины её расстояние считается финальным, и происходит релаксация всех выходящих рёбер.

Почему он не работает с отрицательными весами:
- Если ребро имеет отрицательный вес, то после "финализации" расстояния до вершины может появиться путь короче, что нарушает ключевое свойство алгоритма — **локальная оптимальность становится недействительной**, и алгоритм даёт неверный результат.

---

## 5. Топологическая сортировка: определение, применимость и пример

Топологическая сортировка — это упорядочивание вершин ориентированного графа так, что все рёбра направлены слева направо (из ранних вершин в поздние). Она применима **только к DAG (ориентированным ацикличным графам)**. Если граф содержит цикл, корректного топологического порядка не существует.

Примеры задач:
- порядок выполнения задач с зависимостями;
- компиляция модулей (какие модули должны быть собраны раньше);
- планирование курсов: курс B нельзя пройти до курса A;
- построение порядка вычисления формул.


