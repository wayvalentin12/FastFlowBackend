# FastFlow Backend

Backend del sistema de gestión de inventario y ventas FastFlow, desarrollado con FastAPI. Controla, valida y asegura toda la información manejada en el sistema.

## Demo en vivo

[Ver API en producción](https://fastflowbackend-production.up.railway.app/docs)

# Tecnologías

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (Supabase)
- JWT Authentication
- Railway (despliegue)

# Funcionalidades

- Registro y autenticación de usuarios con JWT
- Gestión de productos e inventario
- Gestión de categorías
- Registro de ventas
- Sistema de apertura y cierre de caja diario
- Resumen de ventas del día
- Historial de cajas cerradas
- Actualización de perfiles de usuario

# Instalación local

1. Clona el repositorio
```bash
git clone https://github.com/wayvalentin12/FastFlowBackend.git
cd FastFlowBackend
```

2. Crea y activa el entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con las siguientes variables

5. Corre las migraciones
```bash
alembic upgrade head
```

6. Inicia el servidor
```bash
uvicorn main:app --reload
```

# Documentación

La documentación completa de los endpoints está disponible en `/docs` una vez iniciado el servidor.

# Autor

**Wayner Consuegra**  
wayvalentin12@gmail.com  
[GitHub](https://github.com/wayvalentin12)