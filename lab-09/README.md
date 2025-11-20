# Отчет по лабораторной работе 9

# Динамическое программирование

**Дата:** 2025-11-06
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы

Изучить метод динамического программирования (ДП) как мощный инструмент для решения сложных задач путём их разбиения на перекрывающиеся подзадачи. Освоить два основных подхода к реализации ДП: нисходящий (с мемоизацией) и восходящий (с заполнением таблицы). Получить практические навыки выявления оптимальной подструктуры задач, построения таблиц ДП и анализа временной и пространственной сложности алгоритмов.

## Практическая часть

### Выполненные задачи

- [ ] Реализовать классические алгоритмы динамического программирования.
- [ ] Реализовать оба подхода (нисходящий и восходящий) для решения задач.
- [ ] Провести сравнительный анализ эффективности двух подходов.
- [ ] Проанализировать временную и пространственную сложность алгоритмов.
- [ ] Решить практические задачи с применением ДП.

### Ключевые фрагменты кода

```PYTHON
# dynamic_programming.py

def fib_naive(n):
    """
    Вычисление n-го числа Фибоначчи с помощью наивной рекурсии.
    F(n) = F(n-1) + F(n-2)

    Args:
        n (int): Позиция числа Фибоначчи для вычисления.
    Returns:
        int: n-е число Фибоначчи.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

#   Временная сложность: O(2^n)
#   Пространственная сложность: O(n) (глубина рекурсии)


def fib_memo(n, memo=None):
    """
    Рекурсивное вычисление n-го числа Фибоначчи с мемоизацией (топ-даун).
    Args:
        n: Позиция числа Фибоначчи для вычисления.
        memo: Словарь для хранения уже вычисленных значений.
    Returns:
        int: n-е число Фибоначчи.
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

#   Временная сложность: O(n)
#   Пространственная сложность: O(n) (для мемоизации и рекурсии)


def fib_tabulation(n):
    """
    Итеративное табличное решение (боттом-ап).
    Args:
        n: Позиция числа Фибоначчи для вычисления.
    Returns:
        int: n-е число Фибоначчи.
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

#   Временная сложность: O(n)
#   Пространственная сложность: O(n) (для таблицы)


def knapsack_01(weights, values, capacity):
    """
    Вычисляет максимальную стоимость, которую можно унести
    в рюкзаке емкостью capacity с помощью
    динамического программирования (боттом-ап).
    Args:
        weights: список весов предметов
        values: список стоимостей предметов
        capacity: максимальная емкость рюкзака
    Returns:
        int: максимальная стоимость, которую можно унести
    """
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Заполнение таблицы
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]],
                               dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


# Временная сложность: O(n * capacity)
# Пространственная сложность: O(n * capacity)

def knapsack_01_with_items(weights, values, capacity):
    """
    Вычисляет максимальную стоимость и выбранные предметы, которые можно унести
    в рюкзаке емкостью capacity с
    помощью динамического программирования (боттом-ап).
    Args:
        weights: список весов предметов
        values: список стоимостей предметов
        capacity: максимальная емкость рюкзака
    Returns:
        tuple: (максимальная стоимость, список выбранных предметов)
    """
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Заполнение таблицы
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]],
                               dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Восстановление выбранных предметов
    w = capacity
    items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append((values[i - 1], weights[i - 1]))  # индекс предмета
            w -= weights[i - 1]

    items.reverse()  # чтобы порядок соответствовал исходной последовательности
    return dp[n][capacity], items


def lcs(str1, str2):
    """
    Вычисляет длину наибольшей общей подпоследовательности (LCS)
    двух строк str1 и str2 с помощью динамического программирования (восходящий
    подход).
    Args:
        str1: первая строка
        str2: вторая строка
    Returns:
        int: длина LCS
    """
    n = len(str1)
    m = len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Заполнение таблицы
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]

# Временная сложность: O(n * m)
# Пространственная сложность: O(n * m)


def lcs_with_sequence(str1, str2):
    """
    Вычисляет длину и саму наибольшую общую подпоследователь
    двух строк str1 и str2 с помощью динамического программирования (восходящий
    подход).
    Args:
        str1: первая строка
        str2: вторая строка
    Returns:
        tuple: (длина LCS, сама LCS)
    """
    n = len(str1)
    m = len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Заполнение таблицы
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Восстановление самой LCS
    i, j = n, m
    sequence = []
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            sequence.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[n][m], ''.join(reversed(sequence))


def levenshtein_distance(str1, str2):
    """
    Вычисляет расстояние Левенштейна между двумя строками str1 и str2
    с помощью динамического программирования (восходящий подход).

    dp[i][j] — минимальное количество операций (вставка, удаление, замена),
    чтобы преобразовать первые i символов str1 в первые j символов str2.

    Args:
        str1: первая строка
        str2: вторая строка
    Returns:
        int: расстояние Левенштейна между str1 и str2
    """
    n = len(str1)
    m = len(str2)

    # Создаём таблицу (n+1) x (m+1)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Инициализация: преобразование пустой строки
    for i in range(n + 1):
        dp[i][0] = i  # i удалений
    for j in range(m + 1):
        dp[0][j] = j  # j вставок

    # Заполняем таблицу
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0  # символы совпадают, замена не нужна
            else:
                cost = 1  # символы разные, потребуется замена

            dp[i][j] = min(
                dp[i - 1][j] + 1,      # удаление
                dp[i][j - 1] + 1,      # вставка
                dp[i - 1][j - 1] + cost  # замена
            )

    return dp[n][m]


# Временная сложность: O(n * m)
# Пространственная сложность: O(n * m)


def fib_tabulation_with_print(n):
    """
    Итеративное табличное решение (боттом-ап).
    Печатает таблицу вычислений на каждом шаге.
    Args:
        n: Позиция числа Фибоначчи для вычисления.
    Returns:
        int: n-е число Фибоначчи.
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print_fib_table(dp)
    return dp[n]


def print_fib_table(dp):
    """
    Печатает текущую таблицу вычислений Фибоначчи.

    Args:
        dp: список с вычисленными значениями Фибоначчи.
    """
    print("i:", end="  ")
    for i in range(len(dp)):
        print(i, end="  ")
    print("\nF(i):", end="  ")
    for val in dp:
        print(val, end="  ")
    print("\n")

def knapsack_1d(weights, values, capacity):
    """
    Оптимизированная версия 0/1 рюкзака.
    Используется один массив dp[w].

    dp[w] — максимальная стоимость при вместимости w.

    Время:  O(n * W)
    Память: O(W)
    """
    n = len(values)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):  # обратный проход
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

    return dp[capacity]
```

