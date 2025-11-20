# Отчет по лабораторной работе 11

# Алгоритмы на строках

**Дата:** 2025-11-20
**Семестр:** 3 курс 5 семестр
**Группа:** ПИЖ-б-о-23-2(1)
**Дисциплина:** Анализ сложности алгоритмов
**Студент:** Черников Дмитрий Дмитриевич

## Цель работы

Изучить специализированные алгоритмы для эффективной работы со строками. Освоить методы поиска подстрок, вычисление префикс-функции и Z-функции. Получить практические навыки реализации и анализа алгоритмов обработки строк, исследовать их производительность.

## Практическая часть

### Выполненные задачи

- [ ] Реализовать вычисление префикс-функции для строки.
- [ ] Реализовать алгоритм Кнута-Морриса-Пратта для поиска подстроки.
- [ ] Реализовать вычисление Z-функции.
- [ ] Реализовать один из дополнительных алгоритмов поиска подстроки.
- [ ] Провести сравнительный анализ эффективности алгоритмов на различных данных.

### Ключевые фрагменты кода

```PYTHON
# prefix_function.py

def prefix_function(string):
    """
    Вычисляет префикс-функцию для заданной строки.
    Args:
        string (str): Входная строка.
    Returns:
        list: Список префикс-функций для каждого префикса строки.
    """
    n = len(string)
    prefixs = [0] * n
    for i in range(1, n):
        j = prefixs[i - 1]
        while j > 0 and string[i] != string[j]:
            j = prefixs[j - 1]
        if string[i] == string[j]:
            j += 1
        prefixs[i] = j
    return prefixs
# Время: O(n)
# Память: O(n)
```

```PYTHON
# kmp_search.py

from modules.prefix_function import prefix_function
# from src.modules.prefix_function import prefix_function  # tests


def kmp_search(pattern, text):
    """
    Выполняет поиск всех вхождений шаблона в текст
    с помощью алгоритма Кнута-Морриса-Пратта (КМП).
    Args:
        pattern (str): Шаблон для поиска.
        text (str): Текст, в котором выполняется поиск.
    Returns:
        list: Список начальных индексов всех вхождений шаблона в текст.
    """
    prefixs = prefix_function(pattern)
    m = len(pattern)
    n = len(text)
    j = 0
    occurrences = []

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = prefixs[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            occurrences.append(i - m + 1)
            j = prefixs[j - 1]

    return occurrences
# Время: O(n + m)
# Память: O(m)
# В худшем случае O(n * m)
# Худший случай возникает при большом количестве
# совпадающих префиксов между шаблоном и текстом.
# Например, при поиске шаблона "aaaa" в тексте "aaaaaaaa".


def naive_search(pattern, text):
    """
    Выполняет наивный поиск всех вхождений шаблона в текст.
    Args:
        pattern (str): Шаблон для поиска.
        text (str): Текст, в котором выполняется поиск.
    Returns:
        list: Список начальных индексов всех вхождений шаблона в текст.
    """
    m = len(pattern)
    n = len(text)
    occurrences = []

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(i)

    return occurrences
# Время: O(n * m) в худшем случае
# Память: O(1)

```

```PYTHON
# z-function.py

def z_function(string):
    """
    Вычисляет Z-функцию для заданной строки.
    Args:
        string (str): Входная строка.
    Returns:
        list: Список Z-функций для каждого префикса строки.
    """
    n = len(string)
    z = [0] * n
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and string[z[i]] == string[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z
# Время: O(n)
# Память: O(n)


def find_substring_z(pattern, text):
    """
    Выполняет поиск всех вхождений шаблона в текст
    с помощью Z-функции.
    Args:
        pattern (str): Шаблон для поиска.
        text (str): Текст, в котором выполняется поиск.
    Returns:
        list: Список начальных индексов всех вхождений шаблона в текст.
    """
    combined = pattern + "$" + text
    z = z_function(combined)
    m = len(pattern)
    occurrences = []

    for i in range(len(z)):
        if z[i] == m:
            occurrences.append(i - m - 1)

    return occurrences
# Время: O(n + m)
# Память: O(n + m)
# В худшем случае O(n * m)
# Худший случай возникает при большом количестве
# совпадающих префиксов между шаблоном и текстом.
# Например, при поиске шаблона "aaaa" в тексте "aaaaaaaa".

```

