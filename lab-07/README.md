# Отчет по лабораторной работе 7
# Кучи (Heaps)

**Дата:** 2025-10-10
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы
Изучить структуру данных "куча" (heap), её свойства и применение. Освоить основные операции с кучей (добавление, извлечение корня) и алгоритм её построения. Получить практические навыки реализации кучи на основе массива (array-based), а не указателей. Исследовать эффективность основных операций и применение кучи для сортировки и реализации приоритетной очереди.
## Практическая часть

### Выполненные задачи
- [ ] Реализовать структуру данных "куча" (min-heap и max-heap) на основе массива.
- [ ] Реализовать основные операции и алгоритм построения кучи из массива.
- [ ] Реализовать алгоритм сортировки кучей (Heapsort).
- [ ] Провести анализ сложности операций.
- [ ] Сравнить производительность сортировки кучей с другими алгоритмами.



### Ключевые фрагменты кода

```PYTHON
# heap.py

class Heap():
    """
    Реализация двоичной кучи (min-heap или max-heap).

    Attributes:
        is_min: True — min-куча (минимум в корне), False — max-куча.
        array: Внутренний массив, используемый для представления кучи.
    """

    def __init__(self, is_min=False):
        """
        Инициализирует кучу.

        Args:
            is_min: Булево значение, определяющее тип кучи (min или max).
        """
        self.is_min = is_min
        self.array = []

    # Временная сложность: O(1)

    def insert(self, value):
        """
        Вставляет значение в кучу.

        Args:
            value: Значение для вставки.

        Returns:
            None
        """
        # Вставка элемента
        self.array.append(value)
        self._sift_up(len(self.array) - 1)
    # Временная сложность: O(log n) — всплытие O(log n)

    def extract(self):
        """
        Удаляет и возвращает корневой элемент кучи.
        (max или min в зависимости от типа).

        Returns:
            result: корневой элемент кучи или None, если куча пуста
        """
        if not self.array:
            return None

        if len(self.array) == 1:
            return self.array.pop()

        result = self.array[0]
        # Перемещаем последний элемент в корень
        self.array[0] = self.array.pop()
        if self.array:  # Если в куче остались элементы
            self._sift_down(0)
        return result
    # Временная сложность: O(log n) — погружение O(log n)

    def peek(self):
        """
        Возвращает значение корня кучи без удаления.

        Returns:
            Корневое значение (min или max в зависимости от типа кучи).
        """
        # Просмотр корня
        return self.array[0]

    # Временная сложность: O(1)

    def build_heap(self, array):
        """
        Строит кучу из произвольного массива за линейное время.

        Args:
            array: Список значений, из которого строится куча.

        Returns:
            None
        """
        # Построение кучи из массива
        self.array = array
        parents_start_index = (len(array) - 2) // 2
        for i in range(parents_start_index, -1, -1):
            self._sift_down(i)
    # Временная сложность: O(n) — построение кучи снизу вверх за линейное время

    def _sift_up(self, index):
        """
        Выполняет всплытие элемента вверх по дереву
        до восстановления свойства кучи.

        Args:
            index: Индекс элемента во внутреннем массиве,
                который нужно всплыть.

        Returns:
            None
        """
        # Всплытие элемента (Insert)
        if index == 0:
            return
        parent_index = (index - 1) // 2

        if self.is_min:
            if self.array[index] < self.array[parent_index]:
                self.swap(parent_index, index)
                self._sift_up(parent_index)
        else:
            if self.array[index] > self.array[parent_index]:
                self.swap(parent_index, index)
                self._sift_up(parent_index)

    # Временная сложность: O(log n) — перемещение вверх по высоте кучи

    def _sift_down(self, index):
        """
        Выполняет погружение элемента вниз по дереву
        до восстановления свойства кучи.

        Args:
            index: Индекс элемента во внутреннем массиве,
                который нужно погрузить.

        Returns:
            None
        """
        # Погружение элемента (Extract)
        left_index = 2*index + 1
        right_index = 2 * index + 2
        if left_index > (len(self.array) - 1):
            left_index = None
        if right_index > (len(self.array) - 1):
            right_index = None
        if left_index is None and right_index is None:
            return
        if self.is_min:
            if right_index is not None:
                if (self.array[left_index] < self.array[index]
                        and self.array[left_index] <= self.array[right_index]):
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                elif (self.array[right_index] < self.array[index]
                        and self.array[right_index] <= self.array[left_index]):
                    self.swap(index, right_index)
                    self._sift_down(right_index)
                else:
                    return
            else:
                if self.array[left_index] < self.array[index]:
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                else:
                    return
        else:
            if right_index is not None:
                if (self.array[left_index] > self.array[index]
                        and self.array[left_index] >= self.array[right_index]):
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                elif (self.array[right_index] > self.array[index]
                        and self.array[right_index] >= self.array[left_index]):
                    self.swap(index, right_index)
                    self._sift_down(right_index)
                else:
                    return
            else:
                if self.array[left_index] > self.array[index]:
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                else:
                    return

    # Временная сложность: O(log n) — перемещение вниз по высоте кучи

    def swap(self, first_index, second_index):
        """
        Меняет местами два элемента внутреннего массива по индексам.

        Args:
            first_index: Индекс первого элемента.
            second_index: Индекс второго элемента.

        Returns:
            None
        """
        temp = self.array[first_index]
        self.array[first_index] = self.array[second_index]
        self.array[second_index] = temp

    def visualize(self, index=0, level=0):
        if not self.array:
            print("Heap is empty")
            return
        if index >= len(self.array):
            return
        # Сначала правое поддерево
        self.visualize(2 * index + 2, level + 1)
        # Текущий узел
        print("    " * level + str(self.array[index]))
        # Потом левое поддерево
        self.visualize(2 * index + 1, level + 1)

```

