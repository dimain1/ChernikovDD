# Отчет по лабораторной работе 8

# Жадные алгоритмы

**Дата:** 2025-11-06
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы

Изучить метод проектирования алгоритмов, известный как "жадный алгоритм". Освоить принцип принятия локально оптимальных решений на каждом шаге и понять условия, при которых этот подход приводит к глобально оптимальному решению. Получить практические навыки реализации жадных алгоритмов для решения классических задач, анализа их корректности и оценки эффективности.

## Практическая часть

### Выполненные задачи

- [ ] Реализовать классические жадные алгоритмы.
- [ ] Проанализировать их корректность (доказать или объяснить, почему жадный выбор приводит к оптимальному решению).
- [ ] Провести сравнительный анализ эффективности жадного подхода и других методов (например, полного перебора для маленьких входных данных).
- [ ] Решить практические задачи с применением жадного подхода.

### Ключевые фрагменты кода

```PYTHON
# greedy_algorithms.py

import heapq


def generate_intervals(n, start_range=0, end_range=1000):
    """
    Генерирует список случайных интервалов.

    Args:
        n: количество интервалов
        start_range: минимальное значение начала интервала
        end_range: максимальное значение конца интервала

    Returns:
        intervals: список кортежей (start, end)
    """
    import random

    intervals = []
    for _ in range(n):
        start = random.randint(start_range, end_range - 1)
        end = random.randint(start + 1, end_range)
        intervals.append((start, end))

    return intervals


def interval_scheduling(intervals):
    """
    Возвращает максимальное количество непересекающихся интервалов.

    Args:
        intervals: список кортежей (start, end)

    Returns:
        selected: список непересекающихся интервалов
    """
    # Сортируем интервалы по времени окончания
    intervals.sort(key=lambda x: x[1])

    selected = []
    last_end = float('-inf')

    for start, end in intervals:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected
    # Временная сложность: O(n log n) из-за сортировки


def generate_items(n, value_range=(10, 100), weight_range=(1, 50)):
    """
    Генерирует список случайных предметов.

    Args:
        n: количество предметов
        value_range: кортеж (min_value, max_value)
        weight_range: кортеж (min_weight, max_weight)

    Returns:
        items: список кортежей (value, weight)
    """
    import random

    items = []
    for _ in range(n):
        value = random.randint(*value_range)
        weight = random.randint(*weight_range)
        items.append((value, weight))

    return items


def fractional_knapsack(items, capacity):
    """
    Возвращает максимальную суммарную стоимость для данного объема рюкзака.

    Args:
        items: список кортежей (value, weight)
        capacity: максимальный вес рюкзака

    Returns:
        total_value: максимальная суммарная стоимость
    """
    # Сортируем предметы по убыванию удельной стоимости (value / weight)
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0  # суммарная стоимость
    for value, weight in items:
        if capacity == 0:
            break

        if weight <= capacity:
            # Берем весь предмет
            total_value += value
            capacity -= weight
        else:
            # Берем часть предмета
            fraction = capacity / weight
            total_value += value * fraction
            capacity = 0  # рюкзак заполнен

    return total_value
    # Временная сложность: O(n log n) из-за сортировки


def generate_text(length):
    """
    Генерирует случайный текст заданной длины.

    Args:
        length: длина текста

    Returns:
        text: сгенерированная строка
    """
    import random
    import string

    characters = string.ascii_uppercase  # заглавные буквы A-Z
    text = ''.join(random.choice(characters) for _ in range(length))
    return text


def generate_frequencies(text):
    """
    Генерирует частоты символов в тексте.

    Args:
        text: входная строка

    Returns:
        frequencies: словарь {символ: частота}
    """
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies


class Node:
    def __init__(self, char, freq):
        self.char = char      # символ
        self.freq = freq      # частота
        self.left = None
        self.right = None

    # для корректной работы heapq
    def __lt__(self, other):
        return self.freq < other.freq


def huffman_coding(frequencies):
    """
    Строит коды Хаффмана для заданных частот символов.

    Args: 
        frequencies: словарь {символ: частота}
    Returns:
        codes: словарь {символ: код}
    """
    # создаем очередь с приоритетом (минимальная куча)
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    # пока в куче больше одного элемента — объединяем два наименьших
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    # в конце в куче останется одно дерево
    root = heap[0]
    codes = {}

    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(root, "")

    return codes
    # Временная сложность: O(n log n) из-за операций с кучей


def build_tree(codes):
    tree = {}
    for char, code in codes.items():
        node = tree
        for bit in code:
            if bit not in node:
                node[bit] = {}
            node = node[bit]
        node['char'] = char
    return tree


def print_tree(node, prefix=''):
    for key, child in node.items():
        if key == 'char':
            print(f"{prefix}: {child}")
        else:
            print(f"{prefix}{key}")
            print_tree(child, prefix + '  ')

```