```PYTHON
# boier_mura.py

def boier_mura(pattern, text):
    """
    Выполняет поиск всех вхождений шаблона в текст
    с помощью алгоритма Бойера-Мура.
    Args:
        pattern (str): Шаблон для поиска.
        text (str): Текст, в котором выполняется поиск.
    Returns:
        list: Список начальных индексов всех вхождений шаблона в текст.
    """

    m = len(pattern)
    n = len(text)
    if m == 0 or n == 0 or m > n:
        return []

    # Создание таблицы смещений для символов
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    occurrences = []
    s = 0  # сдвиг шаблона относительно текста
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            occurrences.append(s)
            s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))

    return occurrences
# Время: O(n) в среднем случае
# Особенности: 
# Сравнение справа налево
# Использование таблицы плохих символов для оптимизации сдвигов
# Память: O(k), где k - размер алфавита
# Оптимален для больших алфавитов и длинных шаблонов
# В худшем случае O(n * m)
# Худший случай возникает при большом количестве
# совпадающих символов между шаблоном и текстом.
# Например, при поиске шаблона "aaaa" в тексте "aaaaaaaa".


```

```PYTHON
# perfomance_analysis.py

from modules.kmp_search import kmp_search, naive_search
from modules.z_function import find_substring_z
from modules.boier_mura import boier_mura
import timeit
from matplotlib import pyplot as plt

# График сравнения алгоритмов фиксированный паттерн, но увеличение текста
# График сравнения алгоритмов фиксированный текст, но увеличение паттерна


def generate_random_string(size):
    """
    Генерирует случайную строку заданного размера.
    Args:
        size: Размер строки.
    Returns:
        str: Случайная строка.
    """
    alphabet = 'abcde'
    import random
    return ''.join(random.choices(alphabet, k=size))


def measure_time_fix_pat(size, pat_size=25):
    """
    Измеряет время выполнения алгоритмов при фиксированном размере паттерна
    и изменяющемся размере текста.
    Args:
        size: Размер текста.
        pat_size: Размер паттерна.
    Returns:
        tuple: Времена выполнения для каждого алгоритма.
    """
    text = generate_random_string(size)
    pattern = generate_random_string(pat_size)

    kmp_time = timeit.timeit(lambda: kmp_search(pattern, text), number=10)
    naive_time = timeit.timeit(lambda: naive_search(pattern, text), number=10)
    z_time = timeit.timeit(lambda: find_substring_z(pattern, text), number=10)
    boier_mura_time = timeit.timeit(
        lambda: boier_mura(pattern, text), number=10)

    return (kmp_time * 1000, naive_time * 1000,
            z_time * 1000, boier_mura_time * 1000)


def measure_time_fix_text(pat_sizes, size=100000):
    """
    Измеряет время выполнения алгоритмов при фиксированном размере текста
    и изменяющемся размере паттерна.
    Args:
        pat_sizes: Размер паттерна.
        size: Размер текста.
    Returns:
        tuple: Времена выполнения для каждого алгоритма."""
    text = generate_random_string(size)
    pattern = generate_random_string(pat_sizes)

    kmp_time = timeit.timeit(lambda: kmp_search(pattern, text), number=10)
    naive_time = timeit.timeit(lambda: naive_search(pattern, text), number=10)
    z_time = timeit.timeit(lambda: find_substring_z(pattern, text), number=10)
    boier_mura_time = timeit.timeit(
        lambda: boier_mura(pattern, text), number=10)

    return (kmp_time * 1000, naive_time * 1000,
            z_time * 1000, boier_mura_time * 1000)


def Visualisation(Sizes, pat_sizes):
    """
    Визуализирует результаты измерений времени выполнения алгоритмов.
    Args:
        Sizes: Список размеров текста.
        pat_sizes: Список размеров паттерна.
    """
    kmp_times_fix_pat = []
    naive_times_fix_pat = []
    z_times_fix_pat = []
    boier_mura_times_fix_pat = []

    for size in Sizes:
        kmp_time, naive_time, z_time, boier_mura_time = measure_time_fix_pat(
            size)
        kmp_times_fix_pat.append(kmp_time)
        naive_times_fix_pat.append(naive_time)
        z_times_fix_pat.append(z_time)
        boier_mura_times_fix_pat.append(boier_mura_time)

    print("Measures for fixed pattern size:")
    print("Sizes:", Sizes)
    print("KMP times:", kmp_times_fix_pat)
    print("Naive times:", naive_times_fix_pat)
    print("Z-Function times:", z_times_fix_pat)
    print("Boier-Mura times:", boier_mura_times_fix_pat)

    plt.figure(figsize=(12, 6))
    plt.plot(Sizes, kmp_times_fix_pat, label='KMP Search')
    plt.plot(Sizes, naive_times_fix_pat, label='Naive Search')
    plt.plot(Sizes, z_times_fix_pat, label='Z-Function Search')
    plt.plot(Sizes, boier_mura_times_fix_pat, label='Boier-Mura Search')
    plt.xlabel('Size of Text')
    plt.ylabel('Time (mseconds)')
    plt.title('Performance Comparison (Fixed Pattern Size)')
    plt.legend()
    plt.grid()
    plt.show()

    kmp_times_fix_text = []
    naive_times_fix_text = []
    z_times_fix_text = []
    boier_mura_times_fix_text = []

    for pat_size in pat_sizes:
        kmp_time, naive_time, z_time, boier_mura_time = measure_time_fix_text(
            pat_size)
        kmp_times_fix_text.append(kmp_time)
        naive_times_fix_text.append(naive_time)
        z_times_fix_text.append(z_time)
        boier_mura_times_fix_text.append(boier_mura_time)

    print("Measures for fixed text size:")
    print("Pattern Sizes:", pat_sizes)
    print("KMP times:", kmp_times_fix_text)
    print("Naive times:", naive_times_fix_text)
    print("Z-Function times:", z_times_fix_text)
    print("Boier-Mura times:", boier_mura_times_fix_text)

    plt.figure(figsize=(12, 6))
    plt.plot(pat_sizes, kmp_times_fix_text, label='KMP Search')
    plt.plot(pat_sizes, naive_times_fix_text, label='Naive Search')
    plt.plot(pat_sizes, z_times_fix_text, label='Z-Function Search')
    plt.plot(pat_sizes, boier_mura_times_fix_text, label='Boier-Mura Search')
    plt.xlabel('Size of Pattern')
    plt.ylabel('Time (mseconds)')
    plt.title('Performance Comparison (Fixed Text Size)')
    plt.legend()
    plt.grid()
    plt.show()

```