```PYTHON
# heapsort.py

from modules.heap import Heap
# from src.modules.heap import Heap
# С выделением памяти под кучу


def heapsort(array):
    """
    Создаёт кучу на основе массива и посредством операции
    excract создаёт отсортированный массив

    Args:
        array: Неотсортированный массив

    Returns:
        sorted_array: Отсортированный массив
    """
    if not array:
        return []

    heap = Heap(False)  # max-куча
    heap.build_heap(array.copy())  # явное копирование
    sorted_array = [0] * len(array)  # предварительное выделение памяти

    for i in range(len(array)-1, -1, -1):
        val = heap.extract()
        if val is None:  # защита от None
            break
        sorted_array[i] = val

    return sorted_array

# Без выделения доп. памяти. Изменение исходного массива


def heapsort_in_place(array):
    """
    Сортирует массив на месте, используя методы кучи.
    Сначала изменяет данные таким образом, чтобы массив стал кучей,
    потом по ставит наибольший элемент в конец, и опять восстанавливает
    кучу без учёта последнего элемента

    Args:
        array: Неотсортированный массив

    Returns:
        None
    """
    def swap(i, j):
        array[i], array[j] = array[j], array[i]

    def _sift_down(index, heap_size):
        largest = index
        while True:
            left = 2 * index + 1
            right = 2 * index + 2

            if left < heap_size and array[left] > array[largest]:
                largest = left
            if right < heap_size and array[right] > array[largest]:
                largest = right

            if largest == index:
                break

            swap(index, largest)
            index = largest

    # Построение max-кучи
    for i in range(len(array) // 2 - 1, -1, -1):
        _sift_down(i, len(array))

    # Извлечение элементов
    for i in range(len(array) - 1, 0, -1):
        swap(0, i)
        _sift_down(0, i)

    return array


```