```PYTHON
# comparison.py

import timeit
import tracemalloc
import matplotlib.pyplot as plt
from modules.dynamic_programming import fib_memo, fib_tabulation
from modules.dynamic_programming import knapsack_01_with_items


def measure_performance(func, n_values):
    """
    Измеряет время и память для функции func
    при различных значениях n.
    Args:
        func: функция для измерения
        n_values: список значений n для измерения
    Returns:
        tuple: (список времен, список потребляемой памяти)
    """
    times = []
    memories = []

    for n in n_values:
        tracemalloc.start()
        start_time = timeit.default_timer()
        func(n)

        end_time = timeit.default_timer()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append((end_time - start_time) * 1000)
        memories.append(peak / 1024)  # в КБ

    return times, memories


def visualization(sizes):
    """
    Визуализация сравнения
    временной и пространственной сложности
    алгоритмов вычисления чисел Фибоначчи:
    1. С мемоизацией (top-down).
    2. С табуляцией (bottom-up).
    Args:
        sizes: список значений n для анализа
    """

    memo_times, memo_mem = measure_performance(fib_memo, sizes)
    bottom_times, bottom_mem = measure_performance(fib_tabulation, sizes)

    # --- Построение графиков ---

    print("Время выполнения (Top-Down):", memo_times)
    print("Время выполнения (Bottom-Up):", bottom_times)
    plt.figure(figsize=(12, 5))

    # Время
    plt.subplot(1, 2, 1)
    plt.plot(sizes, memo_times, label='Top-Down (Memoization)', marker='o')
    plt.plot(sizes, bottom_times, label='Bottom-Up (Tabulation)', marker='o')
    plt.title('Время выполнения vs n')
    plt.xlabel('n')
    plt.ylabel('Время (ms)')
    plt.legend()
    plt.grid(True)

    print("Память(Top-Down): ", memo_mem)
    print("Память(Bottom-Up): ", bottom_mem)

    # Память
    plt.subplot(1, 2, 2)
    plt.plot(sizes, memo_mem, label='Top-Down (Memoization)', marker='o')
    plt.plot(sizes, bottom_mem, label='Bottom-Up (Tabulation)', marker='o')
    plt.title('Потребление памяти vs n')
    plt.xlabel('n')
    plt.ylabel('Память (КБ)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('./report/fib_analysis.png')
    plt.show()


def greedy_discrete_knapsack(items, capacity):
    """
    Жадный алгоритм для дискретного рюкзака
    (0-1), без дробления предметов.

    Args:
        items: список кортежей (стоимость, вес) предметов
        capacity: максимальная емкость рюкзака
    Returns:
        tuple: (общая стоимость, список взятых предметов)
    """
    items = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    taken_items = []
    for value, weight in items:
        if weight <= capacity:
            total_value += value
            capacity -= weight
            taken_items.append((value, weight))
    return total_value, taken_items


def analysis():
    """
    Анализ и сравнение жадных алгоритмов
    и динамического программирования для задачи о рюкзаке.
    1. Жадный алгоритм для дискретного рюкзака (0-1 knapsack).
    2. ДП для дискретного рюкзака (0-1 knapsack).
    """
    # Пример данных
    items = [(60, 10), (100, 20), (120, 30)]  # (стоимость, вес)
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    # Алгоритмы
    greedy_value, greedy_combo = greedy_discrete_knapsack(items, capacity)
    dp_value, dp_combo = knapsack_01_with_items(weights, values, capacity)

    # Вывод
    print("Рюкзак емкостью:", capacity)
    print("Предметы (стоимость, вес):", items)
    print("Жадный алгоритм (дискретный 0-1 рюкзак):", greedy_value,
          greedy_combo)
    print("ДП (дискретный 0-1 рюкзак):", dp_value, dp_combo)

```