```PYTHON
# analysis.py

from itertools import combinations
from modules.greedy_algorithms import fractional_knapsack


def greedy_discrete_knapsack(items, capacity):
    """Жадный алгоритм для дискретного рюкзака (0-1), без дробления предметов."""
    items = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    taken_items = []
    for value, weight in items:
        if weight <= capacity:
            total_value += value
            capacity -= weight
            taken_items.append((value, weight))
    return total_value, taken_items


def knapsack_bruteforce(items, capacity):
    """Точный перебор для дискретного (0-1) рюкзака."""
    n = len(items)
    best_value = 0
    best_combo = []
    for r in range(1, n + 1):
        for combo in combinations(items, r):
            total_weight = sum(w for _, w in combo)
            total_value = sum(v for v, _ in combo)
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_combo = combo
    return best_value, best_combo


def analysis():
    """
    Анализ и сравнение жадных алгоритмов
    и точного перебора для задачи о рюкзаке.
    1. Жадный алгоритм для непрерывного рюкзака (fractional knapsack).
    2. Жадный алгоритм для дискретного рюкзака (0-1 knapsack).
    3. Точный перебор для дискретного рюкзака (0-1 knapsack).
    """
    # Пример данных
    items = [(60, 10), (100, 20), (120, 30)]  # (стоимость, вес)
    capacity = 50

    # Алгоритмы
    frac_value = fractional_knapsack(items, capacity)
    greedy_value, greedy_combo = greedy_discrete_knapsack(items, capacity)
    brute_value, brute_combo = knapsack_bruteforce(items, capacity)

    # Вывод
    print("Рюкзак емкостью:", capacity)
    print("Предметы (стоимость, вес):", items)
    print("Жадный алгоритм (непрерывный рюкзак):", frac_value)
    print("Жадный алгоритм (дискретный 0-1 рюкзак):", greedy_value,
          greedy_combo)
    print("Точный перебор (дискретный 0-1 рюкзак):", brute_value, brute_combo)

```

```PYTHON
# task.py

import sys


def min_coins_greedy(coins, amount):
    """
    Находит минимальное количество монет для выдачи суммы amount
    с помощью жадного алгоритма.

    Args:
        coins (list): Доступные номиналы монет.
        amount (int): Сумма, которую нужно выдать.

    Returns:
        list: Список монет, составляющих сумму amount.
    """
    coins = sorted(coins, reverse=True)  # сортируем по убыванию
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return result


def prim_mst(graph):
    """
    Алгоритм построение минимального остовного дерева алгоритмом прима

    Args:
        graph: матрица смежности, graph[u][v] = вес ребра u-v, 0 если ребра нет

    Returns:
        список ребер MST и их суммарный вес
    """
    V = len(graph)
    selected = [False] * V  # вершины, включённые в MST
    key = [sys.maxsize] * V  # минимальные веса для подключения вершины к MST
    parent = [-1] * V  # родительские вершины в MST

    key[0] = 0  # начинаем с вершины 0

    for _ in range(V):
        # выбираем вершину с минимальным ключом, ещё не включённую в MST
        min_key = sys.maxsize
        u = -1
        for v in range(V):
            if not selected[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        selected[u] = True  # включаем вершину в MST

        # обновляем ключи для смежных вершин
        for v in range(V):
            if graph[u][v] > 0 and not selected[v] and graph[u][v] < key[v]:
                key[v] = graph[u][v]
                parent[v] = u

    # формируем MST
    mst_edges = []
    total_weight = 0
    for v in range(1, V):
        mst_edges.append((parent[v], v, graph[parent[v]][v]))
        total_weight += graph[parent[v]][v]

    return mst_edges, total_weight

```

