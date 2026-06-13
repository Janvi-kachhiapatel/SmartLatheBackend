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
from fastapi import Body
from fastapi.responses import FileResponse
import csv
from datetime import datetime, timedelta
from schemas import ExportRequest
from schemas import LoginRequest
from models import User, LoginHistory
from auth import verify_password
from pydantic import BaseModel
from auth import hash_password
import random
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors
from fastapi.middleware.cors import CORSMiddleware
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Lathe Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

class GoogleLoginRequest(BaseModel):
    email: str
    name: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

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
        "http://10.10.14.131/reset?axis=x",
        timeout=2
    )

    return {"status": "ok"}

@app.post("/zero_y")
def zero_y():

    requests.get(
        "http://10.10.14.131/reset?axis=y",
        timeout=2
    )

    return {"status": "ok"}

@app.post("/zero_both")
def zero_both():

    requests.get(
        "http://10.10.14.131/reset?axis=both",
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

    data = cache.latest_data

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

@app.get("/history/power")
def get_power_history(limit: int = 50):

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
            "power": [r.total_kw for r in rows]
        }

    finally:
        db.close()


PARAMETER_MAP = {
        # Position
    "x_position": "x_position",
    "y_position": "y_position",
    "cutting_speed": "cutting_speed",
    "depth_of_cutting": "depth_of_cutting",

    # Machine
    "status": "machine_status",

    # Chuck
    "chuck_on": "chuck_on",
    "red_buzzer": "red_buzzer",

    # Energy
    "voltage_V1N": "voltage_v1n",
    "voltage_V2N": "voltage_v2n",
    "voltage_V3N": "voltage_v3n",

    "current_I1": "current_i1",
    "current_I2": "current_i2",
    "current_I3": "current_i3",

    "avg_current": "avg_current",

    "total_kW": "total_kw",

    "PF1": "pf1",
    "PF2": "pf2",
    "PF3": "pf3",

    "frequency": "frequency",

    "avg_voltage_LN": "avg_voltage_ln",
    "avg_voltage_LL": "avg_voltage_ll",

    "kW1": "kw1",
    "kW2": "kw2",
    "kW3": "kw3",

    "avg_PF": "avg_pf",

    "total_net_kwh_dg": "total_net_kwh_dg",
    "total_net_kvarh_dg": "total_net_kvarh_dg",
    "total_net_kvah_dg": "total_net_kvah_dg",

    "max_dmd_active_power": "max_dmd_active_power",
    "max_dmd_reactive_power": "max_dmd_reactive_power",
    "max_dmd_apparent_power": "max_dmd_apparent_power",

    "kwh1_import": "kwh1_import",
    "kwh2_import": "kwh2_import",
    "kwh3_import": "kwh3_import",

    "kwh1_export": "kwh1_export",
    "kwh2_export": "kwh2_export",
    "kwh3_export": "kwh3_export",

    "total_kwh_import": "total_kwh_import",
    "total_kwh_export": "total_kwh_export",

    "kvarh1_import": "kvarh1_import",

    "kVA1": "kva1_energy",
    "kVA2": "kva2_energy",
    "kVA3": "kva3_energy",

    "kVAR1": "kvar1_energy",
    "kVAR2": "kvar2_energy",
    "kVAR3": "kvar3_energy",

    "kvar1": "kvar1",
    "kvar2": "kvar2",
    "kvar3": "kvar3",

    "kva1": "kva1",
    "kva2": "kva2",
    "kva3": "kva3",

    "total_kvar": "total_kvar",
    "total_kva": "total_kva",

    "total_net_kwh": "total_net_kwh",
    "total_net_kvarh": "total_net_kvarh",

    # RPM
    "rpm": "rpm",

    # VIBIT1
    "temperature": "vibit1_temp",

    "x_rms_acceleration_vibit1": "vibit1_x_rms_acc",
    "y_rms_acceleration_vibit1": "vibit1_y_rms_acc",
    "z_rms_acceleration_vibit1": "vibit1_z_rms_acc",

    "x_rms_velocity_vibit1": "vibit1_x_rms_vel",
    "y_rms_velocity_vibit1": "vibit1_y_rms_vel",
    "z_rms_velocity_vibit1": "vibit1_z_rms_vel",

    "x_peak_acceleration_vibit1": "vibit1_x_peak_acc",
    "y_peak_acceleration_vibit1": "vibit1_y_peak_acc",
    "z_peak_acceleration_vibit1": "vibit1_z_peak_acc",

    "x_peak_velocity_vibit1": "vibit1_x_peak_vel",
    "y_peak_velocity_vibit1": "vibit1_y_peak_vel",
    "z_peak_velocity_vibit1": "vibit1_z_peak_vel",

    # VIBIT2
    "temperature_vibit2": "vibit2_temp",

    "x_rms_acceleration_vibit2": "vibit2_x_rms_acc",
    "y_rms_acceleration_vibit2": "vibit2_y_rms_acc",
    "z_rms_acceleration_vibit2": "vibit2_z_rms_acc",

    "x_rms_velocity_vibit2": "vibit2_x_rms_vel",
    "y_rms_velocity_vibit2": "vibit2_y_rms_vel",
    "z_rms_velocity_vibit2": "vibit2_z_rms_vel",

    "x_peak_acceleration_vibit2": "vibit2_x_peak_acc",
    "y_peak_acceleration_vibit2": "vibit2_y_peak_acc",
    "z_peak_acceleration_vibit2": "vibit2_z_peak_acc",

    "x_peak_velocity_vibit2": "vibit2_x_peak_vel",
    "y_peak_velocity_vibit2": "vibit2_y_peak_vel",
    "z_peak_velocity_vibit2": "vibit2_z_peak_vel",

}



