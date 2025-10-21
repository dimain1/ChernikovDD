# perfomance_analysis.py

from modules.hash_table_chaining import Chaining_HashTable
from modules.hash_table_open_addressing import Linear_HashTable
from modules.hash_table_open_addressing import DoubleHashingHashTable
import random
import string
import timeit
import matplotlib.pyplot as plt


def generate_random_string_loop(length):
    """
    Генерирует рандомную строку длины length
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
    """
    measures = []
    for j in range(20):
        table = Chaining_HashTable(initial_size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
        measures.append((end - start) * 1000)
    return sum(measures) // 20


def get_time_for_linear(load, size, strings):
    """
    Вычисляет среднее время вставкии в хеш таблицу
    открытой адресации линейной пробации
    """
    measures = []
    for j in range(20):
        table = Linear_HashTable(size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
    measures.append((end - start) * 1000)
    return sum(measures) // 20


def get_time_for_double(load, size, strings):
    """
    Вычисляет среднее время вставкии в хеш таблицу
    открытой адресации двойного хеширования
    """
    measures = []
    for j in range(20):
        table = DoubleHashingHashTable(size=size, load=load)
        start = timeit.default_timer()
        for i in range(size):
            table.insert(strings[i], i)
        end = timeit.default_timer()
    measures.append((end - start) * 1000)
    return sum(measures) // 20


def measure_time(loades=[0.1, 0.5, 0.7, 0.9], size=1000):
    """
    Собирает результаты времени выполнения в словарь вида
    ["метод реализации"] - [список значений времени выполнения]
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


def Visualisation(loades=[0.1, 0.5, 0.7, 0.9], size=1000):
    """
    Визуализирует графики зависимости времени выполнения от
    коэффициента заполнения
    """
    measures = measure_time(loades=loades, size=size)
    chained_list = measures["chain"]
    linear_list = measures["linear"]
    double_list = measures["double"]

    Create_plot(chained_list, loades,
                "графики зависимости времени операций от коэффициента заполнения",
                "./report/chained_hashtable.png", label="chain")
    Create_plot(linear_list, loades,
                "графики зависимости времени операций от коэффициента заполнения",
                "./report/linear_hashtable.png", label="linear")
    Create_plot(double_list, loades,
                "графики зависимости времени операций от коэффициента заполнения",
                "./report/double_hashtable.png", label="double")


def Create_plot(data, sizes, title, path, label):
    """
    Строит и сохраняет график времени работы сортировок для одного типа данных.
    Аргументы:
        data: словарь {название метода: список времени}.
        sizes: список размеров массивов.
        title: строка — заголовок графика.
        path: строка — путь для сохранения PNG-файла.
    Возвращает:
        None. Сохраняет график и отображает его.
    """
    plt.plot(sizes, data,
             marker="o", color="red", label=label)

    plt.xlabel("коэффициент заполнения")
    plt.ylabel("Время выполнения ms")
    plt.title(title)
    plt.legend(loc="upper left", title="Метод")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.show()