```PYTHON
# tasks.py

def coin_change(coins, amount):
    """
    Решение задачи размена монет с помощью
    динамического программирования (bottom-up).

    Args:
        coins: список доступных номиналов монет
        amount: сумма, которую нужно разменять
    Returns:
        int: минимальное количество монет, необходимое для размена суммы amount


    """
    # Инициализация dp: dp[i] = минимальное количество монет для суммы i
    # Используем значение amount+1 как "бесконечность"
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # 0 монет для суммы 0

    # Заполнение таблицы
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] <= amount else -1


def lis(sequence):
    """
    Наибольшая возрастающая подпоследовательность (LIS) с DP.

    Args:
        sequence: входная последовательность чисел

    Returns:
        tuple: (длина LIS, сама LIS)
    """
    n = len(sequence)
    if n == 0:
        return 0, []

    # dp[i] — длина LIS, заканчивающейся на элементе i
    dp = [1] * n
    # prev[i] — индекс предыдущего элемента в LIS для восстановления
    prev = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if sequence[j] < sequence[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # Находим индекс конца максимальной LIS
    max_len = max(dp)
    index = dp.index(max_len)

    # Восстанавливаем саму последовательность
    lis_seq = []
    while index != -1:
        lis_seq.append(sequence[index])
        index = prev[index]

    lis_seq.reverse()  # переворачиваем, чтобы получить правильный порядок

    return max_len, lis_seq

```