```PYTHON
# perfomance.analysis.py

import matplotlib.pyplot as plt
import timeit
from modules.greedy_algorithms import (
    huffman_coding, generate_frequencies, generate_text)


def measure_huffman_time(size, repeats=3):
    """
    Измеряет время выполнения алгоритма Хаффмана для текста заданного размера.
    Args:
        size: размер текста
        repeats: количество повторов для усреднения

    Returns:
        среднее время выполнения в миллисекундах
    """
    times = []
    for _ in range(repeats):
        text = generate_text(size)
        frequencies = generate_frequencies(text)
        start = timeit.default_timer()
        huffman_coding(frequencies)
        end = timeit.default_timer()
        times.append(end - start)
    return (sum(times) / repeats) * 1000  # в миллисекунда


def visualization(sizes):
    """
    Визуализация времени выполнения алгоритма Хаффмана
    Args:
        sizes: список размеров для тестирования
    """
    huffman_times = []
    for size in sizes:
        huffman_times.append(measure_huffman_time(size))
    print("Время выполнения алгоритма Хаффмана для разных размеров:")
    print(huffman_times)
    print("")
    plt.plot(sizes, huffman_times, marker='o', color="red", label="huffman")
    plt.xlabel("Количество элементов n")
    plt.ylabel("Время выполнения ms")
    plt.title("Время выполнения алгоритма Хаффмана")
    plt.legend(loc="upper left", title="Метод")
    plt.savefig("./report/Huffman.png", dpi=300, bbox_inches="tight")
    plt.show()

```

```PYTHON
# main.py

from modules.greedy_algorithms import interval_scheduling, generate_intervals
from modules.greedy_algorithms import fractional_knapsack, generate_items
from modules.greedy_algorithms import (huffman_coding, generate_frequencies,
                                       generate_text, build_tree, print_tree)
from modules.analysis import analysis
from modules.task import min_coins_greedy, prim_mst
from modules.perfomance_analysis import visualization

# Пример использования:
intervals = generate_intervals(50)
result = interval_scheduling(intervals)
print("Выбранные интервалы:", result)

print("\n")

# Пример использования:
items = generate_items(10)
capacity = 50

result = fractional_knapsack(items, capacity)
print(f"Максимальная стоимость: {result:.2f}")

print("\n")

# Пример использования:
frequencies = generate_frequencies(generate_text(50))

codes = huffman_coding(frequencies)
print("Коды Хаффмана:")
for char, code in codes.items():
    print(f"{char}: {code}")

tree = build_tree(codes)
print_tree(tree)

print("\n")

# Запуск анализа и сравнения алгоритмов рюкзака
analysis()

print("\n")

# Пример: стандартная система монет (рубли)
coins = [1, 2, 5, 10]
amount = 28

result = min_coins_greedy(coins, amount)
print("Сдача:", result)
print("Количество монет:", len(result))

print("\n")

# Пример графа (матрица смежности)
graph = [
    [0, 2, 0, 6, 0],
    [2, 0, 3, 8, 5],
    [0, 3, 0, 0, 7],
    [6, 8, 0, 0, 9],
    [0, 5, 7, 9, 0]
]

mst_edges, total_weight = prim_mst(graph)
print("Ребра MST:")
for u, v, w in mst_edges:
    print(f"{u} - {v} (вес {w})")
print("Суммарный вес MST:", total_weight)

print("\n")

# Визуализация времени выполнения алгоритма Хаффмана
sizes = [1000, 5000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
visualization(sizes)

```

<image src="./report/Huffman.png" style="display:block; margin: auto;">

```bash
Выбранные интервалы: [(119, 135), (265, 292), (404, 441), (611, 614), (632, 633), (647, 654), (791, 847), (877, 892), (904, 932), (956, 960)]


Максимальная стоимость: 223.04


Коды Хаффмана:
M: 000
U: 001
K: 010
Z: 0110
Y: 0111
N: 1000
C: 1001
X: 101000
P: 101001
G: 10101
D: 1011
R: 110000
H: 110001
W: 110010
J: 110011
E: 1101
I: 11100
O: 11101
T: 111100
Q: 111101
V: 11111
0
  0
    0
      : M
    1
      : U
  1
    0
      : K
    1
      0
        : Z
      1
        : Y
1
  0
    0
      0
        : N
      1
        : C
    1
      0
        0
          0
            : X
          1
            : P
        1
          : G
      1
        : D
  1
    0
      0
        0
          0
            : R
          1
            : H
        1
          0
            : W
          1
            : J
      1
        : E
    1
      0
        0
          : I
        1
          : O
      1
        0
          0
            : T
          1
            : Q
        1
          : V


Рюкзак емкостью: 50
Предметы (стоимость, вес): [(60, 10), (100, 20), (120, 30)]
Жадный алгоритм (непрерывный рюкзак): 240.0
Жадный алгоритм (дискретный 0-1 рюкзак): 160 [(60, 10), (100, 20)]
Точный перебор (дискретный 0-1 рюкзак): 220 ((100, 20), (120, 30))


Сдача: [10, 10, 5, 2, 1]
Количество монет: 5


Ребра MST:
0 - 1 (вес 2)
1 - 2 (вес 3)
0 - 3 (вес 6)
1 - 4 (вес 5)
Суммарный вес MST: 16


Время выполнения алгоритма Хаффмана для разных размеров:
[0.03256666241213679, 0.032966655756657325, 0.03390000589812795, 0.04913331940770149, 0.043100008042529225, 0.048199998370061316, 0.04673333023674786]


Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12

```

