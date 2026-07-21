from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MetodoPagoBase(BaseModel):
    nombre_metodo_pago: str = Field(..., example="Tarjeta de Crédito")
    activo: bool = True

class MetodoPagoCreate(MetodoPagoBase):
    pass

class MetodoPagoResponse(MetodoPagoBase):
    id_metodo_pago: int

class PagoBase(BaseModel):
    monto: float = Field(..., gt=0, example=50.00)
    id_cliente: int
    id_reserva: Optional[int] = None
    id_membresia: Optional[int] = None
    id_metodo_pago: int

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id_pago: int
    fecha_pago: str