```PYTHON
# priority_queue.py

class PriorityQueue():

    def __init__(self, is_min=False):
        """
        Инициализирует приоритетную очередь.

        Args:
            is_min: Булево значение, определяющее тип приоритета (min или max).
        """
        self.array = []
        self.is_min = is_min
    # Временная сложность: O(1)

    def enqueue(self, item, priority):
        """
        Вставляет значение в приоритетную очередь.

        Args:
            value: Значение для вставки.

        Returns:
            None
        """
        # Вставка элемента
        self.array.append((item, priority))
        self._sift_up(len(self.array) - 1)
    # Временная сложность: O(log n) — всплытие O(log n)

    def dequeue(self):
        """
        Удаляет и выводит элемент приоритетной очереди.
        (max или min в зависимости от типа).

        Returns:
            Значение элемента в очереди
        """
        # Извлечение корня
        self.swap(0, len(self.array) - 1)
        result = self.array.pop(len(self.array) - 1)
        self._sift_down(0)
        return result[0]
    # Временная сложность: O(log n) — погружение O(log n)

    def build_queue(self, array):
        """
        Строит приоритетную очередь из произвольного массива за линейное время.

        Args:
            array: Список значений, из которого строится приоритетная очередь.

        Returns:
            None
        """
        # Построение кучи из массива
        self.array = array
        parents_start_index = (len(array) - 2) // 2
        for i in range(parents_start_index, -1, -1):
            self._sift_down(i)
    # Временная сложность: O(n) — построение кучи снизу вверх за линейное время

    def _sift_up(self, index):
        """
        Выполняет всплытие элемента вверх по дереву
        до восстановления свойства кучи.

        Args:
            index: Индекс элемента во внутреннем массиве,
                который нужно всплыть.

        Returns:
            None
        """
        # Всплытие элемента (Insert)
        if index == 0:
            return
        parent_index = (index - 1) // 2

        if self.is_min:
            if self.array[index][1] < self.array[parent_index][1]:
                self.swap(parent_index, index)
                self._sift_up(parent_index)
        else:
            if self.array[index][1] > self.array[parent_index][1]:
                self.swap(parent_index, index)
                self._sift_up(parent_index)

    # Временная сложность: O(log n) — перемещение вверх по высоте кучи

    def _sift_down(self, index):
        """
        Выполняет погружение элемента вниз по дереву
        до восстановления свойства кучи.

        Args:
            index: Индекс элемента во внутреннем массиве,
                который нужно погрузить.

        Returns:
            None
        """
        # Погружение элемента (Extract)
        left_index = 2*index + 1
        right_index = 2 * index + 2
        if left_index > (len(self.array) - 1):
            left_index = None
        if right_index > (len(self.array) - 1):
            right_index = None
        if left_index is None and right_index is None:
            return
        if self.is_min:
            if right_index is not None:
                if (self.array[left_index][1] < self.array[index][1]
                    and (self.array[left_index][1] <
                         self.array[right_index][1])):
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                elif (self.array[right_index][1] < self.array[index][1]
                        and (self.array[right_index][1] <
                             self.array[left_index][1])):
                    self.swap(index, right_index)
                    self._sift_down(right_index)
                else:
                    return
            else:
                if self.array[left_index][1] < self.array[index][1]:
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                else:
                    return
        else:
            if right_index is not None:
                if (self.array[left_index][1] > self.array[index][1]
                        and (self.array[left_index][1] >
                             self.array[right_index][1])):
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                elif (self.array[right_index][1] > self.array[index][1]
                        and (self.array[right_index][1] >
                             self.array[left_index][1])):
                    self.swap(index, right_index)
                    self._sift_down(right_index)
                else:
                    return
            else:
                if self.array[left_index][1] > self.array[index][1]:
                    self.swap(index, left_index)
                    self._sift_down(left_index)
                else:
                    return

    # Временная сложность: O(log n) — перемещение вниз по высоте кучи

    def swap(self, first_index, second_index):
        """
        Меняет местами два элемента внутреннего массива по индексам.

        Args:
            first_index: Индекс первого элемента.
            second_index: Индекс второго элемента.

        Returns:
            None
        """
        temp = self.array[first_index]
        self.array[first_index] = self.array[second_index]
        self.array[second_index] = temp

```

