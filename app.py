from datetime import datetime
from math import ceil

from flask import Flask, jsonify, request, send_file

import database as db
from ps_stack import ArrayStack
from ps_queue_ import LinkedQueue

app = Flask(__name__)

# In-memory structures backing two of the eight modules:
# - waiting_line : Queue -> FIFO line of plates waiting when the lot is full
# - entry_log    : Stack -> LIFO undo log of the most recent registrations
waiting_line = LinkedQueue()
entry_log = ArrayStack()


def slot_counts():
    conn = db.get_connection()
    total = conn.execute("SELECT COUNT(*) AS c FROM slots").fetchone()["c"]
    occupied = conn.execute(
        "SELECT COUNT(*) AS c FROM slots WHERE status = 'OCCUPIED'"
    ).fetchone()["c"]
    conn.close()
    return total, occupied


# ---------------------------------------------------------------------------
# Module 1: Slot Display
# ---------------------------------------------------------------------------
@app.route("/api/slots", methods=["GET"])
def api_slots():
    conn = db.get_connection()
    rows = conn.execute(
        "SELECT slot_id, slot_number, status, zone FROM slots ORDER BY slot_id"
    ).fetchall()
    conn.close()

    total, occupied = slot_counts()
    return jsonify({
        "total_slots": total,
        "occupied": occupied,
        "available": total - occupied,
        "waiting_count": waiting_line.size(),
        "slots": [dict(r) for r in rows],
    })


# ---------------------------------------------------------------------------
# Module 2: Vehicle Entry / Registration
# ---------------------------------------------------------------------------
@app.route("/api/entry", methods=["POST"])
def api_entry():
    data = request.get_json(force=True)
    plate = data.get("plate_number", "").strip().upper()
    vehicle_type = data.get("vehicle_type", "car").strip().lower()

    if not plate:
        return jsonify({"error": "plate_number is required"}), 400

    conn = db.get_connection()
    total, occupied = slot_counts()

    if occupied >= total:
        waiting_line.enqueue(plate)
        conn.close()
        return jsonify({
            "status": "WAITING",
            "message": f"Lot full. {plate} added to the waiting queue.",
            "position": waiting_line.size(),
        })

    free_slot = conn.execute(
        "SELECT slot_id, slot_number FROM slots WHERE status = 'FREE' LIMIT 1"
    ).fetchone()

    vehicle = conn.execute(
        "SELECT vehicle_id FROM vehicles WHERE plate_number = ?", (plate,)
    ).fetchone()
    if vehicle is None:
        cur = conn.execute(
            "INSERT INTO vehicles (plate_number, vehicle_type) VALUES (?, ?)",
            (plate, vehicle_type),
        )
        vehicle_id = cur.lastrowid
    else:
        vehicle_id = vehicle["vehicle_id"]

    entry_time = db.now_str()
    cur = conn.execute(
        "INSERT INTO tickets (vehicle_id, slot_id, entry_time, status) "
        "VALUES (?, ?, ?, 'PARKED')",
        (vehicle_id, free_slot["slot_id"], entry_time),
    )
    ticket_id = cur.lastrowid

    conn.execute(
        "UPDATE slots SET status = 'OCCUPIED' WHERE slot_id = ?",
        (free_slot["slot_id"],),
    )
    conn.commit()
    conn.close()

    entry_log.push({"ticket_id": ticket_id, "plate": plate, "slot_id": free_slot["slot_id"]})

    return jsonify({
        "status": "PARKED",
        "ticket_id": ticket_id,
        "slot_number": free_slot["slot_number"],
        "entry_time": entry_time,
        "entry_plate": plate,
    })


# ---------------------------------------------------------------------------
# Modules 3 & 7: Billing/Fee Calculation + Security & Vehicle Verification
# ---------------------------------------------------------------------------
@app.route("/api/exit", methods=["POST"])
def api_exit():
    data = request.get_json(force=True)
    ticket_id = data.get("ticket_id")
    exit_plate = data.get("exit_plate", "").strip().upper()

    conn = db.get_connection()
    ticket = conn.execute(
        "SELECT t.*, v.plate_number, v.vehicle_type "
        "FROM tickets t JOIN vehicles v ON t.vehicle_id = v.vehicle_id "
        "WHERE t.ticket_id = ?",
        (ticket_id,),
    ).fetchone()

    if ticket is None:
        conn.close()
        return jsonify({"error": "ticket not found"}), 404
    if ticket["status"] != "PARKED":
        conn.close()
        return jsonify({"error": f"ticket is not awaiting exit (status={ticket['status']})"}), 400

    match_result = "MATCH" if exit_plate == ticket["plate_number"] else "MISMATCH"
    checked_at = db.now_str()
    conn.execute(
        "INSERT INTO verification_logs (ticket_id, entry_plate, exit_plate, match_result, checked_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (ticket_id, ticket["plate_number"], exit_plate, match_result, checked_at),
    )
    conn.commit()

    if match_result == "MISMATCH":
        conn.close()
        return jsonify({
            "status": "SECURITY_ALERT",
            "message": f"Exit plate {exit_plate} does not match entry plate {ticket['plate_number']}. "
                       f"Barrier will not open. Attendant must verify.",
        }), 409

    entry_time = datetime.fromisoformat(ticket["entry_time"])
    exit_time = datetime.now()
    duration_minutes = (exit_time - entry_time).total_seconds() / 60
    hours = max(1, ceil(duration_minutes / 60))
    rate = db.get_rate_for(ticket["vehicle_type"])
    amount_due = round(hours * rate, 2)

    conn.execute(
        "UPDATE tickets SET exit_time = ?, amount_due = ?, status = 'AWAITING_PAYMENT' "
        "WHERE ticket_id = ?",
        (exit_time.isoformat(timespec="seconds"), amount_due, ticket_id),
    )
    conn.commit()
    conn.close()

    return jsonify({
        "status": "AWAITING_PAYMENT",
        "ticket_id": ticket_id,
        "duration_minutes": round(duration_minutes, 1),
        "hours_charged": hours,
        "rate_per_hour": rate,
        "amount_due": amount_due,
    })


