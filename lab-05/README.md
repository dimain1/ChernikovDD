# Отчет по лабораторной работе 5
# Хеш-функции и хеш-таблицы

**Дата:** 2025-10-10
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы
Изучить принципы работы хеш-функций и хеш-таблиц. Освоить методы разрешения
 коллизий. Получить практические навыки реализации хеш-таблицы с различными стратегиями
 разрешения коллизий. Провести сравнительный анализ эффективности разных методов.
## Практическая часть

### Выполненные задачи
- [ ] Задача 1: Реализовать несколько хеш-функций для строковых ключей.
- [ ] Задача 2: Реализовать хеш-таблицу с методом цепочек.
- [ ] Задача 3: Реализовать хеш-таблицу с открытой адресацией (линейное пробирование и двойное
 хеширование).
- [ ] Задача 4: Провести сравнительный анализ эффективности разных методов разрешения коллизий.
- [ ] Задача 5: Исследовать влияние коэффициента заполнения на производительность.



### Ключевые фрагменты кода

```PYTHON
# hash_functions.py

def simple_hash(str):
    """
    Вычисляет хеш для строки.

    Args:
        str: Входная строка.
        len: длина массива.

    Returns:
        Значение хеша строки.
    """
    sum = 0
    for i in str:
        sum += ord(i)
    return sum
    # Временная сложность: O(n) — нужно пройти по всем символам строки


def polynomial_hash(str, p=37, mod=10**9 + 7):
    """
    Вычисляет полиномиальный хеш для строки.

    Args:
        str: Входная строка.
        p: Простое число (основание хеша).
        mod: Большое число (модуль хеширования).

    Returns:
        Значение хеша строки.
    """
    hash_value = 0
    p_pow = 1
    for i in str:
        char_code = ord(i)
        hash_value = (hash_value + char_code * p_pow) % mod
        p_pow = (p_pow * p) % mod
    return hash_value
    # Временная сложность: O(n) — один проход по символам


def djb2_hash(str):
    """
    Вычисляет DJB2 хеш для строки.

    Args:
        str: Входная строка.

    Returns:
        Значение хеша строки.
    """
    hash_value = 5381
    for i in str:
        hash_value = ((hash_value << 5) + hash_value) + \
            ord(i)  # hash * 33 = (2^5 + 1(hash)) + ord(i)
    return hash_value & 0xFFFFFFFF  # для ограничения 32-битного числа
    # Временная сложность: O(n) — один проход по символам

```

