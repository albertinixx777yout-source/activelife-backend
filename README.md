# ActiveLife API RESTful

Repositorio grupal para la gestión de la API del gimnasio ActiveLife.

## Estructura del Proyecto

- `routers/`: Contiene los endpoints separados por dominio.
  - `pagos.py`: Módulo de Pagos y Métodos de Pago.
  - `clientes.py`: Módulo de Clientes y Membresías.
  - `servicios.py`: Módulo de Servicios, Instructores y Reservas.
- `models/`: Modelos de datos con Pydantic.
- `database.py`: Configuración de conexión a Supabase.

## Dominio: Gestión de reservas y servicios

Área implementada para la gestión de `SERVICIO`, `INSTRUCTOR` y `RESERVA`.

### Endpoints

Servicios:

- `POST /servicios`
- `GET /servicios`
- `GET /servicios/{id_servicio}`
- `PUT /servicios/{id_servicio}`
- `DELETE /servicios/{id_servicio}`

Instructores:

- `POST /instructores`
- `GET /instructores`
- `GET /instructores/{id_instructor}`
- `PUT /instructores/{id_instructor}`
- `DELETE /instructores/{id_instructor}`

Reservas:

- `POST /reservas`
- `GET /reservas`
- `GET /reservas/{id_reserva}`
- `PUT /reservas/{id_reserva}`
- `DELETE /reservas/{id_reserva}`

El listado `GET /reservas` acepta filtros opcionales por `id_cliente`, `id_servicio`, `id_instructor` y `estado_reserva`.

### Configuración y ejecución

Variables de entorno necesarias para Supabase:

- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY`

Iniciar la API:

```bash
fastapi dev main.py
```

Documentación interactiva:

- `http://127.0.0.1:8000/docs`

Ejecutar pruebas:

```bash
python -m unittest discover -s tests
```

## ¿Cómo trabajar en equipo?

1. Clonar el repositorio.
2. Crear tu propia rama: `git checkout -b feature/tu-modulo`.
3. Hacer *commits* en tu rama y subirlos a GitHub.
4. Crear un *Pull Request* para integrar tus cambios a `main`.