@app.post("/export/csv")
async def export_csv(
        
    request: ExportRequest,
):
    print("REQUEST PARAMETERS =", request.parameters)
    print("REQUEST DASHBOARDS =", request.dashboards)

    filename = (
        f"export_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ".csv"
    )

    db = SessionLocal()

    query = db.query(MachineSnapshot)

    if request.duration == "1H":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(hours=1)
        )

    elif request.duration == "24H":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(hours=24)
        )

    elif request.duration == "7D":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(days=7)
        )

    elif request.duration == "30D":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(days=30)
        )

    elif request.duration == "CUSTOM":

        if request.start_date:

            query = query.filter(
                MachineSnapshot.timestamp >=
                datetime.fromisoformat(
                    request.start_date
                )
            )

        if request.end_date:

            query = query.filter(
                MachineSnapshot.timestamp <=
                datetime.fromisoformat(
                    request.end_date
                )
            )

    rows = (
        query
        .order_by(MachineSnapshot.id.desc())
        .all()
    )

    rows.reverse()

    

    with open(
        filename,
        "w",
        newline="",
      
    ) as file:

        writer = csv.writer(
            file,
            delimiter=',',
            quoting=csv.QUOTE_ALL
        )

        writer.writerow(["SMART LATHE EXPORT"])
        writer.writerow([])
        writer.writerow(["Dashboards"] + request.dashboards)
        writer.writerow(["Parameters"] + request.parameters)
        writer.writerow([])

        print("REQUEST PARAMETERS")
        print(request.parameters)

        print("REQUEST DASHBOARDS")
        print(request.dashboards)

        selected_columns = []

        for p in request.parameters:

            if p in PARAMETER_MAP:
                selected_columns.append(p)
        print("REQUEST PARAMETERS")
        print(request.parameters)

        print("REQUEST DASHBOARDS")
        print(request.dashboards)

        headers = ["timestamp"]

        headers.extend(selected_columns)

        writer.writerow(headers)

        # csv_row = [row.timestamp]

        # for param in selected_columns:

        #     db_field = PARAMETER_MAP[param]

        #     csv_row.append(
        #         getattr(
        #             row,
        #             db_field,
        #             ""
        #         )
        #     )

        # writer.writerow(csv_row)



        print("ROWS FOUND =", len(rows))
        print("SELECTED COLUMNS =", selected_columns)
        for row in rows:

            csv_row = [
                row.timestamp
            ]

            for param in selected_columns:

                db_field = PARAMETER_MAP[param]

                csv_row.append(
                    getattr(
                        row,
                        db_field,
                        ""
                    )
                )

            writer.writerow(csv_row)

    return FileResponse(
        filename,
        media_type="text/csv",
        filename=filename,
    )