```PYTHON
# hash_table_chaining.py

from modules.hash_functions import polynomial_hash
# from src.modules.hash_functions import polynomial_hash  # by test


class Node:
    """
    Класс узла односвязного списка.

    Attributes:
        key: Ключ элемента.
        value: Значение элемента.
        next: Ссылка на следующий узел в цепочке.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class ChainingHashTable:
    """
    Класс хеш-таблицы методом цепочек с динамическим масштабированием.
    Поддерживает вставку, поиск и удаление элементов.


    """

    def __init__(self, initial_size=8, load=0.7, hash_func=polynomial_hash):
        """
        Инициализация хеш-таблицы.

         Args:
            initial_size : Начальный размер внутреннего массива;
            load : Порог коэффициента заполнения.
            hash_func : Функция хеширования.
        """
        self.size = initial_size
        self.count = 0
        self.table = [None] * self.size
        self.min_size = 8
        self.load = load
        self._hash = hash_func

    def _resize(self):
        """
        Увеличивает размер таблицы вдвое при превышении порога загрузки.
        Перераспределяет все элементы в новые индексы.
        """
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            current = node
            while current:
                self.insert(current.key, current.value)
                current = current.next
    # Временная сложность: O(n) — перераспределение всех элементов
    # Пространственная сложность: O(1) — перераспределение
    # происходит in-place

    def _shrink(self):
        """
        Уменьшает размер таблицы вдвое при низкой загрузке (не меньше min_size)
        Перераспределяет все элементы в новые индексы.
        """
        old_table = self.table
        self.size = max(self.min_size, self.size // 2)
        self.table = [None] * self.size
        self.count = 0
        for node in old_table:
            current = node
            while current:
                self.insert(current.key, current.value)
                current = current.next
    # Временная сложность: O(n) — перераспределение всех элементов
    # Пространственная сложность: O(1) — используется константное
    # дополнительное пространство

    def insert(self, key, value):
        """
        Вставляет элемент с ключом и значением в таблицу.
        Если ключ уже существует, обновляет значение.
        Args:
            key: Ключ элемента.
            value: Значение элемента.

        Returns:
            None
        """
        if self.count / self.size > self.load:
            self._resize()
        index = self._hash(key) % self.size
        head = self.table[index]
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        new_node = Node(key, value)
        new_node.next = head
        self.table[index] = new_node
        self.count += 1
    # Временная сложность: среднее O(1), худшее O(n)
    # при длинной цепочке или при resize
    # Пространственная сложность: O(1) — добавляется один узел

    def get(self, key):
        """
        Возвращает значение элемента по ключу.
        Args:
            key: Ключ элемента.
        Returns:
            Значение элемента, либо None, если ключ не найден.
        """
        index = self._hash(key) % self.size
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None
        # Временная сложность: среднее O(1), худшее O(n) при коллизиях
        # Пространственная сложность: O(1)

    def remove(self, key):
        """
        Удаляет элемент по ключу.

        Args:
            key: Ключ элемента для удаления.

        Returns:
            True, если элемент удалён, иначе False.
        """
        index = self._hash(key) % self.size
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.count -= 1
                if self.size > self.min_size and self.count / self.size < 0.25:
                    self._shrink()
                return True
            prev = current
            current = current.next
        return False
        # Временная сложность: среднее O(1), худшее O(n) при длинной цепочке
        # Пространственная сложность: O(1)

    def display(self):
        """
        Выводит текущее состояние таблицы для отладки.
        Показывает все цепочки в таблице.
        """
        for i, node in enumerate(self.table):
            print(f"Bucket {i}:", end=" ")
            current = node
            while current:
                print(f"({current.key}: {current.value})", end=" -> ")
                current = current.next
            print("None")

```

