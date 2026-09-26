# DSA Task One – Automated Parking System

Multimedia University of Kenya — Data Structures and Algorithms, Task One.

## Brief

Design a modern automated parking system for a client in Kenya: a visual
display of available slots before entry, automatic vehicle recording on
arrival, automatic fee calculation on exit (based on time parked), and a
barrier that opens once the fee is paid.

## Contents

| File | Description |
|---|---|
| `Parking_System_Task1.docx` | Full write-up: proposed modules, algorithm (pseudocode) for each module, data structures with justification, and a dynamic database design with ER diagram |
| `stack.py` | Stack ADT — array-based (`ArrayStack`) and linked-list-based (`LinkedStack`) implementations |
| `queue_.py` | Queue ADT — array/deque-based (`ArrayQueue`) and linked-list-based (`LinkedQueue`) implementations |
| `factorial_stack.py` | Factorial computed via an explicit stack, a recursive call stack, and iteratively — for the practical session on stack applications |
| `parking_demo.py` | Applies `Stack` and `Queue` to the parking system itself: a `Queue` for the waiting line when the lot is full, and a `Stack` as an attendant undo/audit log |
| `main.py` | Single entry point — menu-driven script that runs all the demos above (Stack, Queue, factorial, parking system) from one place |

## Modules proposed

1. Slot Display
2. Vehicle Entry / Registration
3. Billing / Fee Calculation
4. Payment
5. Barrier Control
6. Database / Records
7. Security & Vehicle Verification
8. Reporting & Analytics

## Data structures used

- **Array** — fixed-size slot grid (fast O(1) index access for the display)
- **Hash Map** — active tickets, keyed by ticket ID (O(1) lookup on exit)
- **Queue** — FIFO waiting line when the lot is full
- **Stack** — LIFO undo log for the attendant
- **Linked list / dynamic array** — growing transaction history log

## How to run

Run the whole system from one place via the menu:

```bash
python3 main.py
```

Or run any individual file directly to see just that demo:

```bash
python3 stack.py
python3 queue_.py
python3 factorial_stack.py
python3 parking_demo.py
```

No external dependencies — standard library only (Python 3.8+).
