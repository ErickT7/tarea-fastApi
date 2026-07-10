from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI(
    title="API REST de Items",
    version="1.0.0"
)

# Modelo de datos del Recurso (Item)
class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    titulo: str = Field(..., min_length=1, max_length=100, example="Mi Recurso")
    descripcion: Optional[str] = Field(None, max_length=300, example="Detalles del recurso")
    completada: bool = Field(default=False)

# Modelo para la creación de un recurso
class ItemCrear(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None

# Base de datos simulada en memoria
db_items: List[Item] = []

# --- ENDPOINTS REQUERIDOS ---

# 1. GET /items - Listado con paginación opcional (?pag=1&limit=10)
@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def listar_items(
    pag: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página")
):
    """Lista los recursos aplicando paginación matemática."""
    inicio = (pag - 1) * limit
    fin = inicio + limit
    return db_items[inicio:fin]

# 2. GET /items/:id - Obtener recurso por ID
@app.get("/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def obtener_item_por_id(id: UUID):
    """Busca y retorna un recurso específico por su ID único."""
    for item in db_items:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Recurso no encontrado")

# 3. POST /items - Crear un recurso
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def crear_recurso(item_input: ItemCrear):
    """Crea un nuevo recurso y lo almacena en la lista."""
    nuevo_item = Item(
        titulo=item_input.titulo,
        descripcion=item_input.descripcion
    )
    db_items.append(nuevo_item)
    return nuevo_item

# 4. PATCH /items/:id - Actualizar estado de recurso (completada)
@app.patch("/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def actualizar_estado_recurso(id: UUID):
    """Alterna el estado lógico ('completada') del recurso entre True y False."""
    for index, item in enumerate(db_items):
        if item.id == id:
            db_items[index].completada = not db_items[index].completada
            return db_items[index]
    raise HTTPException(status_code=404, detail="Recurso no encontrado")