@app.post("/export/pdf")
async def export_pdf(
    request: ExportRequest,
    
):
    print("REQUEST PARAMETERS =", request.parameters)
    print("REQUEST DASHBOARDS =", request.dashboards)

    filename = (
        f"export_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ".pdf"
    )

    from reportlab.pdfgen import canvas

    db = SessionLocal()

    query = db.query(MachineSnapshot)

    if request.duration == "1H":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(hours=1)
        )

    elif request.duration == "24H":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(hours=24)
        )

    elif request.duration == "7D":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(days=7)
        )

    elif request.duration == "30D":

        query = query.filter(
            MachineSnapshot.timestamp >=
            datetime.utcnow() - timedelta(days=30)
        )

    elif request.duration == "CUSTOM":

        if request.start_date:

            query = query.filter(
                MachineSnapshot.timestamp >=
                datetime.fromisoformat(
                    request.start_date
                )
            )

        if request.end_date:

            query = query.filter(
                MachineSnapshot.timestamp <=
                datetime.fromisoformat(
                    request.end_date
                )
            )

    rows = query.all()
    print("PDF ROWS =", len(rows))
    selected_columns = []

    for p in request.parameters:
        if p in PARAMETER_MAP:
            selected_columns.append(p)

    print("PDF COLUMNS =", selected_columns)
    print("PDF ROWS =", len(rows))
    print("FIRST ROW =", rows[0] if rows else "NO DATA")
    print("LAST ROW =", rows[-1] if rows else "NO DATA")

    

    # pdf = canvas.Canvas(
    #     filename,
    #     pagesize=(2000, 842)
    # )
    from reportlab.lib.pagesizes import landscape

    col_widths = [120]

    for i in range(len(selected_columns)):
        col_widths.append(70)

    pdf = SimpleDocTemplate(
        filename,
        pagesize=(3500, 1200)
    )
    # y = 800
    table_data = []

    header = ["Timestamp"]

    for param in selected_columns:
        header.append(param)

    table_data.append(header)

    for row in rows:

        row_data = [str(row.timestamp)]

        for param in selected_columns:

            db_field = PARAMETER_MAP[param]

            value = getattr(
                row,
                db_field,
                ""
            )

            row_data.append(str(value))

        table_data.append(row_data)

    table = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=1,
        splitByRow=1,
        
    )

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 7),
        ])
    )

    print("TABLE ROW COUNT =", len(table_data))

    pdf.build([table])

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename,
    )
    # pdf.build([table])
    # pdf.drawString(
    #     100,
    #     y,
    #     "Smart Lathe Export Report"
    # )

    # y -= 40

    # pdf.drawString(
    #     100,
    #     y,
    #     "Dashboards: {', '.join(request.dashboards)}"
    # )

    # y -= 20

    # pdf.drawString(
    #     100,
    #     y,
    #     "Parameters: {', '.join(request.parameters)}"
    # )

    # y -= 30

    # pdf.drawString(
    #     100,
    #     y,
    #     "Data:"
    # )

    # y -= 20

    # # for row in rows[:100]:

    #     line = str(row.timestamp)

    #     for param in selected_columns:

    #         db_field = PARAMETER_MAP[param]

    #         value = getattr(
    #             row,
    #             db_field,
    #             ""
    #         )

    #         line += f" | {param}: {value}"

    #     pdf.drawString(
    #         20,
    #         y,
    #         line[:180]
    #     )

    #     y -= 15

    #     if y < 40:
    #         pdf.showPage()
    #         y = 800

    # pdf.drawString(
    #     100,
    #     y,
    #     "Smart Lathe Export Report"
    # )

    # y -= 40

    # pdf.drawString(
    #     100,
    #     y,
    #     f"Dashboards: "
    #     f"{', '.join(request.dashboards)}"
    # )

    # y -= 20

    # pdf.drawString(
    #     100,
    #     y,
    #     f"Parameters: "
    #     f"{', '.join(request.parameters)}"
    # )

    # y -= 20

    # pdf.drawString(
    #     100,
    #     y,
    #     f"Duration: "
    #     f"{request.duration}"
    # )

    # y -= 20

    # pdf.drawString(
    #     100,
    #     y,
    #     f"Start Date: "
    #     f"{request.start_date}"
    # )

    # y -= 20

    # pdf.drawString(
    #     100,
    #     y,
    #     f"End Date: "
    #     f"{request.end_date}"
    # )

    # y -= 40

    # pdf.drawString(
    #     100,
    #     y,
    #     "DATA"
    # )

    # y -= 30
    print("START PDF GENERATION")
    for row in rows:

        line = str(row.timestamp)

        for param in selected_columns:

            db_field = PARAMETER_MAP[param]

            value = getattr(
                row,
                db_field,
                ""
            )

            line += f" | {param}: {value}"

        pdf.drawString(
            30,
            y,
            line[:180]
        )

        y -= 15

        if y < 50:

            pdf.showPage()

            y = 800

    pdf.save()
    print("PDF FINISHED")
    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename,
    )