```PYTHON
# perfomance_analysis.py

import tracemalloc
import timeit
import random
from modules.dynamic_programming import (
    knapsack_01, fib_tabulation, lcs, levenshtein_distance)
import matplotlib.pyplot as plt


# --- knapsack ---

def measure_performance(func, weights, values, capacity):
    """
    Измеряет время и память для функции func
    при заданных весах, значениях и емкости рюкзака.
    Args:
        func: функция для измерения
        weights: список весов предметов
        values: список стоимостей предметов
        capacity: максимальная емкость рюкзака
    Returns:
        tuple: (время выполнения в мс, потребляемая память в КБ)
    """
    time = []
    memory = []

    tracemalloc.start()
    start_time = timeit.default_timer()

    func(weights, values, capacity)

    end_time = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time = ((end_time - start_time) * 1000)
    memory = (peak / 1024)  # в КБ

    return time, memory


def generate_items(capacitiy):
    """
    Генерирует случайные веса и стоимости предметов
    для задачи рюкзака.
    Args:
        capacitiy: максимальная емкость рюкзака
    Returns:
        tuple: (список весов, список стоимостей)
    """
    weights = []
    values = []
    for i in range(capacitiy * 10):
        weights.append(random.randint(0, capacitiy // 10))
        values.append(random.randint(0, capacitiy * 10))
    return weights, values


def visualization_knapsack(capacities):
    """
    Визуализация анализа производительности
    алгоритма рюкзака 0/1
    Args:
        capacities: список емкостей рюкзака для анализа
    """
    knap_time = []
    knap_mem = []
    for i in capacities:
        weights, values = generate_items(i)
        knap_time_i, knap_mem_i = measure_performance(
            knapsack_01, weights, values, i)
        knap_time.append(knap_time_i)
        knap_mem.append(knap_mem_i)

    plt.subplot(1, 2, 1)
    plt.plot(capacities, knap_time, label='Knapsack 0/1', marker='o')
    plt.title('Время выполнения Knapsack 0/1 vs Capacity')
    plt.xlabel('Capacity')
    plt.ylabel('Время (ms)')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(capacities, knap_mem, label='Knapsack 0/1', marker='o')
    plt.title('Потребление памяти Knapsack 0/1 vs Capacity')
    plt.xlabel('Capacity')
    plt.ylabel('Память (КБ)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('./report/knapsack_analysis.png')
    plt.show()

# --- fib ---


def visualization_fib(n_values):
    """
    Визуализация анализа производительности
    алгоритма вычисления чисел Фибоначчи с табуляцией.
    Args:
        n_values: список значений n для анализа
    """
    time = []
    for n in n_values:
        start_time = timeit.default_timer()
        fib_tabulation(n)
        end_time = timeit.default_timer()
        time.append((end_time - start_time) * 1000)

    plt.plot(n_values, time, label='Fib Tabulation', marker='o')
    plt.title('Время выполнения Fibonacci Tabulation vs n')
    plt.xlabel('n')
    plt.ylabel('Время (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./report/fib_tabulation_analysis.png')
    plt.show()

# --- lcs ---


def generate_strings(length):
    """
    Генерирует две случайные строки заданной длины.
    Args:
        length: длина строк
    Returns:
        tuple: (строка 1, строка 2)
    """
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str1 = ''.join(random.choice(letters) for _ in range(length))
    str2 = ''.join(random.choice(letters) for _ in range(length))
    return str1, str2


def visualization_lcs(lengths):
    """
    Визуализация анализа производительности
    алгоритма нахождения наибольшей общей подпоследовательности (LCS).
    Args:
        lengths: список длин строк для анализа
    """
    lcs_time = []
    for length in lengths:
        str1, str2 = generate_strings(length)
        start_time = timeit.default_timer()
        lcs(str1, str2)
        end_time = timeit.default_timer()
        lcs_time.append((end_time - start_time) * 1000)

    plt.plot(lengths, lcs_time, label='LCS', marker='o')
    plt.title('Время выполнения LCS vs Length')
    plt.xlabel('Length')
    plt.ylabel('Время (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./report/lcs_analysis.png')
    plt.show()

# --- levenshtein ---


def visualization_levenshtein(lengths):
    """
    Визуализация анализа производительности
    алгоритма вычисления расстояния Левенштейна.
    Args:
        lengths: список длин строк для анализа
    """
    lev_time = []
    for length in lengths:
        str1, str2 = generate_strings(length)
        start_time = timeit.default_timer()
        levenshtein_distance(str1, str2)
        end_time = timeit.default_timer()
        lev_time.append((end_time - start_time) * 1000)

    plt.plot(lengths, lev_time, label='Levenshtein Distance', marker='o')
    plt.title('Время выполнения Levenshtein Distance vs Length')
    plt.xlabel('Length')
    plt.ylabel('Время (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./report/levenshtein_analysis.png')
    plt.show()

```