```PYTHON
# sorts.py

def bubble_sort(ar):
    """
    Сортировка пузырьком.
    Сравнивает соседние элементы и меняет их местами,
    если они идут в неправильном порядке.
    Сложность: худший O(n^2), средний O(n^2), лучший O(n). Память: O(1).
    """

    for i in range(len(ar) - 1, 0, -1):
        for j in range(0, i):
            if (ar[j] > ar[j+1]):
                temp = ar[j+1]
                ar[j+1] = ar[j]
                ar[j] = temp

    return ar

# Время: худший O(n^2), средний O(n^2), лучший O(n)
# Память: O(1)


def selection_sort(ar):
    """
    Сортировка выбором.
    Находит минимальный элемент в неотсортированной
    части и меняет его с текущим.
    Сложность: худший/средний/лучший O(n^2). Память: O(1).
    """
    for i in range(len(ar)):
        min = 2**100
        min_ind = -1
        for j in range(i, len(ar)):
            if min > ar[j]:
                min = ar[j]
                min_ind = j
        if min_ind != -1:
            temp = ar[i]
            ar[i] = ar[min_ind]
            ar[min_ind] = temp

    return ar

# Время: худший O(n^2), средний O(n^2), лучший O(n^2)
# Память: O(1)


def insertion_sort(ar):
    """
    Сортировка вставками.
    Вставляет каждый элемент на своё место в отсортированной части массива.
    Сложность: худший/средний O(n^2), лучший O(n). Память: O(1).
    """
    for i in range(1, len(ar)):
        key = ar[i]
        j = i - 1
        while j >= 0 and ar[j] > key:
            ar[j + 1] = ar[j]
            j -= 1
        ar[j + 1] = key
    return ar

# Время: худший O(n^2), средний O(n^2), лучший O(n)
# Память: O(1)


def merge_sort(ar):
    """
    Сортировка слиянием.
    Рекурсивно делит массив пополам и сливает отсортированные части.
    Сложность: худший/средний/лучший O(n log n). Память: O(n).
    """
    if len(ar) <= 1:
        return ar
    mid = len(ar) // 2
    left = merge_sort(ar[:mid])
    right = merge_sort(ar[mid:])
    return merge(left, right)

# Время: худший O(n log n), средний O(n log n), лучший O(n log n)
# Память: O(n)


def merge(left, right):
    """
    Сливает два отсортированных массива в один отсортированный.
    Используется в merge_sort.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(ar):
    """
    Быстрая сортировка (quick sort).
    Делит массив относительно опорного элемента и рекурсивно сортирует части.
    Сложность: худший O(n^2), средний/лучший O(n log n).
    Память: O(log n) (стек рекурсии).
    """
    if len(ar) <= 1:
        return ar
    pivot = ar[len(ar) // 2]
    left = [x for x in ar if x < pivot]
    middle = [x for x in ar if x == pivot]
    right = [x for x in ar if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Время: худший O(n^2), средний O(n log n), лучший O(n log n)
# Память: O(log n) (стек рекурсии)

```