# ---------------------------------------------------------------------------
# Modules 4 & 5: Payment + Barrier Control
# ---------------------------------------------------------------------------
@app.route("/api/pay", methods=["POST"])
def api_pay():
    data = request.get_json(force=True)
    ticket_id = data.get("ticket_id")
    amount_paid = float(data.get("amount_paid", 0))
    method = data.get("payment_method", "cash")

    conn = db.get_connection()
    ticket = conn.execute(
        "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
    ).fetchone()

    if ticket is None:
        conn.close()
        return jsonify({"error": "ticket not found"}), 404
    if ticket["status"] != "AWAITING_PAYMENT":
        conn.close()
        return jsonify({"error": f"ticket is not awaiting payment (status={ticket['status']})"}), 400

    if amount_paid < ticket["amount_due"]:
        conn.close()
        return jsonify({
            "status": "INSUFFICIENT_PAYMENT",
            "amount_due": ticket["amount_due"],
            "amount_paid": amount_paid,
            "message": "Barrier stays closed. Insufficient payment.",
        }), 402

    conn.execute(
        "INSERT INTO payments (ticket_id, amount_paid, payment_method, timestamp) "
        "VALUES (?, ?, ?, ?)",
        (ticket_id, amount_paid, method, db.now_str()),
    )
    conn.execute("UPDATE tickets SET status = 'PAID' WHERE ticket_id = ?", (ticket_id,))
    conn.execute(
        "UPDATE slots SET status = 'FREE' WHERE slot_id = ?", (ticket["slot_id"],)
    )
    conn.commit()

    # A slot just freed up: let the next plate in the waiting queue proceed (FIFO)
    released_to = None
    if not waiting_line.is_empty():
        released_to = waiting_line.dequeue()
    conn.close()

    return jsonify({
        "status": "PAID",
        "message": "Payment accepted. Barrier open.",
        "next_in_queue": released_to,
    })


# ---------------------------------------------------------------------------
# Attendant override: Stack-based undo of the most recent entry
# ---------------------------------------------------------------------------
@app.route("/api/undo", methods=["POST"])
def api_undo():
    if entry_log.is_empty():
        return jsonify({"message": "Nothing to undo."})

    last = entry_log.pop()
    conn = db.get_connection()
    conn.execute(
        "UPDATE tickets SET status = 'CANCELLED' WHERE ticket_id = ?",
        (last["ticket_id"],),
    )
    conn.execute(
        "UPDATE slots SET status = 'FREE' WHERE slot_id = ?", (last["slot_id"],)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Reversed entry for {last['plate']}.", "ticket_id": last["ticket_id"]})


# ---------------------------------------------------------------------------
# Module 8: Reporting & Analytics
# ---------------------------------------------------------------------------
@app.route("/api/reports", methods=["GET"])
def api_reports():
    conn = db.get_connection()

    total_revenue = conn.execute(
        "SELECT COALESCE(SUM(amount_paid), 0) AS total FROM payments"
    ).fetchone()["total"]

    rows = conn.execute(
        "SELECT entry_time FROM tickets"
    ).fetchall()
    occupancy_by_hour = {}
    for r in rows:
        hour = datetime.fromisoformat(r["entry_time"]).hour
        occupancy_by_hour[hour] = occupancy_by_hour.get(hour, 0) + 1

    peak_hour = max(occupancy_by_hour, key=occupancy_by_hour.get) if occupancy_by_hour else None
    total_tickets = conn.execute("SELECT COUNT(*) AS c FROM tickets").fetchone()["c"]
    conn.close()

    return jsonify({
        "total_revenue": total_revenue,
        "total_tickets": total_tickets,
        "occupancy_by_hour": occupancy_by_hour,
        "peak_hour": peak_hour,
    })


@app.route("/")
def index():
    return send_file("index.html")


if __name__ == "__main__":
    db.init_db(total_slots=10)
    app.run(debug=True, port=5000)
