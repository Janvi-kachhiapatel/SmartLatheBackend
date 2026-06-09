from sqlalchemy import Column, Integer, Float, String, DateTime
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

    # Position
    x_position = Column(Float)
    y_position = Column(Float)
    rpm = Column(Float)
    
    cutting_speed = Column(Float)
    depth_of_cutting = Column(Float)

    # Chuck
    chuck_on = Column(Integer)
    red_buzzer = Column(Integer)