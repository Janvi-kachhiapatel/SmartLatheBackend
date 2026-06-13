from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class MachineSnapshotSchema(BaseModel):
    machine_status: str

    vibit1_temp: float
    vibit1_rpm: float

    vibit2_temp: float
    vibit2_rpm: float

    voltage_v1n: float
    avg_current: float
    total_kw: float

    x_position: float
    y_position: float
    cutting_speed: float
    depth_of_cutting: float

    timestamp: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import List, Optional


class ExportRequest(BaseModel):
    dashboards: List[str]
    parameters: List[str]

    duration: str

    start_date: Optional[str] = None
    end_date: Optional[str] = None