from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime
from database import Base


class MachineSnapshot(Base):
    __tablename__ = "machine_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Machine
    machine_status = Column(String)

    # Vibit 1
    vibit1_temp = Column(Float)
    

    vibit1_x_rms_acc = Column(Float)
    vibit1_y_rms_acc = Column(Float)
    vibit1_z_rms_acc = Column(Float)

    vibit1_x_rms_vel = Column(Float)
    vibit1_y_rms_vel = Column(Float)
    vibit1_z_rms_vel = Column(Float)

    vibit1_x_peak_acc = Column(Float)
    vibit1_y_peak_acc = Column(Float)
    vibit1_z_peak_acc = Column(Float)

    vibit1_x_peak_vel = Column(Float)
    vibit1_y_peak_vel = Column(Float)
    vibit1_z_peak_vel = Column(Float)

    # Vibit 2
    vibit2_temp = Column(Float)
    

    vibit2_x_rms_acc = Column(Float)
    vibit2_y_rms_acc = Column(Float)
    vibit2_z_rms_acc = Column(Float)

    vibit2_x_rms_vel = Column(Float)
    vibit2_y_rms_vel = Column(Float)
    vibit2_z_rms_vel = Column(Float)

    vibit2_x_peak_acc = Column(Float)
    vibit2_y_peak_acc = Column(Float)
    vibit2_z_peak_acc = Column(Float)

    vibit2_x_peak_vel = Column(Float)
    vibit2_y_peak_vel = Column(Float)
    vibit2_z_peak_vel = Column(Float)

    # Energy Meter
    voltage_v1n = Column(Float)
    voltage_v2n = Column(Float)
    voltage_v3n = Column(Float)

    voltage_v12 = Column(Float)
    voltage_v23 = Column(Float)
    voltage_v31 = Column(Float)

    avg_current = Column(Float)
    current_i1 = Column(Float)
    current_i2 = Column(Float)
    current_i3 = Column(Float)

    total_kw = Column(Float)

    pf1 = Column(Float)
    pf2 = Column(Float)
    pf3 = Column(Float)

    frequency = Column(Float)

    # Additional Energy Fields

    avg_voltage_ln = Column(Float)
    avg_voltage_ll = Column(Float)

    kw1 = Column(Float)
    kw2 = Column(Float)
    kw3 = Column(Float)

    avg_pf = Column(Float)

    total_net_kwh_dg = Column(Float)
    total_net_kvarh_dg = Column(Float)
    total_net_kvah_dg = Column(Float)

    max_dmd_active_power = Column(Float)
    max_dmd_reactive_power = Column(Float)
    max_dmd_apparent_power = Column(Float)

    kwh1_import = Column(Float)
    kwh2_import = Column(Float)
    kwh3_import = Column(Float)

    kwh1_export = Column(Float)
    kwh2_export = Column(Float)
    kwh3_export = Column(Float)

    total_kwh_import = Column(Float)
    total_kwh_export = Column(Float)

    kvarh1_import = Column(Float)

    kva1_energy = Column(Float)
    kva2_energy = Column(Float)
    kva3_energy = Column(Float)

    kvar1_energy = Column(Float)
    kvar2_energy = Column(Float)
    kvar3_energy = Column(Float)

    kvar1 = Column(Float)
    kvar2 = Column(Float)
    kvar3 = Column(Float)

    kva1 = Column(Float)
    kva2 = Column(Float)
    kva3 = Column(Float)

    total_kvar = Column(Float)
    total_kva = Column(Float)

    total_net_kwh = Column(Float)
    total_net_kvarh = Column(Float)

    # Position
    x_position = Column(Float)
    y_position = Column(Float)
    rpm = Column(Float)
    
    cutting_speed = Column(Float)
    depth_of_cutting = Column(Float)

    # Chuck
    chuck_on = Column(Integer)
    red_buzzer = Column(Integer)

    #from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)

    email = Column(String, unique=True)

    password_hash = Column(String)

    role = Column(String, default="operator")



    otp_code = Column(String)

    is_active = Column(Boolean, default=False)

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String)

    login_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    ip_address = Column(String)

    device_info = Column(String)

    location = Column(String)