```PYTHON
# main.py

import sys
from modules.comparison import visualization
from modules.comparison import analysis
from modules.dynamic_programming import (
    lcs_with_sequence, fib_tabulation_with_print)
from modules.tasks import coin_change, lis
from modules.perfomance_analysis import (
    visualization_knapsack, visualization_fib, visualization_lcs,
    visualization_levenshtein)


sys.setrecursionlimit(30000)  # увеличиваем лимит рекурсии для больших n
# можно увеличить до 2000-5000 для наглядности
n_values = list(range(100, 1001, 100))
visualization(n_values)

print("\n")

analysis()

print("\n")


# Пример использования:
length, subseq = lcs_with_sequence("AGGTAB", "GXTXAYB")
print(length)
print(subseq)

print("\n")

# --- Пример использования ---
coins = [1, 2, 5]
amount = 11

min_coins = coin_change(coins, amount)
print(f"Минимальное количество монет для {amount}:", min_coins)

print("\n")

# --- Пример использования ---
seq = [10, 22, 9, 33, 21, 50, 41, 60]
length, subsequence = lis(seq)
print("Длина LIS:", length)            # 5
print("LIS:", subsequence)            # [10, 22, 33, 50, 60]

print("\n")

n_values = [100, 1000, 5000, 10000, 25000]
visualization_fib(n_values)

capasities = list(range(100, 501, 100))
visualization_knapsack(capasities)

lengths = [10, 50, 100, 250, 500, 1000, 2500, 10000]
visualization_lcs(lengths)
visualization_levenshtein(lengths)

fib_tabulation_with_print(10)

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

<image src="./report/fib_analysis.png" style="display:block; margin: auto;">
<image src="./report/fib_tabulation_analysis.png" style="display:block; margin: auto;">
<image src="./report/knapsack_analysis.png" style="display:block; margin: auto;">
<image src="./report/lcs_analysis.png" style="display:block; margin: auto;">
<image src="./report/levenshtein_analysis.png" style="display:block; margin: auto;">

```bash
Время выполнения (Top-Down): [0.09380000119563192, 0.21070000366307795, 0.39619999733986333, 0.7901999997557141, 1.4594000022043474, 2.133599999069702, 3.351600003952626, 5.173100005777087, 7.925500001874752, 9.603400001651607]
Время выполнения (Bottom-Up): [0.053800002206116915, 0.0788000033935532, 0.1655000014579855, 0.2798999994411133, 0.4107999993721023, 0.5413999970187433, 0.6685999978799373, 0.8267000011983328, 1.0605999996187165, 1.378699998895172]
Память(Top-Down):  [9.0703125, 19.3984375, 22.796875, 46.3203125, 51.1015625, 62.09765625, 108.390625, 111.515625, 118.5546875, 133.16796875]
Память(Bottom-Up):  [3.796875, 8.87109375, 14.84375, 21.703125, 29.46875, 38.12109375, 47.6875, 58.16796875, 69.5390625, 81.80859375]


Рюкзак емкостью: 50
Предметы (стоимость, вес): [(60, 10), (100, 20), (120, 30)]
Жадный алгоритм (дискретный 0-1 рюкзак): 160 [(60, 10), (100, 20)]
ДП (дискретный 0-1 рюкзак): 220 [(100, 20), (120, 30)]


4
GTAB


Минимальное количество монет для 11: 3


Длина LIS: 5
LIS: [10, 22, 33, 50, 60]


i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  0  0  0  0  0  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  0  0  0  0  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  0  0  0  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  0  0  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  8  0  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  8  13  0  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  8  13  21  0  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  8  13  21  34  0

i:  0  1  2  3  4  5  6  7  8  9  10
F(i):  0  1  1  2  3  5  8  13  21  34  55


Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12