```PYTHON
# hash_table_open_addressing.py

from modules.hash_functions import polynomial_hash, djb2_hash
# from src.modules.hash_functions import polynomial_hash, djb2_hash


class LinearHashTable:
    """
    Класс хеш-таблицы с открытой адресацией и линейным пробированием.
    Поддерживает вставку, поиск и удаление элементов.
    """

    def __init__(self, size=8, load=0.7, hash_func=polynomial_hash):
        """
        Инициализация хеш-таблицы.

        Args:
            initial_size : Начальный размер внутреннего массива;
            load : Порог коэффициента заполнения.
            hash_func : Функция хеширования.
        """
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.load = load
        self._hash = hash_func

    def _probe(self, key, for_insert=False):
        """
        Линейное пробирование для поиска индекса ключа или свободной ячейки.
        Args:
            key: Ключ элемента.
            for_insert: Если True, ищем первую свободную ячейку или
                        ячейку с этим ключом;
                        если False, ищем существующий ключ.

        Returns:
            Индекс найденной ячейки или None,
            если ключ не найден (for_insert=False).

        """
        index = self._hash(key) % self.size
        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return index
            index = (index + 1) % self.size
            if index == start_index:
                break
        if for_insert:
            return index
        return None
        # Временная сложность: среднее O(1), худшее O(n)
        # Пространственная сложность: O(1)

    def insert(self, key, value):
        """
        Вставляет элемент с ключом и значением в таблицу.
        Если ключ уже существует, обновляет значение.
        Args:
            key: Ключ элемента.
            value: Значение элемента.
        """
        if self.count >= self.size * self.load:
            self._resize()
        index = self._probe(key, for_insert=True)
        if self.table[index] is None:
            self.count += 1
        self.table[index] = (key, value)
        # Временная сложность: среднее O(1), худшее O(n) при долгой цепочке
        # Пространственная сложность: O(1)

    def get(self, key):
        """
        Возвращает значение элемента по ключу.
        Args:
            key: Ключ элемента.
        Returns:
            Значение элемента, либо None, если ключ не найден.
        """
        index = self._probe(key)
        if index is not None:
            return self.table[index][1]
        return None
        # Временная сложность: среднее O(1), худшее O(n) при коллизиях
        # Пространственная сложность: O(1)

    def remove(self, key):
        """
        Удаляет элемент по ключу и перехеширует затронутые элементы.
        Args:
            key: Ключ элемента для удаления.
        Returns:
            True, если элемент удалён, иначе False.
        """
        index = self._probe(key)
        if index is not None:
            self.table[index] = None
            self.count -= 1
            self._rehash(index)
            return True
        return False
        # Временная сложность: среднее O(1), худшее O(n)
        # Пространственная сложность: O(1)

    def _rehash(self, empty_index):
        """
        Перехеширование элементов после удаления для линейного пробирования.

        Args:
            empty_index: Индекс только что освободившейся ячейки.
        """
        index = (empty_index + 1) % self.size
        while self.table[index] is not None:
            key, value = self.table[index]
            self.table[index] = None
            self.count -= 1
            self.insert(key, value)
            index = (index + 1) % self.size
        # Временная сложность: O(n) в худшем случае (перехеширование цепочки)
        # Пространственная сложность: O(1)

    def _resize(self):
        """
        Увеличивает размер таблицы вдвое и перераспределяет все элементы.
        """
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item is not None:
                self.insert(*item)
        # Временная сложность: O(n) — перераспределение всех элементов
        # Пространственная сложность: O(1)

    def display(self):
        """
        Выводит текущее состояние таблицы для отладки.
        Показывает все элементы с их индексами.
        """
        for i in range(self.size):
            if self.table[i] is None:
                print(f"{i}) {None}")
            else:
                print(f"{i}) {self.table[i][0]}: {self.table[i][1]}")
        # Временная сложность: O(n) — проход по всей таблице
        # Пространственная сложность: O(1)


def next_prime(n):
    """
    Возвращает простое число >= n.

    Args:
        n: число больше которого выбирают простое.

    Returns:
        n: Возвращает простое число большее n
    """
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n


class DoubleHashingHashTable:
    """
    Класс хеш-таблицы с открытой адресацией и двойным хешированием.
    Поддерживает вставку, поиск и удаление элементов.
    """

    def __init__(self, size=7, load=0.7, hash_func1=polynomial_hash,
                 hash_func2=djb2_hash):
        """
        Инициализация хеш-таблицы.
        Args:
            initial_size : Начальный размер внутреннего массива;
            load : Порог коэффициента заполнения.
            hash_func1 : Функция хеширования значений.
            hash_func2 : Функция хеширования шага пробирования
        """
        self.size = next_prime(size)  # размер таблицы — простое число
        self.table = [None] * self.size
        self.count = 0
        self.load = load
        self._hash1 = hash_func1
        self._hash2 = hash_func2

    def _probe(self, key, for_insert=False):
        """
        Двойное хеширование для поиска индекса ключа или свободной ячейки.

        Args:
            key: Ключ значения.
            for_insert: Переменная-флаг на вставку.
        """
        index = self._hash1(key) % self.size

        # step не должен быть кратен size
        step = self._hash2(key) % (self.size - 1) + 1
        if step % self.size == 0:
            step = 1

        start_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return index
            index = (index + step) % self.size
            if index == start_index:
                break

        if for_insert:
            return index
        return None

    def insert(self, key, value):
        """
        Вставляет элемент с ключом и значением в таблицу.
        Если ключ уже существует, обновляет значение.

        Args:
            key: Ключ значения для вставки
            value: Значение для вставки
        """
        if self.count >= self.size * self.load:
            self._resize()

        index = self._probe(key, for_insert=True)
        if self.table[index] is None:
            self.count += 1
        self.table[index] = (key, value)
        # Временная сложность: среднее O(1), худшее O(n)
        # Пространственная сложность: O(1)

    def get(self, key):
        """
        Возвращает значение элемента по ключу.

        Args:
            key: ключ значения для получения
        """
        index = self._probe(key)
        if index is not None:
            return self.table[index][1]
        return None
        # Временная сложность: среднее O(1), худшее O(n)
        # Пространственная сложность: O(1)

    def remove(self, key):
        """
        Удаляет элемент по ключу и полностью перехеширует таблицу.

        Args:
            key: Ключ значения для удаления.
        """
        index = self._probe(key)
        if index is not None:
            self.table[index] = None
            self.count -= 1
            self._rehash()
            return True
        return False
        # Временная сложность: среднее O(1), худшее O(n)
        # Пространственная сложность: O(1)

    def _rehash(self):
        """
        Перехеширование всех элементов таблицы после удаления.
        """
        old_table = self.table
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item is not None:
                key, value = item
                self.insert(key, value)
        # Временная сложность: O(n) — восстановление всех элементов
        # Пространственная сложность: O(1)

    def _resize(self):
        """
        Увеличивает размер таблицы до следующего простого числа
        и перераспределяет все элементы.
        """
        old_table = self.table
        self.size = next_prime(self.size * 2)
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item is not None:
                self.insert(*item)
        # Временная сложность: O(n) — перераспределение всех элементов
        # Пространственная сложность: O(1)

    def display(self):
        """
        Выводит текущее состояние таблицы для отладки.
        """
        for i in range(self.size):
            if self.table[i] is None:
                print(f"{i}) {None}")
            else:
                print(f"{i}) {self.table[i][0]}: {self.table[i][1]}")

```

