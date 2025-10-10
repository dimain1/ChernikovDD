

# Импорт необходимых библиотек
import matplotlib.pyplot as plt
import timeit


def linear_search(arr, target):
    """
    Линейный поиск элемента в массиве.
    Возвращает индекс target или -1, если не найден.
    Сложность: O(n), где n - длина массива.
    """
    for i in range(len(arr)):      # O(n) - проход по всем элементам
        if arr[i] == target:       # O(1) - сравнение
            return i               # O(1) - возврат индекса
    return -1                      # O(1) - если не найден
    # Общая сложность: O(n)


def binary_search(arr, target):
    """
    Бинарный поиск элемента в отсортированном массиве.
    Возвращает индекс target или -1, если не найден.
    Сложность: O(log n), где n - длина массива.
    """
    left = 0                       # O(1) - инициализация
    right = len(arr) - 1           # O(1) - инициализация
    while left <= right:           # O(log n) - деление диапазона
        mid = (left + right) // 2  # O(1) - вычисление середины
        if arr[mid] == target:     # O(1) - сравнение
            return mid             # O(1) - возврат индекса
        elif arr[mid] < target:    # O(1) - сравнение
            left = mid + 1         # O(1) - сдвиг границы
        else:
            right = mid - 1        # O(1) - сдвиг границы
    return -1                      # O(1) - если не найден
    # Общая сложность: O(log n)


sizes = [1000, 2000, 5000, 10000, 50000, 100000, 500000, 1000000]


def generate_test_data(sizes):
    """
    Генерирует отсортированные массивы заданных размеров и целевые элементы.
    Возвращает словарь: {size: {'array': [...], 'targets': {...}}}
    """
    data = {}
    for size in sizes:
        arr = list(range(size))
        targets = {
            'first': arr[0],
            'middle': arr[size // 2],
            'last': arr[-1],
            'absent': -1
        }
        data[size] = {'array': arr, 'targets': targets}
    return data


test_data = generate_test_data(sizes)


def measure_time(search_func, arr, target, repeat=10):
    """
    Замеряет среднее время выполнения функции поиска по массиву.
    Возвращает: float: Среднее время поиска (в миллисекундах)
    за repeat запусков.
    """
    times = []
    for _ in range(repeat):
        t = timeit.timeit(lambda: search_func(arr, target), number=1)
        times.append(t * 1000)
    return sum(times) / len(times)


# Новый способ хранения:
# для каждого алгоритма — словарь {size: [first, middle, last, absent]}
element_keys = ['first', 'middle', 'last', 'absent']
results_linear = {}
results_binary = {}
for size, info in test_data.items():
    arr = info['array']
    targets = info['targets']
    # Сохраняем времена в фиксированном порядке: [first, middle, last, absent]
    results_linear[size] = [
        measure_time(linear_search, arr, targets['first']),
        measure_time(linear_search, arr, targets['middle']),
        measure_time(linear_search, arr, targets['last']),
        measure_time(linear_search, arr, targets['absent'])
    ]
    results_binary[size] = [
        measure_time(binary_search, arr, targets['first']),
        measure_time(binary_search, arr, targets['middle']),
        measure_time(binary_search, arr, targets['last']),
        measure_time(binary_search, arr, targets['absent'])
    ]


def plot_results(sizes, results_linear, results_binary):
    """
    Рисует графики в нормальном формате и в логарифмическом по оси y
    В результате работы функции сохраняются два изображения в рабочую
    директорию
    """
    y_linear = [results_linear[size][2] for size in sizes]  # last
    y_binary = [results_binary[size][2] for size in sizes]  # last
    plt.plot(sizes, y_linear, marker='o', label='linear_search')
    plt.plot(sizes, y_binary, marker='o', label='binary_search')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (мс)')
    plt.title('Время поиска (последний элемент)')
    plt.legend()
    plt.grid(True)
    # plt.ticklabel_format(style='plain', axis='x')
    plt.savefig('./report/time_complexity_plot.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    # log scale
    plt.plot(sizes, y_linear, marker='o', label='linear_search')
    plt.plot(sizes, y_binary, marker='o', label='binary_search')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (мс, log scale)')
    plt.yscale('log')
    plt.title('Время поиска (логарифмическая шкала, последний элемент)')
    plt.legend()
    plt.grid(True)
    # plt.ticklabel_format(style='plain', axis='x')
    plt.savefig('./report/time_complexity_plot_log.png',
                dpi=300, bbox_inches='tight')
    plt.show()


plot_results(sizes, results_linear, results_binary)

# Характеристики вычислительной машины
pc_info = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
"""
print(pc_info)
