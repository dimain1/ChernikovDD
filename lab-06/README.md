# Отчет по лабораторной работе 6
# Деревья. Бинарные деревья поиска

**Дата:** 2025-10-10
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы
Изучить древовидные структуры данных, их свойства и применение. Освоить основные
 операции с бинарными деревьями поиска (BST). Получить практические навыки реализации BST на
 основе узлов (pointer-based), рекурсивных алгоритмов обхода и анализа их эффективности.
 Исследовать влияние сбалансированности дерева на производительность операций.
## Практическая часть

### Выполненные задачи
- [ ] Задача 1: Реализовать бинарное дерево поиска на основе узлов с основными операциями.
- [ ] Задача 2: Реализовать различные методы обхода дерева (рекурсивные и итеративные).
- [ ] Задача 3: Реализовать дополнительные методы для работы с BST.
- [ ] Задача 4: Провести анализ сложности операций для сбалансированного и вырожденного деревьев.
- [ ] Задача 5: Визуализировать структуру дерева.



### Ключевые фрагменты кода

```PYTHON
# analysis.py

import random
import time
from modules.binary_search_tree import BinarySearchTree


def build_random_tree(size):
    """
    Генерирует сбалансированное бинарное дерево

    Args:
        size: Количество узлов в дереве

    Returns:
        tree: Сбалансированное бинарное дерево поиска
    """
    values = list(range(size))
    random.shuffle(values)
    tree = BinarySearchTree()
    for v in values:
        tree.insert(v)
    return tree


def build_sorted_tree(size):
    """
    Генерирует вырожденное бинарное дерево

    Args:
        size: Количество узлов в дереве

    Returns:
        tree: Вырожденное бинарное дерево поиска
    """
    values = list(range(size))
    tree = BinarySearchTree()
    for v in values:
        tree.insert(v)
    return tree


def measure_search_time(tree, size, trials=1000):
    """
    Измеряет время выполнения 1000 операций поиска в бинарном
    дереве

    Args:
        tree: Бинарное дерево поиска
        size: Размер дерева
        trials: Количество операций поиска

    Returns:
        out: Время выполнения всех операций поиска в секундах
    """
    keys = [random.randrange(size) for _ in range(trials)]
    start = time.perf_counter()
    for k in keys:
        tree.search(k)
    end = time.perf_counter()
    return end - start


def run_experiment(sizes, trials_per_size=1000, repeats=5):
    """
    Измеряет среднее время выполнения операций поиска для сбалансированного
    и вырожденного бинарного дерева

    Args:
        sizes: Список размеров деревьев для тестирования
        trials_per_size: Количество операций поиска для каждого размера
        repeats: Количество повторений эксперимента для усреднения

    Returns:
        results: Список кортежей (размер, время_сбалансированного,
                время_вырожденного)
    """
    results = []
    for n in sizes:
        balanced_times = []
        degenerate_times = []
        for r in range(repeats):
            t_bal = build_random_tree(n)
            bt = measure_search_time(t_bal, n, trials=trials_per_size)
            balanced_times.append(bt)

            t_deg = build_sorted_tree(n)
            dt = measure_search_time(t_deg, n, trials=trials_per_size)
            degenerate_times.append(dt)

        balanced_avg = sum(balanced_times) / repeats
        degenerate_avg = sum(degenerate_times) / repeats
        results.append((n, balanced_avg, degenerate_avg))
        print(
            f"n={n}: Сбалансированное avg {balanced_avg:.6f}s, "
            f"Вырожденное avg {degenerate_avg:.6f}s"
        )

    return results

```