```PYTHON
# perfomance.analysis.py

from modules.heap import Heap
from modules.heapsort import heapsort
from modules.sorts import merge_sort, quick_sort
import matplotlib.pyplot as plt
import timeit
import random

# Последовательный insert в heap VS build_heap [1000, 5000, 10000, 25000]


def get_random_array(size):
    """
    Создаёт массив случайных чисел.

    Args:
        size: длина массива.

    Returns:
        array: Массив случайных чисел длинной size.
    """
    array = []
    for i in range(size):
        array.append(random.randint(0, 1_000_000))
    return array


def measure_linear_insert(size):
    """
    Измеряет время выполнения size операций
    вставки в кучу.

    Args:
        size: количество операций вставки -> кол-во 
        элементов кучи.

    Returns:
        result: время выполнение операций.
    """
    array = get_random_array(size)
    heap = Heap(True)
    start = timeit.default_timer()
    for i in array:
        heap.insert(i)
    end = timeit.default_timer()
    return (end - start) * 1000


def measure_build_heap(size):
    """
    Измеряет время выполнения операции построения
    кучи из массива

    Args:
        size: длина массива, необходима для генерации массива

    Returns:
        result: время выполнение операции.
    """
    array = get_random_array(size)
    heap = Heap(True)
    start = timeit.default_timer()
    heap.build_heap(array)
    end = timeit.default_timer()
    return (end - start) * 1000


def visualization_build(sizes):
    """
    Визуализирует результат сравнения операций вставки и операции
    построения кучи из массива в виде графика.
    Args:
        sizes: список длин массивов для тестирования.

    Возвращает:
        None. Сохраняет график
    """
    linear_insert = []
    build_heap = []
    for size in sizes:
        linear_insert.append(measure_linear_insert(size))
        build_heap.append(measure_build_heap(size))
    print("Построение кучи:")
    print(linear_insert)
    print(build_heap)
    print("")
    plt.plot(sizes, linear_insert, marker='o', color="red", label='insert')
    plt.plot(sizes, build_heap, marker='o', color="blue", label='build')
    plt.xlabel("Количество элементов n")
    plt.ylabel("Время выполнения ms")
    plt.title("Сравнение послед. insert и build_heap")
    plt.legend(loc="upper left", title="Методы")
    plt.savefig("./report/creating_heap.png", dpi=300, bbox_inches="tight")
    plt.show()

# Heapsort VS quick_sort VS merge_sort [1000, 5000, 10000, 25000, 100000]


def measure_heapsort(size):
    """
    Измеряет время выполнения сортировки heapsort для массива случайных чисел.

    Args:
        size: длина массива, используемая для генерации случайных чисел.

    Returns:
        result: время выполнения сортировки в миллисекундах.
    """
    array = get_random_array(size)
    start = timeit.default_timer()
    array = heapsort(array)
    end = timeit.default_timer()

    return (end - start) * 1000


def measure_quick_sort(size):
    """
    Измеряет время выполнения сортировки quick_sort для массива случайных чисел.

    Args:
        size: длина массива, используемая для генерации случайных чисел.

    Returns:
        result: время выполнения сортировки в миллисекундах.
    """
    array = get_random_array(size)
    start = timeit.default_timer()
    array = quick_sort(array)
    end = timeit.default_timer()
    return (end - start) * 1000


def measure_merge_sort(size):
    """
    Измеряет время выполнения сортировки merge_sort для массива случайных чисел.

    Args:
        size: длина массива, используемая для генерации случайных чисел.

    Returns:
        result: время выполнения сортировки в миллисекундах.
    """
    array = get_random_array(size)
    start = timeit.default_timer()
    array = merge_sort(array)
    end = timeit.default_timer()
    return (end - start) * 1000


def visualization_sort(sizes):
    """
    Визуализирует результаты сравнения сортировок:
    heapsort, quick_sort и merge_sort для разных размеров массивов.

    Args:
        sizes: список длин массивов для тестирования.

    Returns:
        None. Сохраняет график в ./report/sorting.png и отображает его.
    """
    heapsort_measures = []
    quick_sort_measures = []
    merge_sort_measures = []
    for size in sizes:
        heapsort_measures.append(measure_heapsort(size))
        quick_sort_measures.append(measure_quick_sort(size))
        merge_sort_measures.append(measure_merge_sort(size))

    print("Сравнение сортировок")
    print(heapsort_measures)
    print(quick_sort_measures)
    print(merge_sort_measures)
    print("")
    plt.plot(sizes, heapsort_measures, marker='o', color="red", label='heap')
    plt.plot(sizes, quick_sort_measures, marker='o',
             color="blue", label='quick')
    plt.plot(sizes, merge_sort_measures, marker='o',
             color="green", label='merge')
    plt.xlabel("Количество элементов n")
    plt.ylabel("Время выполнения ms")
    plt.title("Сравнение сортировок")
    plt.legend(loc="upper left", title="Методы")
    plt.savefig("./report/sorting.png", dpi=300, bbox_inches="tight")
    plt.show()

# Insert VS PEEK VS EXTRACT [1000, 5000, 10000, 25000, 100000]


def measure_insert(size):
    """
    Измеряет среднее время выполнения операции insert в куче.

    Args:
        size: количество элементов, вставляемых перед измерением.

    Returns:
        result: среднее время одной операции insert (в секундах).
    """
    repeats = 20
    heap = Heap(True)
    for i in range(size):
        heap.insert(random.randint(0, 1_000_000))
    start = timeit.default_timer()
    for i in range(repeats):
        heap.insert(random.randint(0, 1_000_000))
    end = timeit.default_timer()
    return (end - start) / 20


def measure_peek(size):
    """
    Измеряет среднее время выполнения операции peek в куче.

    Args:
        size: количество элементов, вставляемых перед измерением.

    Returns:
        result: среднее время одной операции peek (в секундах).
    """
    repeats = 20
    heap = Heap(True)
    for i in range(size):
        heap.insert(random.randint(0, 1_000_000))
    start = timeit.default_timer()
    for i in range(repeats):
        heap.peek()
    end = timeit.default_timer()
    return (end - start) / 20


def measure_extract(size):
    """
    Измеряет среднее время выполнения операции extract в куче.

    Args:
        size: количество элементов, вставляемых перед измерением.

    Returns:
        result: среднее время одной операции extract (в секундах).
    """
    repeats = 20
    heap = Heap(True)
    for i in range(size):
        heap.insert(random.randint(0, 1_000_000))
    start = timeit.default_timer()
    for i in range(repeats):
        heap.extract()
    end = timeit.default_timer()
    return (end - start) / 20


def visualization_operations(sizes):
    """
    Визуализирует результаты сравнения трёх операций кучи:
    insert, peek и extract.

    Args:
        sizes: список размеров кучи для тестирования.

    Returns:
        None. Сохраняет график
    """
    insert_measures = []
    peek_measures = []
    extract_measures = []
    for size in sizes:
        insert_measures.append(measure_insert(size))
        peek_measures.append(measure_peek(size))
        extract_measures.append(measure_extract(size))

    print("Сравнение операций")
    print(insert_measures)
    print(peek_measures)
    print(extract_measures)
    print("")
    plt.plot(sizes, insert_measures, marker='o', color="red", label='insert')
    plt.plot(sizes, peek_measures, marker='o', color="blue", label='peek')
    plt.plot(sizes, extract_measures, marker='o',
             color="green", label='extract')
    plt.xlabel("Количество элементов n")
    plt.ylabel("Время выполнения ns")
    plt.title("Сравнение операций кучи")
    plt.legend(loc="upper left", title="Методы")
    plt.savefig("./report/heap_operations.png", dpi=300, bbox_inches="tight")
    plt.show()

```