```PYTHON
# HistCollision.py

import random
import string
import matplotlib.pyplot as plt
from modules.hash_functions import djb2_hash


class ChainHashTableByCollision:
    """
    Урезанная реализация класса хеш таблицы методом
    цепочек под посчёт распределения
    колизий
    """

    def __init__(self, size=100, hash_func=djb2_hash):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = []
        self._hash = hash_func

    def insert(self, key):
        """
        Вставляет элемент с ключом и значением в таблицу.
        Если ключ уже существует, обновляет значение.

        Args:
            key: Ключ значения для вставки
            value: Значение для вставки
        """
        index = self._hash(key) % self.size
        chain = self.table[index]
        if len(chain) > 0:
            self.collisions.append(len(chain))  # коллизия
        chain.append(key)
        if sum(len(c) for c in self.table) / self.size > 0.7:
            self._resize()

    def _resize(self):
        """
        Увеличивает размер внутренней таблицы и перераспределяет ключи.
        """
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        for chain in old_table:
            for key in chain:
                self.insert(key)


class LinearProbingHashTableByCollision:
    """
    Урезанная реализация класса хеш таблицы открытой
    адресации с линейной пробацией под посчёт распределения
    колизий
    """

    def __init__(self, size=100, hash_func=djb2_hash):
        self.size = size
        self.table = [None] * size
        self.collisions = []
        self._hash = hash_func

    def insert(self, key):
        """
        Вставляет ключ в таблицу с линейным пробированием.
        При столкновении считает количество шагов до свободной ячейки.

        Args:
            key: Ключ (строка) для вставки.
        """
        index = self._hash(key) % self.size
        start = index
        steps = 0
        while self.table[index] is not None:
            steps += 1
            index = (index + 1) % self.size
            if index == start:
                raise Exception("Таблица переполнена")
        if steps > 0:
            self.collisions.append(steps)
        self.table[index] = key


def next_prime(n):
    """
    Возвращает простое число >= n.

    Args:
        n: число больше которого выбирают простое.

    Returns:
        n: Возвращает простое число большее n
    """
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n


class DoubleHashingHashTableByCollision:
    """
    Урезанная реализация класса хеш таблицы открытой
    адресации с двойным хешированием под посчёт распределения
    колизий
    """

    def __init__(self, size=100, hash_func1=djb2_hash,
                 hash_func2=djb2_hash):
        self.size = next_prime(size)
        self.table = [None] * self.size
        self.collisions = []
        self._hash1 = hash_func1
        self._hash2 = hash_func2

    def insert(self, key):
        """
        Вставляет ключ в таблицу с двойным хешированием.
        Использует вторую хеш-функцию для вычисления шага пробирования.
        При коллизиях фиксирует число шагов до свободной ячейки.

        Args:
            key: Ключ (строка) для вставки.
        """
        checked_ind = []
        index = self._hash1(key) % self.size

        step = self._hash2(key) % (self.size - 1) + 1
        if step % self.size == 0:
            step = 1

        steps = 0
        while self.table[index] is not None:
            steps += 1
            index = (index + step) % self.size
            if index not in checked_ind:
                checked_ind.append(index)
            if len(checked_ind) == self.size:
                raise Exception("Таблица переполнена")
        if steps > 0:
            self.collisions.append(steps)
        self.table[index] = key


def generate_random_string_loop(length):
    """
    Генерирует рандомную строку длины length

    Args:
        length: длина строки для генерации

    Returns:
        random_string: Сгенерированная строка
    """
    characters = string.ascii_letters + string.digits
    random_string = ""
    for _ in range(length):
        random_string += random.choice(characters)
    return random_string


def visualisation(hash_func, N=2000, func_name="table"):
    """
    Собирает данные по распределению колизий и вызывает
    функцию по созданию графиков

    Args:
        hash_func: Хеш функция для которой производится замер
        N: Размер хеш-таблиц и количество элементов
        func_name: Наименование функции для графика
    """

    keys = [generate_random_string_loop(10) for _ in range(N)]

    chain_ht = ChainHashTableByCollision(N//10, hash_func=hash_func)
    linear_ht = LinearProbingHashTableByCollision(N, hash_func=hash_func)
    double_ht = DoubleHashingHashTableByCollision(
        N, hash_func1=hash_func, hash_func2=hash_func)

    for k in keys:
        chain_ht.insert(k)
        linear_ht.insert(k)
        double_ht.insert(k)

    data = [chain_ht, linear_ht, double_ht]

    create_plot(data, "./report/" + func_name + ".png")


def create_plot(data, path):
    """
    Создаёт рисунок по пути path, на котором изображены 3 графика
    зависимости распределения колизий от хеш-функции

    Args:
        data: Списко колизий для постройки гистограммы
        path: Путь для сохранения графика
    """
    plt.figure(figsize=(14, 5))

    plt.subplot(1, 3, 1)
    plt.hist(data[0].collisions, bins=20, edgecolor='black')
    plt.title("Метод цепочек")
    plt.xlabel("Количество коллизий на вставку")
    plt.ylabel("Частота")

    plt.subplot(1, 3, 2)
    plt.hist(data[1].collisions, bins=20, edgecolor='black', color='orange')
    plt.title("Линейное пробирование")
    plt.xlabel("Количество коллизий на вставку")

    plt.subplot(1, 3, 3)
    plt.hist(data[2].collisions, bins=20, edgecolor='black', color='green')
    plt.title("Двойное хеширование")
    plt.xlabel("Количество коллизий на вставку")

    plt.tight_layout()
    plt.savefig(path)
    plt.show()

```

