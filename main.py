from fastapi import FastAPI, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import List, Optional, Any

app = FastAPI(
    title="API de Gestión de Items",
    description="API REST con campos title y priority, paginación y respuestas JSON consistentes",
    version="3.0"
)

# =====================================================================
# 1. MODELOS DE DATOS (Pydantic)
# =====================================================================

# Estructura unificada para todas las respuestas
class RespuestaEstandar(BaseModel):
    codigo: int                  
    estado: str                  # "exito" o "error"
    mensaje: str                 
    datos: Optional[Any] = None  

# Modelo del recurso Item con los nuevos campos solicitados
class Item(BaseModel):
    id: Optional[int] = None
    title: str                   # Título del recurso
    description: str             # Descripción del recurso
    priority: str                # Prioridad (ej. "alta", "media", "baja")
    completed: bool = False      # Estado de la tarea/item

# Modelo específico para el método PATCH (para actualizar solo el estado)
class ActualizarEstadoItem(BaseModel):
    completed: bool


# Base de datos en memoria (Simulada)
items_db = []


# =====================================================================
# 2. MANEJADORES GLOBALES DE ERRORES (Código 400 y 404)
# =====================================================================

@app.exception_handler(HTTPException)
async def manejador_errores_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "codigo": exc.status_code,
            "estado": "error",
            "mensaje": exc.detail,
            "datos": None
        }
    )

@app.exception_handler(RequestValidationError)
async def manejador_errores_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "codigo": 400,
            "estado": "error",
            "mensaje": "Datos de entrada inválidos, faltantes o de tipo incorrecto",
            "datos": exc.errors()
        }
    )


# =====================================================================
# 3. ENDPOINTS REQUERIDOS
# =====================================================================

# [GET] /items - Lista de recursos con paginación opcional (?pag=1&limit=10)
@app.get("/items", response_model=RespuestaEstandar)
def listar_items(
    pag: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Límite de elementos por página")
):
    inicio = (pag - 1) * limit
    fin = inicio + limit
    items_paginados = items_db[inicio:fin]
    
    return {
        "codigo": 200,
        "estado": "exito",
        "mensaje": f"Listado obtenido (Página {pag}, Límite {limit})",
        "datos": {
            "items": items_paginados,
            "total_items": len(items_db),
            "pagina_actual": pag,
            "limite_por_pagina": limit
        }
    }

# [GET] /items/:id - Obtener recurso por ID
@app.get("/items/{item_id}", response_model=RespuestaEstandar)
def obtener_item_por_id(item_id: int):
    item = next((i for i in items_db if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"El recurso con ID {item_id} no existe")
    return {
        "codigo": 200,
        "estado": "exito",
        "mensaje": "Recurso encontrado",
        "datos": item
    }

# [POST] /items - Crear un recurso (Retorna 201 Created)
@app.post("/items", response_model=RespuestaEstandar, status_code=201)
def crear_recurso(item: Item):
    nueva_id = len(items_db) + 1
    item.id = nueva_id
    items_db.append(item.dict())
    return {
        "codigo": 201,
        "estado": "exito",
        "mensaje": "Recurso creado correctamente",
        "datos": item
    }

# [PATCH] /items/:id - Actualizar únicamente el estado del recurso
@app.patch("/items/{item_id}", response_model=RespuestaEstandar)
def actualizar_estado_recurso(item_id: int, datos_actualizados: ActualizarEstadoItem):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            # Modificamos únicamente el estado 'completed'
            items_db[index]["completed"] = datos_actualizados.completed
            return {
                "codigo": 200,
                "estado": "exito",
                "mensaje": "Estado del recurso actualizado correctamente",
                "datos": items_db[index]
            }
    raise HTTPException(status_code=404, detail=f"No se pudo actualizar. El recurso con ID {item_id} no existe")