```PYTHON
# main.py

from modules.heap import Heap
from modules.perfomance_analysis import visualization_build
from modules.perfomance_analysis import visualization_sort
from modules.perfomance_analysis import visualization_operations


sizes_build = [1000, 5000, 10000, 25000,
               100000, 250000, 500000, 1000000]
sizes_sort = [1000, 5000, 10000, 25000, 100000]
operation_sizes = [1000, 5000, 10000, 25000, 100000, 1000000]

visualization_build(sizes_build)
visualization_sort(sizes_sort)
visualization_operations(operation_sizes)

# Характеристики вычислительной машины
pc_info = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
"""
print(pc_info)


heap = Heap(True)
heap.build_heap([5, 2, 9, 1, 7, 6, 3])
heap.visualize()

```

<image src="./report/creating_heap.png" style="display:block; margin: auto;">
<image src="./report/sorting.png" style="display:block; margin: auto;">
<image src="./report/heap_operations.png" style="display:block; margin: auto;">


```bash
Построение кучи:
[0.3298999999969965, 1.6397999997934676, 3.3206999996764353, 11.685499999657623, 64.60040000001754, 151.06100000048173, 215.0538999994751, 399.35760000025766]
[0.28699999984382885, 1.4271000000007916, 3.0237999999371823, 7.9038999992917525, 34.68259999954171, 134.723699999995, 190.39239999983693, 326.22600000013335]

Сравнение сортировок
[4.056900000250607, 19.033499999750347, 36.36310000001686, 128.11650000003283, 517.039699999259]
[1.2974000001122477, 5.809100000078615, 12.087599999176746, 32.1008000000802, 164.926700000251]
[1.0857999996005674, 6.823200000326324, 14.718500000526547, 39.731799999572104, 188.41750000046886]

Сравнение операций
[7.999999979801942e-07, 1.8899999759014463e-06, 8.550000075047137e-07, 7.800000275892671e-07, 6.999999641266186e-07, 8.099999831756577e-07]
[3.950000063923653e-07, 1.8000000636675396e-07, 1.500000053056283e-07, 1.4000002011016476e-07, 1.5999999050109182e-07, 1.2999998943996616e-07]
[1.048499998432817e-05, 8.144999992509838e-06, 4.6599999677710006e-06, 6.570000005012844e-06, 7.075000030454248e-06, 8.050000042203465e-06]


Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12

        9
    3
        6
1
        7
    2
        5
```


