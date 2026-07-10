from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum

app = FastAPI(
    title="API REST de Items",
    version="1.0.0"
)

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=100)
    priority: PriorityEnum = Field(...)
    description: Optional[str] = Field(None, max_length=300)
    completada: bool = Field(default=False)

class ItemCrear(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    priority: str = Field(...)  # Recibimos texto para validar manualmente si es correcto
    description: Optional[str] = None

# Base de datos simulada en memoria
db_items: List[Item] = []

# --- ENDPOINTS ---

# 1. GET /items -> Retorna 200 OK
@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def listar_items(
    pag: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    inicio = (pag - 1) * limit
    fin = inicio + limit
    return db_items[inicio:fin]

# 2. GET /items/:id -> Retorna 200 OK o 404 Not Found
@app.get("/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def obtener_item_por_id(id: UUID):
    for item in db_items:
        if item.id == id:
            return item
    # 404: El recurso con ese ID no existe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Recurso no encontrado"
    )

# 3. POST /items -> Retorna 201 Created o 400 Bad Request
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def crear_recurso(item_input: ItemCrear):
    # Validación manual del negocio para forzar un 400 Bad Request si la prioridad es inválida
    if item_input.priority not in [p.value for p in PriorityEnum]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La prioridad enviada es inválida. Debe ser 'low', 'medium' o 'high'."
        )
        
    nuevo_item = Item(
        title=item_input.title,
        priority=PriorityEnum(item_input.priority),
        description=item_input.description
    )
    db_items.append(nuevo_item)
    return nuevo_item

# 4. PATCH /items/:id -> Retorna 200 OK o 404 Not Found
@app.patch("/items/{id}", response_model=Item, status_code=status.HTTP_200_OK)
def actualizar_estado_recurso(id: UUID):
    for index, item in enumerate(db_items):
        if item.id == id:
            db_items[index].completada = not db_items[index].completada
            return db_items[index]
    # 404: No se puede actualizar un recurso que no existe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Recurso no encontrado"
    )


