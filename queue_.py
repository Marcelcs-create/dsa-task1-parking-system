"""
queue_.py
---------
(named queue_.py to avoid clashing with Python's built-in `queue` module)

Two implementations of the Queue Abstract Data Type (FIFO: First In, First Out).

1. ArrayQueue  -> backed by collections.deque (a dynamic array-like structure
                  optimised for O(1) operations at BOTH ends)
2. LinkedQueue -> backed by a singly linked list with head + tail pointers

Both expose the same interface:
    enqueue(item) -> add item to the back of the queue
    dequeue()     -> remove and return the item at the front
    front()       -> look at the front item without removing it
    is_empty()    -> True if the queue has no items
    size()        -> number of items currently in the queue
"""

from collections import deque


class QueueEmptyError(Exception):
    """Raised when dequeue() or front() is called on an empty queue."""
    pass


class ArrayQueue:
    """
    Queue implemented on top of collections.deque.

    Why deque instead of a plain list?
    - A plain Python list is O(n) for pop(0)/insert(0, x) because every
      remaining element has to shift.
    - deque is a doubly linked list of blocks under the hood, giving O(1)
      appends/removals at BOTH ends -- exactly what a queue needs
      (enqueue at the back, dequeue at the front).
    """

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)          # add to the back

    def dequeue(self):
        if self.is_empty():
            raise QueueEmptyError("dequeue from an empty queue")
        return self._items.popleft()      # remove from the front

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
    """A single node in the linked list used by LinkedQueue."""
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedQueue:
    """
    Queue implemented on top of a singly linked list with head (front)
    and tail (back) pointers.

    Why a linked list here?
    - Keeping a tail pointer means enqueue() is O(1) (attach after tail).
    - head pointer means dequeue() is O(1) (detach from head).
    - No resizing/shifting is ever needed, and memory grows one node
      at a time -- good when the queue length is unpredictable
      (e.g. a variable-length line of cars waiting for a parking slot).
    """

    def __init__(self):
        self._head = None   # front of the queue
        self._tail = None   # back of the queue
        self._size = 0

    def enqueue(self, item):
        node = _Node(item)
        if self._tail is None:            # queue was empty
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
        if self._head is None:            # queue became empty
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
    print("-- ArrayQueue demo --")
    q = ArrayQueue()
    for x in ["car1", "car2", "car3"]:
        q.enqueue(x)
        print(f"enqueued {x} ->", q)
    print("front:", q.front())
    print("dequeued:", q.dequeue(), "->", q)

    print("\n-- LinkedQueue demo --")
    lq = LinkedQueue()
    for x in ["car1", "car2", "car3"]:
        lq.enqueue(x)
        print(f"enqueued {x} ->", lq)
    print("front:", lq.front())
    print("dequeued:", lq.dequeue(), "->", lq)