```PYTHON
# binary_search_tree.py

class TreeNode:
    """
    Класс отвечающий за реализацию узлов бинарного дерева.
    """

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinarySearchTree:
    """
    Класс реализующий структуру данных бинарное дерево.
    Поддерживает визуализацию, проверку валидности и получение высоты
    """

    def __init__(self, root=None):
        self.root = root

    def insert(self, value):
        """
        Вставляет значение в дерево.

        Args:
            value: Значение для вставки в дерево
        """
        self.root = self._insert_rec(self.root, value)

    def _insert_rec(self, node, value):
        """
        Рекурсивно вставляет значение в дерево.

        Args:
            node: Текущий узел дерева
            value: Значение для вставки

        Returns:
            node: Обновленный узел дерева
        """
        if node is None:
            return TreeNode(value)
        if value == node.value:
            return node
        if value < node.value:
            node.left = self._insert_rec(node.left, value)
        else:
            node.right = self._insert_rec(node.right, value)
        return node

    # Среднее время: O(log n), Худшее время: O(n)

    def search(self, value):
        """
        Ищет значение в дереве, возвращает узел или None.

        Args:
            value: Искомое значение

        Returns:
            node: Найденный узел или None, если значение не найдено
        """
        return self._search_rec(self.root, value)

    def _search_rec(self, node, value):
        """
        Рекурсивный поиск значения в дереве.

        Args:
            node: Текущий узел дерева
            value: Искомое значение

        Returns:
            node: Найденный узел или None, если значение не найдено
        """
        if node is None:
            return None
        if value == node.value:
            return node
        if value < node.value:
            return self._search_rec(node.left, value)
        return self._search_rec(node.right, value)

    # Среднее время: O(log n), Худшее время: O(n)

    def delete(self, value):
        """
        Удаляет узел со значением value из дерева.
        Возвращает True, если удалено, иначе False.

        Args:
            value: Значение для удаления

        Returns:
            deleted: Флаг успешности удаления
        """
        self.root, deleted = self._delete_rec(self.root, value)
        return deleted

    # Среднее время: O(log n), Худшее время: O(n)

    def _delete_rec(self, node, value):
        """
        Рекурсивное удаление значения из дерева.

        Args:
            node: Текущий узел дерева
            value: Значение для удаления

        Returns:
            node: Обновленный узел дерева
            deleted: Флаг успешности удаления
        """
        if node is None:
            return node, False

        deleted = False
        if value < node.value:
            node.left, deleted = self._delete_rec(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_rec(node.right, value)
        else:
            deleted = True
            # нет потомков
            if node.left is None and node.right is None:
                return None, True
            # один потомок
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            # два потомка
            successor = self.find_min(node.right)
            node.value = successor.value
            node.right, _ = self._delete_rec(node.right, successor.value)

        return node, deleted

    def find_min(self, node):
        """
        Находит минимальный узел в поддереве node.

        Args:
            node: Корень поддерева

        Returns:
            node: Узел с минимальным значением
        """
        current = node
        if current is None:
            return None
        while current.left:
            current = current.left
        return current

    # Среднее время: O(log n), Худшее время: O(n)

    def find_max(self, node):
        """
        Находит максимальный узел в поддереве node.

        Args:
            node: Корень поддерева

        Returns:
            node: Узел с максимальным значением
        """
        current = node
        if current is None:
            return None
        while current.right:
            current = current.right
        return current

    # Среднее время: O(log n), Худшее время: O(n)

    def visualize(self, node=None, level=0):
        """
        Простая текстовая визуализация дерева (отступами).
        Печатает дерево повернутым: правые поддеревья сверху, левыe снизу.

        Args:
            node: Корень дерева/поддерева для визуализации
            level: Текущий уровень отступа
        """
        if node is None:
            node = self.root

        def _viz(n, lvl):
            if n is None:
                return
            _viz(n.right, lvl + 1)
            print("    " * lvl + str(n.value))
            _viz(n.left, lvl + 1)

        _viz(node, level)

    def is_valid_bst(self):
        """
        Проверяет, является ли дерево корректным BST.
        Временная сложность: O(n), Пространственная: O(h) рекурсивный стек.

        Returns:
            out: True если дерево является корректным BST, иначе False
        """
        def helper(node, low, high):
            if node is None:
                return True
            val = node.value
            if low is not None and val <= low:
                return False
            if high is not None and val >= high:
                return False
            left_ok = helper(node.left, low, val)
            if not left_ok:
                return False
            return helper(node.right, val, high)

        return helper(self.root, None, None)

    def height(self, node):
        """
        Вычисляет высоту дерева/поддерева (количество узлов в самом длинном
        пути от node до листа). Возвращает 0 для пустого поддерева.
        Временная сложность: O(n), Пространственная: O(h).

        Args:
            node: Корень дерева/поддерева

        Returns:
            height: Высота дерева/поддерева
        """
        if node is None:
            return 0
        left_h = self.height(node.left)
        right_h = self.height(node.right)
        return 1 + max(left_h, right_h)

```