```

# Сравнение эффективности подходов динамического программирования

## 1. Общая характеристика подходов

| Критерий | Нисходящее ДП (Top-Down, с мемоизацией) | Восходящее ДП (Bottom-Up, табличное) |
|-----------|------------------------------------------|--------------------------------------|
| **Принцип работы** | Рекурсивное вычисление с сохранением уже найденных результатов | Итеративное заполнение таблицы от базовых случаев |
| **Реализация** | Использует рекурсию и словарь/массив для кэша | Использует двойные циклы и массив для хранения |
| **Выделение памяти** | Динамическое — хранит только нужные подзадачи | Фиксированное — таблица для всех возможных подзадач |
| **Переполнение стека** | Возможна при глубокой рекурсии | Исключено |
| **Порядок вычислений** | Только по мере необходимости | Все подзадачи вычисляются заранее |
| **Удобство реализации** | Простая и наглядная логика | Требует знания порядка заполнения таблицы |
| **Эффективность при редких подзадачах** | Лучше, так как вычисляет только нужные состояния | Хуже — вычисляет все, даже неиспользуемые |
| **Оптимизация по памяти (rolling array)** | Сложнее реализовать | Легко реализуется при известной зависимости только от предыдущих состояний |

---

## 2. Влияние параметров задачи на время и память

| Задача | Время (Top-Down) | Время (Bottom-Up) | Память (Top-Down) | Память (Bottom-Up) | Комментарий |
|--------|------------------|------------------|------------------|------------------|--------------|
| **Фибоначчи (n)** | O(n) — благодаря кэшированию | O(n) | O(n) для кэша | O(n) для таблицы | При большом `n` рекурсия может вызвать переполнение стека |
| **0-1 Рюкзак (n × W)** | O(n×W) (кэш по [i][w]) | O(n×W) | O(n×W), но можно уменьшить до O(W) | O(n×W) или O(W) при оптимизации | Bottom-Up обычно быстрее за счёт отсутствия вызовов функций |
| **LCS (m × n)** | O(m×n) | O(m×n) | O(m×n) | O(m×n), можно сократить до O(min(m,n)) | Bottom-Up проще реализовать и контролировать |
| **Левенштейн (m × n)** | O(m×n) | O(m×n) | O(m×n) | O(m×n), возможно O(min(m,n)) | При больших строках лучше использовать табличный подход |

---

## 3. Итоговое сравнение влияния роста параметров

| Параметр | Влияние на Top-Down | Влияние на Bottom-Up | Общая рекомендация |
|-----------|---------------------|----------------------|---------------------|
| **Рост размерности входных данных** | Увеличивает глубину рекурсии и объём кэша | Увеличивает размер таблицы линейно/квадратично | Bottom-Up предпочтителен при больших данных |
| **Редкие подзадачи (разреженное пространство)** | Вычисляет только нужные состояния → эффективнее | Все состояния обрабатываются → избыточно | Top-Down эффективнее |
| **Ограниченная память** | Может использовать меньше памяти при редких вызовах | Можно оптимизировать до O(n) или O(1) при «скользящем окне» | Bottom-Up при оптимизации |
| **Необходимость трассировки пути (например, LCS)** | Требует хранения кэша и стековых вызовов | Можно хранить таблицу направлений | Bottom-Up удобнее для восстановления пути |

---

### **Вывод:**
- **Top-Down** лучше для простоты кода, работы с редкими подзадачами и быстрой прототипизации.  
- **Bottom-Up** — более предсказуем и стабилен по времени и памяти, подходит для больших входных данных и промышленного использования.

# Ответы на контрольные вопросы

---

### 1. Какие два основных свойства задачи указывают на то, что для ее решения можно применить динамическое программирование?

Для применения динамического программирования задача должна обладать **двумя ключевыми свойствами**:

1. **Оптимальная подструктура** — решение исходной задачи можно выразить через оптимальные решения её подзадач.  
   Например, кратчайший путь из A в C через B можно найти как сумму кратчайших путей A→B и B→C. Если подзадачи решаются независимо и их решения можно комбинировать для получения оптимального результата, это свойство выполняется.

2. **Перекрывающиеся подзадачи** — при решении задачи возникают одинаковые подзадачи, которые повторяются многократно.  
   Например, при вычислении чисел Фибоначчи `F(n)` требуется `F(n-1)` и `F(n-2)`, но `F(n-2)` потом вычисляется ещё раз при расчёте `F(n-1)`. Вместо многократных пересчётов их можно сохранять и переиспользовать.

---

### 2. В чем разница между нисходящим (top-down) и восходящим (bottom-up) подходами в динамическом программировании?

- **Нисходящий подход (Top-Down)**:
  - Реализуется через **рекурсию с мемоизацией**.
  - Сначала решается основная задача, рекурсивно вызывая подзадачи.
  - Результаты подзадач сохраняются (кэшируются), чтобы не пересчитывать их заново.
  - Преимущество — простая и понятная логика, вычисляются только нужные подзадачи.
  - Недостаток — возможны большие затраты памяти под стек вызовов.

- **Восходящий подход (Bottom-Up)**:
  - Решение строится **итеративно**, начиная с самых простых подзадач.
  - Используется таблица (массив), в которой постепенно заполняются значения.
  - Каждое новое значение вычисляется на основе уже известных предыдущих.
  - Преимущество — отсутствие рекурсии и более предсказуемое использование памяти.
  - Недостаток — приходится заполнять всю таблицу, даже если не все подзадачи нужны.

---

### 3. Как задача о рюкзаке 0-1 демонстрирует свойство оптимальной подструктуры?

В задаче о рюкзаке 0-1 требуется выбрать набор предметов с максимальной ценностью, не превышая заданный вес.  
Если обозначить `dp[i][w]` — максимальную ценность при использовании первых `i` предметов и вместимости `w`,  
то решение задачи можно выразить через подзадачи:

- Если предмет `i` **не включается** в рюкзак, то `dp[i][w] = dp[i-1][w]`.
- Если предмет `i` **включается**, то `dp[i][w] = value[i] + dp[i-1][w - weight[i]]`.

Таким образом, **оптимальное решение задачи для n предметов** строится из **оптимальных решений подзадач** — для меньшего количества предметов и меньшей вместимости. Это и есть свойство оптимальной подструктуры: решение зависит от оптимальных решений меньших подзадач.

---

### 4. Опишите, как строится и заполняется таблица для решения задачи о наибольшей общей подпоследовательности (LCS).

Для двух строк `A` длиной `m` и `B` длиной `n` создаётся таблица `dp[m+1][n+1]`,  
где `dp[i][j]` — длина LCS для первых `i` символов `A` и первых `j` символов `B`.

Шаги заполнения:

1. Инициализация: первая строка и первый столбец заполняются нулями (если одна строка пустая — общая подпоследовательность отсутствует).
2. Проход по всем `i` и `j`:
   - Если `A[i-1] == B[j-1]`, то `dp[i][j] = dp[i-1][j-1] + 1`.
   - Иначе `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.