<image src="./report/Simple.png" style="display:block; margin: auto; ">
<div style="text-align:center; font-size: 24px">Simple hash function</div>
<image src="./report/Polynomial.png" style="display:block; margin: auto; ">
<div style="text-align:center; font-size: 24px">Polynomial hash function</div>
<image src="./report/DJB2.png" style="display:block; margin: auto; ">
<div style="text-align:center; font-size: 24px">DJB2 hash function</div>

```PYTHON
# perfomance_analysis.py

from modules.hash_table_chaining import ChainingHashTable
from modules.hash_table_open_addressing import LinearHashTable
from modules.hash_table_open_addressing import DoubleHashingHashTable
import random
import string
import timeit
import matplotlib.pyplot as plt


def generate_random_string_loop(length):
    """
    Генерирует рандомную строку длины length

    Args:
        length: длина строки для генерации

    Returns:
        random_string: Сгенерированная строка
    """
    characters = string.ascii_letters + string.digits
    random_string = ""
    for _ in range(length):
        random_string += random.choice(characters)
    return random_string


def get_time_for_chained(load, size, strings):
    """
    Вычисляет среднее время вставкии в хеш таблицу
    реализованную методом цепочек

    Args:
        load: целевой коэффициент заполнения.
        size: количество элементов для вставки.
        strings: список ключей (строк) длины >= size для вставки.

    Returns:
        out: среднее время вставки всех элементов в миллисекундах,
               усреднённое по нескольким прогонам.
    """
    measures = []
    for j in range(20):
        table = ChainingHashTable(initial_size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
        measures.append((end - start) * 1000)
    return sum(measures) / len(measures)


def get_time_for_linear(load, size, strings):
    """
    Вычисляет среднее время вставкии в хеш таблицу
    открытой адресации линейной пробации

    Args:
        load: целевой коэффициент заполнения.
        size: количество элементов для вставки.
        strings: список ключей (строк) длины >= size для вставки.

    Returns:
        out: среднее время вставки всех элементов в миллисекундах,
               усреднённое по нескольким прогонам.
    """
    measures = []
    for j in range(20):
        table = LinearHashTable(size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
        measures.append((end - start) * 1000)
    return sum(measures) / len(measures)


def get_time_for_double(load, size, strings):
    """
    Вычисляет среднее время вставкии в хеш таблицу
    открытой адресации двойного хеширования

    Args:
        load: целевой коэффициент заполнения.
        size: количество элементов для вставки.
        strings: список ключей (строк) длины >= size для вставки.

    Returns:
        out: среднее время вставки всех элементов в миллисекундах,
               усреднённое по нескольким прогонам.
    """
    measures = []
    for j in range(20):
        table = DoubleHashingHashTable(size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
        measures.append((end - start) * 1000)
    return sum(measures) / len(measures)


def measure_time(loades=[0.1, 0.5, 0.7, 0.9], size=1000):
    """
    Собирает результаты времени выполнения в словарь вида
    ["метод реализации"] - [список значений времени выполнения]

    Args:
        loades: список коэффициентов заполнения для тестирования.
        size: количество элементов, вставляемых в
            каждую таблицу при каждом замере.

    Returns:
        dict: словарь с ключами 'chain', 'linear', 'double' и значениями -
              списками средних времени (в миллисекундах)
              для каждого коэффициента заполнения.
    """
    strings = []
    chained_list = []
    linear_list = []
    double_list = []
    for i in range(size):
        strings.append(generate_random_string_loop(10))
    for i in loades:
        chained_list.append(get_time_for_chained(i, size, strings))
        linear_list.append(get_time_for_linear(i, size, strings))
        double_list.append(get_time_for_double(i, size, strings))

    result = {}
    result["chain"] = chained_list
    result["linear"] = linear_list
    result["double"] = double_list

    return result


def visualisation(loads=[0.1, 0.5, 0.7, 0.9], size=1000):
    """
    Визуализирует графики зависимости времени выполнения от
    коэффициента заполнения

    Args:
        loads: список коэффициентов заполнения для оси X.
        size: количество элементов, вставляемых в каждой таблице для измерения.
    """
    measures = measure_time(loades=loads, size=size)
    chained_list = measures["chain"]
    linear_list = measures["linear"]
    double_list = measures["double"]

    create_plot(chained_list, loads,
                "графики зависимости времени от коэффициента заполнения",
                "./report/chained_hashtable.png", label="chain")
    create_plot(linear_list, loads,
                "графики зависимости времени от коэффициента заполнения",
                "./report/linear_hashtable.png", label="linear")
    create_plot(double_list, loads,
                "графики зависимости времени от коэффициента заполнения",
                "./report/double_hashtable.png", label="double")


def create_plot(data, sizes, title, path, label):
    """
    Строит и сохраняет график времени работы сортировок для одного типа данных.
    Args:
        data: список значений времени (ms) для каждой точки по оси X.
        sizes: список коэффициентов заполнения (ось X).
        title: заголовок графика.
        path: путь для сохранения PNG-файла.
        label: подпись кривой на графике.
    """
    plt.plot(sizes, data,
             marker="o", color="red", label=label)

    plt.xlabel("коэффициент заполнения")
    plt.ylabel("Время выполнения ms")
    plt.title(title)
    plt.legend(loc="upper left", title="Метод")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.show()

```

