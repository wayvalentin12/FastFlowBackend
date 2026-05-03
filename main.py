from fastapi import FastAPI
from routers import login,productos,ventas,usuarios, categorias,register, caja
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(register.router, prefix="/register", tags=["Register"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
app.include_router(ventas.router, prefix="/ventas", tags=["Ventas"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(caja.router, prefix="/caja", tags=["Caja"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wfastflow.netlify.app/"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

@app.get("/")
async def start():
    return {"Welcome": "Esta es la api de Fastflow"}