from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, status

from database import supabase
from models.servicio import (
    ESTADOS_RESERVA_PERMITIDOS,
    InstructorCreate,
    InstructorResponse,
    InstructorUpdate,
    ReservaCreate,
    ReservaResponse,
    ReservaUpdate,
    ServicioCreate,
    ServicioResponse,
    ServicioUpdate,
)


SERVICIO_TABLE = "SERVICIO"
INSTRUCTOR_TABLE = "INSTRUCTOR"
RESERVA_TABLE = "RESERVA"
CLIENTE_TABLE = "CLIENTE"

router = APIRouter()

servicios_router = APIRouter(prefix="/servicios", tags=["Servicios"])
instructores_router = APIRouter(prefix="/instructores", tags=["Instructores"])
reservas_router = APIRouter(prefix="/reservas", tags=["Reservas"])


def _get_supabase():
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no configurada",
        )
    return supabase


def _execute(query):
    try:
        return query.execute()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al consultar la base de datos",
        ) from exc


def _first_or_none(table: str, column: str, value: Any) -> Optional[dict]:
    db = _get_supabase()
    result = _execute(db.table(table).select("*").eq(column, value).limit(1))
    return result.data[0] if result.data else None


def _require_record(table: str, column: str, value: Any, message: str) -> dict:
    record = _first_or_none(table, column, value)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return record


def _serialize_payload(payload: dict) -> dict:
    serialized = payload.copy()
    fecha_reserva = serialized.get("fecha_reserva")
    if isinstance(fecha_reserva, datetime):
        serialized["fecha_reserva"] = fecha_reserva.isoformat()
    return serialized


def _ensure_cliente_exists(id_cliente: int) -> None:
    _require_record(CLIENTE_TABLE, "id_cliente", id_cliente, "Cliente no encontrado")


def _ensure_servicio_exists(id_servicio: int) -> dict:
    return _require_record(SERVICIO_TABLE, "id_servicio", id_servicio, "Servicio no encontrado")


def _ensure_instructor_exists(id_instructor: Optional[int]) -> None:
    if id_instructor is not None:
        _require_record(
            INSTRUCTOR_TABLE,
            "id_instructor",
            id_instructor,
            "Instructor no encontrado",
        )


def _ensure_reserva_dependencies(payload: dict) -> dict:
    _ensure_cliente_exists(payload["id_cliente"])
    servicio = _ensure_servicio_exists(payload["id_servicio"])
    _ensure_instructor_exists(payload.get("id_instructor"))
    return servicio


def _ensure_capacity_available(
    *,
    id_servicio: int,
    fecha_reserva: Any,
    estado_reserva: str,
    capacidad: int,
    id_reserva_excluida: Optional[int] = None,
) -> None:
    if estado_reserva == "Cancelada":
        return

    db = _get_supabase()
    fecha = fecha_reserva.isoformat() if isinstance(fecha_reserva, datetime) else fecha_reserva
    query = (
        db.table(RESERVA_TABLE)
        .select("id_reserva")
        .eq("id_servicio", id_servicio)
        .eq("fecha_reserva", fecha)
        .in_("estado_reserva", ["Pendiente", "Confirmada"])
    )

    if id_reserva_excluida is not None:
        query = query.neq("id_reserva", id_reserva_excluida)

    result = _execute(query)
    if len(result.data or []) >= capacidad:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La capacidad del servicio para esa fecha ya esta completa",
        )


def _ensure_not_referenced(
    *,
    table: str,
    column: str,
    value: int,
    message: str,
) -> None:
    db = _get_supabase()
    result = _execute(db.table(table).select("id_reserva").eq(column, value).limit(1))
    if result.data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


@servicios_router.post(
    "",
    response_model=ServicioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_servicio(servicio: ServicioCreate):
    db = _get_supabase()
    result = _execute(db.table(SERVICIO_TABLE).insert(servicio.model_dump()))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el servicio",
        )
    return result.data[0]


@servicios_router.get("", response_model=list[ServicioResponse])
def list_servicios():
    db = _get_supabase()
    result = _execute(db.table(SERVICIO_TABLE).select("*"))
    return result.data or []


@servicios_router.get("/{id_servicio}", response_model=ServicioResponse)
def get_servicio(id_servicio: int):
    return _require_record(
        SERVICIO_TABLE,
        "id_servicio",
        id_servicio,
        "Servicio no encontrado",
    )


@servicios_router.put("/{id_servicio}", response_model=ServicioResponse)
def update_servicio(id_servicio: int, servicio: ServicioUpdate):
    db = _get_supabase()
    _require_record(SERVICIO_TABLE, "id_servicio", id_servicio, "Servicio no encontrado")
    payload = servicio.model_dump(exclude_unset=True)
    result = _execute(
        db.table(SERVICIO_TABLE).update(payload).eq("id_servicio", id_servicio)
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el servicio",
        )
    return result.data[0]


@servicios_router.delete(
    "/{id_servicio}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_servicio(id_servicio: int):
    db = _get_supabase()
    _require_record(SERVICIO_TABLE, "id_servicio", id_servicio, "Servicio no encontrado")
    _ensure_not_referenced(
        table=RESERVA_TABLE,
        column="id_servicio",
        value=id_servicio,
        message="No se puede eliminar el servicio porque tiene reservas asociadas",
    )
    result = _execute(db.table(SERVICIO_TABLE).delete().eq("id_servicio", id_servicio))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el servicio",
        )
    return None


