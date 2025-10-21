# main.py

import modules.perfomance_analysis as perf_test
from modules.hash_functions import simple_hash, polynomial_hash, djb2_hash
import modules.HistCollision as hist

perf_test.Visualisation(size=100000)

hist.Visualisation(simple_hash, func_name="Simple")
hist.Visualisation(polynomial_hash, func_name="Polynomial")
hist.Visualisation(djb2_hash, func_name="DJB2")

# Характеристики вычислительной машины
pc_info = """
Характеристики ПК для тестирования:
- Процессор: Intel Core i5-12500H @ 2.50GHz
- Оперативная память: 32 GB DDR4
- ОС: Windows 11
- Python: 3.12
"""
print(pc_info)
