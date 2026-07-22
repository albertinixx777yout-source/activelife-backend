from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TIPOS_SERVICIO_PERMITIDOS = {"Clase", "Gimnasio", "Reserva"}
ESTADOS_RESERVA_PERMITIDOS = {"Pendiente", "Confirmada", "Cancelada"}


class ServicioBase(BaseModel):
    nombre_servicio: str = Field(..., examples=["Yoga"])
    tipo_servicio: str = Field(..., examples=["Clase"])
    capacidad: int = Field(..., gt=0, examples=[20])
    costo: float = Field(..., ge=0, examples=[35.0])

    @field_validator("nombre_servicio")
    @classmethod
    def validar_nombre_servicio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre del servicio no puede estar vacio")
        return value

    @field_validator("tipo_servicio")
    @classmethod
    def validar_tipo_servicio(cls, value: str) -> str:
        if value not in TIPOS_SERVICIO_PERMITIDOS:
            raise ValueError("El tipo de servicio debe ser Clase, Gimnasio o Reserva")
        return value


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str] = Field(None, examples=["Natacion"])
    tipo_servicio: Optional[str] = Field(None, examples=["Clase"])
    capacidad: Optional[int] = Field(None, gt=0, examples=[15])
    costo: Optional[float] = Field(None, ge=0, examples=[25.0])

    @field_validator("nombre_servicio")
    @classmethod
    def validar_nombre_servicio(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("El nombre del servicio no puede estar vacio")
        return value

    @field_validator("tipo_servicio")
    @classmethod
    def validar_tipo_servicio(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in TIPOS_SERVICIO_PERMITIDOS:
            raise ValueError("El tipo de servicio debe ser Clase, Gimnasio o Reserva")
        return value

    @model_validator(mode="after")
    def validar_cuerpo_no_vacio(self) -> "ServicioUpdate":
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return self


class ServicioResponse(ServicioBase):
    id_servicio: int

    model_config = ConfigDict(from_attributes=True)


class InstructorBase(BaseModel):
    nombre_instructor: str = Field(..., examples=["Laura Sanchez"])

    @field_validator("nombre_instructor")
    @classmethod
    def validar_nombre_instructor(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre del instructor no puede estar vacio")
        return value


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    nombre_instructor: Optional[str] = Field(None, examples=["Andres Molina"])

    @field_validator("nombre_instructor")
    @classmethod
    def validar_nombre_instructor(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("El nombre del instructor no puede estar vacio")
        return value

    @model_validator(mode="after")
    def validar_cuerpo_no_vacio(self) -> "InstructorUpdate":
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return self


class InstructorResponse(InstructorBase):
    id_instructor: int

    model_config = ConfigDict(from_attributes=True)


class ReservaBase(BaseModel):
    id_cliente: int = Field(..., gt=0, examples=[1])
    id_servicio: int = Field(..., gt=0, examples=[1])
    id_instructor: Optional[int] = Field(None, gt=0, examples=[1])
    fecha_reserva: datetime = Field(..., examples=["2026-08-15T10:00:00"])
    estado_reserva: str = Field(..., examples=["Pendiente"])

    @field_validator("estado_reserva")
    @classmethod
    def validar_estado_reserva(cls, value: str) -> str:
        if value not in ESTADOS_RESERVA_PERMITIDOS:
            raise ValueError("El estado de reserva debe ser Pendiente, Confirmada o Cancelada")
        return value


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    id_cliente: Optional[int] = Field(None, gt=0, examples=[1])
    id_servicio: Optional[int] = Field(None, gt=0, examples=[1])
    id_instructor: Optional[int] = Field(None, gt=0, examples=[1])
    fecha_reserva: Optional[datetime] = Field(None, examples=["2026-08-15T10:00:00"])
    estado_reserva: Optional[str] = Field(None, examples=["Confirmada"])

    @field_validator("estado_reserva")
    @classmethod
    def validar_estado_reserva(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in ESTADOS_RESERVA_PERMITIDOS:
            raise ValueError("El estado de reserva debe ser Pendiente, Confirmada o Cancelada")
        return value

    @model_validator(mode="after")
    def validar_cuerpo_no_vacio(self) -> "ReservaUpdate":
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return self


class ReservaResponse(ReservaBase):
    id_reserva: int

    model_config = ConfigDict(from_attributes=True)