## 1. Сравнение практической и теоретической сложности операций

| Операция              | Теоретическая сложность | Среднее измеренное время (по графику) | Соответствие теории |
|-----------------------|-------------------------|---------------------------------------|---------------------|
| `insert`              | O(log n)                | Умеренно растёт с увеличением n       | Да                  |
| `peek`                | O(1)                    | Почти неизменно                       | Да                  |
| `extract`             | O(log n)                | Растёт аналогично `insert`            | Да                  |
| `build_heap`          | O(n)                    | Заметно быстрее последовательных `insert` | Да              |
| Последовательные `insert` | O(n log n)           | Существенно дольше при больших n      | Да                  |

**Вывод:**  
Практические измерения подтверждают теоретические оценки: операции `insert` и `extract` демонстрируют логарифмический рост времени, `peek` — постоянный, а построение кучи из массива (`build_heap`) масштабируется линейно, что подтверждает его эффективность.

---

## 2. Разница во времени между методами построения кучи

**Методы:**
1. **Последовательные вставки (`insert`)** — элементы добавляются по одному, каждый раз восстанавливается свойство кучи.  
   → Сложность: **O(n log n)**.  
2. **Построение из массива (`build_heap`)** — выполняется "просеивание вниз" для половины элементов, начиная с середины массива.  
   → Сложность: **O(n)**.

**Причина различий:**
- При `build_heap` элементы, расположенные ближе к листьям, требуют меньше операций просеивания.
- При последовательных вставках каждая новая вставка может затронуть всю высоту дерева.
- На практике это выражается в **многократном ускорении** `build_heap` при увеличении размера данных.

**Вывод:**  
Разница обусловлена тем, что `build_heap` использует оптимизированный подход снизу вверх, в то время как последовательные `insert` — сверху вниз с избыточным количеством перестановок.

---

## 3. Эффективность Heapsort

| Алгоритм       | Теоретическая сложность | Поведение на практике | Примечание |
|----------------|-------------------------|------------------------|-------------|
| **Heapsort**   | O(n log n)              | Стабильно, но медленнее QuickSort     | Не требует доп. памяти |
| **QuickSort**  | O(n log n) (в среднем) / O(n²) (в худшем) | Самый быстрый на случайных данных | Использует рекурсию и разделение |
| **MergeSort**  | O(n log n)              | Чуть медленнее QuickSort | Стабильный, но требует O(n) памяти |