## **Для каждого алгоритма указать его временную сложность и объяснить, почему жадный выбор корректен**
| Алгоритм | Временная сложность | Обоснование корректности жадного выбора |
|-----------|----------------------|------------------------------------------|
| **Алгоритм Хаффмана (Huffman Coding)** | `O(n log n)` | На каждом шаге объединяются два узла с наименьшими частотами. Это минимизирует рост общей длины кодов. Любое другое объединение привело бы к большей суммарной длине. Жадный выбор корректен. |
| **Непрерывный рюкзак (Fractional Knapsack)** | `O(n log n)` | Предметы сортируются по убыванию удельной стоимости (ценность/вес). Так как можно брать дробные части, локальный выбор предмета с максимальной удельной ценностью всегда ведёт к глобальному максимуму стоимости. |
| **Задача о выборе заявок (Interval Scheduling)** | `O(n log n)` | Интервалы сортируются по времени окончания, и выбирается первый непересекающийся. Замена любого интервала, начинающегося позже, на более ранний по окончанию не уменьшает количество выбранных интервалов. Поэтому жадный выбор — оптимален. |

## **Анализ корректности:**

### Алгоритм Хаффмана (Huffman Coding)
Жадная стратегия заключается в объединении двух символов с наименьшими частотами на каждом шаге.  
Это минимизирует увеличение общей длины кодов, потому что редко встречающиеся символы получают более длинные коды, не влияя на частые символы.  
Такой выбор локально оптимален на каждом этапе и приводит к глобально оптимальному префиксному коду.

---

### Непрерывный рюкзак (Fractional Knapsack)
Жадная стратегия состоит в том, чтобы сначала брать предметы с наибольшей удельной стоимостью (ценность/вес).  
Поскольку можно брать дробные части предметов, такой выбор всегда обеспечивает максимальный прирост стоимости на единицу веса.  
Следовательно, последовательное добавление наиболее «выгодных» предметов приводит к оптимальному результату.

---

### Задача о выборе заявок (Interval Scheduling)
Жадная стратегия — выбирать интервалы, которые заканчиваются раньше всех и не пересекаются с уже выбранными.  
Это позволяет освободить как можно больше времени для последующих заявок.  
Так как любой другой выбор не увеличит число совместимых интервалов, жадная стратегия приводит к оптимальному решению.

## Сравнение эффективности жадных алгоритмов с наивными реализациями

| Алгоритм | Жадный подход | Наивная/переборная реализация | Временная сложность | Комментарий |
|-----------|---------------|-------------------------------|-------------------|-------------|
| **Задача о выборе заявок (Interval Scheduling)** | Сортировка по времени окончания + выбор непересекающихся интервалов | Перебор всех подмножеств интервалов | O(n log n) | Жадный алгоритм всегда даёт оптимальное решение. Перебор — O(2^n), сильно медленнее при больших n. |
| **Непрерывный рюкзак (Fractional Knapsack)** | Сортировка по удельной стоимости + добавление максимально возможного предмета | Перебор всех комбинаций предметов | O(n log n) | Жадный подход оптимален только для дробного рюкзака. Перебор для дискретного рюкзака (0-1) имеет сложность O(2^n). |
| **Алгоритм Хаффмана** | Построение минимальной кучи, объединение двух узлов с минимальной частотой | Перебор всех возможных деревьев (непрактично) | O(n log n) | Жадный выбор минимальных частот гарантирует оптимальный префиксный код. Полный перебор для больших n невозможен. |
| **Задача сдачи монет (стандартная система)** | Всегда брать максимальную доступную монету | Перебор всех комбинаций монет для минимизации их числа | O(n) | Работает корректно только для канонических систем монет. Перебор всегда даёт оптимальное решение, но сильно медленнее. |
| **Минимальное остовное дерево (Prim)** | На каждом шаге добавляем минимальное ребро, соединяющее MST с остальными вершинами | Проверка всех возможных подмножеств ребер | O(V^2) или O(E log V) с кучей | Жадный подход всегда даёт MST. Перебор всех подмножеств ребер имеет экспоненциальную сложность. |

---

## Ограничения жадного подхода