```PYTHON
# main.py

import modules.perfomance_analysis as perf_test
from modules.hash_functions import simple_hash, polynomial_hash, djb2_hash
import modules.HistCollision as hist

perf_test.visualisation(size=100000)

hist.visualisation(simple_hash, func_name="Simple")
hist.visualisation(polynomial_hash, func_name="Polynomial")
hist.visualisation(djb2_hash, func_name="DJB2")

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

<image src="./report/chained_hashtable.png" style="display:block; margin: auto;">
<image src="./report/linear_hashtable.png" style="display:block; margin: auto; ">
<image src="./report/double_hashtable.png" style="display:block; margin: auto; ">

```bash
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
```



| Функция                  | Особенности                                                                                                                          | Качество распределения                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Сумма кодов символов** | Очень простая: суммирует коды всех символов строки. Легко вычисляется.                                                               | Плохое: строки с одинаковыми символами в разном порядке дают одинаковый хеш (коллизии часты).                                        |
| **Полиномиальная (p^i)** | Использует степени числа p для каждого символа. Можно брать модуль m, чтобы ограничить размер. Позволяет учитывать порядок символов. | Хорошее: порядок символов влияет на хеш, коллизий меньше, чем у простой суммы. Выбор простого p и большого m улучшает распределение. |
| **DJB2**                 | Стартовое число 5381, каждый символ умножается на 33 (через сдвиг) и добавляется. Легко вычисляется, широко используется.            | Очень хорошее: хорошо распределяет похожие строки, меньше коллизий на практике, стабильное и быстрое.                                |

| Тип хеш-таблицы                               | Операция | Средняя сложность | Худшая сложность |
| --------------------------------------------- | -------- | ----------------- | ---------------- |
| Метод цепочек с динамическим масштабированием | Вставка  | O(1)              | O(n)             |
|                                               | Поиск    | O(1 + α)          | O(n)             |
|                                               | Удаление | O(1 + α)          | O(n)             |
| Открытая адресация с линейным пробированием   | Вставка  | O(1)    | O(n)             |
|                                               | Поиск    | O(1)    | O(n)             |
|                                               | Удаление | O(1)    | O(n)             |
| Открытая адресация с двойным хешированием     | Вставка  | O(1)   | O(n)             |
|                                               | Поиск    | O(1)   | O(n)             |
|                                               | Удаление | O(1)    | O(n)             |

## Методы разрешения коллизий

1. Метод цепочек (с динамическим масштабированием)

- Каждый элемент корзины — список (цепочка). При коллизии элементы добавляются в конец списка.

- Сложность:

- Средний случай: O(1) для поиска, вставки.

- Худший случай: O(n) (все элементы в одной цепочке).

- Масштабирование (увеличение таблицы) уменьшает длину цепочек.

- Оптимальный коэффициент заполнения (α): 0.5–0.7.

- Преимущества: простая реализация, устойчивость к коллизиям.

- Недостатки: требует дополнительную память (списки).

2. Открытая адресация с линейным пробированием

- При коллизии ищется следующая свободная ячейка по формуле h + i mod m.

- Сложность:

- Средний случай: O(1).

- Худший случай: O(n) (при «скоплении» элементов).

- Оптимальный α: 0.5–0.7. При большем заполнении резко растет количество проб.

- Преимущества: компактность (всё в одном массиве).

- Недостатки: кластеризация (скопление занятых слотов снижает производительность).

3. Открытая адресация с двойным хешированием

- При коллизии используется вторая хеш-функция: h2(k) для шага пробирования.

- Сложность:

- Средний случай: O(1).

- Худший случай: O(n), но реже, чем при линейном пробировании.

- Оптимальный α: 0.5–0.7.

- Преимущества: лучшее распределение, меньше кластеризация.

- Недостатки: чуть более сложная реализация и вычислительная нагрузка (две функции).

## Влияние хеш-функции на производительность

- Качество распределения хеш-функции напрямую влияет на длину цепочек и количество проб.

- Плохая функция (например, простая сумма кодов) создаёт частые коллизии → производительность падает.

- Хорошая функция (DJB2, полиномиальная) обеспечивает равномерное распределение → операции выполняются почти за O(1).

- В таблицах с открытой адресацией качество хеша особенно важно, поскольку коллизии влияют на всю структуру массива.



## Ответы на контрольные вопросы


### 1. Каким требованиям должна удовлетворять "хорошая" хеш-функция?
- **Равномерность распределения:** значения хеша должны равномерно распределяться по всей таблице, чтобы избежать скоплений (кластеризации).  
- **Детерминированность:** для одного и того же ключа всегда возвращается одинаковое значение.  
- **Эффективность:** вычисление должно быть быстрым (O(n), где n — длина ключа).  
- **Минимум коллизий:** разные ключи должны как можно реже давать одинаковый хеш.  
- **Чувствительность к изменениям:** небольшое изменение входных данных должно сильно менять хеш.

---

### 2. Что такое коллизия в хеш-таблице? Опишите два основных метода разрешения коллизий.
**Коллизия** — это ситуация, когда два разных ключа имеют одинаковое значение хеш-функции и попадают в одну ячейку таблицы.  

**Основные методы разрешения:**
1. **Метод цепочек:** каждая ячейка хранит список (цепочку) всех элементов с одинаковым хешом.  
2. **Открытая адресация:** при коллизии ищется другая свободная ячейка по определённому правилу (линейное пробирование, двойное хеширование и т.д.).

---

### 3. В чем разница между методом цепочек и открытой адресацией с точки зрения использования памяти и сложности операций при высоком коэффициенте заполнения?
- **Использование памяти:**
  - Метод цепочек требует дополнительной памяти для хранения связанных списков.  
  - Открытая адресация хранит все элементы в одном массиве, что экономит память.
- **Сложность при большом коэффициенте заполнения:**
  - В цепочках длина списков растёт, операции могут стать ближе к O(n).  
  - В открытой адресации увеличивается количество проб, резко падает скорость вставки и поиска.  

---

### 4. Почему операции вставки, поиска и удаления в хеш-таблице в среднем выполняются за O(1)?
Потому что:
- Хеш-функция напрямую вычисляет позицию элемента.  
- При хорошем распределении коллизии редки, и большинство операций требует лишь одно обращение к ячейке.  
- Масштабирование таблицы поддерживает низкий коэффициент заполнения, сохраняя среднее время O(1).

---

### 5. Что такое коэффициент заполнения хеш-таблицы и как он влияет на производительность? Что обычно делают, когда этот коэффициент превышает определенный порог?
**Коэффициент заполнения (α)** — это отношение числа элементов в таблице к её размеру:  
\[
α = \frac{n}{m}
\]
где *n* — количество элементов, *m* — количество ячеек.  

**Влияние:**
- При низком α операции выполняются быстро (мало коллизий).  
- При высоком α увеличивается число коллизий → падает производительность.

**При превышении порога (обычно 0.7–0.8):**
- Таблицу **масштабируют (rehash)** — создают новую таблицу большего размера.  
- Все элементы пересчитываются новой хеш-функцией или с новым модулем.


