from fastapi import FastAPI, HTTPException, Request, Query, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional, Any

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(
    title="API de Gestión de Items",
    description="API REST con persistencia en SQLite, paginación y respuestas consistentes (Acceso Público)",
    version="7.0"
)

# Configuración de SQLite
DATABASE_URL = "sqlite:///./items_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Tabla
class DBItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

# Crear tablas
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
class RespuestaEstandar(BaseModel):
    codigo: int                  
    estado: str                  
    mensaje: str                 
    datos: Optional[Any] = None  

class ItemSchema(BaseModel):
    id: Optional[int] = None
    title: str                   
    description: str             
    priority: str                
    completed: bool = False      

class ActualizarEstadoItem(BaseModel):
    completed: bool

# Manejadores de Errores (Códigos 400 y 404)
@app.exception_handler(HTTPException)
async def manejador_errores_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"codigo": exc.status_code, "estado": "error", "mensaje": exc.detail, "datos": None}
    )

@app.exception_handler(RequestValidationError)
async def manejador_errores_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"codigo": 400, "estado": "error", "mensaje": "Datos de entrada inválidos", "datos": jsonable_encoder(exc.errors())}
    )

# Endpoints Públicos
@app.get("/items", response_model=RespuestaEstandar)
def listar_items(pag: int = Query(default=1, ge=1), limit: int = Query(default=10, ge=1), db: Session = Depends(get_db)):
    offset = (pag - 1) * limit
    total_items = db.query(DBItem).count()
    items_paginados = db.query(DBItem).offset(offset).limit(limit).all()
    return {
        "codigo": 200, "estado": "exito", "mensaje": f"Página {pag}",
        "datos": {"items": jsonable_encoder(items_paginados), "total_items": total_items}
    }

@app.get("/items/{item_id}", response_model=RespuestaEstandar)
def obtener_item_por_id(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="No existe")
    return {"codigo": 200, "estado": "exito", "mensaje": "Encontrado", "datos": jsonable_encoder(item)}

# [POST] /items - Ahora es público (Se removió la validación)
@app.post("/items", response_model=RespuestaEstandar, status_code=201)
def crear_recurso(item: ItemSchema, db: Session = Depends(get_db)):
    nuevo_item = DBItem(title=item.title, description=item.description, priority=item.priority, completed=item.completed)
    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)
    return {"codigo": 201, "estado": "exito", "mensaje": "Guardado en SQLite", "datos": jsonable_encoder(nuevo_item)}

@app.patch("/items/{item_id}", response_model=RespuestaEstandar)
def actualizar_estado_recurso(item_id: int, datos_actualizados: ActualizarEstadoItem, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="No existe")
    item.completed = datos_actualizados.completed
    db.commit()
    db.refresh(item)
    return {"codigo": 200, "estado": "exito", "mensaje": "Actualizado", "datos": jsonable_encoder(item)}