```PYTHON
# perfomance_analysis.py

import random
import timeit
import matplotlib.pyplot as plt

from modules.binary_search_tree import BinarySearchTree


def build_tree(n, balanced=True):
    """
    Создает бинарное дерево поиска заданного размера.

    Args:
        n: Количество узлов в дереве
        balanced: Флаг создания сбалансированного дерева

    Returns:
        tree: Созданное бинарное дерево поиска
    """
    values = list(range(n))
    if balanced:
        random.shuffle(values)
    tree = BinarySearchTree()
    for v in values:
        tree.insert(v)
    return tree


def time_insert(n, balanced=True):
    """
    Измеряет время выполнения для операции вставки в бинарное дерево

    Args:
        n: Размер дерева
        balanced: Флаг использования сбалансированного дерева

    Returns:
        out: Время выполнения вставки в миллисекундах
    """
    tree = build_tree(n, balanced=balanced)

    new_value = n
    start = timeit.default_timer()
    tree.insert(new_value)
    end = timeit.default_timer()
    return (end - start) * 1000


def measure_time(sizes):
    """
    Вычисляет среднее время выполнения для сбалансированного и
    вырожденного бинарного дерева.

    Args:
        sizes: Список размеров деревьев для тестирования

    Returns:
        res: Словарь с результатами измерений для разных размеров деревьев
    """
    res = {'sizes': list(sizes), 'balanced': [], 'degenerate': []}

    for n in sizes:
        res['balanced'].append(time_insert(n, True))
        res['degenerate'].append(time_insert(n, False))

    return res


def visualisation(sizes, out_png=None):
    """
    Визуализирует график зависимости времени выполнения
    от размера бинарного дерева

    Args:
        sizes: Список размеров деревьев для визуализации
        out_png: Путь к файлу для сохранения графика
    """
    series = measure_time(sizes)
    x = series['sizes']
    plt.plot(x, series['balanced'], marker='o', label='Сбалансированное '
             '(insert)')
    plt.plot(x, series['degenerate'], marker='o', label='Вырожденное (insert)')
    plt.xlabel('n')
    plt.ylabel('time(ms)')
    plt.title('BST insert time: Сбалансированное vs Вырожденное')
    plt.legend()
    if out_png:
        plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.show()

```

```PYTHON
# tree_traversal.py


def inorder_recursive(node, visit=print):
    """
    Рекурсивный in-order обход: left, root, right.
    Временная сложность: O(n), Пространственная: O(h) стек рекурсии.

    Args:
        node: Корень дерева/поддерева для обхода
        visit: Функция, применяемая к значению каждого узла
    """
    if node is None:
        return
    inorder_recursive(node.left, visit)
    visit(node.value)
    inorder_recursive(node.right, visit)


def preorder_recursive(node, visit=print):
    """
    Рекурсивный pre-order обход: root, left, right.
    Временная сложность: O(n), Пространственная: O(h) стек рекурсии.

    Args:
        node: Корень дерева/поддерева для обхода
        visit: Функция, применяемая к значению каждого узла
    """
    if node is None:
        return
    visit(node.value)
    preorder_recursive(node.left, visit)
    preorder_recursive(node.right, visit)


def postorder_recursive(node, visit=print):
    """
    Рекурсивный post-order обход: left, right, root.
    Временная сложность: O(n), Пространственная: O(h) стек рекурсии.

    Args:
        node: Корень дерева/поддерева для обхода
        visit: Функция, применяемая к значению каждого узла
    """
    if node is None:
        return
    postorder_recursive(node.left, visit)
    postorder_recursive(node.right, visit)
    visit(node.value)


def inorder_iterative(node, visit=print):
    """
    Итеративный in-order обход с использованием явного стека.
    Временная сложность: O(n), Пространственная: O(h) для стека.

    Args:
        node: Корень дерева/поддерева для обхода
        visit: Функция, применяемая к значению каждого узла
    """
    stack = []
    current = node
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        visit(current.value)
        current = current.right

```

