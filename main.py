from fastapi import FastAPI
from routers import pagos, clientes, servicios

app = FastAPI(
    title="ActiveLife API RESTful",
    description="API para la gestión del gimnasio ActiveLife (Trabajo Grupal)",
    version="1.0.0"
)

# Registrar los routers de cada integrante del equipo
app.include_router(pagos.router)
app.include_router(clientes.router)
app.include_router(servicios.router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de ActiveLife"}
