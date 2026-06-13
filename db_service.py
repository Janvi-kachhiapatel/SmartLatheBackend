from database import SessionLocal
from models import MachineSnapshot


def save_snapshot(data):
    db = SessionLocal()

    try:
        snapshot = MachineSnapshot(

    machine_status=data["machine"]["status"],

    # Vibit1
    vibit1_temp=data["vibit1"].get("temperature", 0),
    

    vibit1_x_rms_acc=data["vibit1"].get("x_rms_acceleration", 0),
    vibit1_y_rms_acc=data["vibit1"].get("y_rms_acceleration", 0),
    vibit1_z_rms_acc=data["vibit1"].get("z_rms_acceleration", 0),

    vibit1_x_rms_vel=data["vibit1"].get("x_rms_velocity", 0),
    vibit1_y_rms_vel=data["vibit1"].get("y_rms_velocity", 0),
    vibit1_z_rms_vel=data["vibit1"].get("z_rms_velocity", 0),

    vibit1_x_peak_acc=data["vibit1"].get("x_peak_acceleration", 0),
    vibit1_y_peak_acc=data["vibit1"].get("y_peak_acceleration", 0),
    vibit1_z_peak_acc=data["vibit1"].get("z_peak_acceleration", 0),

    vibit1_x_peak_vel=data["vibit1"].get("x_peak_velocity", 0),
    vibit1_y_peak_vel=data["vibit1"].get("y_peak_velocity", 0),
    vibit1_z_peak_vel=data["vibit1"].get("z_peak_velocity", 0),

    # Vibit2
    vibit2_temp=data["vibit2"].get("temperature", 0),
    

    vibit2_x_rms_acc=data["vibit2"].get("x_rms_acceleration", 0),
    vibit2_y_rms_acc=data["vibit2"].get("y_rms_acceleration", 0),
    vibit2_z_rms_acc=data["vibit2"].get("z_rms_acceleration", 0),

    vibit2_x_rms_vel=data["vibit2"].get("x_rms_velocity", 0),
    vibit2_y_rms_vel=data["vibit2"].get("y_rms_velocity", 0),
    vibit2_z_rms_vel=data["vibit2"].get("z_rms_velocity", 0),

    vibit2_x_peak_acc=data["vibit2"].get("x_peak_acceleration", 0),
    vibit2_y_peak_acc=data["vibit2"].get("y_peak_acceleration", 0),
    vibit2_z_peak_acc=data["vibit2"].get("z_peak_acceleration", 0),

    vibit2_x_peak_vel=data["vibit2"].get("x_peak_velocity", 0),
    vibit2_y_peak_vel=data["vibit2"].get("y_peak_velocity", 0),
    vibit2_z_peak_vel=data["vibit2"].get("z_peak_velocity", 0),

    # Energy
    voltage_v1n=data["energy"]["data"].get("voltage_V1N", 0),
    voltage_v2n=data["energy"]["data"].get("voltage_V2N", 0),
    voltage_v3n=data["energy"]["data"].get("voltage_V3N", 0),

    voltage_v12=data["energy"]["data"].get("voltage_V12", 0),
    voltage_v23=data["energy"]["data"].get("voltage_V23", 0),
    voltage_v31=data["energy"]["data"].get("voltage_V31", 0),

    avg_current=data["energy"]["data"].get("avg_current", 0),
    current_i1=data["energy"]["data"].get("current_I1", 0),
    current_i2=data["energy"]["data"].get("current_I2", 0),
    current_i3=data["energy"]["data"].get("current_I3", 0),

    total_kw=data["energy"]["data"].get("total_kW", 0),

    pf1=data["energy"]["data"].get("PF1", 0),
    pf2=data["energy"]["data"].get("PF2", 0),
    pf3=data["energy"]["data"].get("PF3", 0),

    frequency=data["energy"]["data"].get("frequency", 0),

    avg_voltage_ln=data["energy"]["data"].get("avg_voltage_LN", 0),
    avg_voltage_ll=data["energy"]["data"].get("avg_voltage_LL", 0),

    kw1=data["energy"]["data"].get("kW1", 0),
    kw2=data["energy"]["data"].get("kW2", 0),
    kw3=data["energy"]["data"].get("kW3", 0),

    avg_pf=data["energy"]["data"].get("avg_PF", 0),

    total_net_kwh_dg=data["energy"]["data"].get("total_net_kwh_dg", 0),
    total_net_kvarh_dg=data["energy"]["data"].get("total_net_kvarh_dg", 0),
    total_net_kvah_dg=data["energy"]["data"].get("total_net_kvah_dg", 0),

    max_dmd_active_power=data["energy"]["data"].get("max_dmd_active_power", 0),
    max_dmd_reactive_power=data["energy"]["data"].get("max_dmd_reactive_power", 0),
    max_dmd_apparent_power=data["energy"]["data"].get("max_dmd_apparent_power", 0),

    kwh1_import=data["energy"]["data"].get("kwh1_import", 0),
    kwh2_import=data["energy"]["data"].get("kwh2_import", 0),
    kwh3_import=data["energy"]["data"].get("kwh3_import", 0),

    kwh1_export=data["energy"]["data"].get("kwh1_export", 0),
    kwh2_export=data["energy"]["data"].get("kwh2_export", 0),
    kwh3_export=data["energy"]["data"].get("kwh3_export", 0),

    total_kwh_import=data["energy"]["data"].get("total_kwh_import", 0),
    total_kwh_export=data["energy"]["data"].get("total_kwh_export", 0),

    kvarh1_import=data["energy"]["data"].get("kvarh1_import", 0),

    kva1_energy=data["energy"]["data"].get("kVA1", 0),
    kva2_energy=data["energy"]["data"].get("kVA2", 0),
    kva3_energy=data["energy"]["data"].get("kVA3", 0),

    kvar1_energy=data["energy"]["data"].get("kVAR1", 0),
    kvar2_energy=data["energy"]["data"].get("kVAR2", 0),
    kvar3_energy=data["energy"]["data"].get("kVAR3", 0),

    kvar1=data["energy"]["data"].get("kvar1", 0),
    kvar2=data["energy"]["data"].get("kvar2", 0),
    kvar3=data["energy"]["data"].get("kvar3", 0),

    kva1=data["energy"]["data"].get("kva1", 0),
    kva2=data["energy"]["data"].get("kva2", 0),
    kva3=data["energy"]["data"].get("kva3", 0),

    total_kvar=data["energy"]["data"].get("total_kvar", 0),
    total_kva=data["energy"]["data"].get("total_kva", 0),

    total_net_kwh=data["energy"]["data"].get("total_net_kwh", 0),
    total_net_kvarh=data["energy"]["data"].get("total_net_kvarh", 0),

    # Position
    x_position=data["position"].get("x_position", 0),
    y_position=data["position"].get("y_position", 0),
    rpm=data["vibit1"].get("rpm", 0),

    cutting_speed=data["position"].get("cutting_speed", 0),
    depth_of_cutting=data["position"].get("depth_of_cutting", 0),

    # Chuck
    chuck_on=1 if data["chuck"].get("chuck_on", 0) else 0,
    red_buzzer=1 if data["chuck"].get("red_buzzer", 0) else 0,
)
        print("SAVING TO DATABASE")
        db.add(snapshot)
        db.commit()
        print("DATABASE COMMIT SUCCESS")

    except Exception as e:
        print("DB save error:", e)

    finally:
        db.close()