```PYTHON
# string_matching.py

from modules.prefix_function import prefix_function
from modules.kmp_search import kmp_search


def find_period(string):
    """
    Находит минимальный период строки с помощью префикс-функции.
    Args:
        string (str): Входная строка.
    Returns:
        int: Длина минимального периода строки.
    """
    n = len(string)
    prefixs = prefix_function(string)
    period_length = n - prefixs[-1]
    if n % period_length == 0:
        return period_length
    else:
        return n


def cyclic_shift(a, b):
    """
    Проверяет, является ли строка b циклическим сдвигом строки a.
    Args:
        a (str): Первая строка.
        b (str): Вторая строка.
    Returns:
        bool: True, если b является циклическим сдвигом a, иначе False.
    """
    if kmp_search(a, b+b):
        return True
    return False

# def is_cyclic_shift(a, b):
#     """
#     Проверяет, является ли строка b циклическим сдвигом строки a.
#     Args:
#         a (str): Первая строка.
#         b (str): Вторая строка.
#     Returns:
#         bool: True, если b является циклическим сдвигом a, иначе False.
#     """
#     if len(a) != len(b):
#         return False
#     return b in (a + a)


# print(is_cyclic_shift("abcd", "cdab"))  # True
# print(is_cyclic_shift("abcd", "acbd"))  # False

```

```PYTHON
# main.py

from modules.kmp_search import kmp_search, naive_search
from modules.prefix_function import prefix_function
from modules.z_function import z_function, find_substring_z
from modules.boier_mura import boier_mura
from modules.perfomance_analysis import Visualisation
from modules.string_matching import find_period, cyclic_shift

string = "acabababcababc"
pattern = "abcab"

print("String:", string)
print("Pattern:", pattern)

print("\nPrefix Function:", prefix_function(string))

print("kpm_search occurrences:", kmp_search(pattern, string))

print("naive_search occurrences:", naive_search(pattern, string))

print("Z-Function:", z_function(string))
print("find_substring_using_z_function occurrences:",
      find_substring_z(pattern, string))

print("boier_mura occurrences:", boier_mura(pattern, string))

# Performance Analysis Visualization
Sizes = [100, 500, 1000, 5000, 10000, 20000, 50000, 100000, 200000]
pat_sizes = [5, 10, 20, 50, 100, 200, 500, 1000]
Visualisation(Sizes, pat_sizes)

string_for_period = "abcabcabcabc"
period_length = find_period(string_for_period)
print(f"\nString for period finding: {string_for_period}")
print("prefix_function:", prefix_function(string_for_period))
print(f"Minimal period length: {period_length}")

a = "abcd"
b = "cdab"
print(f"\nIs '{b}' a cyclic shift of '{a}'? {cyclic_shift(a, b)}")

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

<image src="./report/fix_pattern.png" style="display:block; margin: auto;">
<image src="./report/fix_text.png" style="display:block; margin: auto;">


```bash
String: acabababcababc
Pattern: abcab

