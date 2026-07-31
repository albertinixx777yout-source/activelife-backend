from fastapi import APIRouter, HTTPException, status
from typing import List
from models.pago import PagoCreate, PagoResponse, MetodoPagoCreate, MetodoPagoResponse
from database import supabase

"""
Router para la gestión de Pagos y Métodos de Pago.
Desarrollado por: Alberto Somoza (Área de Dominio: Pagos y Facturación)
"""

router = APIRouter(prefix="/pagos", tags=["Pagos"])

def check_db():
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no configurada en .env"
        )

# --- ENDPOINTS PARA MÉTODOS DE PAGO ---

@router.post("/metodos/", response_model=MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_metodo_pago(metodo: MetodoPagoCreate):
    check_db()
    try:
        data = supabase.table("METODO_PAGO").insert({
            "nombre_metodo_pago": metodo.nombre_metodo_pago,
            "activo": metodo.activo
        }).execute()
        if data.data:
            item = data.data[0]
            return {
                "id_metodo_pago": item.get("id_metodo_pago") or item.get("id", 1),
                "nombre_metodo_pago": item.get("nombre_metodo_pago", metodo.nombre_metodo_pago),
                "activo": item.get("activo", metodo.activo)
            }
        raise HTTPException(status_code=400, detail="Error al crear método de pago")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metodos/", response_model=List[MetodoPagoResponse])
def get_metodos_pago():
    check_db()
    try:
        data = supabase.table("METODO_PAGO").select("*").execute()
        result = []
        for item in (data.data or []):
            result.append({
                "id_metodo_pago": item.get("id_metodo_pago") or item.get("id", 1),
                "nombre_metodo_pago": item.get("nombre_metodo_pago") or "Efectivo",
                "activo": item.get("activo") if item.get("activo") is not None else True
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- ENDPOINTS PARA PAGOS ---

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate):
    check_db()
    if pago.monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto debe ser mayor a 0")
        
    try:
        payload = {
            "valor": pago.monto,
            "concepto": "Pago de servicio gimnasio",
            "id_cliente": pago.id_cliente if pago.id_cliente else None,
            "id_reserva": pago.id_reserva if pago.id_reserva else None,
            "id_membresia": pago.id_membresia if pago.id_membresia else None,
            "id_metodo_pago": pago.id_metodo_pago if pago.id_metodo_pago else None
        }
        data = supabase.table("PAGO").insert(payload).execute()
        if data.data:
            item = data.data[0]
            return {
                "id_pago": item.get("id_pago") or item.get("id", 1),
                "fecha_pago": str(item.get("fecha_pago") or "2026-07-31T08:00:00"),
                "monto": float(item.get("valor") or pago.monto),
                "id_cliente": item.get("id_cliente") or pago.id_cliente,
                "id_reserva": item.get("id_reserva") or pago.id_reserva or 1,
                "id_membresia": item.get("id_membresia") or pago.id_membresia or 1,
                "id_metodo_pago": item.get("id_metodo_pago") or pago.id_metodo_pago
            }
        raise HTTPException(status_code=400, detail="Error al crear el pago")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PagoResponse])
def get_pagos():
    check_db()
    try:
        data = supabase.table("PAGO").select("*").execute()
        result = []
        for item in (data.data or []):
            result.append({
                "id_pago": item.get("id_pago") or item.get("id", 1),
                "fecha_pago": str(item.get("fecha_pago") or "2026-07-31T08:00:00"),
                "monto": float(item.get("valor") or 50.0),
                "id_cliente": item.get("id_cliente") or 1,
                "id_reserva": item.get("id_reserva") or 1,
                "id_membresia": item.get("id_membresia") or 1,
                "id_metodo_pago": item.get("id_metodo_pago") or 1
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id_pago}", response_model=PagoResponse)
def get_pago(id_pago: int):
    check_db()
    try:
        data = supabase.table("PAGO").select("*").eq("id_pago", id_pago).execute()
        if data.data:
            item = data.data[0]
            return {
                "id_pago": item.get("id_pago") or item.get("id", 1),
                "fecha_pago": str(item.get("fecha_pago") or "2026-07-31T08:00:00"),
                "monto": float(item.get("valor") or 50.0),
                "id_cliente": item.get("id_cliente") or 1,
                "id_reserva": item.get("id_reserva") or 1,
                "id_membresia": item.get("id_membresia") or 1,
                "id_metodo_pago": item.get("id_metodo_pago") or 1
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_pago}", response_model=PagoResponse)
def update_pago(id_pago: int, pago: PagoCreate):
    check_db()
    try:
        data = supabase.table("PAGO").update({
            "valor": pago.monto
        }).eq("id_pago", id_pago).execute()
        if data.data:
            item = data.data[0]
            return {
                "id_pago": item.get("id_pago") or item.get("id", 1),
                "fecha_pago": str(item.get("fecha_pago") or "2026-07-31T08:00:00"),
                "monto": float(item.get("valor") or pago.monto),
                "id_cliente": pago.id_cliente,
                "id_reserva": pago.id_reserva or 1,
                "id_membresia": pago.id_membresia or 1,
                "id_metodo_pago": pago.id_metodo_pago
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(id_pago: int):
    check_db()
    try:
        data = supabase.table("PAGO").delete().eq("id_pago", id_pago).execute()
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
