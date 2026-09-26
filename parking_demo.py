"""
parking_demo.py
----------------
Ties today's practical (Stack + Queue) back to Task One's parking system.

Where each structure is used, and why:

- QUEUE (LinkedQueue) -> the waiting line of cars when the lot is FULL.
  First car to arrive at a full lot is the first one let in once a slot
  frees up: classic FIFO behaviour.

- STACK (ArrayStack)  -> the attendant's "undo" / audit log of entries.
  If the last vehicle was registered by mistake, the attendant needs to
  reverse the MOST RECENT action first: classic LIFO behaviour.
"""

from stack import ArrayStack
from queue_ import LinkedQueue


class ParkingLot:
    def __init__(self, total_slots: int):
        self.total_slots = total_slots
        self.occupied = 0
        self.waiting_line = LinkedQueue()   # cars waiting for a free slot
        self.entry_log = ArrayStack()       # most recent entries, for undo

    def available_slots(self) -> int:
        return self.total_slots - self.occupied

    def vehicle_arrives(self, plate: str):
        if self.available_slots() > 0:
            self.occupied += 1
            self.entry_log.push(plate)
            print(f"[ENTRY]   {plate} parked. Slots available: {self.available_slots()}")
        else:
            self.waiting_line.enqueue(plate)
            print(f"[WAITING] Lot full. {plate} added to the queue "
                  f"(position {self.waiting_line.size()}).")

    def vehicle_exits(self):
        if self.occupied == 0:
            print("[EXIT]    No vehicles currently parked.")
            return
        self.occupied -= 1
        print(f"[EXIT]    A vehicle left. Slots available: {self.available_slots()}")

        # If anyone was waiting, let the one at the FRONT of the queue in next
        if not self.waiting_line.is_empty():
            next_plate = self.waiting_line.dequeue()
            self.occupied += 1
            self.entry_log.push(next_plate)
            print(f"[ENTRY]   {next_plate} let in from the waiting queue. "
                  f"Slots available: {self.available_slots()}")

    def undo_last_entry(self):
        """Attendant override: reverse the most recent registration (LIFO)."""
        if self.entry_log.is_empty():
            print("[UNDO]    Nothing to undo.")
            return
        last_plate = self.entry_log.pop()
        self.occupied -= 1
        print(f"[UNDO]    Reversed entry for {last_plate}. "
              f"Slots available: {self.available_slots()}")


if __name__ == "__main__":
    lot = ParkingLot(total_slots=2)

    lot.vehicle_arrives("KDA 001A")
    lot.vehicle_arrives("KDB 002B")
    lot.vehicle_arrives("KDC 003C")   # lot is full -> goes to waiting queue
    lot.vehicle_arrives("KDD 004D")   # also waits

    lot.undo_last_entry()             # attendant realises KDB 002B was a mistake

    lot.vehicle_exits()               # a slot frees up -> KDC 003C (front of queue) let in