@app.post("/login")
def login(
    request: LoginRequest,
):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.username == request.username
        )
        .first()
    )

    if not user:
        return {
            "success": False,
            "message": "User not found",
        }

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        return {
            "success": False,
            "message": "Wrong password",
        }

    history = LoginHistory(
        username=user.username,
        ip_address="unknown",
        device_info="Android App",
        location="unknown",
    )

    db.add(history)
    db.commit()

    return {
        "success": True,
        "role": user.role,
        "username": user.username,
    }
@app.get("/users")
def users():

    db = SessionLocal()

    try:

        users = db.query(User).all()

        return [
            {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "active": user.is_active,
            }
            for user in users
        ]

    finally:
        db.close()

@app.post("/create_user")
def create_user(req: CreateUserRequest):

    db = SessionLocal()

    try:

        existing = db.query(User).filter(
            User.username == req.username
        ).first()

        if existing:
            return {
                "success": False,
                "message": "User already exists"
            }

        user = User(
            username=req.username,
            email=req.email,
            password_hash=hash_password(req.password),
            role=req.role,
            is_active=True,
        )

        db.add(user)
        db.commit()

        return {
            "success": True
        }

    finally:
        db.close()
@app.get("/login_history")
def get_login_history():

    db = SessionLocal()

    history = (
        db.query(LoginHistory)
        .order_by(
            LoginHistory.login_time.desc()
        )
        .all()
    )

    return [
        {
            "username": h.username,
            "login_time": str(h.login_time),
            "ip": h.ip_address,
            "device": h.device_info,
            "location": h.location,
        }
        for h in history
    ]

# @app.post("/google-login")
# def google_login(
#     request: GoogleLoginRequest,
# ):
#     print("GOOGLE EMAIL =", request.email)
#     db = SessionLocal()

#     user = (
#         db.query(User)
#         .filter(
#             User.email ==
#             request.email
#         )
#         .first()
#     )

#     if not user:

#         user = User(
#             username=request.name,
#             email=request.email,
#             role="operator",
#             is_active=True,
#         )

#         db.add(user)
#         db.commit()

#     return {
#         "success": True,
#         "username": user.username,
#         "role": user.role,
#     }

@app.post("/google-login")
def google_login(req: GoogleLoginRequest):

    print("GOOGLE LOGIN CALLED")
    print(req.email)

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == req.email)
        .first()
    )

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    return {
        "success": True,
        "username": user.username,
        "role": user.role,
    }

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            return {"success": False}

        db.delete(user)
        db.commit()

        return {"success": True}

    finally:
        db.close()


