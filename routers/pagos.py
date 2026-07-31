from fastapi import APIRouter, HTTPException, status
from typing import List
from models.pago import PagoCreate, PagoResponse, MetodoPagoCreate, MetodoPagoResponse
from database import supabase

"""
Router para la gestión de Pagos y Métodos de Pago.
Desarrollado por: Alberto Somoza (Área de Dominio: Pagos y Facturación)
"""

router = APIRouter(prefix="/pagos", tags=["Pagos"])

fake_metodos = [
    {"id_metodo_pago": 1, "nombre_metodo_pago": "Tarjeta de Crédito", "activo": True},
    {"id_metodo_pago": 2, "nombre_metodo_pago": "Transferencia Bancaria", "activo": True},
    {"id_metodo_pago": 3, "nombre_metodo_pago": "Efectivo", "activo": True}
]

fake_pagos = [
    {
        "id_pago": 1,
        "monto": 50.0,
        "fecha_pago": "2026-07-31T08:00:00",
        "id_cliente": 1,
        "id_reserva": 1,
        "id_membresia": 1,
        "id_metodo_pago": 1
    }
]

@router.post("/metodos/", response_model=MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_metodo_pago(metodo: MetodoPagoCreate):
    if supabase:
        try:
            data = supabase.table("METODO_PAGO").insert({
                "nombre_metodo_pago": metodo.nombre_metodo_pago,
                "activo": metodo.activo
            }).execute()
            if data.data:
                item = data.data[0]
                return {
                    "id_metodo_pago": item.get("id") or item.get("id_metodo_pago", 1),
                    "nombre_metodo_pago": item.get("nombre_metodo_pago") or metodo.nombre_metodo_pago,
                    "activo": item.get("activo") if item.get("activo") is not None else metodo.activo
                }
        except Exception:
            pass
            
    new_item = {
        "id_metodo_pago": len(fake_metodos) + 1,
        "nombre_metodo_pago": metodo.nombre_metodo_pago,
        "activo": metodo.activo
    }
    fake_metodos.append(new_item)
    return new_item

@router.get("/metodos/", response_model=List[MetodoPagoResponse])
def get_metodos_pago():
    if supabase:
        try:
            data = supabase.table("METODO_PAGO").select("*").execute()
            if data.data:
                result = []
                for item in data.data:
                    result.append({
                        "id_metodo_pago": item.get("id") or item.get("id_metodo_pago", 1),
                        "nombre_metodo_pago": item.get("nombre_metodo_pago") or "Efectivo",
                        "activo": item.get("activo") if item.get("activo") is not None else True
                    })
                return result
        except Exception:
            pass
    return fake_metodos

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate):
    if pago.monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto debe ser mayor a 0")
        
    if supabase:
        try:
            data = supabase.table("PAGO").insert({
                "monto": pago.monto,
                "id_cliente": pago.id_cliente,
                "id_reserva": pago.id_reserva,
                "id_membresia": pago.id_membresia,
                "id_metodo_pago": pago.id_metodo_pago
            }).execute()
            if data.data:
                item = data.data[0]
                return {
                    "id_pago": item.get("id") or item.get("id_pago", 1),
                    "fecha_pago": str(item.get("created_at") or "2026-07-31T08:00:00"),
                    "monto": item.get("monto", pago.monto),
                    "id_cliente": item.get("id_cliente", pago.id_cliente),
                    "id_reserva": item.get("id_reserva", pago.id_reserva),
                    "id_membresia": item.get("id_membresia", pago.id_membresia),
                    "id_metodo_pago": item.get("id_metodo_pago", pago.id_metodo_pago)
                }
        except Exception:
            pass
            
    new_pago = {
        "id_pago": len(fake_pagos) + 1,
        "fecha_pago": "2026-07-31T08:00:00",
        "monto": pago.monto,
        "id_cliente": pago.id_cliente,
        "id_reserva": pago.id_reserva,
        "id_membresia": pago.id_membresia,
        "id_metodo_pago": pago.id_metodo_pago
    }
    fake_pagos.append(new_pago)
    return new_pago

@router.get("/", response_model=List[PagoResponse])
def get_pagos():
    if supabase:
        try:
            data = supabase.table("PAGO").select("*").execute()
            if data.data:
                result = []
                for item in data.data:
                    result.append({
                        "id_pago": item.get("id") or item.get("id_pago", 1),
                        "fecha_pago": str(item.get("created_at") or "2026-07-31T08:00:00"),
                        "monto": item.get("monto", 50.0),
                        "id_cliente": item.get("id_cliente", 1),
                        "id_reserva": item.get("id_reserva", 1),
                        "id_membresia": item.get("id_membresia", 1),
                        "id_metodo_pago": item.get("id_metodo_pago", 1)
                    })
                return result
        except Exception:
            pass
    return fake_pagos

@router.get("/{id_pago}", response_model=PagoResponse)
def get_pago(id_pago: int):
    if supabase:
        try:
            data = supabase.table("PAGO").select("*").eq("id", id_pago).execute()
            if data.data:
                item = data.data[0]
                return {
                    "id_pago": item.get("id") or item.get("id_pago", 1),
                    "fecha_pago": str(item.get("created_at") or "2026-07-31T08:00:00"),
                    "monto": item.get("monto", 50.0),
                    "id_cliente": item.get("id_cliente", 1),
                    "id_reserva": item.get("id_reserva", 1),
                    "id_membresia": item.get("id_membresia", 1),
                    "id_metodo_pago": item.get("id_metodo_pago", 1)
                }
        except Exception:
            pass
            
    for p in fake_pagos:
        if p["id_pago"] == id_pago:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

@router.put("/{id_pago}", response_model=PagoResponse)
def update_pago(id_pago: int, pago: PagoCreate):
    if supabase:
        try:
            data = supabase.table("PAGO").update({
                "monto": pago.monto,
                "id_cliente": pago.id_cliente,
                "id_reserva": pago.id_reserva,
                "id_membresia": pago.id_membresia,
                "id_metodo_pago": pago.id_metodo_pago
            }).eq("id", id_pago).execute()
            if data.data:
                item = data.data[0]
                return {
                    "id_pago": item.get("id") or item.get("id_pago", 1),
                    "fecha_pago": str(item.get("created_at") or "2026-07-31T08:00:00"),
                    "monto": item.get("monto", pago.monto),
                    "id_cliente": item.get("id_cliente", pago.id_cliente),
                    "id_reserva": item.get("id_reserva", pago.id_reserva),
                    "id_membresia": item.get("id_membresia", pago.id_membresia),
                    "id_metodo_pago": item.get("id_metodo_pago", pago.id_metodo_pago)
                }
        except Exception:
            pass
            
    for p in fake_pagos:
        if p["id_pago"] == id_pago:
            p["monto"] = pago.monto
            p["id_cliente"] = pago.id_cliente
            p["id_reserva"] = pago.id_reserva
            p["id_membresia"] = pago.id_membresia
            p["id_metodo_pago"] = pago.id_metodo_pago
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(id_pago: int):
    if supabase:
        try:
            data = supabase.table("PAGO").delete().eq("id", id_pago).execute()
            if data.data:
                return None
        except Exception:
            pass
    return None
