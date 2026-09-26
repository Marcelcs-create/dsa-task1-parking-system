from collections import deque


class QueueEmptyError(Exception):
    pass


class ArrayQueue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise QueueEmptyError("dequeue from an empty queue")
        return self._items.popleft()

    def front(self):
        if self.is_empty():
            raise QueueEmptyError("front of an empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"ArrayQueue(front -> back): {list(self._items)}"


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedQueue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        node = _Node(item)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise QueueEmptyError("dequeue from an empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def front(self):
        if self.is_empty():
            raise QueueEmptyError("front of an empty queue")
        return self._head.value

    def is_empty(self):
        return self._head is None

    def size(self):
        return self._size

    def __str__(self):
        items = []
        node = self._head
        while node:
            items.append(node.value)
            node = node.next
        return f"LinkedQueue(front -> back): {items}"


if __name__ == "__main__":
    q = ArrayQueue()
    for x in ["car1", "car2", "car3"]:
        q.enqueue(x)
        print(f"enqueued {x} ->", q)
    print("front:", q.front())
    print("dequeued:", q.dequeue(), "->", q)

    lq = LinkedQueue()
    for x in ["car1", "car2", "car3"]:
        lq.enqueue(x)
        print(f"enqueued {x} ->", lq)
    print("front:", lq.front())
    print("dequeued:", lq.dequeue(), "->", lq)
