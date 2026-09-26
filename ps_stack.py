class StackEmptyError(Exception):
    pass


class ArrayStack:
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
        return f"ArrayStack(bottom -> top): {self._items}"


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedStack:
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
        return f"LinkedStack(bottom -> top): {list(reversed(items))}"


if __name__ == "__main__":
    s = ArrayStack()
    for x in [10, 20, 30]:
        s.push(x)
        print(f"pushed {x} ->", s)
    print("peek:", s.peek())
    print("popped:", s.pop(), "->", s)

    ls = LinkedStack()
    for x in ["a", "b", "c"]:
        ls.push(x)
        print(f"pushed {x} ->", ls)
    print("peek:", ls.peek())
    print("popped:", ls.pop(), "->", ls)
