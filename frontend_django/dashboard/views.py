from django.shortcuts import render
import requests
from django.conf import settings

def index(request):
    try:
        # Consumimos directamente tu API de produccion (en la nube)
        response = requests.get('https://activelife-backend.fastapicloud.dev/pagos', timeout=5)
        # Si todo va bien, los guardamos
        if response.status_code == 200:
            pagos = response.json()
        else:
            pagos = []
    except Exception:
        # Si la API esta caida (Render dormido, etc), lista vacia para evitar error 500
        pagos = []

    ingreso_total = sum(p.get("monto", 0) for p in pagos)
    pagos_hoy = len(pagos)
    ticket_promedio = round(ingreso_total / pagos_hoy, 2) if pagos_hoy > 0 else 0

    data = {
        "title": "Dashboard - Pagos y Facturación",
        "ingreso_total": ingreso_total,
        "pagos_hoy": pagos_hoy,
        "ticket_promedio": ticket_promedio,
        "pagos": pagos,
    }
    return render(request, "dashboard/index.html", data)