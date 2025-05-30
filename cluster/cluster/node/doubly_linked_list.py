class Node:
    def __init__(self, value: str):
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def lpush(self, *values: str) -> int:
        for val in values:
            node = Node(val)
            if not self.head:
                self.head = self.tail = node
            else:
                node.next = self.head
                self.head.prev = node
                self.head = node
            self.size += 1
        return self.size

    def rpush(self, *values: str) -> int:
        for val in values:
            node = Node(val)
            if not self.tail:
                self.head = self.tail = node
            else:
                node.prev = self.tail
                self.tail.next = node
                self.tail = node
            self.size += 1
        return self.size

    def lrange(self, start: int, end: int) -> list[str]:
        values = []
        if end == -1:
            end = self.size - 1
        i = 0
        current = self.head
        while current and i <= end:
            if i >= start:
                values.append(current.value)
            current = current.next
            i += 1
        return values