@app.put("/users/{user_id}/disable")
def disable_user(user_id: int):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user:
            user.is_active = False
            db.commit()

        return {"success": True}

    finally:
        db.close()


@app.put("/users/{user_id}/enable")
def enable_user(user_id: int):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user:
            user.is_active = True
            db.commit()

        return {"success": True}

    finally:
        db.close()


@app.put("/users/{user_id}/role")
def update_role(
    user_id: int,
    role: str,
):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user:
            user.role = role
            db.commit()

        return {"success": True}

    finally:
        db.close()

@app.get("/database_records")
def database_records():

    db = SessionLocal()

    try:

        rows = (
            db.query(MachineSnapshot)
            .order_by(
                MachineSnapshot.timestamp.desc()
            )
            .limit(500)
            .all()
        )

        for row in rows:
            row.__dict__.pop("_sa_instance_state", None)



        return [
        row.__dict__
        for row in rows
    ]
    

    finally:
        db.close()
# @app.get("/admin/dashboard")
# def admin_dashboard():

#     db = SessionLocal()

#     total_users = db.query(User).count()

#     active_users = (
#         db.query(User)
#         .filter(User.is_active == True)
#         .count()
#     )

#     total_machines = 1

#     today_logins = (
#         db.query(LoginHistory)
#         .filter(
#             LoginHistory.login_time >=
#             datetime.utcnow() - timedelta(days=1)
#         )
#         .count()
#     )

#     latest = (
#         db.query(MachineSnapshot)
#         .order_by(MachineSnapshot.timestamp.desc())
#         .first()
#     )

#     online_machines = (
#     1
#     if latest and latest.machine_status == "ON"
#         else 0
#     )

#     offline_machines = (
#         0
#         if online_machines == 1
#         else 1
#     )

#     return {
#             "total_users": total_users,

#         "active_users": active_users,

#         "total_machines": total_machines,

#         "online_machines": online_machines,

#         "offline_machines": offline_machines,

#         "today_logins": today_logins,
#     } 
@app.get("/admin/dashboard")
def admin_dashboard():

    db = SessionLocal()

    try:

        total_users = db.query(User).count()

        active_users = (
            db.query(User)
            .filter(User.is_active == True)
            .count()
        )

        today_logins = (
            db.query(LoginHistory)
            .filter(
                LoginHistory.login_time >=
                datetime.utcnow() - timedelta(days=1)
            )
            .count()
        )

        total_machines = 1

        latest = (
            db.query(MachineSnapshot)
            .order_by(
                MachineSnapshot.timestamp.desc()
            )
            .first()
        )

        online_machines = (
            1
            if latest and latest.machine_status == "ON"
            else 0
        )

        offline_machines = (
            0
            if online_machines == 1
            else 1
        )

        return {

            "total_users": total_users,

            "active_users": active_users,

            "total_machines": total_machines,

            "online_machines": online_machines,

            "offline_machines": offline_machines,

            "today_logins": today_logins,

            "machine_status":
                latest.machine_status
                if latest else "OFF",

            "x_position":
                latest.x_position
                if latest else 0,

            "y_position":
                latest.y_position
                if latest else 0,

            "cutting_speed":
                latest.cutting_speed
                if latest else 0,

            "depth_of_cutting":
                latest.depth_of_cutting
                if latest else 0,
        }

    finally:
        db.close()
@app.get("/admin/records")
def get_records():

    db = SessionLocal()

    try:

        rows = (
            db.query(MachineSnapshot)
            .order_by(
                MachineSnapshot.timestamp.desc()
            )
            .limit(500)
            .all()
        )

        return [
            {
                "timestamp":
                    str(r.timestamp),

                "rpm":
                    r.rpm,

                "machine_status":
                    r.machine_status,

                "x_position":
                    r.x_position,

                "y_position":
                    r.y_position,

                "cutting_speed":
                    r.cutting_speed,

                "depth_of_cutting":
                    r.depth_of_cutting,
            }
            for r in rows
        ]

    finally:
        db.close()