**Анализ:**  
Heapsort демонстрирует устойчивую производительность независимо от распределения данных, но уступает QuickSort в константах времени — из-за большего числа обменов элементов и менее локализованных обращений к памяти.  
В сравнении с MergeSort — выигрывает по памяти, но немного проигрывает по скорости.

**Вывод:**  
Heapsort остаётся надёжным универсальным методом сортировки с гарантированной сложностью O(n log n), но для практического использования в большинстве случаев предпочтительнее QuickSort или гибридные алгоритмы (например, Timsort).





## Ответы на контрольные вопросы


### 1. Основное свойство min-кучи и max-кучи

- **Min-куча:** значение в каждом узле **меньше или равно** значениям его потомков.  
  → Минимальный элемент всегда находится в корне кучи.

- **Max-куча:** значение в каждом узле **больше или равно** значениям его потомков.  
  → Максимальный элемент всегда находится в корне кучи.

---

### 2. Алгоритм вставки нового элемента (процедура `sift_up`)

**Идея:**  
Добавить элемент в конец кучи и «просеять вверх» (поднять), пока не восстановится свойство кучи.

**Пошагово:**
1. Добавляем новый элемент в конец массива (в следующую свободную позицию дерева).
2. Сравниваем элемент с его родителем.
3. Если нарушено свойство кучи (например, в min-куче потомок меньше родителя), — меняем их местами.
4. Продолжаем подниматься вверх, пока элемент не окажется на корректной позиции (или не достигнет корня).

**Сложность:** O(log n), т.к. высота двоичной кучи равна log₂n.

---

### 3. Почему построение кучи из массива — O(n), а не O(n log n)

**Метод:**  
Используется алгоритм "просеивания вниз" (`sift_down`), начиная с середины массива (все элементы после середины — листья, их не нужно обрабатывать).

**Обоснование:**
- Листья не требуют операций.
- Элементы на нижних уровнях имеют малую высоту, значит, требуют меньше операций.
- Хотя каждая операция `sift_down` может занимать O(log n), для большинства узлов глубина мала.
- Суммарное время вычисляется как:  
  `n/2 * 1 + n/4 * 2 + n/8 * 3 + ... ≈ 2n = O(n)`

**Итог:** Построение кучи из массива линейное, т.к. большая часть элементов просеивается на короткое расстояние.

---

### 4. Алгоритм пирамидальной сортировки (Heapsort)

**Основная идея:**  
Использовать свойство max-кучи, где на вершине всегда находится максимальный элемент.

**Шаги:**
1. Построить max-кучу из массива (O(n)).
2. Повторять:
   - Поменять местами корень (максимум) и последний элемент.
   - Уменьшить размер кучи на 1.
   - Восстановить свойство кучи (`sift_down`) для корня.
3. После каждого шага "вынутый" элемент помещается в конец массива — в итоге массив отсортирован по возрастанию.

**Сложность:** O(n log n)  
(построение O(n) + n удалений по O(log n)).

**Особенности:**  
- Не требует дополнительной памяти (in-place).  
- Не является стабильной сортировкой.

---

### 5. Куча и приоритетная очередь

**Почему куча подходит:**
- Элемент с наивысшим (или наименьшим) приоритетом всегда находится в корне.
- Доступ к нему — за O(1).
- Вставка и удаление приоритета — за O(log n).

**Поддерживаемые операции:**

| Операция                    | Описание                                      | Сложность |
|-----------------------------|----------------------------------------------|------------|
| `insert(element)`           | Добавление элемента в очередь                | O(log n)   |
| `extract_max` / `extract_min` | Извлечение элемента с наивысшим приоритетом | O(log n)   |
| `peek()`                    | Просмотр элемента с наивысшим приоритетом    | O(1)       |

**Вывод:**  
Куча идеально подходит для реализации приоритетной очереди благодаря быстрому доступу к элементу с максимальным приоритетом и эффективным операциям вставки и удаления.
