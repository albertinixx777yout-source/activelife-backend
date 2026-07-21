# ActiveLife API RESTful

Repositorio grupal para la gestión de la API del gimnasio ActiveLife.

## Estructura del Proyecto

- `routers/`: Contiene los endpoints separados por dominio.
  - `pagos.py`: Módulo de Pagos y Métodos de Pago.
  - `clientes.py`: Módulo de Clientes y Membresías.
  - `servicios.py`: Módulo de Servicios, Instructores y Reservas.
- `models/`: Modelos de datos con Pydantic.
- `database.py`: Configuración de conexión a Supabase.

## ¿Cómo trabajar en equipo?

1. Clonar el repositorio.
2. Crear tu propia rama: `git checkout -b feature/tu-modulo`.
3. Hacer *commits* en tu rama y subirlos a GitHub.
4. Crear un *Pull Request* para integrar tus cambios a `main`.