```PYTHON
# main.py

from modules.binary_search_tree import BinarySearchTree
from modules.analysis import run_experiment
import sys
from modules.perfomance_analysis import visualisation

# Tree visualize
tree = BinarySearchTree()


tree.insert(5)

tree.insert(3)
tree.insert(7)

tree.insert(2)
tree.insert(4)
tree.insert(6)
tree.insert(8)
tree.insert(1)


tree.visualize()


# analysis
sys.setrecursionlimit(40000)
sizes = [100, 1000, 5000, 10000]
res = run_experiment(
    sizes, trials_per_size=1000, repeats=3
)

# Perf_analysis
sizes = [100, 1000, 5000, 10000, 25000]
visualisation(sizes, out_png="./report/insert.png")


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

<image src="./report/insert.png" style="display:block; margin: auto;">


```bash
        8
    7
        6
5
        4
    3
        2
            1
n=100: Сбалансированное avg 0.000404s, Вырожденное avg 0.002483s
n=1000: Сбалансированное avg 0.000857s, Вырожденное avg 0.052115s
n=5000: Сбалансированное avg 0.001126s, Вырожденное avg 0.271026s
n=10000: Сбалансированное avg 0.001359s, Вырожденное avg 0.603855s
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
```









## Сравнение практической и теоретической сложности операций
| Операция     | Теоретическая сложность (средний случай) | Худший случай (вырожденное дерево) | Практическое поведение |
|---------------|------------------------------------------|-------------------------------------|------------------------|
| Вставка       | O(log n)                                 | O(n)                                | Обычно близка к O(log n), если дерево сбалансировано или данные случайны |
| Поиск         | O(log n)                                 | O(n)                                | В большинстве случаев быстрее, чем линейный поиск, но сильно зависит от формы дерева |
| Удаление      | O(log n)                                 | O(n)                                | Зависит от реализации балансировки и структуры узлов |
| Обход дерева  | O(n)                                     | O(n)                                | Всегда линейный, так как каждый узел посещается ровно один раз |

**Вывод:**  
Структура дерева напрямую влияет на производительность. Если дерево сбалансировано — операции выполняются за O(log n). Если дерево вырождено (похоже на список) — операции деградируют до O(n).





## Ответы на контрольные вопросы


## 1. Основное свойство бинарного дерева поиска (BST)
Для любого узла дерева:
- Все значения в **левом поддереве** меньше значения узла.  
- Все значения в **правом поддереве** больше значения узла.  
- Оба поддерева также являются бинарными деревьями поиска.

---

## 2. Алгоритм вставки нового элемента в BST
**Пошагово:**
1. Начать с корня дерева.  
2. Если значение меньше значения текущего узла — перейти в левое поддерево.  
3. Если больше — перейти в правое поддерево.  
4. Когда достигнут `None` (пустое место), вставить новый узел туда.  
5. Рекурсивно вернуть обновлённое поддерево.

**Сложность:**
- В **сбалансированном дереве**: O(log n)  
- В **вырожденном дереве** (например, при вставке отсортированных данных): O(n)

---

## 3. Обход дерева в глубину (DFS) и в ширину (BFS)

**DFS (Depth-First Search)** — обход в глубину:
- Использует **стек** (рекурсия или структура данных).
- Обходит одну ветвь до конца, затем возвращается.
- Варианты:
  - **Pre-order** (корень → левое → правое) — используется для копирования дерева.
  - **In-order** (левое → корень → правое) — выдаёт значения в порядке возрастания.
  - **Post-order** (левое → правое → корень) — полезен при удалении дерева.

**BFS (Breadth-First Search)** — обход в ширину:
- Использует **очередь**.
- Обходит дерево **по уровням** (от корня к нижним узлам).
- Полезен для поиска кратчайшего пути или визуализации структуры дерева.

---

## 4. Почему в вырожденном BST сложность O(n)
Если элементы вставляются **в отсортированном порядке**, дерево превращается в **цепочку узлов**, где каждый элемент имеет только одного потомка.  
В результате глубина дерева равна `n`, и любая операция (вставка, поиск, удаление) требует обхода всех узлов.

---

## 5. Сбалансированное дерево и решение проблемы вырождения
**Сбалансированное дерево** — это BST, в котором разница высот левого и правого поддерева каждого узла **не превышает 1**.

**Пример: AVL-дерево**
- После каждой вставки или удаления выполняются **повороты**, чтобы восстановить баланс.
- Гарантирует высоту дерева O(log n).
- Благодаря этому, операции **вставки, удаления и поиска** всегда выполняются за O(log n), предотвращая вырождение структуры.





