"""
stack.py
--------
Two implementations of the Stack Abstract Data Type (LIFO: Last In, First Out).

1. ArrayStack  -> backed by a Python list (dynamic array)
2. LinkedStack -> backed by a singly linked list

Both expose the same interface, so either can be swapped in wherever
a "Stack" is needed:
    push(item)   -> add item to the top
    pop()        -> remove and return the top item
    peek()       -> look at the top item without removing it
    is_empty()   -> True if the stack has no items
    size()       -> number of items currently in the stack
"""


class StackEmptyError(Exception):
    """Raised when pop() or peek() is called on an empty stack."""
    pass


class ArrayStack:
    """
    Stack implemented on top of a Python list.

    Why an array/list here?
    - Appending/removing from the END of a list is O(1) amortised.
    - Simple, cache-friendly, and exactly matches how a stack behaves:
      the "top" of the stack is the end of the list.
    """

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise StackEmptyError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        # Show bottom -> top, with the top marked
        return f"ArrayStack(bottom -> top): {self._items}"


class _Node:
    """A single node in the linked list used by LinkedStack."""
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedStack:
    """
    Stack implemented on top of a singly linked list.

    Why a linked list here?
    - push()/pop() only ever touch the HEAD of the list -> O(1), no
      resizing/copying like a dynamic array occasionally needs.
    - Memory is allocated one node at a time, so there's no wasted
      pre-allocated capacity. Useful when stack size is unpredictable.
    """

    def __init__(self):
        self._head = None
        self._size = 0

    def push(self, item):
        self._head = _Node(item, self._head)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("pop from an empty stack")
        node = self._head
        self._head = node.next
        self._size -= 1
        return node.value

    def peek(self):
        if self.is_empty():
            raise StackEmptyError("peek at an empty stack")
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
        # items is currently top -> bottom; reverse for bottom -> top
        return f"LinkedStack(bottom -> top): {list(reversed(items))}"


if __name__ == "__main__":
    print("-- ArrayStack demo --")
    s = ArrayStack()
    for x in [10, 20, 30]:
        s.push(x)
        print(f"pushed {x} ->", s)
    print("peek:", s.peek())
    print("popped:", s.pop(), "->", s)

    print("\n-- LinkedStack demo --")
    ls = LinkedStack()
    for x in ["a", "b", "c"]:
        ls.push(x)
        print(f"pushed {x} ->", ls)
    print("peek:", ls.peek())
    print("popped:", ls.pop(), "->", ls)