Prefix Function: [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0]
kpm_search occurrences: [6]
naive_search occurrences: [6]
Z-Function: [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0]
find_substring_using_z_function occurrences: [6]
boier_mura occurrences: [6]
Measures for fixed pattern size:
Sizes: [1000, 5000, 10000, 20000, 50000, 100000, 200000]
KMP times: [1.288700004806742, 7.293800008483231, 16.63630000257399, 55.00239999673795, 84.64280000771396, 159.13429998909123, 221.15489999123383]
Naive times: [2.260499997646548, 15.161400006036274, 35.1857000059681, 69.57019999390468, 154.40939999825787, 353.42640000453684, 396.25610000803135]
Z-Function times: [3.973700004280545, 22.341399992001243, 69.80149999435525, 84.1286999930162, 254.75510000251234, 424.5111999916844, 668.8711000024341]
Boier-Mura times: [0.9714999905554578, 5.2900000009685755, 19.025100002181716, 18.841800003428943, 30.07949999300763, 52.363700000569224, 89.42560000286903]
Measures for fixed text size:
Pattern Sizes: [5, 10, 20, 50, 100, 200, 500]
KMP times: [109.43070000212174, 97.92770000058226, 106.70200000458863, 107.66250001324806, 107.7281000034418, 107.94760000135284, 113.26480000570882]
Naive times: [150.75739999883808, 190.40590000804514, 206.81420000619255, 200.74629998998716, 199.87830000172835, 205.90650000667665, 221.96969999640714]
Z-Function times: [231.9595000008121, 326.68420000118203, 322.9845000023488, 329.4308999902569, 335.71100000699516, 331.6437000030419, 333.3656000031624]
Boier-Mura times: [54.97530000866391, 106.96350000216626, 86.54309999838006, 51.632300004712306, 77.68119999673218, 121.90510000800714, 38.74419999192469]

