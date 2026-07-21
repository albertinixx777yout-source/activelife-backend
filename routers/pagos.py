from fastapi import APIRouter, HTTPException, status
from typing import List
from models.pago import PagoCreate, PagoResponse, MetodoPagoCreate, MetodoPagoResponse
from database import supabase

router = APIRouter(prefix="/pagos", tags=["Pagos"])

# --- ENDPOINTS PARA MÉTODOS DE PAGO ---

@router.post("/metodos/", response_model=MetodoPagoResponse, status_code=status.HTTP_201_CREATED)
def create_metodo_pago(metodo: MetodoPagoCreate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    
    data = supabase.table("METODO_PAGO").insert({
        "nombre_metodo_pago": metodo.nombre_metodo_pago,
        "activo": metodo.activo
    }).execute()
    
    if not data.data:
        raise HTTPException(status_code=400, detail="Error al crear el método de pago")
    return data.data[0]

@router.get("/metodos/", response_model=List[MetodoPagoResponse])
def get_metodos_pago():
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
    
    data = supabase.table("METODO_PAGO").select("*").execute()
    return data.data

# --- ENDPOINTS PARA PAGOS ---

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
        
    if pago.monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto debe ser mayor a 0")
        
    data = supabase.table("PAGO").insert({
        "monto": pago.monto,
        "id_cliente": pago.id_cliente,
        "id_reserva": pago.id_reserva,
        "id_membresia": pago.id_membresia,
        "id_metodo_pago": pago.id_metodo_pago
    }).execute()
    
    if not data.data:
        raise HTTPException(status_code=400, detail="Error al procesar el pago")
    return data.data[0]

@router.get("/", response_model=List[PagoResponse])
def get_pagos():
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
        
    data = supabase.table("PAGO").select("*").execute()
    return data.data

@router.get("/{id_pago}", response_model=PagoResponse)
def get_pago(id_pago: int):
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
        
    data = supabase.table("PAGO").select("*").eq("id_pago", id_pago).execute()
    if not data.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return data.data[0]

@router.put("/{id_pago}", response_model=PagoResponse)
def update_pago(id_pago: int, pago: PagoCreate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
        
    data = supabase.table("PAGO").update({
        "monto": pago.monto,
        "id_cliente": pago.id_cliente,
        "id_reserva": pago.id_reserva,
        "id_membresia": pago.id_membresia,
        "id_metodo_pago": pago.id_metodo_pago
    }).eq("id_pago", id_pago).execute()
    
    if not data.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado o no actualizado")
    return data.data[0]

@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(id_pago: int):
    if not supabase:
        raise HTTPException(status_code=500, detail="Base de datos no configurada")
        
    data = supabase.table("PAGO").delete().eq("id_pago", id_pago).execute()
    if not data.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return None
