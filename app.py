import threading
from background_logger import background_logger
from fastapi import FastAPI
from collector import collect_live_data
from db_service import save_snapshot
from database import SessionLocal
from models import MachineSnapshot
from database import engine
from models import Base
import requests
import cache

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Lathe Backend")

@app.on_event("startup")
def startup_event():

    thread = threading.Thread(
        target=background_logger,
        daemon=True
    )

    thread.start()

    print("Background logger started")


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/all")
def get_all():

    return cache.latest_data

@app.get("/latest")
def get_latest():

    db = SessionLocal()

    try:
        row = (
            db.query(MachineSnapshot)
            .order_by(MachineSnapshot.id.desc())
            .first()
        )

        if not row:
            return {"error": "No data"}

        return {
            "machine_status": row.machine_status,
            "vibit1_temp": row.vibit1_temp,
            "vibit2_temp": row.vibit2_temp,
            "rpm": row.rpm,
            "voltage_v1n": row.voltage_v1n,
            "avg_current": row.avg_current,
            "total_kw": row.total_kw,
            "x_position": row.x_position,
            "y_position": row.y_position,
            "timestamp": row.timestamp
        }

    finally:
        db.close()

@app.post("/zero_x")
def zero_x():

    requests.get(
        "http://10.10.14.131/zero_x",
        timeout=2
    )

    return {"status": "ok"}

@app.post("/zero_y")
def zero_y():

    requests.get(
        "http://10.10.14.131/zero_y",
        timeout=2
    )

    return {"status": "ok"}

@app.post("/zero_both")
def zero_both():

    requests.get(
        "http://10.10.14.131/zero_both",
        timeout=2
    )

    return {"status": "ok"}

@app.post("/reset_all")
def reset_all():

    requests.get(
        "http://10.10.14.131/reset_all",
        timeout=2
    )

    return {"status": "ok"}

@app.get("/history")
def get_history(limit: int = 50):
    db = SessionLocal()

    try:
        rows = (
            db.query(MachineSnapshot)
            .order_by(MachineSnapshot.id.desc())
            .limit(limit)
            .all()
        )

        rows.reverse()

        return {
            "rpm": [r.rpm for r in rows],
            "temperature": [r.vibit1_temp for r in rows],
            "vibration": [r.avg_current for r in rows]
        }

    finally:
        db.close()

@app.get("/history/rpm")
def get_rpm_history(limit: int = 50):

    db = SessionLocal()

    try:
        rows = (
            db.query(MachineSnapshot)
            .order_by(MachineSnapshot.id.desc())
            .limit(limit)
            .all()
        )

        rows.reverse()

        return {
            "rpm": [r.rpm for r in rows]
        }

    finally:
        db.close()


@app.get("/history/temperature")
def get_temperature_history(limit: int = 50):

    db = SessionLocal()

    try:
        rows = (
            db.query(MachineSnapshot)
            .order_by(MachineSnapshot.id.desc())
            .limit(limit)
            .all()
        )

        rows.reverse()

        return {
            "temperature": [r.vibit1_temp for r in rows]
        }

    finally:
        db.close()


@app.get("/history/vibration")
def get_vibration_history(limit: int = 50):

    db = SessionLocal()

    try:
        rows = (
            db.query(MachineSnapshot)
            .order_by(MachineSnapshot.id.desc())
            .limit(limit)
            .all()
        )

        rows.reverse()

        return {
            "vibration": [r.avg_current for r in rows]
        }

    finally:
        db.close()

@app.get("/alarms")
def get_alarms():

    data = latest_data

    alarms = []

    vibit1 = data.get("vibit1", {})
    vibit2 = data.get("vibit2", {})
    machine = data.get("machine", {})
    chuck = data.get("chuck", {})

    if vibit1.get("temperature", 0) > 50:
        alarms.append({
            "title": "VIBIT1 HIGH TEMPERATURE",
            "severity": "ACTIVE"
        })

    if vibit2.get("temperature", 0) > 50:
        alarms.append({
            "title": "VIBIT2 HIGH TEMPERATURE",
            "severity": "ACTIVE"
        })

    if machine.get("status") == "OFF":
        alarms.append({
            "title": "PLC COMMUNICATION LOST",
            "severity": "ACTIVE"
        })

    if chuck.get("chuck_on", 0) == 0:
        alarms.append({
            "title": "CHUCK OPEN",
            "severity": "WARNING"
        })

    return alarms