| Ограничение | Пояснение | Пример |
|-------------|-----------|--------|
| Локальная оптимальность не всегда ведёт к глобальной | Жадный выбор делает оптимальное локальное решение, но это не гарантирует глобальное | Дискретный рюкзак 0-1: жадный алгоритм по удельной стоимости может пропустить оптимальную комбинацию предметов |
| Требуется каноническая или «правильная» структура данных | Для корректной работы жадного алгоритма нужна определённая система весов/монет | Сдача монет: для системы [1, 3, 4] жадный подход может не дать минимальное количество монет |
| Не применим для всех задач оптимизации | Некоторые задачи требуют глобального анализа или динамического программирования | Задача коммивояжёра, где жадный выбор ближайшего города не гарантирует минимальный путь |
| Чувствителен к сортировке/критерию выбора | Ошибочный критерий может привести к неоптимальному решению | Рюкзак: если сортировать предметы не по удельной стоимости, а по весу, результат не будет оптимальным |


## Ответы на контрольные вопросы

### 1. Основная идея жадных алгоритмов

Жадный алгоритм принимает решения **шаг за шагом**, на каждом шаге выбирая **локально оптимальный вариант**, который кажется наилучшим в данный момент.  
Цель состоит в том, чтобы комбинация этих локальных оптимумов привела к **глобально оптимальному решению**.  
Жадные алгоритмы эффективны, когда локальный оптимум гарантирует глобальный.

---

### 2. Жадный алгоритм для задачи о выборе заявок (Interval Scheduling)

Жадная стратегия выбирает **интервалы с наименьшим временем окончания**, которые не пересекаются с уже выбранными.  
Почему это работает:  
- Выбирая рано заканчивающийся интервал, мы оставляем **максимально возможное пространство для последующих интервалов**.  
- Любой другой выбор, начинающийся позже, либо пересекается с текущим, либо оставляет меньше места для будущих интервалов.  
Таким образом, локальный оптимум (раннее окончание) гарантирует **максимальное количество непересекающихся интервалов**.

---

### 3. Примеры задач с оптимальным и не оптимальным применением жадного алгоритма

| Задача | Жадный алгоритм дает оптимальное решение? | Комментарий |
|--------|-----------------------------------------|-------------|
| Interval Scheduling (выбор заявок) |  Да | Выбор по раннему окончанию всегда оптимален |
| Fractional Knapsack (непрерывный рюкзак) |  Да | Можно брать дробные части предметов |
| 0-1 Knapsack (дискретный рюкзак) |  Нет | Жадный выбор по удельной стоимости может пропустить оптимальную комбинацию предметов |
| Coin Change для нестандартных монет [1,3,4] |  Нет | Жадный выбор наибольшей монеты не всегда минимизирует количество монет |

---

### 4. Разница между непрерывной (дробной) и дискретной (0-1) задачами о рюкзаке

- **Непрерывный рюкзак (Fractional Knapsack):** можно брать **любую часть предмета**, пропорционально его весу.  
  - Жадный алгоритм по удельной стоимости (value/weight) **всегда оптимален**.  

- **Дискретный рюкзак (0-1 Knapsack):** каждый предмет можно взять **либо целиком, либо не брать**.  
  - Жадный подход **не гарантирует оптимального решения**, нужно использовать динамическое программирование или перебор.  

| Характеристика | Непрерывный рюкзак | Дискретный рюкзак |
|----------------|------------------|-----------------|
| Возможность дробления предметов |  Да |  Нет |
| Оптимальность жадного алгоритма |  Да |  Нет |
| Сложность точного решения | O(n log n) | O(2^n) перебор / O(nW) динамика |
| Используемый критерий | Удельная стоимость (value/weight) | Обычно динамика или перебор |

---

### 5. Жадный алгоритм построения кода Хаффмана и его оптимальность

**Алгоритм Хаффмана:**
1. Для каждого символа создаём узел с его частотой.  
2. Формируем **минимальную кучу** по частотам.  
3. Пока в куче больше одного узла:  
   - Извлекаем два узла с наименьшими частотами.  
   - Создаём новый узел с суммарной частотой и присоединяем два узла как дочерние.  
   - Добавляем новый узел обратно в кучу.  
4. После окончания остаётся одно дерево, из которого строим коды: левый путь = `0`, правый путь = `1`.

**Оптимальность:**
- На каждом шаге объединяются **символы с минимальными частотами**, что минимизирует суммарную длину кодов.  
- Жадный выбор минимальных частот гарантирует **минимальную среднюю длину префиксного кода**, что и требуется для эффективной компрессии.