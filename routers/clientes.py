from fastapi import APIRouter, HTTPException, status
from typing import List

from database import supabase

from models.clientes import (
    ClienteCreate,
    ClienteResponse,
    MembresiaCreate,
    MembresiaResponse,
    TipoMembresiaCreate,
    TipoMembresiaResponse
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes y Membresías"]
)

# =====================================================
# CRUD CLIENTES
# =====================================================

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("CLIENTE").insert({
        "nombres": cliente.nombres,
        "apellidos": cliente.apellidos,
        "identificacion": cliente.identificacion,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
        "fecha_inscripcion": str(cliente.fecha_inscripcion),
        "estado_cliente": cliente.estado_cliente
    }).execute()

    if not data.data:
        raise HTTPException(status_code=400, detail="Error al crear el cliente")

    return data.data[0]


@router.get("/", response_model=List[ClienteResponse])
def get_clientes():

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("CLIENTE").select("*").execute()

    return data.data


@router.get("/{id_cliente}", response_model=ClienteResponse)
def get_cliente(id_cliente: int):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("CLIENTE").select("*").eq("id_cliente", id_cliente).execute()

    if not data.data:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return data.data[0]


@router.put("/{id_cliente}", response_model=ClienteResponse)
def update_cliente(id_cliente: int, cliente: ClienteCreate):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("CLIENTE").update({
        "nombres": cliente.nombres,
        "apellidos": cliente.apellidos,
        "identificacion": cliente.identificacion,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
        "fecha_inscripcion": str(cliente.fecha_inscripcion),
        "estado_cliente": cliente.estado_cliente
    }).eq("id_cliente", id_cliente).execute()

    if not data.data:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return data.data[0]


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(id_cliente: int):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("CLIENTE").delete().eq("id_cliente", id_cliente).execute()

    if not data.data:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return None


# =====================================================
# CRUD TIPO MEMBRESIA
# =====================================================

@router.post("/tipos", response_model=TipoMembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_tipo(tipo: TipoMembresiaCreate):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("TIPO_MEMBRESIA").insert({
        "nombre_tipo": tipo.nombre_tipo,
        "precio_base": tipo.precio_base
    }).execute()

    if not data.data:
        raise HTTPException(status_code=400, detail="Error al crear el tipo de membresía")

    return data.data[0]


@router.get("/tipos", response_model=List[TipoMembresiaResponse])
def get_tipos():

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("TIPO_MEMBRESIA").select("*").execute()

    return data.data


# =====================================================
# CRUD MEMBRESIAS
# =====================================================

@router.post("/membresias", response_model=MembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_membresia(membresia: MembresiaCreate):

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("MEMBRESIA").insert({
        "id_cliente": membresia.id_cliente,
        "id_tipo_membresia": membresia.id_tipo_membresia,
        "fecha_inicio": str(membresia.fecha_inicio),
        "fecha_fin": str(membresia.fecha_fin),
        "estado_membresia": membresia.estado_membresia
    }).execute()

    if not data.data:
        raise HTTPException(status_code=400, detail="Error al crear la membresía")

    return data.data[0]


@router.get("/membresias", response_model=List[MembresiaResponse])
def get_membresias():

    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")

    data = supabase.table("MEMBRESIA").select("*").execute()

    return data.data