# Automated Parking System — Full-Stack Version

- **Frontend:** HTML/CSS/JS (`index.html`)
- **Backend:** Python + Flask (`app.py`)
- **Database:** SQLite (`database.py`)

## Setup

```bash
pip install -r requirements.txt
python3 app.py
```

Open **http://127.0.0.1:5000**. `parking.db` is created automatically on
first run, seeded with 10 slots and rates for `car` (KES 50/hr) and
`motorcycle` (KES 20/hr).

## Modules

| # | Module | Where it lives |
|---|---|---|
| 1 | Slot Display | `GET /api/slots` |
| 2 | Vehicle Entry/Registration | `POST /api/entry` |
| 3 | Billing/Fee Calculation | `POST /api/exit` |
| 4 | Payment | `POST /api/pay` |
| 5 | Barrier Control | `POST /api/pay` (frees slot, releases queue) |
| 6 | Database/Records | `database.py` |
| 7 | Security & Vehicle Verification | `POST /api/exit` (plate match check) |
| 8 | Reporting & Analytics | `GET /api/reports` |

Attendant undo: `POST /api/undo`.

## Files

```
app.py             Flask backend
database.py        SQLite schema + seed data
ps_stack.py        Stack ADT
ps_queue_.py       Queue ADT
requirements.txt
index.html         Frontend
```
