from stack import ArrayStack, LinkedStack
from queue_ import ArrayQueue, LinkedQueue
from factorial_stack import (
    factorial_explicit_stack,
    factorial_recursive,
    factorial_iterative,
)
from parking_demo import ParkingLot


def demo_stack():
    print("\n--- Stack demo (ArrayStack) ---")
    s = ArrayStack()
    for x in [10, 20, 30]:
        s.push(x)
        print(f"push({x}) ->", s)
    print("peek() ->", s.peek())
    print("pop()  ->", s.pop(), "->", s)

    print("\n--- Stack demo (LinkedStack) ---")
    ls = LinkedStack()
    for x in ["a", "b", "c"]:
        ls.push(x)
        print(f"push({x!r}) ->", ls)
    print("peek() ->", ls.peek())
    print("pop()  ->", ls.pop(), "->", ls)


def demo_queue():
    print("\n--- Queue demo (ArrayQueue) ---")
    q = ArrayQueue()
    for x in ["car1", "car2", "car3"]:
        q.enqueue(x)
        print(f"enqueue({x!r}) ->", q)
    print("front() ->", q.front())
    print("dequeue() ->", q.dequeue(), "->", q)

    print("\n--- Queue demo (LinkedQueue) ---")
    lq = LinkedQueue()
    for x in ["car1", "car2", "car3"]:
        lq.enqueue(x)
        print(f"enqueue({x!r}) ->", lq)
    print("front() ->", lq.front())
    print("dequeue() ->", lq.dequeue(), "->", lq)


def demo_factorial():
    print("\n--- Factorial via Stack ---")
    n = 6
    print(f"n = {n}")
    print("explicit stack ->", factorial_explicit_stack(n))
    print("recursive (call stack) ->", factorial_recursive(n))
    print("iterative (no stack) ->", factorial_iterative(n))


def demo_parking():
    print("\n--- Parking system demo (Stack + Queue applied) ---")
    lot = ParkingLot(total_slots=2)
    lot.vehicle_arrives("KDA 001A")
    lot.vehicle_arrives("KDB 002B")
    lot.vehicle_arrives("KDC 003C")
    lot.vehicle_arrives("KDD 004D")
    lot.undo_last_entry()
    lot.vehicle_exits()


MENU = """
=====================================================
 DSA Task One - Parking System Practical
=====================================================
 1. Stack demo (array-based + linked-list-based)
 2. Queue demo (array-based + linked-list-based)
 3. Factorial using a Stack
 4. Parking system demo (Stack + Queue applied)
 5. Run ALL demos
 0. Exit
=====================================================
"""


def main():
    actions = {
        "1": demo_stack,
        "2": demo_queue,
        "3": demo_factorial,
        "4": demo_parking,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "5":
            for action in actions.values():
                action()
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
