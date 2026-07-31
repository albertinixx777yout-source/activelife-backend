from fastapi import FastAPI, Form, HTTPException, status
from typing import Annotated
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

# Endpoint de Autenticación con Usuario y Contraseña
@app.post("/auth/login", tags=["Autenticación"])
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if username and password:
        return {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.activelife_token",
            "token_type": "bearer",
            "mensaje": f"Bienvenido {username}, sesión iniciada correctamente"
        }
    raise HTTPException(status_code=400, detail="Usuario y contraseña requeridos")
