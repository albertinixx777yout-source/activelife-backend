from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# ==========================
# CLIENTE
# ==========================

class ClienteBase(BaseModel):
    nombres: str
    apellidos: str
    identificacion: str
    correo: str
    telefono: str
    fecha_inscripcion: date
    estado_cliente: str


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id_cliente: int


class TipoMembresiaBase(BaseModel):
    nombre_tipo: str
    precio_base: float = Field(..., gt=0)


class TipoMembresiaCreate(TipoMembresiaBase):
    pass


class TipoMembresiaResponse(TipoMembresiaBase):
    id_tipo_membresia: int


# ==========================
# MEMBRESIA
# ==========================

class MembresiaBase(BaseModel):
    id_cliente: int
    id_tipo_membresia: int
    fecha_inicio: date
    fecha_fin: date
    estado_membresia: str


class MembresiaCreate(MembresiaBase):
    pass


class MembresiaResponse(MembresiaBase):
    id_membresia: int