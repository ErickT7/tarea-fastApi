from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import List, Optional, Any

app = FastAPI(
    title="API de Gestión de Tareas",
    description="API REST con códigos HTTP explícitos en la respuesta JSON",
    version="1.0"
)

# =====================================================================
# 1. MODELOS DE DATOS (Pydantic)
# =====================================================================

# Estructura unificada que incluye el código HTTP explícito
class RespuestaEstandar(BaseModel):
    codigo: int                  # Ejemplo: 200, 201, 400, 404
    estado: str                  # "exito" o "error"
    mensaje: str                 # Mensaje descriptivo
    datos: Optional[Any] = None  # Carga útil de datos o null

# Modelo del recurso Tarea
class Tarea(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    completada: bool = False


# Base de datos en memoria (Simulada)
tareas_db = []


# =====================================================================
# 2. MANEJADORES GLOBALES DE ERRORES (Estructura consistente)
# =====================================================================

# Captura errores HTTP manuales (como el 404)
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

# Captura errores de validación de datos (Mapea automáticamente a un código 400 Bad Request)
@app.exception_handler(RequestValidationError)
async def manejador_errores_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "codigo": 400,
            "estado": "error",
            "mensaje": "Datos de entrada inválidos o faltantes",
            "datos": exc.errors()  # Muestra qué campo falló (ej. título faltante)
        }
    )


# =====================================================================
# 3. ENDPOINTS CON CÓDIGOS HTTP EN EL JSON
# =====================================================================

# [POST] Crear tarea -> Retorna Código 201 (Created)
@app.post("/tareas/", response_model=RespuestaEstandar, status_code=201)
def crear_tarea(tarea: Tarea):
    nueva_id = len(tareas_db) + 1
    tarea.id = nueva_id
    tareas_db.append(tarea.dict())
    return {
        "codigo": 201,
        "estado": "exito",
        "mensaje": "Tarea creada correctamente",
        "datos": tarea
    }

# [GET] Obtener todas -> Retorna Código 200 (OK)
@app.get("/tareas/", response_model=RespuestaEstandar)
def obtener_tareas():
    return {
        "codigo": 200,
        "estado": "exito",
        "mensaje": "Listado de tareas obtenido con éxito",
        "datos": tareas_db
    }

# [GET] Obtener una por ID -> Retorna Código 200 (OK) o 404 (Not Found)
@app.get("/tareas/{tarea_id}", response_model=RespuestaEstandar)
def obtener_tarea(tarea_id: int):
    tarea = next((t for t in tareas_db if t["id"] == tarea_id), None)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"La tarea con ID {tarea_id} no existe")
    return {
        "codigo": 200,
        "estado": "exito",
        "mensaje": "Tarea encontrada",
        "datos": tarea
    }

# [PUT] Actualizar -> Retorna Código 200 (OK) o 404 (Not Found)
@app.put("/tareas/{tarea_id}", response_model=RespuestaEstandar)
def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea):
    for index, tarea in enumerate(tareas_db):
        if tarea["id"] == tarea_id:
            tarea_actualizada.id = tarea_id
            tareas_db[index] = tarea_actualizada.dict()
            return {
                "codigo": 200,
                "estado": "exito",
                "mensaje": "Tarea actualizada correctamente",
                "datos": tareas_db[index]
            }
    raise HTTPException(status_code=404, detail=f"No se pudo actualizar. La tarea con ID {tarea_id} no existe")

# [DELETE] Eliminar -> Retorna Código 200 (OK) o 404 (Not Found)
@app.delete("/tareas/{tarea_id}", response_model=RespuestaEstandar)
def eliminar_tarea(tarea_id: int):
    for index, tarea in enumerate(tareas_db):
        if tarea["id"] == tarea_id:
            tareas_db.pop(index)
            return {
                "codigo": 200,
                "estado": "exito",
                "mensaje": "Tarea eliminada correctamente",
                "datos": {"id_eliminada": tarea_id}
            }
    raise HTTPException(status_code=404, detail=f"No se pudo eliminar. La tarea con ID {tarea_id} no existe")