@instructores_router.post(
    "",
    response_model=InstructorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_instructor(instructor: InstructorCreate):
    db = _get_supabase()
    result = _execute(db.table(INSTRUCTOR_TABLE).insert(instructor.model_dump()))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el instructor",
        )
    return result.data[0]


@instructores_router.get("", response_model=list[InstructorResponse])
def list_instructores():
    db = _get_supabase()
    result = _execute(db.table(INSTRUCTOR_TABLE).select("*"))
    return result.data or []


@instructores_router.get("/{id_instructor}", response_model=InstructorResponse)
def get_instructor(id_instructor: int):
    return _require_record(
        INSTRUCTOR_TABLE,
        "id_instructor",
        id_instructor,
        "Instructor no encontrado",
    )


@instructores_router.put("/{id_instructor}", response_model=InstructorResponse)
def update_instructor(id_instructor: int, instructor: InstructorUpdate):
    db = _get_supabase()
    _require_record(
        INSTRUCTOR_TABLE,
        "id_instructor",
        id_instructor,
        "Instructor no encontrado",
    )
    payload = instructor.model_dump(exclude_unset=True)
    result = _execute(
        db.table(INSTRUCTOR_TABLE).update(payload).eq("id_instructor", id_instructor)
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el instructor",
        )
    return result.data[0]


@instructores_router.delete(
    "/{id_instructor}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_instructor(id_instructor: int):
    db = _get_supabase()
    _require_record(
        INSTRUCTOR_TABLE,
        "id_instructor",
        id_instructor,
        "Instructor no encontrado",
    )
    _ensure_not_referenced(
        table=RESERVA_TABLE,
        column="id_instructor",
        value=id_instructor,
        message="No se puede eliminar el instructor porque tiene reservas asociadas",
    )
    result = _execute(db.table(INSTRUCTOR_TABLE).delete().eq("id_instructor", id_instructor))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el instructor",
        )
    return None


@reservas_router.post(
    "",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reserva(reserva: ReservaCreate):
    db = _get_supabase()
    payload = _serialize_payload(reserva.model_dump())
    servicio = _ensure_reserva_dependencies(payload)
    _ensure_capacity_available(
        id_servicio=payload["id_servicio"],
        fecha_reserva=payload["fecha_reserva"],
        estado_reserva=payload["estado_reserva"],
        capacidad=servicio["capacidad"],
    )
    result = _execute(db.table(RESERVA_TABLE).insert(payload))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear la reserva",
        )
    return result.data[0]


@reservas_router.get("", response_model=list[ReservaResponse])
def list_reservas(
    id_cliente: Optional[int] = Query(None, gt=0),
    id_servicio: Optional[int] = Query(None, gt=0),
    id_instructor: Optional[int] = Query(None, gt=0),
    estado_reserva: Optional[str] = Query(None),
):
    if estado_reserva is not None and estado_reserva not in ESTADOS_RESERVA_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estado de reserva debe ser Pendiente, Confirmada o Cancelada",
        )

    db = _get_supabase()
    query = db.table(RESERVA_TABLE).select("*")
    if id_cliente is not None:
        query = query.eq("id_cliente", id_cliente)
    if id_servicio is not None:
        query = query.eq("id_servicio", id_servicio)
    if id_instructor is not None:
        query = query.eq("id_instructor", id_instructor)
    if estado_reserva is not None:
        query = query.eq("estado_reserva", estado_reserva)

    result = _execute(query)
    return result.data or []


@reservas_router.get("/{id_reserva}", response_model=ReservaResponse)
def get_reserva(id_reserva: int):
    return _require_record(
        RESERVA_TABLE,
        "id_reserva",
        id_reserva,
        "Reserva no encontrada",
    )


@reservas_router.put("/{id_reserva}", response_model=ReservaResponse)
def update_reserva(id_reserva: int, reserva: ReservaUpdate):
    db = _get_supabase()
    current = _require_record(
        RESERVA_TABLE,
        "id_reserva",
        id_reserva,
        "Reserva no encontrada",
    )
    payload = _serialize_payload(reserva.model_dump(exclude_unset=True))
    updated = {**current, **payload}

    servicio = _ensure_reserva_dependencies(updated)
    _ensure_capacity_available(
        id_servicio=updated["id_servicio"],
        fecha_reserva=updated["fecha_reserva"],
        estado_reserva=updated["estado_reserva"],
        capacidad=servicio["capacidad"],
        id_reserva_excluida=id_reserva,
    )

    result = _execute(db.table(RESERVA_TABLE).update(payload).eq("id_reserva", id_reserva))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar la reserva",
        )
    return result.data[0]


@reservas_router.delete(
    "/{id_reserva}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reserva(id_reserva: int):
    db = _get_supabase()
    _require_record(RESERVA_TABLE, "id_reserva", id_reserva, "Reserva no encontrada")
    result = _execute(db.table(RESERVA_TABLE).delete().eq("id_reserva", id_reserva))
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar la reserva",
        )
    return None


router.include_router(servicios_router)
router.include_router(instructores_router)
router.include_router(reservas_router)