3. После завершения обхода таблицы значение `dp[m][n]` содержит длину наибольшей общей подпоследовательности.

Для восстановления самой подпоследовательности таблицу просматривают в обратном порядке: если символы совпадают — включают их в результат.

---

### 5. Как с помощью динамического программирования можно уменьшить сложность вычисления чисел Фибоначчи с экспоненциальной до линейной или даже до O(log n)?

Наивный рекурсивный алгоритм вычисляет `F(n)` экспоненциально — `O(2^n)`,  
поскольку многократно пересчитывает одни и те же значения.

- **С мемоизацией (Top-Down)** или **табличным методом (Bottom-Up)**:
  - Каждый элемент `F(i)` вычисляется один раз и сохраняется.
  - Каждый последующий результат строится по формуле `F(i) = F(i-1) + F(i-2)`.
  - Таким образом, общая сложность снижается до **O(n)** по времени и **O(n)** по памяти (или O(1), если хранить только два последних числа).

- **С помощью быстрого возведения матрицы Фибоначчи**:
  - Используется матричное представление:  
    ```
    |F(n+1) F(n)  | = |1 1|^n
    |F(n)   F(n-1)|   |1 0|
    ```
  - Возведение матрицы в степень выполняется методом «разделяй и властвуй» за **O(log n)**.
  - Это даёт ещё более эффективный способ вычисления чисел Фибоначчи с логарифмической сложностью.