String for period finding: abcabcabcabc
prefix_function: [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Minimal period length: 3

Is 'cdab' a cyclic shift of 'abcd'? True

Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12

```

## Эффективность алгоритмов

| Алгоритм          | Худшее время | Среднее время | Лучшая время | Память | Примечания |
|------------------|--------------|---------------|--------------|--------|------------|
| Naive search      | O((n - m + 1) * m) | O((n - m + 1) * m) | O(n) | O(1) | Простая реализация, перебор всех позиций |
| KMP (Knuth-Morris-Pratt) | O(n * m) | O(n + m) | O(n + m) | O(m) | Использует префикс-функцию, избегает повторного сравнения |
| Z-function        | O(n * m) | O(n + m) | O(n + m) | O(n + m) | Вычисляется Z-массив, эффективен для поиска всех вхождений |
| Boyer-Moore       | O(n * m) | O(n / m) (на практике ≈ O(n)) | O(n / m) | O(k) | Использует эвристику смещения по плохому символу и хорошему суффиксу, очень быстрый на больших алфавитах |


Давай разберём влияние разных характеристик строк на производительность алгоритмов поиска подстроки. Я буду ориентироваться на таблицу с алгоритмами `Naive`, `KMP`, `Z-function`, `Boyer-Moore`.

## Анализ влияние характеристик строк на производительность 



| Характеристика строки        | Naive search                   | KMP (Knuth-Morris-Pratt)       | Z-function                     | Boyer-Moore                    |
|-------------------------------|--------------------------------|--------------------------------|--------------------------------|--------------------------------|
| Длина текста (n)             | Время растёт почти пропорционально n * m | Линейно O(n + m)               | Линейно O(n + m)               | На практике почти линейно, может замедляться при частых совпадениях |
| Длина шаблона (m)            | Прямое влияние на количество сравнений | Строится префикс-функция O(m), поиск O(n) | Зависит от m, затраты увеличиваются | Длинный шаблон часто ускоряет поиск (большие смещения) |
| Размер алфавита               | Почти не влияет                | Почти не влияет                | Почти не влияет                | Большой алфавит → быстрый поиск, малый → потенциально медленнее |
| Повторяющиеся подстроки       | Худший случай: много проверок  | Эффективно благодаря префикс-функции | Эффективно, Z-массив учитывает повторы | Может снизить эффективность эвристик, особенно при совпадении конца шаблона |
| Распределение символов        | Редкие совпадения — мало ускорения | Практически не влияет          | Практически не влияет          | Редкие совпадения → быстрый поиск, частые совпадения → замедление |

## Оптимальные области применения

| Алгоритм          | Оптимальная область применения |
|------------------|-------------------------------|
| Naive search      | Короткие тексты и шаблоны; одноразовый поиск; когда важна простота реализации и не критична скорость. |
| KMP (Knuth-Morris-Pratt) | Длинные тексты с потенциальными повторяющимися подстроками; шаблоны со сложной структурой; когда нужно стабильное линейное время независимо от структуры текста. |
| Z-function        | Поиск всех вхождений шаблона; обработка повторяющихся подстрок; задачи типа «поиск периодов строки» или «сжатие/анализ текста». |
| Boyer-Moore       | Большие тексты и длинные шаблоны; тексты с большим алфавитом; когда в среднем шаблон встречается редко и важна максимальная практическая скорость поиска. |

# Ответы на контрольные вопросы

### 1. Префикс-функция строки и использование в KMP

**Префикс-функция** строки `s` длины `n` — это массив `π` длины `n`, где `π[i]` равен длине **наибольшего собственного префикса** строки `s[0..i]`, который одновременно является её суффиксом. "Собственный" означает, что префикс не совпадает со всей строкой.

**Пример:**
Для строки `s = "ababc"`:

* `π[0] = 0` (нет префикса)
* `π[1] = 0` (`a` ≠ `b`)
* `π[2] = 1` (`a` совпадает с `a`)
* `π[3] = 2` (`ab` совпадает с `ab`)
* `π[4] = 0`

**Использование в KMP:**
Префикс-функция позволяет **избегать повторного сравнения уже проверенных символов** при несовпадении. Когда сравнение шаблона с текстом даёт несоответствие, KMP сдвигает шаблон на длину, определяемую префикс-функцией, не проверяя символы, которые уже совпали.

---

### 2. Преимущество KMP перед наивным алгоритмом

| Критерий             | Наивный поиск               | KMP                            |
| -------------------- | --------------------------- | ------------------------------ |
| Худшее время         | O((n - m + 1) * m)          | O(n + m)                       |
| Количество сравнений | Много повторяющихся         | Минимально, не повторяются     |
| Стабильность         | Зависит от структуры текста | Линейная, независимо от текста |

**Пример:**
Текст: `"aaaaab"`
Шаблон: `"aaab"`

* **Наивный поиск:** проверяет почти все позиции, много повторных сравнений `"aaa..."`.
* **KMP:** использует префикс-функцию, при несоответствии сразу сдвигается, пропуская проверку уже совпавших `"aa"`.

---

### 3. Z-функция строки и использование для поиска подстроки

**Z-функция** строки `s` длины `n` — это массив `Z[0..n-1]`, где `Z[i]` — длина наибольшего префикса строки `s[i..n-1]`, совпадающего с префиксом `s`.

**Применение для поиска подстроки:**
Для поиска шаблона `p` в тексте `t` создают строку `s = p + "$" + t`, где `$` — символ-разделитель. Затем вычисляют Z-функцию для `s`. Если `Z[i] == len(p)`, значит шаблон полностью совпал с текстом на позиции `i - len(p) - 1`.

---

### 4. Идея алгоритма Бойера-Мура

**Идея:**
Boyer-Moore сравнивает шаблон с текстом **справа налево**. При несовпадении алгоритм сдвигает шаблон **не на один символ**, а на большее расстояние, используя информацию о тексте и шаблоне.

**Эвристики ускорения:**

1. **Bad character** (плохой символ) — сдвигаем шаблон так, чтобы последний несовпавший символ текста совпадал с правой копией этого символа в шаблоне (если есть).
2. **Good suffix** (хороший суффикс) — если часть шаблона совпала, сдвигаем шаблон так, чтобы совпавший суффикс наложился на его следующее вхождение в шаблоне.

---

### 5. Практические задачи применения префикс- и Z-функций

* **Поиск периода строки:** определить наименьший повторяющийся блок в строке.
* **Поиск всех вхождений подстрок** в текстах и геномах.
* **Анализ текстов и сжатие данных:** нахождение повторяющихся фрагментов.
* **Синтаксический анализ:** проверка шаблонов или структур в коде и тексте.
* **Сравнение строк и нахождение LCP (Longest Common Prefix)** в массивах строк.

---
