from stack import ArrayStack
from queue_ import LinkedQueue


class ParkingLot:
    def __init__(self, total_slots: int):
        self.total_slots = total_slots
        self.occupied = 0
        self.waiting_line = LinkedQueue()
        self.entry_log = ArrayStack()

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

        if not self.waiting_line.is_empty():
            next_plate = self.waiting_line.dequeue()
            self.occupied += 1
            self.entry_log.push(next_plate)
            print(f"[ENTRY]   {next_plate} let in from the waiting queue. "
                  f"Slots available: {self.available_slots()}")

    def undo_last_entry(self):
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
    lot.vehicle_arrives("KDC 003C")
    lot.vehicle_arrives("KDD 004D")

    lot.undo_last_entry()

    lot.vehicle_exits()
