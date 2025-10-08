

class Node:
    """
    Класс узла односвязного списка.
    Аргументы:
        value: Значение, хранимое в узле.
        next: Ссылка на следующий узел (или None).
    """

    def __init__(self, value, next):
        """
        Инициализация узла.
        value: Значение узла.
        next: Следующий узел (Node) или None.
        """
        self.value = value
        self.next = next


class LinkedList:
    """
    Класс односвязного списка.
    Содержит методы для вставки, удаления и обхода элементов.
    """

    def __init__(self):
        """
        Инициализация пустого списка.
        head: Ссылка на последний добавленный элемент (конец списка).
        tail: Ссылка на первый элемент (начало списка).
        """
        self.head = None
        self.tail = None

    def insert_at_start(self, value):
        """
        Вставляет новый элемент в начало (head) односвязного списка.
        Если список пуст, новый элемент становится и head, и tail.
        Аргументы:
            value: Значение, которое будет храниться в новом узле.
        Время выполнения: O(1)
        """
        if (self.head is None and self.tail is None):   # 1
            temp = Node(value, None)    # 1
            self.head = temp    # 1
            self.tail = temp    # 1
        else:
            temp = Node(value, self.tail)   # 1
            self.tail = temp    # 1
    # O(1)

    def insert_at_end(self, value):
        """
        Вставляет новый элемент в конец (tail) односвязного списка.
        Если список пуст, новый элемент становится и head, и tail.
        Аргументы:
            value: Значение, которое будет храниться в новом узле.
        Время выполнения: O(1)
        """
        if (self.head is None and self.tail is None):   # 1
            temp = Node(value, None)    # 1
            self.head = temp    # 1
            self.tail = temp    # 1
        else:
            temp = Node(value, None)    # 1
            self.head.next = temp   # 1
            self.head = temp    # 1
    # O(1)

    def delete_from_start(self):
        """
        Удаляет элемент из начала (tail) односвязного списка.
        Если список пуст, возбуждается исключение.
        Время выполнения: O(1)
        """
        if (self.head is None):  # 1
            raise Exception("Linked_List empty")    # 1
        elif (self.head == self.tail):  # 1
            self.head = None    # 1
            self.tail = None    # 1
        else:
            self.tail = self.tail.next  # 1
    # O(1)

    def traversal(self):
        """
        Обходит односвязный список с начала (tail) до конца (head)
        и выводит значения элементов.
        Если список пуст, выводит сообщение.
        Время выполнения: O(N)
        """
        if (self.head is None):  # 1
            print("Linked_List empty")  # 1
        else:
            current = self.tail  # 1
            while (True):   # O(N)
                print(current.value)    # 1
                if (current.next is None):  # 1
                    break
                current = current.next  # 1
    # O(N)
